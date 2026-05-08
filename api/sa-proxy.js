// SA API Proxy - forwards requests to avoid CORS issues
// The SA API at api-tiktok-dev.sourcesage.co doesn't return CORS headers,
// so browser requests fail. This serverless function proxies the calls.

const SA_API_BASE = 'https://api-tiktok-dev.sourcesage.co/api';
const SA_API_KEY = '3f03537cfb4c4ac089e50b08e4e0471f';
const UPSTREAM_TIMEOUT_MS = 25000; // 25 second timeout for upstream API calls

// Demo data removed - only real data should be displayed
// When API is unavailable, return empty data instead of demo data
const EMPTY_DATA_RESPONSE = {
  _apiUnavailable: true,
  _isEmpty: true,
};

// Helper to create a timeout promise
function createTimeoutPromise(ms) {
  return new Promise((_, reject) => {
    setTimeout(() => reject(new Error('TIMEOUT')), ms);
  });
}

module.exports = async function handler(req, res) {
  // CORS headers for browser
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization, X-SA-AGENT-KEY, Cache-Control, Pragma');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { endpoint, payload } = req.body;

    if (!endpoint) {
      return res.status(400).json({ error: 'Missing endpoint' });
    }

    // Validate endpoint starts with expected prefix to prevent abuse
    // Allow analytics and orders endpoints
    if (!endpoint.startsWith('/v1.0/agent/analytics/') && !endpoint.startsWith('/v1.0/agent/orders/')) {
      return res.status(400).json({ error: 'Invalid endpoint' });
    }

    const url = `${SA_API_BASE}${endpoint}`;
    const upstreamPayload = normalizePayloadForSA(endpoint, payload || {});

    // Race between fetch and timeout
    let apiResponse;
    try {
      apiResponse = await Promise.race([
        fetch(url, {
          method: 'POST',
          headers: {
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ',
            'X-SA-AGENT-KEY': SA_API_KEY,
          },
          body: JSON.stringify(upstreamPayload),
        }),
        createTimeoutPromise(UPSTREAM_TIMEOUT_MS)
      ]);
    } catch (raceError) {
      if (raceError.message === 'TIMEOUT') {
        console.error('SA API timeout (race):', endpoint);
        
        // For orders/values endpoint, return clear error instead of masking with zeros
        if (endpoint.includes('orders/values')) {
          return res.status(504).json({
            error: 'SA API timeout',
            message: 'The upstream API request timed out',
            _apiUnavailable: true,
          });
        }
        
        // Return empty data instead of demo data for other endpoints
        const emptyData = getEmptyResponse(endpoint);
        return res.status(200).json(emptyData);
      }
      throw raceError;
    }

    // Handle non-OK responses
    if (!apiResponse.ok) {
      const errorText = await apiResponse.text().catch(() => 'Unknown error');
      console.error('SA API error response:', apiResponse.status, errorText);
      
      // For orders/values endpoint, return clear error instead of masking with zeros
      if (endpoint.includes('orders/values')) {
        return res.status(502).json({
          error: 'SA API error',
          status: apiResponse.status,
          message: errorText,
          _apiUnavailable: true,
        });
      }
      
      // Return empty data for other upstream API errors (4xx or 5xx)
      // This ensures the UI gets _apiUnavailable flag instead of an error
      const emptyData = getEmptyResponse(endpoint);
      return res.status(200).json(emptyData);
    }

    const data = await apiResponse.json();
    
    // Check if the response contains an error message (SA API sometimes returns 200 with error body)
    if (data && (data.message || data.traceback || data.error)) {
      console.error('SA API returned error in body:', data);
      
      // For orders/values endpoint, return clear error instead of masking with zeros
      if (endpoint.includes('orders/values')) {
        return res.status(502).json({
          error: 'SA API returned error in response body',
          message: data.message || data.error || 'Unknown API error',
          _apiUnavailable: true,
        });
      }
      
      // Return empty data instead of demo data for other endpoints
      const emptyData = getEmptyResponse(endpoint);
      return res.status(200).json(emptyData);
    }
    
    return res.status(apiResponse.status).json(data);
  } catch (error) {
    console.error('SA API proxy error:', error);
    const endpoint = req.body?.endpoint;
    
    // For orders/values endpoint, return clear error instead of masking with zeros
    if (endpoint && endpoint.includes('orders/values')) {
      return res.status(500).json({
        error: 'SA API proxy error',
        message: error.message || 'Unknown proxy error',
        _apiUnavailable: true,
      });
    }
    
    // Return empty data instead of demo data for other endpoints
    const emptyData = getEmptyResponse(endpoint);
    return res.status(200).json(emptyData);
  }
};

// Normalize payloads for SA endpoints.
// The TikTok orders/values API currently returns SERVER_ERROR for ISO date strings
// with milliseconds or +00:00 offsets, while accepting second-precision UTC Z.
function normalizePayloadForSA(endpoint, payload) {
  if (!endpoint || !endpoint.includes('orders/values') || !payload || typeof payload !== 'object') {
    return payload;
  }

  return {
    ...payload,
    from_date: normalizeSADate(payload.from_date),
    to_date: normalizeSADate(payload.to_date),
  };
}

function normalizeSADate(value) {
  if (typeof value !== 'string' || !value.includes('T')) return value;

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;

  return parsed.toISOString().replace(/\.\d{3}Z$/, 'Z');
}

// Get empty response when API is unavailable (no demo data)
function getEmptyResponse(endpoint) {
  if (!endpoint) return { _apiUnavailable: true, _isEmpty: true };
  
  if (endpoint.includes('entity-margin')) {
    return {
      data: [],
      _apiUnavailable: true,
      _isEmpty: true,
    };
  }
  
  if (endpoint.includes('order-analysis')) {
    return {
      items: [],
      _apiUnavailable: true,
      _isEmpty: true,
    };
  }
  
  if (endpoint.includes('orders/values')) {
    return {
      from_currency: 'SGD',
      to_currency: 'SGD',
      fx_rate: 1,
      po_unfulfilled: 0,
      po_fulfilled: 0,
      client_paid_value: 0,
      _apiUnavailable: true,
      _isEmpty: true,
    };
  }
  
  if (endpoint.includes('margin/region')) {
    return { _apiUnavailable: true, _isEmpty: true };
  }
  
  if (endpoint.includes('regions')) {
    return { regions: [], _apiUnavailable: true, _isEmpty: true };
  }
  
  return { _apiUnavailable: true, _isEmpty: true };
}
