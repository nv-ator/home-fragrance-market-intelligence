import React from 'react';
import { Search, RotateCcw, Filter } from 'lucide-react';

export default function FilterBar({
  filters,
  filterOptions,
  onFilterChange,
  onReset
}) {
  const handleInputChange = (field, value) => {
    onFilterChange({
      ...filters,
      [field]: value
    });
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-sm mb-6">
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100">
        <div className="flex items-center space-x-2 text-slate-800 font-semibold text-sm">
          <Filter className="w-4 h-4 text-blue-600" />
          <span>Interactive Product Filtering</span>
        </div>
        <button
          onClick={onReset}
          className="flex items-center space-x-1 text-xs text-slate-500 hover:text-slate-800 transition-colors font-medium px-2 py-1 rounded hover:bg-slate-100"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Reset Filters</span>
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {/* Search */}
        <div className="col-span-1 sm:col-span-2 md:col-span-1">
          <label className="block text-xs font-medium text-slate-600 mb-1">Search Keyword</label>
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="e.g. lavender, gel, refill..."
              value={filters.search || ''}
              onChange={(e) => handleInputChange('search', e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white"
            />
          </div>
        </div>

        {/* Brand */}
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Brand</label>
          <select
            value={filters.brand || ''}
            onChange={(e) => handleInputChange('brand', e.target.value)}
            className="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white"
          >
            <option value="">All Brands ({filterOptions?.brands?.length || 5})</option>
            {filterOptions?.brands?.map((b) => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>
        </div>

        {/* Category */}
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Category</label>
          <select
            value={filters.category || ''}
            onChange={(e) => handleInputChange('category', e.target.value)}
            className="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white"
          >
            <option value="">All Categories ({filterOptions?.categories?.length || 0})</option>
            {filterOptions?.categories?.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        {/* Platform */}
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Source Platform</label>
          <select
            value={filters.platform || ''}
            onChange={(e) => handleInputChange('platform', e.target.value)}
            className="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white"
          >
            <option value="">All Platforms</option>
            {filterOptions?.platforms?.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
        </div>

        {/* Product Type / Format */}
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Product Type / Format</label>
          <select
            value={filters.product_type || ''}
            onChange={(e) => handleInputChange('product_type', e.target.value)}
            className="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white"
          >
            <option value="">All Formats ({(filterOptions?.product_formats || filterOptions?.product_types)?.length || 0})</option>
            {(filterOptions?.product_formats || filterOptions?.product_types)?.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>

        {/* Availability */}
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Availability</label>
          <select
            value={filters.availability || ''}
            onChange={(e) => handleInputChange('availability', e.target.value)}
            className="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white"
          >
            <option value="">All Statuses</option>
            {(filterOptions?.availability || filterOptions?.availability_statuses)?.map((a) => (
              <option key={a} value={a}>{a}</option>
            ))}
          </select>
        </div>

        {/* Pack Size / Count */}
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Pack Size / Count</label>
          <select
            value={filters.pack_size || filters.pack_count || ''}
            onChange={(e) => handleInputChange('pack_size', e.target.value)}
            className="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white"
          >
            <option value="">All Pack Sizes</option>
            {filterOptions?.pack_sizes?.map((ps) => (
              <option key={ps} value={ps}>Pack of {ps}</option>
            ))}
          </select>
        </div>


        {/* Price Range */}
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Price Range (INR)</label>
          <div className="flex items-center space-x-1.5">
            <input
              type="number"
              placeholder="Min"
              value={filters.min_price || ''}
              onChange={(e) => handleInputChange('min_price', e.target.value)}
              className="w-1/2 px-2 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
            <span className="text-slate-400 text-xs">-</span>
            <input
              type="number"
              placeholder="Max"
              value={filters.max_price || ''}
              onChange={(e) => handleInputChange('max_price', e.target.value)}
              className="w-1/2 px-2 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Rating Range */}
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Min Rating (0 - 5★)</label>
          <select
            value={filters.min_rating || ''}
            onChange={(e) => handleInputChange('min_rating', e.target.value)}
            className="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white"
          >
            <option value="">Any Rating (incl. unrated)</option>
            <option value="4.0">★ 4.0 & above</option>
            <option value="4.2">★ 4.2 & above</option>
            <option value="4.4">★ 4.4 & above</option>
            <option value="4.6">★ 4.6 & above</option>
          </select>
        </div>
      </div>
    </div>
  );
}
