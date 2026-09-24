import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
  PieChart, Pie, Legend
} from 'recharts';
import { Package, Building2, IndianRupee, Star, Percent, Scale, MessageSquare, RefreshCw } from 'lucide-react';
import KpiCard from '../components/KpiCard';
import ChartCard from '../components/ChartCard';
import EmptyState from '../components/EmptyState';
import { getDashboardSample, summarizeDashboardSample } from '../utils/dashboardSample';

const BRAND_COLORS = {
  'AromaPure': '#2563EB',   // Royal Blue
  'Odonil': '#10B981',      // Emerald Green
  'Godrej aer': '#F59E0B',   // Warm Amber
  'Air Wick': '#8B5CF6',    // Violet
  'Ambi Pur': '#EC4899',    // Rose Pink
};

const PLATFORM_COLORS = ['#3B82F6', '#06B6D4'];

export default function Overview() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadOverview = async () => {
    setLoading(true);
    setError(null);
    try {
      const sample = await getDashboardSample();
      setData(summarizeDashboardSample(sample));
    } catch (err) {
      setError(err.message || 'Failed to load market overview from API');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOverview();
  }, []);

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center">
        <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mb-3" />
        <p className="text-sm font-medium text-slate-600">Loading market intelligence dataset...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <EmptyState
        isError={true}
        title="Unable to Load Market Overview"
        message={error || "FastAPI analytical server is unreachable at http://localhost:8000"}
        onRetry={loadOverview}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Title & Scope Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Market Overview</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Aggregated observed catalogue metrics across 5 major home fragrance competitor brands.
          </p>
        </div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-medium border border-blue-200">
          <span>Public Catalogue Analysis</span>
        </div>
      </div>

      {/* Top KPI Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-7 gap-4">
        <KpiCard
          title="Observed Products"
          value={data.total_products}
          subtitle="Observed SKUs"
          note="Dashboard sample — 120 products"
          icon={Package}
          color="blue"
        />
        <KpiCard
          title="Tracked Brands"
          value={data.total_brands}
          subtitle="Brands"
          note="All monitored brands"
          icon={Building2}
          color="indigo"
        />
        <KpiCard
          title="Average Price"
          value={data.average_price != null ? `₹${Number(data.average_price).toFixed(2)}` : "N/A"}
          subtitle="INR"
          note="Observed selling price"
          icon={IndianRupee}
          color="emerald"
        />
        <KpiCard
          title="Median Price"
          value={data.median_price != null ? `₹${Number(data.median_price).toFixed(2)}` : "N/A"}
          subtitle="INR"
          note="Dashboard sample central tendency"
          icon={Scale}
          color="emerald"
        />
        <KpiCard
          title="Average Rating"
          value={data.average_rating != null ? `${Number(data.average_rating).toFixed(2)} / 5` : "N/A"}
          subtitle="Stars"
          note="Rated products only"
          icon={Star}
          color="amber"
        />
        <KpiCard
          title="Average Discount"
          value={data.average_discount != null ? `${Number(data.average_discount).toFixed(1)}%` : "N/A"}
          subtitle="Off List Price"
          note="Valid MRP observations"
          icon={Percent}
          color="slate"
        />
        <KpiCard
          title="Observed Marketplace Reviews"
          value={data.observed_reviews != null ? Number(data.observed_reviews).toLocaleString() : "N/A"}
          subtitle="Public reviews"
          note="Public marketplace reviews in sample"
          icon={MessageSquare}
          color="blue"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Products by Brand */}
        <ChartCard
          title="Assortment by Brand"
          subtitle="Share of the balanced dashboard sample"
          note="Each monitored brand contributes 24 products."
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.products_by_brand || []} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748B' }} interval={0} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} />
                <Tooltip
                  formatter={(val, name, item) => [`${val} products (${item.payload.pct_share}%)`, 'Assortment']}
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', border: 'none', fontSize: '12px' }}
                />
                <Bar dataKey="product_count" radius={[4, 4, 0, 0]}>
                  {(data.products_by_brand || []).map((entry) => (
                    <Cell key={entry.name} fill={BRAND_COLORS[entry.name] || '#3B82F6'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Chart 2: Products by Platform */}
        <ChartCard
          title="Public Catalogue Sources"
          subtitle="Distribution of collected items between marketplace and official catalogue"
          note="Sample records include Amazon India and AromaPure Official sources."
        >
          <div className="h-72 w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.products_by_platform || []}
                  dataKey="product_count"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={85}
                  innerRadius={50}
                  paddingAngle={3}
                  label={({ name, pct_share }) => `${name}: ${pct_share}%`}
                >
                  {(data.products_by_platform || []).map((entry, idx) => (
                    <Cell key={entry.name} fill={PLATFORM_COLORS[idx % PLATFORM_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(val, name, item) => [`${val} products (${item.payload.pct_share}%)`, name]}
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', border: 'none', fontSize: '12px' }}
                />
                <Legend verticalAlign="bottom" height={36} wrapperStyle={{ fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Chart 3: Products by Category */}
        <ChartCard
          title="Products by Fragrance Category"
          subtitle="Distribution of observed products across standardized fragrance types"
          note="Counts reflect the balanced dashboard sample, not commercial market share."
        >
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                layout="vertical"
                data={data.products_by_category || []}
                margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
              >
                <XAxis type="number" tick={{ fontSize: 11, fill: '#64748B' }} />
                <YAxis dataKey="name" type="category" tick={{ fontSize: 11, fill: '#475569' }} width={140} />
                <Tooltip
                  formatter={(val, name, item) => [`${val} items (${item.payload.pct_share}%)`, 'Products']}
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', border: 'none', fontSize: '12px' }}
                />
                <Bar dataKey="product_count" fill="#3B82F6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Chart 4: Price Distribution */}
        <ChartCard
          title="Observed Price Distribution"
          subtitle="Count of products across defined retail price brackets"
          note="Catalogue pricing distribution within the dashboard sample."
        >
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={data.price_distribution || []}
                margin={{ top: 10, right: 20, left: -10, bottom: 20 }}
              >
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748B' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} />
                <Tooltip
                  formatter={(val, name, item) => [`${val} products (${item.payload.pct_share}%)`, 'Assortment']}
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', border: 'none', fontSize: '12px' }}
                />
                <Bar dataKey="product_count" fill="#10B981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* Methodology & Data Hygiene Notice */}
      <div className="bg-slate-900 text-slate-100 rounded-xl p-6 shadow-sm">
        <div>
          <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-400 mb-2">
            <Scale className="w-4 h-4" />
            <span>Methodological Discipline</span>
          </div>
          <h3 className="text-base font-bold text-white mb-2">
            Observed Catalogue vs. Commercial Sales
          </h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            Analysis is based on publicly accessible product listings collected from the selected sources. This Market Overview uses the deterministic dashboard sample of 120 products, while the full validated dataset contains 684 products.
          </p>
          <ul className="mt-3 space-y-2 text-xs text-slate-400 list-disc list-inside">
            <li>Percentages indicate <strong className="text-slate-200">Share of Collected Assortment</strong>, NOT commercial market share.</li>
            <li>AromaPure D2C products have no marketplace star ratings and remain strictly <code className="text-blue-300">NULL</code> (never defaulted to 0.0).</li>
            <li>Mass ($g$) and Volume ($ml$) are strictly separated without artificial density assumptions.</li>
          </ul>
        </div>
        <div className="mt-6 pt-4 border-t border-slate-800 text-[11px] text-slate-400">
          Source Provenance: Ingested via Python <code>requests</code> + <code>BeautifulSoup4</code>; verified with 100% test coverage.
        </div>
      </div>
    </div>
  );
}

