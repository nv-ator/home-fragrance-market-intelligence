import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { RefreshCw, Layers } from 'lucide-react';
import ChartCard from '../components/ChartCard';
import EmptyState from '../components/EmptyState';
import { api } from '../api/client';

export default function BrandComparison() {
  const [comparison, setComparison] = useState([]);
  const [selectedBrand, setSelectedBrand] = useState('All');
  const [brandDetail, setBrandDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getBrandComparison();
      setComparison(res);

      if (selectedBrand !== 'All') {
        const detail = await api.getBrandDetail(selectedBrand);
        setBrandDetail(detail);
      } else {
        setBrandDetail(null);
      }
    } catch (err) {
      setError(err.message || 'Failed to load brand comparison');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedBrand]);

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center">
        <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mb-3" />
        <p className="text-sm font-medium text-slate-600">Loading brand benchmark data...</p>
      </div>
    );
  }

  if (error || !comparison.length) {
    return (
      <EmptyState
        isError={true}
        title="Unable to Load Brand Comparison"
        message={error || "Could not retrieve brand benchmark data"}
        onRetry={loadData}
      />
    );
  }

  // Prepare price comparison chart data
  const priceChartData = comparison.map(b => ({
    name: b.brand,
    'Average Price': b.average_price,
    'Median Price': b.median_price
  }));

  // Prepare rating chart data (only where ratings exist or clearly annotated)
  const ratingChartData = comparison.map(b => ({
    name: b.brand,
    'Average Rating': b.average_rating || 0,
    hasRating: b.average_rating !== null
  }));

  // Prepare assortment count data
  const assortmentChartData = comparison.map(b => ({
    name: b.brand,
    'Product Count': b.product_count,
    'Share': b.share_of_collected_assortment_pct
  }));

  // Prepare category coverage count data
  const coverageChartData = comparison.map(b => ({
    name: b.brand,
    'Categories Represented': b.category_count
  }));

  return (
    <div className="space-y-6">
      {/* Header and Brand Focus Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Brand Comparison Matrix</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Comparison of collected catalogue pricing, assortment and publicly visible review data.
            <span className="block text-[11px] text-slate-400 mt-1">Full dataset benchmark — 767 validated products.</span>
          </p>
        </div>

        {/* Brand Focus Dropdown */}
        <div className="flex items-center gap-2">
          <label className="text-xs font-semibold text-slate-500">Focus Brand:</label>
          <select
            value={selectedBrand}
            onChange={(e) => setSelectedBrand(e.target.value)}
            className="text-xs font-medium bg-white border border-slate-300 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 shadow-sm"
          >
            <option value="All">All 5 Brands</option>
            {comparison.map(b => (
              <option key={b.brand} value={b.brand}>{b.brand}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Benchmark Matrix Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-900">Observed Catalogue Benchmark Matrix</h3>
          <span className="text-[11px] text-slate-400">Strictly empirical observations</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
              <tr>
                <th className="py-3 px-4">Brand</th>
                <th className="py-3 px-4 text-right">Assortment Count</th>
                <th className="py-3 px-4 text-right">Share of Assortment</th>
                <th className="py-3 px-4 text-right">Average Price (₹)</th>
                <th className="py-3 px-4 text-right">Median Price (₹)</th>
                <th className="py-3 px-4 text-right">Average Rating</th>
                <th className="py-3 px-4 text-right">Observed Reviews</th>
                <th className="py-3 px-4 text-right">Average Discount</th>
                <th className="py-3 px-4 text-center">Categories</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {comparison.map((b) => (
                <tr
                  key={b.brand}
                  className={`hover:bg-slate-50 transition-colors ${selectedBrand === b.brand ? 'bg-blue-50/60 font-semibold' : ''}`}
                >
                  <td className="py-3 px-4 font-semibold text-slate-900">{b.brand}</td>
                  <td className="py-3 px-4 text-right">{b.product_count}</td>
                  <td className="py-3 px-4 text-right text-slate-600">{b.share_of_collected_assortment_pct}%</td>
                  <td className="py-3 px-4 text-right text-emerald-700">{b.average_price != null ? `₹${Number(b.average_price).toFixed(2)}` : '—'}</td>
                  <td className="py-3 px-4 text-right text-emerald-800">{b.median_price != null ? `₹${Number(b.median_price).toFixed(2)}` : '—'}</td>
                  <td className="py-3 px-4 text-right">
                    {b.average_rating !== null && b.average_rating !== undefined ? (
                      <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                        ★ {b.average_rating.toFixed(2)}
                      </span>
                    ) : (
                      <span className="text-slate-400 italic">No ratings</span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-right text-slate-600">
                    {b.total_reviews !== null && b.total_reviews !== undefined ? b.total_reviews.toLocaleString() : 'Not available'}
                  </td>
                  <td className="py-3 px-4 text-right text-indigo-700">
                    {b.average_discount !== null && b.average_discount !== undefined ? `${Number(b.average_discount).toFixed(1)}%` : 'Not available'}
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className="inline-block bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[11px]">
                      {b.category_count} categories
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Comparison Visualizations - 4 Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Average vs. Median Price */}
        <ChartCard
          title="Price Positioning: Mean vs. Median by Brand"
          subtitle="Observed list and selling price metrics (INR)"
          note="Air Wick exhibits higher mean prices driven by electrical devices, whereas Odonil and Godrej aer concentrate in accessible price bands."
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priceChartData} margin={{ top: 10, right: 10, left: -10, bottom: 20 }}>
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748B' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} />
                <Tooltip
                  formatter={(val) => [val != null ? `₹${Number(val).toFixed(2)}` : '—', 'Price']}
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', border: 'none', fontSize: '12px' }}
                />
                <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: '10px', fontSize: '12px' }} />
                <Bar dataKey="Average Price" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Median Price" fill="#10B981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Chart 2: Rating Signals */}
        <ChartCard
          title="Average Customer Rating by Brand"
          subtitle="Customer satisfaction score on 5-star scale (when publicly available)"
          note="AromaPure direct catalogue does not carry marketplace star ratings and is accurately kept as NULL."
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={ratingChartData} margin={{ top: 10, right: 10, left: -10, bottom: 20 }}>
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748B' }} />
                <YAxis domain={[0, 5]} tick={{ fontSize: 11, fill: '#64748B' }} />
                <Tooltip
                  formatter={(val, name, item) => [item.payload.hasRating ? `★ ${Number(val).toFixed(2)} / 5` : 'No Public Rating', 'Rating']}
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', border: 'none', fontSize: '12px' }}
                />
                <Bar dataKey="Average Rating" fill="#F59E0B" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Chart 3: Assortment Count by Brand */}
        <ChartCard
          title="Assortment Count by Brand"
          subtitle="Total validated unique product count in collected catalogue"
          note="Reflects the observed catalogue footprint across each brand's public listings."
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={assortmentChartData} margin={{ top: 10, right: 10, left: -10, bottom: 20 }}>
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748B' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} />
                <Tooltip
                  formatter={(val, name, item) => [`${val} products (${item.payload.Share}%)`, 'Assortment']}
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', border: 'none', fontSize: '12px' }}
                />
                <Bar dataKey="Product Count" fill="#6366F1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Chart 4: Category Coverage by Brand */}
        <ChartCard
          title="Category Coverage by Brand"
          subtitle="Number of distinct home fragrance categories represented"
          note="Evaluates observed catalogue breadth across categories in the collected dataset."
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={coverageChartData} margin={{ top: 10, right: 10, left: -10, bottom: 20 }}>
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748B' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} />
                <Tooltip
                  formatter={(val) => [`${val} categories`, 'Coverage']}
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', border: 'none', fontSize: '12px' }}
                />
                <Bar dataKey="Categories Represented" fill="#14B8A6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* Brand Drilldown Details (When specific brand is selected) */}
      {selectedBrand !== 'All' && brandDetail && (
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-4">
          <div className="flex items-center gap-2 text-slate-800 font-bold text-sm">
            <Layers className="w-4 h-4 text-blue-600" />
            <span>Detailed Portfolio Breakdown for {selectedBrand}</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-xs">
              <span className="text-[11px] text-slate-400 uppercase font-semibold">Price Span</span>
              <p className="text-base font-bold text-slate-900 mt-1">
                ₹{brandDetail.price_statistics.min_price} – ₹{brandDetail.price_statistics.max_price}
              </p>
              <span className="text-[11px] text-slate-500">Median: ₹{brandDetail.price_statistics.median_price}</span>
            </div>
            <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-xs">
              <span className="text-[11px] text-slate-400 uppercase font-semibold">Assortment Share</span>
              <p className="text-base font-bold text-slate-900 mt-1">
                {brandDetail.share_of_collected_assortment_pct}%
              </p>
              <span className="text-[11px] text-slate-500">{brandDetail.product_count} total products</span>
            </div>
            <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-xs">
              <span className="text-[11px] text-slate-400 uppercase font-semibold">Customer Reviews</span>
              <p className="text-base font-bold text-slate-900 mt-1">
                {brandDetail.rating_statistics.total_reviews !== null && brandDetail.rating_statistics.total_reviews !== undefined
                  ? brandDetail.rating_statistics.total_reviews.toLocaleString()
                  : 'Not available'}
              </p>
              <span className="text-[11px] text-slate-500">
                Avg Rating: {brandDetail.rating_statistics.avg_rating ? `★ ${brandDetail.rating_statistics.avg_rating.toFixed(2)}` : 'Not available'}
              </span>
            </div>
            <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-xs">
              <span className="text-[11px] text-slate-400 uppercase font-semibold">Promotional Depth</span>
              <p className="text-base font-bold text-slate-900 mt-1">
                {brandDetail.discount_statistics.avg_discount_pct ? `${brandDetail.discount_statistics.avg_discount_pct}%` : '—'}
              </p>
              <span className="text-[11px] text-slate-500">Avg observed discount</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
