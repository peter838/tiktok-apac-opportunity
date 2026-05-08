// SA API Client for TikTok Singapore Opportunity Dashboard
// Routes through /api/sa-proxy.js to avoid CORS issues

class SAAPIClient {
  constructor() {
    // Use same-origin proxy to bypass CORS
    this.proxyUrl = '/api/sa-proxy';
    this.maxRetries = 2;
    this.baseDelay = 1000;
  }

  async makeRequest(endpoint, payload, retryCount = 0) {
    try {
      // Add timeout to the fetch itself (client-side)
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s client timeout

      const response = await fetch(this.proxyUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ endpoint, payload }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        
        // Handle 504 upstream timeout with retry
        if (response.status === 504 && retryCount < this.maxRetries) {
          console.log(`[SA API] 504 timeout, retrying ${endpoint} (attempt ${retryCount + 1}/${this.maxRetries})...`);
          await this.delay(this.baseDelay * (retryCount + 1));
          return this.makeRequest(endpoint, payload, retryCount + 1);
        }
        
        // Handle 502 Bad Gateway (SA API error) - don't retry, return empty data
        if (response.status === 502) {
          console.warn(`[SA API] Upstream API error (502), returning empty data for ${endpoint}`);
          return this.getEmptyResponse(endpoint);
        }
        
        throw new Error(errorData.message || errorData.error || `API Error (${response.status})`);
      }

      return await response.json();
    } catch (error) {
      // Handle network errors and aborts with retry
      if ((error.name === 'AbortError' || error.name === 'TypeError') && retryCount < this.maxRetries) {
        console.log(`[SA API] Network error, retrying ${endpoint} (attempt ${retryCount + 1}/${this.maxRetries})...`);
        await this.delay(this.baseDelay * (retryCount + 1));
        return this.makeRequest(endpoint, payload, retryCount + 1);
      }
      
      console.error(`SA API Error for ${endpoint}:`, error);
      // Return empty data instead of throwing to prevent UI from getting stuck
      return this.getEmptyResponse(endpoint);
    }
  }
  
  getEmptyResponse(endpoint) {
    // Return appropriate empty response structure based on endpoint
    if (endpoint.includes('order-analysis')) {
      return { items: [] }; // Object with items array
    }
    if (endpoint.includes('regions')) {
      return { regions: [] };
    }
    return {};
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Order Analysis by Category - Get category breakdown for Total Spend and Total Orders
  // This is the ONLY endpoint used for dashboard metrics (entity-margin and margin/region removed)
  async getOrderAnalysisByCategory(fromDate, toDate, region = 'SG', entityGroup = 'TikTok') {
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

  // Get available regions
  async getRegions() {
    return this.makeRequest('/v1.0/agent/analytics/regions', {});
  }
}

// Demo data removed - only real data should be displayed

// Data processor for dashboard metrics
class DashboardDataProcessor {
  constructor(region = 'SG') {
    this.apiClient = new SAAPIClient();
    this.region = region;
  }

  async fetchAllMetrics(year = '2025') {
    const fromDate = `${year}-01-01`;
    const toDate = `${year}-12-31`;

    // Only fetch order-analysis endpoint for Total Spend and Total Orders
    const orderAnalysisResult = await this.apiClient.getOrderAnalysisByCategory(fromDate, toDate, this.region, 'TikTok');

    // Check if we have data
    const hasOrderData = orderAnalysisResult?.items?.length > 0 || orderAnalysisResult?._apiUnavailable;

    // If no data available, return empty data
    if (!hasOrderData) {
      console.warn('[DashboardDataProcessor] No data available from API, returning empty data');
      return {
        orderAnalysis: { categories: [], totalSpend: 0, totalOrders: 0, categoryCount: 0 },
        raw: {
          orderAnalysis: { items: [] },
        },
        _isEmpty: true,
      };
    }

    const orderAnalysis = this.processOrderAnalysis(orderAnalysisResult, 'TikTok');
    
    // Check if we're using demo data from the proxy
    const isDemoData = orderAnalysisResult?._isDemoData || orderAnalysisResult?._apiUnavailable;
    
    return {
      orderAnalysis: orderAnalysis,
      raw: {
        orderAnalysis: orderAnalysisResult,
      },
      _isDemoData: isDemoData || false,
    };
  }

  // NOTE: processEntityMargin removed - entity-margin endpoint no longer used
  // Total Spend and Total Orders now come from order-analysis endpoint only

  processOrderAnalysis(data, entityGroupFilter = 'TikTok') {
    // Handle {items: array, values: number} response format
    // Also handle case where API returns array directly
    let items = data?.items || [];
    
    // If data is an array directly, use it as items
    if (Array.isArray(data)) {
      items = data;
    }
    
    if (!items.length) {
      return { categories: [], totalSpend: 0, totalOrders: 0, categoryCount: 0, entities: [] };
    }

    // Check if items have entity_group field
    const hasEntityGroup = items.some(item => item.entity_group !== undefined);

    // Filter by entity_group only if items have that field AND filter is specified
    // The API already filters by region='SG', and for TikTok Singapore page we want all TikTok entities
    const filteredItems = (entityGroupFilter && entityGroupFilter !== 'ALL' && hasEntityGroup)
      ? items.filter(item => item.entity_group === entityGroupFilter)
      : items;

    // Category Analysis: group by category_name
    // Each item in the API response represents one order with order_value
    const categoryMap = new Map();
    filteredItems.forEach(item => {
      const catName = item.category_name || 'Unknown';
      if (!categoryMap.has(catName)) {
        categoryMap.set(catName, {
          name: catName,
          spend: 0,
          orders: 0,
          margin: 0,
        });
      }
      const cat = categoryMap.get(catName);
      cat.spend += parseFloat(item.order_value) || 0;
      // Each item represents one order, so increment by 1
      cat.orders += 1;
      // Margin may not be present in all items
      cat.margin += parseFloat(item.margin) || 0;
    });
    const categories = Array.from(categoryMap.values());

    // Entity Breakdown: group by entity_name
    const entityMap = new Map();
    filteredItems.forEach(item => {
      const entityName = item.entity_name || 'Unknown';
      if (!entityMap.has(entityName)) {
        entityMap.set(entityName, {
          name: entityName,
          spend: 0,
          orders: 0,
          margin: 0,
          entityGroup: item.entity_group || 'TikTok',
        });
      }
      const entity = entityMap.get(entityName);
      entity.spend += parseFloat(item.order_value) || 0;
      // Each item represents one order, so increment by 1
      entity.orders += 1;
      // Margin may not be present in all items
      entity.margin += parseFloat(item.margin) || 0;
    });
    const entities = Array.from(entityMap.values());

    // Total Spend: use the `values` attribute from API response (not calculated from items)
    const totalSpend = parseFloat(data?.values) || 0;
    
    // Total Orders: use the length of items array (count of items)
    const totalOrders = items.length;

    return {
      categories,
      entities,
      totalSpend,
      totalOrders,
      categoryCount: categories.length,
      entityCount: entities.length,
    };
  }
}

// Shared SGD currency formatter for all regional dashboards
function formatSGD(value) {
  if (value === null || value === undefined || isNaN(value)) return '--';
  if (value >= 100000000) return 'S$ ' + (value / 100000000).toFixed(2) + 'B';
  if (value >= 1000000) return 'S$ ' + (value / 1000000).toFixed(2) + 'M';
  if (value >= 1000) return 'S$ ' + (value / 1000).toFixed(2) + 'K';
  return 'S$ ' + value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// Export for use in dashboard
window.SAAPIClient = SAAPIClient;
window.DashboardDataProcessor = DashboardDataProcessor;
window.formatSGD = formatSGD;
