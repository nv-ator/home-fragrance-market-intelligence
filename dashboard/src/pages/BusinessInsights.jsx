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
  RefreshCw,
  ChevronDown,
  ChevronUp
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
  const [expandedInsights, setExpandedInsights] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const toggleInsight = (id) => {
    setExpandedInsights(prev => ({
      ...prev,
      [id]: prev[id] === false ? true : false
    }));
  };

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
      metric: '76.0% in Top 2 Categories',
      observation: selectedBrand === 'All'
        ? 'Ambient Fragrance (General) represents 430 out of 767 observed products (56.1%), followed by Scented Candle & Wax with 153 products (19.9%), together comprising 76.0% of the entire collected catalogue.'
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
      metric: '61.1% Under ₹500',
      observation: 'Across all 767 products, 469 items (61.1%) fall below ₹500 (181 under ₹250 and 288 between ₹250–₹499), 199 items (25.9%) fall between ₹500–₹999, and 99 items (12.9%) exceed ₹1,000.',
      interpretation: 'The collected catalogue displays a prominent volume anchor below ₹500 for single units, with price points above ₹1,000 driven primarily by multi-pack refills, electrical devices, and gift diffusers.',
      businessQuestion: 'Are price points above ₹1,000 generating sustainable standalone purchase volumes, or do they serve primarily as price anchors to drive conversion on sub-₹500 packs?',
      validationRequired: 'Cross-reference unit conversion rates, basket addition patterns, and revenue per transaction across retail price brackets.'
    },
    {
      id: 'price_vs_rating',
      title: '3. Price vs. Rating Relationship',
      icon: <Star className="w-4 h-4 text-yellow-600" />,
      metric: 'Weak Empirical Correlation (r = +0.24)',
      observation: 'Among the 364 products with public ratings, selling prices range from ₹50.00 to ₹6,345.00 while ratings cluster tightly between 1.0 and 5.0 stars (mean 4.15 ★), showing a weak positive correlation (r = +0.24).',
      interpretation: 'Visual inspection and empirical correlation indicate that higher retail price does not guarantee a noticeably higher customer rating in the observed catalogue.',
      businessQuestion: 'If customer ratings remain comparable across lower and higher price points, what specific product attributes justify price premiums to prospective buyers?',
      validationRequired: 'Review fragrance longevity benchmarks, customer sentiment on refill durability, and return rates across price bands.'
    },
    {
      id: 'discount_dynamics',
      title: '4. Promotional Discount Depth',
      icon: <Percent className="w-4 h-4 text-amber-600" />,
      metric: '39.5% Average Observed Discount',
      observation: 'Among the 545 products where valid MRP and discount data were observed, the average catalogue discount is 39.5%, ranging from 25.0% for Air Wick (n=44) to 43.8% for AromaPure (n=348).',
      interpretation: 'The observed dataset indicates widespread promotional discounting off listed MRP across online retail channels, with notable differences in promotional depth across brands.',
      businessQuestion: 'Does continuous double-digit discounting improve net margin through volume acceleration, or does it condition shoppers to avoid full-price purchases?',
      validationRequired: 'Evaluate promotional price elasticity curves, baseline sales lift, and trade allowance deductions from channel partners.'
    },
    {
      id: 'category_coverage',
      title: '5. Catalogue Whitespace & Coverage Voids',
      icon: <Eye className="w-4 h-4 text-indigo-600" />,
      metric: '2 to 7 Categories per Brand',
      observation: 'Observed brand footprints span from 2 categories (Air Wick) to 7 categories (AromaPure). Specific category intersections (e.g. Air Wick in Bathroom Fresheners, or Godrej aer in Scented Candles) show 0 observed products in the collected dataset.',
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
      metric: '₹1,575.96 / 100ml vs. ₹411.30 / 100g',
      observation: 'Normalized liquid formats (271 products) average ₹1,575.96 per 100ml (ranging ₹34.04 to ₹8,090.00), while normalized solid formats (30 products) average ₹411.30 per 100g (ranging ₹78.67 to ₹1,133.33).',
      interpretation: 'Liquid formulations (sprays, oils, automated refills) command higher unit realization per standard volume than solid evaporative blocks and gels on standard mass metrics.',
      businessQuestion: 'Are higher unit realizations on liquid refills offset by packaging and dispensing hardware costs relative to solid formats?',
      validationRequired: 'Review gross margin contribution by physical format, cost of goods sold (COGS) breakdowns, and device-to-refill attachment ratios.'
    },
    {
      id: 'engagement_presence',
      title: '7. Customer Feedback & Review Transparency',
      icon: <HelpCircle className="w-4 h-4 text-purple-600" />,
      metric: '1,387 Total Marketplace Reviews',
      observation: 'A total of 1,387 public reviews were collected across marketplace listings (Odonil: 473, Godrej aer: 453, Air Wick: 336, Ambi Pur: 125), whereas direct brand catalogue listings do not expose public review counts.',
      interpretation: 'Public review visibility is channel-dependent, reflecting marketplace social proof mechanisms rather than commercial market share or aggregate sales volume.',
      businessQuestion: 'How can brands without marketplace review signals establish trust and social proof comparable to high-review competitor listings?',
      validationRequired: 'Audit on-site conversion funnel data, customer satisfaction (CSAT) scores, and direct post-purchase feedback surveys.'
    },
    {
      id: 'pack_size_patterns',
      title: '8. Pack-Size Patterns & Multipack Dynamics',
      icon: <Package className="w-4 h-4 text-cyan-600" />,
      metric: '88.3% Single Units (1-Pack)',
      observation: 'Across all 767 products, 677 items (88.3%) are listed as single units (1-pack), while multipacks comprise 90 items (11.7%, primarily 2-packs at n=40, 20-packs at n=19, and 3-packs at n=12). Standardized volume is explicitly documented on 325 products (271 liquids median 60ml, 30 solids median 75g, 24 unit counts).',
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
            <p className="text-xs text-slate-500 mt-0.5">Empirical overview of collected catalogue pricing, assortment, and public marketplace reviews.</p>
          </div>
          <span className="text-[11px] font-medium text-slate-400 bg-slate-100 px-2 py-0.5 rounded">Observed Data</span>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {[
            { label: 'Products', value: `${overviewData.total_products?.toLocaleString() || 767} Products` },
            { label: 'Brands Tracked', value: `${overviewData.total_brands || 5} Brands` },
            { label: 'Median Price', value: overviewData.median_price != null ? `₹${Number(overviewData.median_price).toFixed(0)} Median Price` : '₹448 Median Price' },
            { label: 'Retail Distribution', value: '61.1% Under ₹500' },
            { label: 'Marketplace Reviews', value: `${observedReviews.toLocaleString()} Observed Marketplace Reviews` },
          ].map((item) => (
            <div key={item.label} className="border-l-2 border-blue-500 pl-3 py-1 bg-slate-50/50 rounded-r">
              <p className="text-sm sm:text-base font-bold text-slate-900">{item.value}</p>
              <p className="text-[11px] text-slate-500 font-medium">{item.label}</p>
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

      {/* 8 Structured Diagnostic Cards */}
      <div className="space-y-4">
        {structuredInsights.map((insight) => (
          <div key={insight.id} className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
            {/* Card Title Bar */}
            <div 
              onClick={() => toggleInsight(insight.id)}
              className="px-5 py-3.5 bg-slate-50 hover:bg-slate-100/70 cursor-pointer transition-colors border-b border-slate-200 flex items-center justify-between"
            >
              <div className="flex items-center space-x-2.5">
                <div className="p-1.5 bg-white rounded border border-slate-200">
                  {insight.icon}
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">{insight.title}</h3>
                  <p className="text-[11px] text-slate-500 line-clamp-1 mt-0.5 sm:hidden">{insight.observation}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className="px-2.5 py-0.5 rounded text-[11px] font-semibold bg-white text-slate-700 border border-slate-200 shadow-2xs">
                  {insight.metric}
                </span>
                <button
                  type="button"
                  aria-label="Toggle section"
                  className="p-1 text-slate-400 hover:text-slate-600 rounded"
                >
                  {expandedInsights[insight.id] !== false ? (
                    <ChevronUp className="w-4 h-4" />
                  ) : (
                    <ChevronDown className="w-4 h-4" />
                  )}
                </button>
              </div>
            </div>

            {/* 4-Part Structure (Collapsible) */}
            {expandedInsights[insight.id] !== false && (
              <div className="p-4 sm:p-5 grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4 text-xs">
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
            )}
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
