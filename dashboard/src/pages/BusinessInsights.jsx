import React, { useState, useEffect } from 'react';
import {
  Lightbulb,
  HelpCircle,
  CheckCircle2,
  Eye,
  FileText,
  AlertCircle,
  TrendingUp,
  Layers,
  Percent,
  Star,
  Scale,
  Tag,
  Compass,
  Package,
  RefreshCw
} from 'lucide-react';
import ChartCard from '../components/ChartCard';
import EmptyState from '../components/EmptyState';
import { api } from '../api/client';
import { getDashboardSample, summarizeDashboardSample } from '../utils/dashboardSample';

export default function BusinessInsights() {
  const [brandsData, setBrandsData] = useState([]);
  const [coverageData, setCoverageData] = useState(null);
  const [overviewData, setOverviewData] = useState(null);
  const [sampleSummary, setSampleSummary] = useState(null);
  const [selectedBrand, setSelectedBrand] = useState('All');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [brandsRes, coverageRes, overviewRes, sample] = await Promise.all([
        api.getBrandComparison(),
        api.getCategoryCoverage(),
        api.getOverview(),
        getDashboardSample()
      ]);
      setBrandsData(brandsRes);
      setCoverageData(coverageRes);
      setOverviewData(overviewRes);
      setSampleSummary(summarizeDashboardSample(sample));
    } catch (err) {
      setError(err.message || 'Failed to load business intelligence insights.');
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
        <p className="text-sm font-medium text-slate-600">Synthesizing market intelligence diagnostic data...</p>
      </div>
    );
  }

  if (error || !coverageData || !overviewData || !sampleSummary) {
    return (
      <EmptyState
        isError={true}
        title="Failed to Load Business Insights"
        message={error || 'Unable to retrieve insights data from the FastAPI analytical backend.'}
        onRetry={loadData}
      />
    );
  }

  const brandsList = ['AromaPure', 'Odonil', 'Godrej aer', 'Air Wick', 'Ambi Pur'];

  // Helper to retrieve brand-specific stats
  const getBrandStats = (bname) => {
    return brandsData.find(b => b.brand === bname) || null;
  };

  const focusBrandStats = selectedBrand !== 'All' ? getBrandStats(selectedBrand) : null;
  const observedReviews = brandsData.reduce((total, brand) => total + (brand.total_reviews ?? 0), 0);

  // 7 Structured Factual Insights following the 4-part framework
  const structuredInsights = [
    {
      id: 'assortment_concentration',
      title: '1. Assortment Concentration & Catalogue Depth',
      icon: <Layers className="w-4 h-4 text-blue-600" />,
      metric: '78.4% in Top 2 Categories',
      observation: selectedBrand === 'All'
        ? 'Ambient Fragrance (General) represents 383 out of 684 observed products (56.0%), followed by Scented Candle & Wax with 153 products (22.4%), together comprising 78.4% of the entire collected catalogue.'
        : `For ${selectedBrand}, observed catalogue footprint comprises ${focusBrandStats?.product_count || 0} products (${focusBrandStats?.share_of_collected_assortment_pct || 0}% of the collected dataset) across ${focusBrandStats?.category_count || 0} categories.`,
      interpretation: 'The collected dataset exhibits substantial operational concentration in room ambience and candle formats, while specialized formats (Automatic Sprays, Bathroom Blocks, Freshener Gels) show narrower SKU listings.',
      businessQuestion: selectedBrand === 'All'
        ? 'Does high catalogue concentration in Ambient Fragrance reflect genuine consumer off-take volume, or does it leave niche specialized formats commercially underserved?'
        : `Does ${selectedBrand}'s current assortment concentration reflect its strongest revenue drivers, or does it risk leaving complementary air care occasions open to competitors?`,
      validationRequired: 'Audit internal sales velocity, category margin contribution, and channel inventory off-take before reallocating catalogue assortment.'
    },
    {
      id: 'price_distribution',
      title: '2. Retail Price Brackets & Dispersion',
      icon: <TrendingUp className="w-4 h-4 text-emerald-600" />,
      metric: '62.0% Under ₹500',
      observation: 'Across all 684 products, 424 items (62.0%) fall below ₹500 (160 under ₹250 and 264 between ₹250–₹499), 170 items (24.9%) fall between ₹500–₹999, and 90 items (13.2%) reach or exceed ₹1,000.',
      interpretation: 'The collected catalogue displays a prominent volume anchor below ₹500 for single units, with price points above ₹1,000 driven primarily by multi-pack refills, electrical devices, and gift diffusers.',
      businessQuestion: 'Are price points above ₹1,000 generating sustainable standalone purchase volumes, or do they serve primarily as price anchors to drive conversion on sub-₹500 packs?',
      validationRequired: 'Cross-reference unit conversion rates, basket addition patterns, and revenue per transaction across retail price brackets.'
    },
    {
      id: 'price_vs_rating',
      title: '3. Price vs. Rating Relationship',
      icon: <Star className="w-4 h-4 text-yellow-600" />,
      metric: 'Weak Empirical Correlation (r = +0.24)',
      observation: 'Among the 340 products with public ratings, selling prices range from ₹51.00 to ₹6,345.00 while ratings cluster tightly between 1.0 and 5.0 stars (mean 4.16 ★), showing a weak positive correlation (r = +0.24).',
      interpretation: 'Visual inspection and empirical correlation indicate that higher retail price does not guarantee a noticeably higher customer rating in the observed catalogue.',
      businessQuestion: 'If customer ratings remain comparable across lower and higher price points, what specific product attributes justify price premiums to prospective buyers?',
      validationRequired: 'Review fragrance longevity benchmarks, customer sentiment on refill durability, and return rates across price bands.'
    },
    {
      id: 'discount_dynamics',
      title: '4. Promotional Discount Depth',
      icon: <Percent className="w-4 h-4 text-amber-600" />,
      metric: '39.3% Average Observed Discount',
      observation: 'Among the 479 products where valid MRP and discount data were observed, the average catalogue discount is 39.3%, ranging from 12.6% for Ambi Pur (n=9) and 23.6% for Air Wick (n=44) to 45.2% for AromaPure (n=289).',
      interpretation: 'The observed dataset indicates widespread promotional discounting off listed MRP across online retail channels, with notable differences in promotional depth across brands.',
      businessQuestion: 'Does continuous double-digit discounting improve net margin through volume acceleration, or does it condition shoppers to avoid full-price purchases?',
      validationRequired: 'Evaluate promotional price elasticity curves, baseline sales lift, and trade allowance deductions from channel partners.'
    },
    {
      id: 'category_coverage',
      title: '5. Catalogue Whitespace & Coverage Voids',
      icon: <Eye className="w-4 h-4 text-indigo-600" />,
      metric: '3 to 6 Categories per Brand',
      observation: 'Observed brand footprints span from 3 categories (Air Wick, Godrej aer, Odonil) to 6 categories (AromaPure). Specific category intersections (e.g. Air Wick in Bathroom Fresheners, or Godrej aer in Scented Candles) show 0 observed products in the collected dataset.',
      interpretation: 'Different competitor brands appear to pursue contrasting catalogue strategies, with some concentrating in specialized automated devices while others span multi-space ambient care.',
      businessQuestion: selectedBrand === 'All'
        ? 'Do observed category voids represent addressable market whitespace or deliberate strategic non-participation due to unfavorable unit economics?'
        : `Does the absence of observed products in unrepresented categories present a viable expansion opportunity for ${selectedBrand}, or would it cause brand-stretch friction?`,
      validationRequired: 'Validate consumer willingness-to-pay, brand perception surveys, packaging feasibility, and competitive barriers to entry in absent categories.'
    },
    {
      id: 'unit_economics',
      title: '6. Unit Economics & Packaging Metrics',
      icon: <Tag className="w-4 h-4 text-teal-600" />,
      metric: '₹1,203.48 / 100ml vs. ₹369.28 / 100g',
      observation: 'Normalized liquid formats (231 products) average ₹1,203.48 per 100ml (ranging ₹34.04 to ₹3,993.33), while normalized solid formats (23 products) average ₹369.28 per 100g (ranging ₹78.67 to ₹1,133.33).',
      interpretation: 'Liquid formulations (sprays, oils, automated refills) command higher unit realization per standard volume than solid evaporative blocks and gels on standard mass metrics.',
      businessQuestion: 'Are higher unit realizations on liquid refills offset by packaging and dispensing hardware costs relative to solid formats?',
      validationRequired: 'Review gross margin contribution by physical format, cost of goods sold (COGS) breakdowns, and device-to-refill attachment ratios.'
    },
    {
      id: 'engagement_presence',
      title: '7. Customer Feedback & Review Transparency',
      icon: <HelpCircle className="w-4 h-4 text-purple-600" />,
      metric: '9,261 Total Observed Reviews',
      observation: 'A total of 9,261 public reviews were observed across 491 listings (AromaPure: 7,958 across 151 items, Godrej aer: 449 across 117 items, Odonil: 427 across 112 items, Air Wick: 332 across 86 items, Ambi Pur: 95 across 25 items).',
      interpretation: 'Public review visibility is channel-dependent, reflecting marketplace and storefront social proof mechanisms rather than commercial market share or aggregate sales volume.',
      businessQuestion: 'How can brands without marketplace review signals establish trust and social proof comparable to high-review competitor listings?',
      validationRequired: 'Audit on-site conversion funnel data, customer satisfaction (CSAT) scores, and direct post-purchase feedback surveys.'
    },
    {
      id: 'pack_size_patterns',
      title: '8. Pack-Size Patterns & Multipack Dynamics',
      icon: <Package className="w-4 h-4 text-cyan-600" />,
      metric: '87.6% Single Units (1-Pack)',
      observation: 'Across all 684 products, 599 items (87.6%) are listed as single units (1-pack), while multipacks comprise 85 items (12.4%, primarily 2-packs at n=38, 20-packs at n=19, and 3-packs at n=10). Explicit volume/mass is documented on 274 products (231 liquids median 100ml, 23 solids median 150g).',
      interpretation: 'The collected catalogue is predominantly represented by single-unit listings, while multipacks form a smaller portion of the observed assortment.',
      businessQuestion: 'Does the observed pack structure align with customer demand, replenishment behaviour and bundle economics?',
      validationRequired: 'Examine repeat purchase cadence, shipping-to-price ratio per single pack, and bundle margin contribution before modifying packaging assortment.'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header Banner & Brand Focus Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Diagnostic Business Insights</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Empirical evidence structured through the objective 4-part diagnostic framework.
          </p>
        </div>

        {/* Brand Focus Selector */}
        <div className="flex items-center gap-2">
          <label className="text-xs font-semibold text-slate-500">Focus Lens:</label>
          <select
            value={selectedBrand}
            onChange={(e) => setSelectedBrand(e.target.value)}
            className="text-xs font-medium bg-white border border-slate-300 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 shadow-sm"
          >
            <option value="All">All 5 Brands (Overview)</option>
            {brandsList.map(b => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Methodology Guardrail Card */}
      <div className="bg-blue-50/70 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-blue-700 flex-shrink-0 mt-0.5" />
          <div className="text-xs text-blue-900 leading-relaxed">
            <span className="font-semibold block mb-0.5">Analytical Guardrails & Diagnostic Principles:</span>
            Insights are derived strictly from observed public catalogue/listing data collected for this project. They describe the collected dataset and should not be interpreted as total market share, sales performance, profitability, or customer preference.
            Portfolio gaps represent categories not observed in the collected dataset; they do not prove that a brand has no such products in uncollected offline channels.
          </div>
        </div>
      </div>

      <section className="bg-white rounded-lg border border-slate-200 p-4 shadow-sm">
        <div className="flex items-center justify-between gap-3 mb-3">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Executive Snapshot</h3>
            <p className="text-xs text-slate-500 mt-0.5">Current metrics from the collected catalogue and public marketplace listings.</p>
          </div>
          <span className="text-[11px] text-slate-400">Observed data</span>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
          {[
            ['Full dataset', `${overviewData.total_products} products`],
            ['Dashboard sample', `${sampleSummary.total_products} products`],
            ['Brands', overviewData.total_brands],
            ['Full dataset median', overviewData.median_price != null ? `₹${Number(overviewData.median_price).toFixed(2)}` : 'Not available'],
            ['Full dataset reviews', observedReviews.toLocaleString()]
          ].map(([label, value]) => (
            <div key={label} className="border-l-2 border-blue-500 pl-3">
              <p className="text-lg font-bold text-slate-900">{value}</p>
              <p className="text-[11px] text-slate-500">{label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Category Presence Matrix */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 mb-4 border-b border-slate-100 gap-2">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Observed Category Presence Matrix</h3>
            <p className="text-xs text-slate-500">Cross-tabulation of catalog presence across all 5 brands and observed categories</p>
          </div>
          <div className="text-xs text-slate-500 italic bg-slate-50 px-2.5 py-1 rounded border border-slate-200">
            * "0" indicates: <strong>No observed product in the collected dataset.</strong> (Does NOT imply brand does not sell this category).
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-700 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-200">
              <tr>
                <th className="px-4 py-3">Category</th>
                {brandsList.map((b) => (
                  <th
                    key={b}
                    className={`px-3 py-3 text-center ${selectedBrand === b ? 'bg-blue-100 text-blue-900 font-bold' : ''}`}
                  >
                    {b}
                  </th>
                ))}
                <th className="px-3 py-3 text-center">Total Observed</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-600">
              {(coverageData?.matrix || coverageData?.coverage_matrix || []).map((row) => (
                <tr key={row.category} className="hover:bg-slate-50 transition-colors">
                  <td className="px-4 py-2.5 font-medium text-slate-900">{row.category}</td>
                  {brandsList.map((brand) => {
                    const count = row[brand] || 0;
                    const isFocus = selectedBrand === brand;
                    return (
                      <td key={brand} className={`px-3 py-2.5 text-center ${isFocus ? 'bg-blue-50/50' : ''}`}>
                        {count > 0 ? (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-50 text-emerald-800">
                            {count} SKUs
                          </span>
                        ) : (
                          <span className="text-slate-400 italic text-[11px]" title="No observed product in the collected dataset">
                            0
                          </span>
                        )}
                      </td>
                    );
                  })}
                  <td className="px-3 py-2.5 text-center font-bold text-slate-800">
                    {row.total || 0}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 7 Structured Diagnostic Cards */}
      <div className="space-y-4">
        {structuredInsights.map((insight) => (
          <div key={insight.id} className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
            {/* Card Title Bar */}
            <div className="px-5 py-3 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
              <div className="flex items-center space-x-2.5">
                <div className="p-1.5 bg-white rounded border border-slate-200">
                  {insight.icon}
                </div>
                <h3 className="text-sm font-bold text-slate-900">{insight.title}</h3>
              </div>
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-slate-100 text-slate-700 border border-slate-200">
                {insight.metric}
              </span>
            </div>

            {/* 4-Part Structure */}
            <div className="p-5 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              {/* Part 1: Observation */}
              <div className="bg-slate-50/80 p-3.5 rounded-lg border border-slate-200 flex flex-col">
                <div className="flex items-center space-x-1.5 text-blue-900 font-bold uppercase tracking-wider text-[11px] mb-2">
                  <Eye className="w-3.5 h-3.5 text-blue-600" />
                  <span>1. What the Data Shows (Factual Observation)</span>
                </div>
                <p className="text-slate-700 leading-relaxed flex-1">
                  {insight.observation}
                </p>
              </div>

              {/* Part 2: Interpretation */}
              <div className="bg-slate-50/80 p-3.5 rounded-lg border border-slate-200 flex flex-col">
                <div className="flex items-center space-x-1.5 text-indigo-900 font-bold uppercase tracking-wider text-[11px] mb-2">
                  <Lightbulb className="w-3.5 h-3.5 text-indigo-600" />
                  <span>2. What This May Mean (Analytical Interpretation)</span>
                </div>
                <p className="text-slate-700 leading-relaxed flex-1">
                  {insight.interpretation}
                </p>
              </div>

              {/* Part 3: Business Question */}
              <div className="bg-amber-50/50 p-3.5 rounded-lg border border-amber-200/70 flex flex-col">
                <div className="flex items-center space-x-1.5 text-amber-900 font-bold uppercase tracking-wider text-[11px] mb-2">
                  <HelpCircle className="w-3.5 h-3.5 text-amber-600" />
                  <span>3. Commercial Business Question</span>
                </div>
                <p className="text-slate-800 leading-relaxed flex-1">
                  {insight.businessQuestion}
                </p>
              </div>

              {/* Part 4: Validation Required */}
              <div className="bg-emerald-50/50 p-3.5 rounded-lg border border-emerald-200/70 flex flex-col">
                <div className="flex items-center space-x-1.5 text-emerald-900 font-bold uppercase tracking-wider text-[11px] mb-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                  <span>4. Internal Validation Required</span>
                </div>
                <p className="text-slate-800 leading-relaxed flex-1">
                  {insight.validationRequired}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Symmetrical Brand Treatment & Portfolio Language Note */}
      <div className="bg-slate-50 border border-slate-200 rounded-lg p-3.5 text-xs text-slate-500 leading-relaxed flex items-center justify-between">
        <div>
          <span className="font-semibold text-slate-700">Analytical Symmetry & Portfolio Framing: </span>
          All 5 brands (AromaPure, Odonil, Godrej aer, Air Wick, Ambi Pur) are treated with identical methodology without biased positioning tiers.
          Limited observed coverage creates a commercial question rather than an unverified launch directive.
        </div>
      </div>
    </div>
  );
}
