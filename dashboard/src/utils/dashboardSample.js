import { getProducts } from '../api/client';

export const SAMPLE_BRANDS = ['AromaPure', 'Odonil', 'Godrej aer', 'Air Wick', 'Ambi Pur'];
export const SAMPLE_SIZE_PER_BRAND = 24;

export async function getDashboardSample() {
  const responses = await Promise.all(SAMPLE_BRANDS.map((brand) => (
    getProducts({ brand, page: 1, limit: 200 })
  )));

  return responses.flatMap((response) => (
    (response.products || [])
      .slice()
      .sort((a, b) => String(a.canonical_id || a.product_id).localeCompare(String(b.canonical_id || b.product_id)))
      .slice(0, SAMPLE_SIZE_PER_BRAND)
  ));
}

function median(values) {
  const sorted = values.filter((value) => value !== null && value !== undefined).sort((a, b) => a - b);
  if (!sorted.length) return null;
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}

function average(values) {
  const valid = values.filter((value) => value !== null && value !== undefined);
  return valid.length ? valid.reduce((sum, value) => sum + value, 0) / valid.length : null;
}

function countShare(products, getName) {
  const counts = new Map();
  products.forEach((product) => {
    const name = getName(product) || 'Not available';
    counts.set(name, (counts.get(name) || 0) + 1);
  });
  return Array.from(counts, ([name, product_count]) => ({
    name,
    product_count,
    pct_share: Number(((product_count * 100) / products.length).toFixed(2))
  })).sort((a, b) => b.product_count - a.product_count);
}

export function summarizeDashboardSample(products) {
  const priceDistribution = [
    ['Under ₹250', (price) => price < 250],
    ['₹250 - ₹499', (price) => price >= 250 && price < 500],
    ['₹500 - ₹999', (price) => price >= 500 && price < 1000],
    ['₹1,000 - ₹1,999', (price) => price >= 1000 && price < 2000],
    ['₹2,000+', (price) => price >= 2000]
  ].map(([name, matches]) => {
    const product_count = products.filter((product) => product.selling_price != null && matches(product.selling_price)).length;
    return { name, product_count, pct_share: Number(((product_count * 100) / products.length).toFixed(2)) };
  });

  return {
    total_products: products.length,
    total_brands: new Set(products.map((product) => product.brand)).size,
    average_price: average(products.map((product) => product.selling_price)),
    median_price: median(products.map((product) => product.selling_price)),
    average_rating: average(products.map((product) => product.rating)),
    average_discount: average(products.map((product) => product.discount_pct)),
    observed_reviews: products.reduce((total, product) => total + (product.review_count ?? 0), 0),
    products_by_brand: countShare(products, (product) => product.brand),
    products_by_platform: countShare(products, (product) => product.platform),
    products_by_category: countShare(products, (product) => product.category),
    price_distribution: priceDistribution
  };
}
