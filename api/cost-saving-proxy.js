// Cost Saving API Proxy - forwards requests to n8n webhook to avoid CORS and keep API key server-side.

const COST_SAVING_API_URL = "https://n8n.sourcesage.co/webhook/bot/cost-saving-summary";
const N8N_API_KEY = process.env.N8N_API_KEY || "";
const UPSTREAM_TIMEOUT_MS = 30000;

const REGION_CURRENCY = {
  SG: "SGD",
  MY: "MYR",
  AU: "AUD",
  JP: "JPY",
  TH: "THB",
  IN: "INR",
  HK: "HKD",
  ID: "IDR",
  CN: "CNY",
  VN: "VND",
};

function timeout(ms) {
  return new Promise((_, reject) => setTimeout(() => reject(new Error("TIMEOUT")), ms));
}

function numeric(value) {
  const n = Number(value || 0);
  return Number.isFinite(n) ? n : 0;
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Accept, X-API-Key");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (!["GET", "POST"].includes(req.method)) return res.status(405).json({ error: "Method not allowed" });

  try {
    const region = String(req.query?.region || req.body?.region || "").toUpperCase().slice(0, 2);
    const currency = region ? (REGION_CURRENCY[region] || "SGD") : "SGD";
    const entityName = String(req.query?.entity_name || req.body?.entity_name || "TikTok").trim() || "TikTok";

    if (!N8N_API_KEY) {
      return res.status(500).json({ error: "N8N_API_KEY not configured", _apiUnavailable: true });
    }

    const payload = {
      buyer_name: null,
      product_name: null,
      entity_name: entityName,
      currency,
      marketplace_id: null,
      category: null,
      timestamp_start: "2025-06-01",
      timestamp_end: "2025-12-31",
    };

    // Only add region if specified (for TikTok-wide totals, omit region)
    if (region) {
      payload.region = region;
    }

    const upstream = await Promise.race([
      fetch(COST_SAVING_API_URL, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-API-Key": N8N_API_KEY,
        },
        body: JSON.stringify(payload),
      }),
      timeout(UPSTREAM_TIMEOUT_MS),
    ]);

    if (!upstream.ok) {
      const message = await upstream.text().catch(() => "Unknown upstream error");
      return res.status(502).json({ error: "Cost Saving API error", status: upstream.status, message, _apiUnavailable: true });
    }

    const data = await upstream.json();
    const records = Array.isArray(data) ? data : data ? [data] : [];

    const totals = records.reduce((acc, record) => {
      acc.totalSpendLocal += numeric(record.total_price);
      acc.totalSavingLocal += numeric(record.total_saving);
      acc.totalSpend += numeric(record.total_price_sgd ?? record.total_price);
      acc.totalSaving += numeric(record.total_saving_sgd ?? record.total_saving);
      return acc;
    }, { totalSpend: 0, totalSaving: 0, totalSpendLocal: 0, totalSavingLocal: 0 });

    const savingsRatePct = totals.totalSpend > 0 ? Number(((totals.totalSaving / totals.totalSpend) * 100).toFixed(2)) : 0;

    return res.status(200).json({
      region,
      entity_name: entityName,
      currency,
      ...totals,
      savingsRatePct,
      records: records.length,
    });
  } catch (error) {
    const status = error.message === "TIMEOUT" ? 504 : 500;
    return res.status(status).json({ error: "Cost Saving proxy error", message: error.message, _apiUnavailable: true });
  }
};
