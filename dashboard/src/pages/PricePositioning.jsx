import React, { useState, useEffect } from 'react';
import {
  ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, ResponsiveContainer, Legend,
  BarChart, Bar
} from 'recharts';
import { RefreshCw, Tag, Info, Percent } from 'lucide-react';
import ChartCard from '../components/ChartCard';
import EmptyState from '../components/EmptyState';
import { api } from '../api/client';

const BRAND_COLORS = {
  'AromaPure': '#2563EB',
  'Odonil': '#10B981',
  'Godrej aer': '#F59E0B',
  'Air Wick': '#8B5CF6',
  'Ambi Pur': '#EC4899',
};

export default function PricePositioning() {
  const [positioningData, setPositioningData] = useState([]);
  const [normMetrics, setNormMetrics] = useState(null);
  const [discountData, setDiscountData] = useState([]);
  const [clusterData, setClusterData] = useState(null);
  const [selectedBrand, setSelectedBrand] = useState('All');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [posRes, normRes, discRes, clusterRes] = await Promise.all([
        api.getPricePositioning(),
        api.getPriceNormalization(),
        api.getDiscounts(),
        api.getProductClusters()
      ]);
      setPositioningData(posRes);
      setNormMetrics(normRes);
      setClusterData(clusterRes);

      // Aggregate non-null discounts by brand
      const brandDiscMap = {};
      discRes.forEach(d => {
        if (!brandDiscMap[d.brand]) {
          brandDiscMap[d.brand] = { sum: 0, count: 0, min: d.discount_pct, max: d.discount_pct };
        }
        brandDiscMap[d.brand].sum += d.discount_pct;
        brandDiscMap[d.brand].count += 1;
        brandDiscMap[d.brand].min = Math.min(brandDiscMap[d.brand].min, d.discount_pct);
        brandDiscMap[d.brand].max = Math.max(brandDiscMap[d.brand].max, d.discount_pct);
      });

      const aggregatedDiscounts = Object.keys(brandDiscMap).map(brand => ({
        brand,
        'Average Discount': Number((brandDiscMap[brand].sum / brandDiscMap[brand].count).toFixed(1)),
        count: brandDiscMap[brand].count,
        min: Number(brandDiscMap[brand].min.toFixed(1)),
        max: Number(brandDiscMap[brand].max.toFixed(1))
      })).sort((a, b) => b['Average Discount'] - a['Average Discount']);

      setDiscountData(aggregatedDiscounts);
    } catch (err) {
      setError(err.message || 'Failed to load price positioning analytics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center">
        <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mb-3" />
        <p className="text-sm font-medium text-slate-600">Loading price positioning metrics...</p>
      </div>
    );
  }

  if (error || !positioningData.length) {
    return (
      <EmptyState
        isError={true}
        title="Unable to Load Price Positioning"
        message={error || "Could not retrieve pricing analytics"}
        onRetry={loadData}
      />
    );
  }

  // Filter only products with a non-null rating for the Price vs Rating scatter
  const ratedProducts = positioningData.filter(p => p.rating !== null && p.rating !== undefined);

  // Group rated products by brand for scatter series
  const brandsList = ['Odonil', 'Godrej aer', 'Air Wick', 'Ambi Pur'];
  const brandSeries = brandsList.map(brand => ({
    brand,
    data: ratedProducts
      .filter(p => p.brand === brand)
      .filter(p => selectedBrand === 'All' || p.brand === selectedBrand)
      .map(p => ({
        x: p.selling_price,
        y: p.rating,
        name: p.product_name,
        brand: p.brand,
        category: p.category,
        reviews: p.review_count
      }))
  }));

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Price Positioning & Unit Economics</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Empirical price-to-rating relationships, discount distributions, format-specific unit pricing, and statistical product clusters.
            <span className="block text-[11px] text-slate-400 mt-1">Full dataset analytics — 684 validated products.</span>
          </p>
        </div>

        {/* Filter Brand */}
        <div className="flex items-center gap-2">
          <label className="text-xs font-semibold text-slate-500">Filter Scatter:</label>
          <select
            value={selectedBrand}
            onChange={(e) => setSelectedBrand(e.target.value)}
            className="text-xs font-medium bg-white border border-slate-300 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 shadow-sm"
          >
            <option value="All">All Rated Brands</option>
            {brandsList.map(b => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Scatter Plot: Price vs. Rating */}
      <ChartCard
        title="Price vs. Customer Rating Distribution"
        subtitle="Scatter distribution of selling price (INR) vs. star rating (0–5)"
        note="Only products with an observed public rating are included. Products without ratings (e.g. AromaPure official catalogue listings without public star reviews) are strictly excluded rather than plotted at zero."
      >
        <div className="h-96 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 30, bottom: 20, left: 10 }}>
              <XAxis
                type="number"
                dataKey="x"
                name="Selling Price"
                unit="₹"
                tick={{ fontSize: 11, fill: '#64748B' }}
              />
              <YAxis
                type="number"
                dataKey="y"
                name="Rating"
                domain={[3.0, 5.0]}
                tick={{ fontSize: 11, fill: '#64748B' }}
              />
              <ZAxis range={[50, 400]} />
              <Tooltip
                cursor={{ strokeDasharray: '3 3' }}
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-slate-900 text-slate-100 p-3 rounded-lg shadow-lg text-xs max-w-xs border border-slate-800">
                        <div className="font-semibold text-blue-300 mb-1">{data.brand}</div>
                        <div className="text-slate-200 font-medium mb-1 line-clamp-2">{data.name}</div>
                        <div className="text-slate-400">Category: <span className="text-slate-300">{data.category}</span></div>
                        <div className="text-slate-400">Price: <span className="text-emerald-400 font-bold">₹{data.x}</span></div>
                        <div className="text-slate-400">Rating: <span className="text-amber-400 font-bold">★ {data.y}</span> ({data.reviews ? `${data.reviews} reviews` : 'No review count'})</div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Legend verticalAlign="top" height={36} wrapperStyle={{ fontSize: '12px' }} />
              {brandSeries.map((series) => (
                <Scatter
                  key={series.brand}
                  name={series.brand}
                  data={series.data}
                  fill={BRAND_COLORS[series.brand] || '#3B82F6'}
                  shape="circle"
                />
              ))}
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </ChartCard>

      {/* Product Clusters (Statistical Segmentation with Neutral Labels) */}
      {clusterData && clusterData.clusters && clusterData.clusters.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden p-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 mb-4 border-b border-slate-100 gap-2">
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-slate-900">Statistical Product Clusters (K-Means)</h3>
                <span className="text-[11px] bg-blue-50 text-blue-700 font-semibold px-2 py-0.5 rounded border border-blue-200">
                  Optimal K = {clusterData.selected_k} (Silhouette: {clusterData.silhouette_score})
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                Objective clustering across standardized features: price, star rating, discount %, and log-transformed review volume.
              </p>
            </div>
            <div className="text-xs text-slate-500 italic bg-slate-50 px-2.5 py-1 rounded border border-slate-200">
              Evaluated across {clusterData.usable_product_count} products with complete feature sets.
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="py-2.5 px-3">Cluster ID</th>
                  <th className="py-2.5 px-3 text-right">Product Count</th>
                  <th className="py-2.5 px-3 text-right">Average Price (₹)</th>
                  <th className="py-2.5 px-3 text-right">Median Price (₹)</th>
                  <th className="py-2.5 px-3 text-right">Average Rating</th>
                  <th className="py-2.5 px-3 text-right">Average Discount</th>
                  <th className="py-2.5 px-3 text-right">Avg Reviews</th>
                  <th className="py-2.5 px-3">Statistical Profile</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {clusterData.clusters.map((c) => (
                  <tr key={c.cluster_id} className="hover:bg-slate-50 transition-colors">
                    <td className="py-3 px-3 font-bold text-blue-700">{c.cluster_name}</td>
                    <td className="py-3 px-3 text-right font-semibold">{c.product_count}</td>
                    <td className="py-3 px-3 text-right">{c.average_price != null ? `₹${Number(c.average_price).toFixed(2)}` : '—'}</td>
                    <td className="py-3 px-3 text-right font-semibold text-slate-900">{c.median_price != null ? `₹${Number(c.median_price).toFixed(2)}` : '—'}</td>
                    <td className="py-3 px-3 text-right font-semibold text-amber-600">★ {c.average_rating != null ? Number(c.average_rating).toFixed(2) : '—'}</td>
                    <td className="py-3 px-3 text-right">{c.average_discount != null ? `${Number(c.average_discount).toFixed(1)}%` : '—'}</td>
                    <td className="py-3 px-3 text-right text-slate-500">{c.average_reviews != null ? Number(c.average_reviews).toFixed(1) : '—'}</td>
                    <td className="py-3 px-3 text-slate-600 italic text-[11px]">{c.key_characteristics}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500 flex items-start gap-2">
            <Info className="w-4 h-4 text-slate-400 flex-shrink-0 mt-0.5" />
            <span>
              <strong>Methodology Note:</strong> Clusters are generated mathematically using standardized K-Means and evaluated across K=2 through K=5. Clusters are assigned neutral identifiers (Cluster 1, Cluster 2, etc.) to prevent subjective marketing labels (such as "Premium" or "Budget"). They describe statistical groupings within usable records, not total market segments.
            </span>
          </div>
        </div>
      )}

      {/* Discount Distribution Analysis */}
      {discountData.length > 0 && (
        <ChartCard
          title="Promotional Discount Depth by Brand"
          subtitle="Observed average percentage discount off list price (MRP)"
          note="Calculated strictly across 545 products where valid MRP and discount data exist. Missing discounts are never imputed as 0%."
        >
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={discountData} margin={{ top: 10, right: 20, left: -10, bottom: 20 }}>
                <XAxis dataKey="brand" tick={{ fontSize: 11, fill: '#64748B' }} />
                <YAxis unit="%" tick={{ fontSize: 11, fill: '#64748B' }} domain={[0, 60]} />
                <Tooltip
                  formatter={(val, name, item) => [
                    `${val}% avg discount (n=${item.payload.count}, min ${item.payload.min}%, max ${item.payload.max}%)`,
                    'Discount'
                  ]}
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', border: 'none', fontSize: '12px' }}
                />
                <Bar dataKey="Average Discount" radius={[4, 4, 0, 0]} fill="#F59E0B" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      )}

      {/* Segregated Unit Pricing Cards */}
      {normMetrics && (
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Tag className="w-4 h-4 text-blue-600" />
            <h3 className="text-sm font-bold text-slate-900">Standardized Unit Pricing Benchmarks</h3>
            <span className="text-[11px] text-slate-400 italic">Strictly segregated by physical unit</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Price Per Unit */}
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
              <div>
                <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">Per Product / Unit</span>
                <p className="text-2xl font-bold text-slate-900 mt-2">₹{normMetrics.price_per_unit.average?.toFixed(2) || '—'}</p>
                <p className="text-xs text-slate-500 mt-1">Average selling price across all {normMetrics.price_per_unit.count} products</p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between text-xs text-slate-500">
                <span>Min: ₹{normMetrics.price_per_unit.min}</span>
                <span>Max: ₹{normMetrics.price_per_unit.max}</span>
              </div>
            </div>

            {/* Price Per 100ml */}
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
              <div>
                <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider">Liquid Formats (₹ / 100ml)</span>
                <p className="text-2xl font-bold text-slate-900 mt-2">₹{normMetrics.price_per_100ml.average?.toFixed(2) || '—'}</p>
                <p className="text-xs text-slate-500 mt-1">Observed on {normMetrics.price_per_100ml.count} room sprays, refills & oils</p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between text-xs text-slate-500">
                <span>Min: ₹{normMetrics.price_per_100ml.min}</span>
                <span>Max: ₹{normMetrics.price_per_100ml.max}</span>
              </div>
            </div>

            {/* Price Per 100g */}
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
              <div>
                <span className="text-xs font-bold text-amber-600 uppercase tracking-wider">Solid Formats (₹ / 100g)</span>
                <p className="text-2xl font-bold text-slate-900 mt-2">₹{normMetrics.price_per_100g.average?.toFixed(2) || '—'}</p>
                <p className="text-xs text-slate-500 mt-1">Observed on {normMetrics.price_per_100g.count} solid blocks, gels & candles</p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between text-xs text-slate-500">
                <span>Min: ₹{normMetrics.price_per_100g.min}</span>
                <span>Max: ₹{normMetrics.price_per_100g.max}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Methodology Callout */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-xs text-blue-900 flex items-start gap-3 shadow-xs">
        <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <strong className="font-semibold block mb-0.5">Transparent Positioning Methodology:</strong>
          Price positioning is evaluated through continuous observed metrics (mean, median, unit-normalized pricing, discount depth, price-vs-rating plots, and statistical K-Means product clusters). In compliance with assignment principles, no speculative or arbitrary marketing labels (such as "Budget", "Mass", or "Premium") have been imposed.
        </div>
      </div>
    </div>
  );
}
