import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, X, ExternalLink, Activity } from 'lucide-react';

export default function DataTable({
  products,
  total,
  page,
  pageSize,
  onPageChange,
  onPageSizeChange,
  isLoading,
  diagnosticProducts = []
}) {
  const [selectedProduct, setSelectedProduct] = useState(null);

  const totalPages = Math.ceil(total / pageSize) || 1;

  const formatPrice = (val) => (val !== null && val !== undefined ? `₹${Number(val).toFixed(2)}` : 'Not available');
  const formatDiscount = (val) => (val !== null && val !== undefined ? `${Number(val).toFixed(1)}%` : 'Not available');
  const formatRating = (val) => (val !== null && val !== undefined ? `${Number(val).toFixed(2)} ★` : 'Not available');
  const formatReviews = (val) => (val !== null && val !== undefined ? Number(val).toLocaleString() : 'Not available');
  const formatValue = (val) => (val !== null && val !== undefined && val !== '' ? val : 'Not available');
  const median = (values) => {
    const sorted = values.filter((value) => value !== null && value !== undefined).sort((a, b) => a - b);
    if (!sorted.length) return null;
    const middle = Math.floor(sorted.length / 2);
    return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
  };
  const average = (values) => {
    const valid = values.filter((value) => value !== null && value !== undefined);
    return valid.length ? valid.reduce((sum, value) => sum + value, 0) / valid.length : null;
  };
  const getDiagnostic = (product) => {
    const sameBrandCategory = diagnosticProducts.filter((peer) => (
      peer.product_id !== product.product_id && peer.brand === product.brand && peer.category === product.category
    ));
    const categoryPeers = diagnosticProducts.filter((peer) => (
      peer.product_id !== product.product_id && peer.category === product.category
    ));
    const peers = sameBrandCategory.length >= 2 ? sameBrandCategory : categoryPeers.length >= 2 ? categoryPeers : [];
    const peerLabel = sameBrandCategory.length >= 2 ? 'same brand + category' : 'same category across brands';
    const metric = (field, statistic = 'median') => {
      const values = peers.map((peer) => peer[field]);
      return statistic === 'average' ? average(values) : median(values);
    };
    const comparison = [
      { label: 'PRICE', value: formatPrice(product.selling_price), peer: metric('selling_price'), format: formatPrice, direction: 'above' },
      { label: 'RATING', value: formatRating(product.rating), peer: product.rating == null ? null : metric('rating', 'average'), format: (value) => value == null ? 'Not available' : `${Number(value).toFixed(2)} / 5`, direction: 'below', average: true },
      { label: 'DISCOUNT', value: formatDiscount(product.discount_pct), peer: product.discount_pct == null ? null : metric('discount_pct', 'average'), format: (value) => value == null ? 'Not available' : `${Number(value).toFixed(1)}%`, direction: 'below', percentage: true, average: true },
      { label: 'REVIEW COUNT', value: formatReviews(product.review_count), peer: product.review_count == null ? null : metric('review_count'), format: (value) => value == null ? 'Not available' : Number(value).toLocaleString(), direction: 'below' }
    ];
    const areas = comparison.filter((item) => item.peer != null && product[item.label === 'PRICE' ? 'selling_price' : item.label === 'RATING' ? 'rating' : item.label === 'DISCOUNT' ? 'discount_pct' : 'review_count'] != null)
      .filter((item) => item.direction === 'above'
        ? product.selling_price > item.peer
        : product[item.label === 'RATING' ? 'rating' : item.label === 'DISCOUNT' ? 'discount_pct' : 'review_count'] < item.peer)
      .map((item) => item.label === 'DISCOUNT' ? 'Discount depth is below the observed peer average.' : item.label === 'RATING' ? 'Observed rating is below the comparable peer average.' : item.label === 'REVIEW COUNT' ? 'Observed review count is below the comparable peer median.' : 'Price is above the comparable peer median.');
    return { peers, peerLabel, comparison, areas };
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      {/* Table Header controls */}
      <div className="p-4 border-b border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3 bg-slate-50">
        <div className="text-xs text-slate-600 font-medium">
          Showing <span className="font-semibold text-slate-900">{total === 0 ? 0 : (page - 1) * pageSize + 1}</span> to{' '}
          <span className="font-semibold text-slate-900">{Math.min(page * pageSize, total)}</span> of{' '}
          <span className="font-semibold text-slate-900">{total}</span> observed products
        </div>

        <div className="flex items-center space-x-2">
          <label className="text-xs text-slate-500">Rows per page:</label>
          <select
            value={pageSize}
            onChange={(e) => onPageSizeChange(Number(e.target.value))}
            className="text-xs bg-white border border-slate-200 rounded px-2 py-1 text-slate-700 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value={20}>20</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>
        </div>
      </div>

      {/* Table area */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-600">
          <thead className="bg-slate-100 text-slate-700 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-200">
            <tr>
              <th className="px-3 py-3">Brand</th>
              <th className="px-4 py-3 min-w-[220px]">Product Name</th>
              <th className="px-3 py-3">Category</th>
              <th className="px-3 py-3">Format</th>
              <th className="px-3 py-3">Platform</th>
              <th className="px-3 py-3 text-right">Selling Price</th>
              <th className="px-3 py-3 text-right">MRP</th>
              <th className="px-3 py-3 text-right">Discount</th>
              <th className="px-3 py-3 text-right">Pack / Size</th>
              <th className="px-3 py-3 text-right">Rating</th>
              <th className="px-3 py-3 text-right">Reviews</th>
              <th className="px-3 py-3 text-center">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {isLoading ? (
              <tr>
                <td colSpan={12} className="text-center py-12 text-slate-400">
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                    <span>Loading catalogue records...</span>
                  </div>
                </td>
              </tr>
            ) : products.length === 0 ? (
              <tr>
                <td colSpan={12} className="text-center py-10 text-slate-500">
                  No observed products match the selected filter criteria.
                </td>
              </tr>
            ) : (
              products.map((p) => (
                <tr
                  key={p.product_id}
                  onClick={() => setSelectedProduct(p)}
                  className="hover:bg-blue-50/50 cursor-pointer transition-colors"
                >
                  <td className="px-3 py-2.5 font-medium text-slate-900 whitespace-nowrap">
                    <span className="px-2 py-0.5 rounded text-[11px] bg-slate-100 text-slate-700 font-medium">
                      {p.brand}
                    </span>
                  </td>
                  <td className="px-4 py-2.5 text-slate-900 font-medium align-top" title={p.title_clean || p.title}>
                    <div className="max-w-[280px] line-clamp-3 whitespace-normal break-words leading-5">
                    {p.title_clean || p.title}
                    </div>
                  </td>
                  <td className="px-3 py-2.5 text-slate-600 align-top"><div className="max-w-[170px] line-clamp-2 whitespace-normal break-words">{p.category}</div></td>
                  <td className="px-3 py-2.5 text-slate-500 align-top"><div className="max-w-[160px] line-clamp-2 whitespace-normal break-words">{p.product_format || p.product_type || 'Not available'}</div></td>
                  <td className="px-3 py-2.5 text-slate-500 align-top"><div className="max-w-[150px] line-clamp-2 whitespace-normal break-words">{p.platform}</div></td>
                  <td className="px-3 py-2.5 text-right font-semibold text-slate-900 whitespace-nowrap">
                    {formatPrice(p.selling_price)}
                  </td>
                  <td className="px-3 py-2.5 text-right text-slate-400 whitespace-nowrap">
                    {formatPrice(p.mrp)}
                  </td>
                  <td className="px-3 py-2.5 text-right whitespace-nowrap">
                    {p.discount_pct !== null && p.discount_pct > 0 ? (
                      <span className="text-amber-700 font-medium bg-amber-50 px-1.5 py-0.5 rounded">
                        {formatDiscount(p.discount_pct)}
                      </span>
                    ) : (
                      <span className="text-slate-400">—</span>
                    )}
                  </td>
                  <td className="px-3 py-2.5 text-right text-slate-500 whitespace-nowrap">
                    {p.total_quantity !== null && p.total_quantity !== undefined
                      ? `${p.total_quantity} ${p.unit || ''}`
                      : p.pack_count !== null && p.pack_count !== undefined
                        ? `Pack of ${p.pack_count}`
                        : 'Not available'}
                  </td>

                  <td className="px-3 py-2.5 text-right whitespace-nowrap">
                    {p.rating !== null ? (
                      <span className="text-amber-600 font-semibold">{Number(p.rating).toFixed(2)} ★</span>
                    ) : (
                      <span className="text-slate-400 italic">Not available</span>
                    )}
                  </td>
                  <td className="px-3 py-2.5 text-right text-slate-500 whitespace-nowrap">
                    {formatReviews(p.review_count)}
                  </td>
                  <td className="px-3 py-2.5 text-center whitespace-nowrap">
                    <span
                      className={`px-2 py-0.5 text-[10px] font-medium rounded-full ${
                        p.availability === 'In Stock'
                          ? 'bg-emerald-50 text-emerald-700'
                          : 'bg-slate-100 text-slate-600'
                      }`}
                    >
                      {formatValue(p.availability)}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="p-3 border-t border-slate-200 flex items-center justify-between bg-slate-50">
        <div className="text-xs text-slate-500">
          Page {page} of {totalPages}
        </div>
        <div className="flex items-center space-x-1">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 1 || isLoading}
            className="p-1.5 rounded border border-slate-200 bg-white text-slate-600 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <div className="px-3 text-xs font-semibold text-slate-700">
            {page} / {totalPages}
          </div>
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= totalPages || isLoading}
            className="p-1.5 rounded border border-slate-200 bg-white text-slate-600 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Product Detail Modal / Drawer */}
      {selectedProduct && (
        <div className="fixed inset-0 z-50 flex items-stretch justify-end bg-black/40">
          <div className="product-drawer bg-white shadow-xl max-w-xl w-full overflow-hidden border-l border-slate-200 animate-in slide-in-from-right duration-150">
            <div className="px-5 py-4 border-b border-slate-100 flex items-start justify-between bg-slate-50">
              <div>
                <span className="px-2 py-0.5 text-xs font-semibold rounded bg-blue-100 text-blue-800">
                  {selectedProduct.brand}
                </span>
                <h3 className="text-sm font-bold text-slate-900 mt-1.5 leading-snug break-words">
                  {selectedProduct.title_clean || selectedProduct.title}
                </h3>
              </div>
              <button
                onClick={() => setSelectedProduct(null)}
                className="text-slate-400 hover:text-slate-700 p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-5 space-y-4 h-[calc(100vh-125px)] overflow-y-auto text-xs text-slate-700">
              <div className="grid grid-cols-2 gap-3 bg-slate-50 p-3 rounded-lg border border-slate-100">
                <div>
                  <span className="text-slate-400 block text-[11px]">Selling Price</span>
                  <span className="text-base font-bold text-slate-900">{formatPrice(selectedProduct.selling_price)}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[11px]">MRP</span>
                  <span className="text-sm text-slate-600 line-through">{formatPrice(selectedProduct.mrp)}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[11px]">Discount</span>
                  <span className="text-xs font-medium text-amber-700">{formatDiscount(selectedProduct.discount_pct)}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[11px]">Observed Rating</span>
                  <span className="text-xs font-semibold text-amber-600">{formatRating(selectedProduct.rating)}</span>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Category:</span>
                  <span className="font-medium text-slate-900">{formatValue(selectedProduct.category)}</span>
                </div>
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Sub-category:</span>
                  <span className="font-medium text-slate-900">Not available</span>
                </div>
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Product Format:</span>
                  <span className="font-medium text-slate-900">{selectedProduct.product_format || selectedProduct.product_type || '—'}</span>
                </div>
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Quantity / Pack:</span>
                  <span className="font-medium text-slate-900">
                    {selectedProduct.total_quantity !== null && selectedProduct.total_quantity !== undefined
                      ? `${selectedProduct.total_quantity} ${selectedProduct.unit || ''}`
                      : 'Not available'}
                    {selectedProduct.pack_count !== null && selectedProduct.pack_count !== undefined ? ` (Pack of ${selectedProduct.pack_count})` : ''}
                  </span>
                </div>
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Product ID:</span>
                  <span className="font-medium text-slate-900">{formatValue(selectedProduct.product_id)}</span>
                </div>
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Seller:</span>
                  <span className="font-medium text-slate-900">Not available</span>
                </div>
                {selectedProduct.price_per_unit !== null && selectedProduct.price_per_unit !== undefined && (
                  <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                    <span className="text-slate-500">Price / Unit:</span>
                    <span className="font-medium text-slate-900">₹{Number(selectedProduct.price_per_unit).toFixed(2)}</span>
                  </div>
                )}
                {selectedProduct.price_per_100ml !== null && selectedProduct.price_per_100ml !== undefined && (
                  <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                    <span className="text-slate-500">Price / 100ml:</span>
                    <span className="font-medium text-slate-900">₹{Number(selectedProduct.price_per_100ml).toFixed(2)}</span>
                  </div>
                )}
                {selectedProduct.price_per_100g !== null && selectedProduct.price_per_100g !== undefined && (
                  <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                    <span className="text-slate-500">Price / 100g:</span>
                    <span className="font-medium text-slate-900">₹{Number(selectedProduct.price_per_100g).toFixed(2)}</span>
                  </div>
                )}
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Source Platform:</span>
                  <span className="font-medium text-slate-900">{formatValue(selectedProduct.platform)}</span>
                </div>
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Observed Reviews:</span>
                  <span className="font-medium text-slate-900">{formatReviews(selectedProduct.review_count)}</span>
                </div>
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Review Source:</span>
                  <span className="font-medium text-slate-900">{formatValue(selectedProduct.review_source)}</span>
                </div>
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Availability:</span>
                  <span className="font-medium text-slate-900">{formatValue(selectedProduct.availability)}</span>
                </div>
                <div className="flex justify-between gap-4 py-1 border-b border-slate-100">
                  <span className="text-slate-500">Observed Date:</span>
                  <span className="font-medium text-slate-900">{selectedProduct.scraped_at ? new Date(selectedProduct.scraped_at).toLocaleDateString() : 'Not available'}</span>
                </div>
              </div>

              <div className="diagnostic-panel rounded-lg border border-blue-200 bg-blue-50 p-4 text-xs text-slate-700">
                <div className="flex items-center gap-2 mb-3">
                  <Activity className="w-4 h-4 text-blue-600" />
                  <h4 className="font-bold text-slate-900">Product Diagnostic</h4>
                </div>
                <h5 className="font-semibold text-slate-900 mb-2">Observed Benchmark Comparison</h5>
                <p className="diagnostic-muted text-[11px] text-slate-500 mb-3">
                  Compared with {getDiagnostic(selectedProduct).peerLabel} peers in the dashboard sample.
                </p>
                {getDiagnostic(selectedProduct).peers.length ? getDiagnostic(selectedProduct).comparison.map((item) => {
                  const difference = item.peer == null ? null : item.label === 'PRICE'
                    ? selectedProduct.selling_price - item.peer
                    : item.label === 'RATING'
                      ? selectedProduct.rating - item.peer
                      : item.label === 'DISCOUNT'
                        ? selectedProduct.discount_pct - item.peer
                        : selectedProduct.review_count - item.peer;
                  return <div key={item.label} className="diagnostic-divider flex items-center justify-between gap-3 border-t border-blue-100 py-2">
                    <span className="diagnostic-label font-semibold text-slate-600">{item.label}</span>
                    <span className="text-right"><strong className="text-slate-900">{item.value}</strong><br /><span className="diagnostic-muted text-[11px] text-slate-500">Peer {item.average ? 'average' : 'median'}: {item.peer == null ? 'Benchmark unavailable' : item.format(item.peer)}</span>{difference != null && <><br /><span className="text-[11px] font-semibold text-blue-700">{difference >= 0 ? '↑' : '↓'} {item.label === 'PRICE' ? formatPrice(Math.abs(difference)) : item.label === 'RATING' ? `${Math.abs(difference).toFixed(2)} points` : item.label === 'DISCOUNT' ? `${Math.abs(difference).toFixed(1)} percentage points` : Number(Math.abs(difference)).toLocaleString()} {difference >= 0 ? 'above' : 'below'} peer benchmark</span></>}</span>
                  </div>;
                }) : <p className="diagnostic-label text-slate-600">Benchmark unavailable - insufficient comparable data.</p>}
                {getDiagnostic(selectedProduct).areas.length > 0 && <>
                  <h5 className="font-semibold text-slate-900 mt-4 mb-2">Areas to Investigate</h5>
                  <ul className="diagnostic-label list-disc list-inside space-y-1 text-slate-600">{getDiagnostic(selectedProduct).areas.map((area) => <li key={area}>{area}</li>)}</ul>
                </>}
                <div className="diagnostic-divider mt-4 pt-3 border-t border-blue-100">
                  <h5 className="font-semibold text-slate-900">Validation Required</h5>
                  <p className="diagnostic-label mt-1 text-slate-600">Observed differences should be validated against product format, pack size, formulation, channel positioning and other commercial factors.</p>
                </div>
              </div>

              {(selectedProduct.product_url || selectedProduct.url) && (
                <div className="pt-2">
                  <a
                    href={selectedProduct.product_url || selectedProduct.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center space-x-1.5 text-xs text-blue-600 hover:text-blue-800 font-medium"
                  >
                    <span>Open Product</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              )}
            </div>

            <div className="px-5 py-3 bg-slate-50 border-t border-slate-100 flex justify-end">
              <button
                onClick={() => setSelectedProduct(null)}

                className="px-4 py-1.5 text-xs font-semibold text-slate-700 bg-white border border-slate-300 rounded hover:bg-slate-100"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
