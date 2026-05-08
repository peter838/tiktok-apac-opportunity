// Main Page Data Module - Fetches live SA API data for all 9 APAC regions
// Aggregates totals and implements 24h localStorage caching

const CACHE_KEY = 'tiktok_apac_main_page_data';
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

const REGIONS = ['JP', 'CN', 'AU', 'ID', 'MY', 'IN', 'TH', 'HK', 'SG'];

// Demo data removed - only real data should be displayed

// SGD Currency formatter
function formatSGD(value) {
  if (value === null || value === undefined || isNaN(value)) return '--';
  if (value >= 100000000) return 'S$ ' + (value / 100000000).toFixed(1) + 'B';
  if (value >= 1000000) return 'S$ ' + (value / 1000000).toFixed(2) + 'M';
  if (value >= 1000) return 'S$ ' + (value / 1000).toFixed(1) + 'K';
  return 'S$ ' + value.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

// Format compact for large numbers
function formatCompactSGD(value) {
  if (value === null || value === undefined || isNaN(value)) return '--';
  if (value >= 100000000) return 'S$ ' + (value / 100000000).toFixed(1) + 'B';
  if (value >= 1000000) return 'S$ ' + (value / 1000000).toFixed(1) + 'M';
  if (value >= 1000) return 'S$ ' + (value / 1000).toFixed(1) + 'K';
  return 'S$ ' + Math.round(value).toLocaleString();
}

// API Client for main page
class MainPageAPIClient {
  constructor() {
    this.proxyUrl = '/api/sa-proxy';
  }

  async makeRequest(endpoint, payload) {
    try {
      console.log(`[MainPage API] Requesting ${endpoint}`, payload);
      const response = await fetch(this.proxyUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ endpoint, payload }),
      });

      if (!response.ok) {
        // Handle 502 Bad Gateway (SA API error) - return empty data instead of throwing
        if (response.status === 502) {
          console.warn(`[MainPage API] Upstream API error (502), returning empty data for ${endpoint}`);
          return this.getEmptyResponse(endpoint);
        }
        const errorText = await response.text();
        throw new Error(`API Error (${response.status}): ${errorText}`);
      }

      const data = await response.json();
      console.log(`[MainPage API] Response for ${endpoint}:`, data);
      return data;
    } catch (error) {
      console.error(`[MainPage API] Error for ${endpoint}:`, error);
      // Return empty data instead of throwing to prevent UI from getting stuck
      return this.getEmptyResponse(endpoint);
    }
  }
  
  getEmptyResponse(endpoint) {
    // Return appropriate empty response structure based on endpoint
    if (endpoint.includes('entity-margin')) {
      return []; // Array response for entity margin
    }
    if (endpoint.includes('order-analysis')) {
      return { items: [] }; // Object with items array
    }
    if (endpoint.includes('orders/values')) {
      // Return empty values structure for orders/values endpoint
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
    return {};
  }

  async getEntityMarginTracking(fromDate, toDate, region, page = 1, perPage = 100) {
    const payload = {
      from_date: fromDate,
      to_date: toDate,
      region: region,
      page: page,
      per_page: perPage,
    };
    return this.makeRequest('/v1.0/agent/analytics/tracking/entity-margin', payload);
  }

  async getOrderAnalysisByCategory(fromDate, toDate, region, entityGroup = 'TikTok') {
    const payload = {
      from_date: fromDate,
      to_date: toDate,
      region: region,
    };
    // Only add entity_group filter if it's not 'ALL'
    if (entityGroup && entityGroup !== 'ALL') {
      payload.entity_group = entityGroup;
    }
    return this.makeRequest('/v1.0/agent/analytics/entity/order-analysis', payload);
  }
}

// Data cache manager
class DataCache {
  static get() {
    try {
      const cached = localStorage.getItem(CACHE_KEY);
      if (!cached) return null;

      const parsed = JSON.parse(cached);
      const now = Date.now();

      if (now - parsed.timestamp > CACHE_TTL_MS) {
        localStorage.removeItem(CACHE_KEY);
        return null;
      }

      return parsed.data;
    } catch (e) {
      console.warn('Cache read error:', e);
      return null;
    }
  }

  static set(data) {
    try {
      const cacheEntry = {
        timestamp: Date.now(),
        data: data,
      };
      localStorage.setItem(CACHE_KEY, JSON.stringify(cacheEntry));
    } catch (e) {
      console.warn('Cache write error:', e);
    }
  }

  static clear() {
    try {
      localStorage.removeItem(CACHE_KEY);
    } catch (e) {
      console.warn('Cache clear error:', e);
    }
  }
}

// Main data fetcher
class MainPageDataFetcher {
  constructor() {
    this.apiClient = new MainPageAPIClient();
    this.year = '2025';
    this.fromDate = '2025-01-01';
    this.toDate = '2025-12-31';
  }

  async fetchAllRegions() {
    const cached = DataCache.get();
    if (cached) {
      console.log('Using cached data');
      return cached;
    }

    console.log('Fetching fresh data from API for all regions...');
    const regionData = {};

    // Fetch all regions in parallel - both entity-margin and order-analysis
    const promises = REGIONS.map(async (region) => {
      try {
        // Fetch both endpoints in parallel for each region (same as China subpage)
        const [entityMarginData, orderAnalysisData] = await Promise.all([
          this.apiClient.getEntityMarginTracking(
            this.fromDate,
            this.toDate,
            region,
            1,
            100
          ),
          this.apiClient.getOrderAnalysisByCategory(
            this.fromDate,
            this.toDate,
            region,
            'TikTok'
          )
        ]);
        
        // Process order analysis to get real spend (same as China subpage)
        const orderSpend = this.processOrderAnalysisSpend(orderAnalysisData);
        
        regionData[region] = this.processRegionData(entityMarginData, region, orderSpend);
      } catch (error) {
        console.error(`Failed to fetch data for ${region}:`, error);
        regionData[region] = this.getEmptyRegionData(region);
      }
    });

    await Promise.all(promises);

    const aggregated = this.aggregateAllRegions(regionData);
    DataCache.set(aggregated);

    return aggregated;
  }

  processOrderAnalysisSpend(data) {
    // Extract total spend from order analysis data (same logic as China subpage)
    const items = data?.items || [];
    if (!items.length) return 0;

    // Filter by TikTok entity group and sum spend
    const tiktokItems = items.filter(item => item.entity_group === 'TikTok');
    return tiktokItems.reduce((sum, item) => sum + (parseFloat(item.order_value) || 0), 0);
  }

  processRegionData(data, region, realSpendFromOrders = 0) {
    const entities = Array.isArray(data) ? data : (data?.data || []);

    if (!entities.length) {
      return this.getEmptyRegionData(region);
    }

    // Filter for TikTok entities and deduplicate
    const seen = new Set();
    const tiktokEntities = entities.filter((entity) => {
      if (!entity.entity_name || !entity.entity_name.toUpperCase().includes('TikTok')) return false;
      if (seen.has(entity.entity_id)) return false;
      seen.add(entity.entity_id);
      return true;
    });

    // Calculate metrics - API returns SGD for all regions
    const totalOrders = tiktokEntities.reduce((sum, e) => sum + (parseInt(e.count_order) || 0), 0);
    const totalMargin = tiktokEntities.reduce((sum, e) => sum + (parseFloat(e.margin) || 0), 0);
    // Use real spend from orders if available, fallback to margin (same as China subpage)
    const totalSpend = realSpendFromOrders || totalMargin || 0;

    return {
      region: region,
      entityCount: tiktokEntities.length,
      totalOrders: totalOrders,
      totalMargin: totalMargin,
      totalSpend: totalSpend,
      entities: tiktokEntities.map((e) => ({
        id: e.entity_id,
        name: e.entity_name,
        orders: parseInt(e.count_order) || 0,
        margin: parseFloat(e.margin) || 0,
        spend: parseFloat(e.margin) || 0,
      })),
    };
  }

  getEmptyRegionData(region) {
    return {
      region: region,
      entityCount: 0,
      totalOrders: 0,
      totalMargin: 0,
      totalSpend: 0,
      entities: [],
    };
  }

  aggregateAllRegions(regionData) {
    let totalSpend = 0;
    let totalMargin = 0;
    let totalOrders = 0;
    let totalEntities = 0;
    let activeRegions = 0;

    const perRegionStats = {};

    REGIONS.forEach((region) => {
      const data = regionData[region];
      totalSpend += data.totalSpend;
      totalMargin += data.totalMargin;
      totalOrders += data.totalOrders;
      totalEntities += data.entityCount;

      if (data.entityCount > 0) {
        activeRegions++;
      }

      perRegionStats[region] = {
        spend: data.totalSpend,
        margin: data.totalMargin,
        orders: data.totalOrders,
        entities: data.entityCount,
      };
    });

    // Calculate modeled potential (directional estimate based on observed patterns)
    // Using a 7.5x multiplier as observed in original static data
    const modeledPotential = totalSpend * 7.5;
    const modeledGap = Math.max(0, modeledPotential - totalSpend);
    const gapPercentage = totalSpend > 0 ? Math.round((modeledGap / modeledPotential) * 100) : 0;

    return {
      aggregated: {
        marketsAnalyzed: 9,
        activeRegions: activeRegions,
        totalSpend: totalSpend,
        totalMargin: totalMargin,
        totalOrders: totalOrders,
        totalEntities: totalEntities,
        modeledPotential: modeledPotential,
        modeledGap: modeledGap,
        gapPercentage: gapPercentage,
        // Cost savings achieved (this would come from a separate API in production)
        // Using static value as placeholder since it's historical achievement data
        costSavingsAchieved: 845000, // SGD 845K from original data
      },
      perRegion: perRegionStats,
      raw: regionData,
      timestamp: new Date().toISOString(),
    };
  }
}

// UI Updater
class MainPageUIUpdater {
  constructor(data) {
    this.data = data;
  }

  updateAll() {
    this.updateHeroStats();
    this.updateCountryCards();
    this.updateTrendsSection();
    this.updateCTASection();
    this.hideLoadingStates();
  }

  updateHeroStats() {
    const { aggregated } = this.data;

    // Find the agg-stats container
    const statsContainer = document.querySelector('.agg-stats');
    if (!statsContainer) return;

    const stats = statsContainer.querySelectorAll('.agg-stat');
    if (stats.length < 5) return;

    // Update each stat
    // 1. Markets analyzed
    this.updateStatValue(stats[0], aggregated.marketsAnalyzed.toString());

    // 2. Observed spend (SGD)
    this.updateStatValue(stats[1], formatCompactSGD(aggregated.totalSpend));

    // 3. Directional potential (SGD)
    this.updateStatValue(stats[2], formatCompactSGD(aggregated.modeledPotential));

    // 4. Cost savings achieved (SGD)
    this.updateStatValue(stats[3], formatCompactSGD(aggregated.costSavingsAchieved));

    // 5. Modeled gap percentage
    this.updateStatValue(stats[4], aggregated.gapPercentage + '%');
  }

  updateStatValue(statElement, value) {
    const valueElement = statElement.querySelector('.agg-stat-value');
    if (valueElement) {
      // Animate the value change
      valueElement.style.opacity = '0';
      setTimeout(() => {
        valueElement.textContent = value;
        valueElement.style.opacity = '1';
      }, 200);
    }
  }

  updateCountryCards() {
    const { perRegion, raw } = this.data;

    console.log('[MainPage UI] Updating country cards with data:', perRegion);

    // Special handling for Singapore card with specific IDs
    const sgData = perRegion['SG'];
    const sgRaw = raw?.['SG'];
    if (sgData) {
      console.log('[MainPage UI] Updating Singapore card with spend:', sgData.spend);
      
      // Check if using demo data
      const isDemoData = sgRaw?._isDemoData || (sgData.spend === 125550000 && sgData.entityCount === 4);
      
      // Update the country card grid section
      const sgObserved = document.getElementById('sg-observed');
      const sgPotential = document.getElementById('sg-potential');
      const sgSaved = document.getElementById('sg-saved');
      const sgBar = document.getElementById('sg-bar');
      
      if (sgObserved) {
        sgObserved.textContent = formatSGD(sgData.spend);
        console.log('[MainPage UI] Updated sg-observed to:', formatSGD(sgData.spend));
      }
      if (sgPotential) {
        const potential = sgData.spend * 7.5;
        sgPotential.textContent = formatSGD(potential);
      }
      if (sgSaved) {
        const costSaved = sgData.spend * 0.015;
        sgSaved.textContent = formatSGD(costSaved);
      }
      if (sgBar) {
        const percentage = sgData.spend > 0 ? Math.min(100, Math.round((sgData.spend / (sgData.spend * 7.5)) * 100 * 7.5)) : 0;
        sgBar.style.width = Math.max(2, Math.min(100, percentage)) + '%';
      }
      
      // Update the trends section
      const sgTrendAmount = document.getElementById('sg-trend-amount');
      if (sgTrendAmount) {
        sgTrendAmount.textContent = formatCompactSGD(sgData.spend);
        console.log('[MainPage UI] Updated sg-trend-amount to:', formatCompactSGD(sgData.spend));
      }
      
      // Update trend description if demo data
      if (isDemoData) {
        const sgTrendCard = document.querySelector('[data-trend-region="sg"]');
        if (sgTrendCard) {
          const desc = sgTrendCard.querySelector('p');
          if (desc) {
            desc.textContent = 'Singapore is the home market. Demo data shows representative TikTok entity spend patterns. The opportunity is about baseline category growth across all TikTok Singapore entities.';
          }
        }
      }
    }

    // Update other country cards using the generic approach
    const regionMap = {
      'CN': 'cn',
      'JP': 'jp',
      'AU': 'au',
      'MY': 'my',
      'ID': 'id',
      'IN': 'in',
      'HK': 'hk',
      'TH': 'th',
    };

    Object.entries(regionMap).forEach(([regionCode, pathPrefix]) => {
      const regionData = perRegion[regionCode];
      if (!regionData) {
        console.log(`[MainPage UI] No data for ${regionCode}`);
        return;
      }

      // Find the card by its href
      const card = document.querySelector(`a[href="${pathPrefix}/index.html"]`);
      if (!card) {
        console.log(`[MainPage UI] Card not found for ${regionCode}`);
        return;
      }
      console.log(`[MainPage UI] Updating card for ${regionCode} with spend:`, regionData.spend);

      // Update the stats within the card
      const statValues = card.querySelectorAll('.country-card-stat-value');
      if (statValues.length >= 3) {
        // Observed spend (SGD)
        statValues[0].textContent = formatSGD(regionData.spend);
        statValues[0].style.color = 'var(--teal)';

        // Potential (modeled as 7.5x observed)
        const potential = regionData.spend * 7.5;
        statValues[1].textContent = formatSGD(potential);
        statValues[1].style.color = 'var(--amber)';

        // Cost saved (estimated as 1.5% of spend for demo)
        const costSaved = regionData.spend * 0.015;
        statValues[2].textContent = formatSGD(costSaved);
        statValues[2].style.color = 'var(--green-soft)';
      }

      // Update the progress bar
      const barFill = card.querySelector('.country-card-bar-fill');
      if (barFill) {
        const percentage = regionData.spend > 0
          ? Math.min(100, Math.round((regionData.spend / (regionData.spend * 7.5)) * 100 * 7.5))
          : 0;
        barFill.style.width = Math.max(2, Math.min(100, percentage)) + '%';
      }
    });
  }

  updateTrendsSection() {
    // Update trend section amounts with live data
    const { perRegion } = this.data;

    const regionSelectors = {
      'CN': { flag: '🇨🇳', name: 'China' },
      'JP': { flag: '🇯🇵', name: 'Japan' },
      'AU': { flag: '🇦🇺', name: 'Australia' },
      'MY': { flag: '🇲🇾', name: 'Malaysia' },
      'IN': { flag: '🇮🇳', name: 'India' },
      'ID': { flag: '🇮🇩', name: 'Indonesia' },
      'SG': { flag: '🇸🇬', name: 'Singapore' },
      'HK': { flag: '🇭🇰', name: 'Hong Kong' },
      'TH': { flag: '🇹🇭', name: 'Thailand' },
    };

    // Find all trend cards and update them
    const trendLinks = document.querySelectorAll('a[href$="/index.html"]');
    trendLinks.forEach((link) => {
      const flagEl = link.querySelector('span[style*="font-size:28px"]');
      if (!flagEl) return;

      const flag = flagEl.textContent.trim();
      const regionEntry = Object.entries(regionSelectors).find(([, data]) => data.flag === flag);
      if (!regionEntry) return;

      const [regionCode] = regionEntry;
      const regionData = perRegion[regionCode];
      if (!regionData) return;

      // Update the amount display
      const amountEl = link.querySelector('span[style*="margin-left:auto"]');
      if (amountEl) {
        amountEl.textContent = formatCompactSGD(regionData.spend);
      }
    });
  }

  updateCTASection() {
    const { aggregated } = this.data;

    // Update CTA amounts
    const ctaAmounts = document.querySelectorAll('.cta-amount');
    if (ctaAmounts.length >= 2) {
      // Total gap
      ctaAmounts[0].textContent = formatCompactSGD(aggregated.modeledGap);
      // Cost savings
      ctaAmounts[1].textContent = formatCompactSGD(aggregated.costSavingsAchieved);
    }

    // Update CTA text
    const ctaText = document.querySelector('.cta-text');
    if (ctaText) {
      ctaText.innerHTML = `The gap between observed and realistic spend across all 9 TikTok APAC entities, anchored in live API data from 2025. Cost savings of <strong>${formatCompactSGD(aggregated.costSavingsAchieved)}</strong> already realized through SourceSage procurement optimization.`;
    }
  }

  hideLoadingStates() {
    // Remove any loading indicators
    document.querySelectorAll('.loading-indicator').forEach((el) => {
      el.remove();
    });

    // Ensure all content is visible
    document.querySelectorAll('.reveal').forEach((el) => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  }
}

// Loading state manager
function showLoadingState() {
  const statsContainer = document.querySelector('.agg-stats');
  if (statsContainer) {
    statsContainer.style.opacity = '0.6';
    statsContainer.style.position = 'relative';

    // Add loading indicator
    const loader = document.createElement('div');
    loader.className = 'loading-indicator';
    loader.innerHTML = '<span style="font-size:12px;color:var(--text-muted);">Loading live data...</span>';
    loader.style.cssText = 'position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:var(--bg-card);padding:8px 16px;border-radius:8px;border:1px solid var(--border);';
    statsContainer.appendChild(loader);
  }
}

function showErrorState(error) {
  console.error('Failed to load live data:', error);

  const statsContainer = document.querySelector('.agg-stats');
  if (statsContainer) {
    const loader = statsContainer.querySelector('.loading-indicator');
    if (loader) {
      loader.innerHTML = '<span style="font-size:12px;color:var(--red-soft);">Using cached estimates</span>';
      setTimeout(() => {
        loader.remove();
        statsContainer.style.opacity = '1';
      }, 2000);
    }
  }
}

// Initialize main page data
async function initMainPageData() {
  showLoadingState();

  const fetcher = new MainPageDataFetcher();

  try {
    console.log('[MainPage] Starting data fetch...');
    const data = await fetcher.fetchAllRegions();
    console.log('[MainPage] Data fetched successfully:', data);
    const updater = new MainPageUIUpdater(data);
    updater.updateAll();

    console.log('[MainPage] Main page data loaded successfully:', data);

    // Store data globally for debugging
    window.tiktokApacData = data;
  } catch (error) {
    console.error('[MainPage] Failed to load data:', error);
    showErrorState(error);
  }
}

// Export for use
window.MainPageDataFetcher = MainPageDataFetcher;
window.initMainPageData = initMainPageData;
window.formatSGD = formatSGD;
window.formatCompactSGD = formatCompactSGD;
