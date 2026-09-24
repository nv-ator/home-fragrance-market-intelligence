/**
 * Centralized API client for Home Fragrance Market Intelligence Dashboard.
 * Consumes the FastAPI backend endpoints with environment variable fallback.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function fetchJson(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      }
    });

    if (!res.ok) {
      let errorDetail = `HTTP ${res.status}: ${res.statusText}`;
      try {
        const errorJson = await res.json();
        if (errorJson.detail) {
          errorDetail = typeof errorJson.detail === 'string' ? errorJson.detail : JSON.stringify(errorJson.detail);
        }
      } catch (e) {
        // Fallback to status text
      }
      throw new Error(errorDetail);
    }

    return await res.json();
  } catch (err) {
    console.error(`[API Client Error] Failed to fetch ${url}:`, err);
    throw err;
  }
}

export const getHealth = () => fetchJson('/api/health');
export const getOverview = () => fetchJson('/api/overview');
export const getBrands = () => fetchJson('/api/brands');
export const getBrandsComparison = () => fetchJson('/api/brands/comparison');
export const getBrandComparison = () => fetchJson('/api/brands/comparison');
export const getBrandDetail = (brandName) => fetchJson(`/api/brands/${encodeURIComponent(brandName)}`);
export const getProducts = (params = {}) => {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') {
      query.append(k, v);
    }
  });
  const queryString = query.toString() ? `?${query.toString()}` : '';
  return fetchJson(`/api/products${queryString}`);
};
export const getProductDetail = (productId) => fetchJson(`/api/products/${productId}`);
export const getPricePositioning = () => fetchJson('/api/analytics/price-positioning');
export const getPriceNormalization = () => fetchJson('/api/analytics/price-normalization');
export const getCategories = () => fetchJson('/api/analytics/categories');
export const getPlatforms = () => fetchJson('/api/analytics/platforms');
export const getDiscounts = () => fetchJson('/api/analytics/discounts');
export const getCategoryCoverage = () => fetchJson('/api/analytics/category-coverage');
export const getProductClusters = () => fetchJson('/api/analytics/product-clusters');
export const getFilters = () => fetchJson('/api/filters');
export const getFilterOptions = () => fetchJson('/api/filters');
export const getInsights = () => fetchJson('/api/insights');

export const api = {
  getHealth,
  getOverview,
  getBrands,
  getBrandComparison,
  getBrandsComparison,
  getBrandDetail,
  getProducts,
  getProductDetail,
  getPricePositioning,
  getPriceNormalization,
  getCategories,
  getPlatforms,
  getDiscounts,
  getCategoryCoverage,
  getProductClusters,
  getFilters,
  getFilterOptions,
  getInsights
};

export default api;
