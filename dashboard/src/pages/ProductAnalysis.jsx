import React, { useState, useEffect } from 'react';
import { Package } from 'lucide-react';
import FilterBar from '../components/FilterBar';
import DataTable from '../components/DataTable';
import EmptyState from '../components/EmptyState';
import { getFilters } from '../api/client';
import { getDashboardSample } from '../utils/dashboardSample';

export default function ProductAnalysis() {
  const [filterOptions, setFilterOptions] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    brand: '',
    category: '',
    platform: '',
    product_type: '',
    pack_size: '',
    availability: '',
    min_price: '',
    max_price: '',
    min_rating: ''
  });

  const [sampleProducts, setSampleProducts] = useState([]);
  const [products, setProducts] = useState([]);
  const [totalProducts, setTotalProducts] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  const [loadingFilters, setLoadingFilters] = useState(true);
  const [loadingProducts, setLoadingProducts] = useState(true);
  const [error, setError] = useState(null);

  // Fetch filter metadata on mount
  useEffect(() => {
    async function loadFilterOptions() {
      try {
        const res = await getFilters();
        setFilterOptions(res);
      } catch (err) {
        console.error('Failed to load filter options:', err);
      } finally {
        setLoadingFilters(false);
      }
    }
    loadFilterOptions();
  }, []);

  // Load a stable, balanced dashboard sample while retaining the full API dataset.
  useEffect(() => {
    let isCancelled = false;

    async function loadSample() {
      setLoadingProducts(true);
      setError(null);
      try {
        const balancedSample = await getDashboardSample();
        if (!isCancelled) setSampleProducts(balancedSample);
      } catch (err) {
        if (!isCancelled) {
          setError(err.message || 'Failed to load the dashboard sample from FastAPI.');
        }
      } finally {
        if (!isCancelled) setLoadingProducts(false);
      }
    }

    loadSample();
    return () => { isCancelled = true; };
  }, []);

  // Apply all Product Analysis filters to the balanced sample, then paginate locally.
  useEffect(() => {
    const normalizedSearch = filters.search.trim().toLowerCase();
    const filtered = sampleProducts.filter((product) => {
      const title = `${product.title_clean || ''} ${product.title_raw || ''}`.toLowerCase();
      const productFormat = product.product_format || product.product_type || '';
      return (!normalizedSearch || title.includes(normalizedSearch))
        && (!filters.brand || product.brand === filters.brand)
        && (!filters.category || product.category === filters.category)
        && (!filters.platform || product.platform === filters.platform)
        && (!filters.product_type || productFormat === filters.product_type)
        && (!filters.pack_size || product.pack_count === Number(filters.pack_size))
        && (!filters.availability || product.availability === filters.availability)
        && (!filters.min_price || product.selling_price >= Number(filters.min_price))
        && (!filters.max_price || product.selling_price <= Number(filters.max_price))
        && (!filters.min_rating || (product.rating !== null && product.rating >= Number(filters.min_rating)));
    });
    setTotalProducts(filtered.length);
    setProducts(filtered.slice((page - 1) * pageSize, page * pageSize));
  }, [sampleProducts, filters, page, pageSize]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    setPage(1); // reset to first page on filter change
  };

  const handleResetFilters = () => {
    setFilters({
      search: '',
      brand: '',
      category: '',
      platform: '',
      product_type: '',
      pack_size: '',
      availability: '',
      min_price: '',
      max_price: '',
      min_rating: ''
    });
    setPage(1);
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div>
        <h2 className="text-xl font-bold text-slate-900 tracking-tight">Product Catalogue Exploration</h2>
        <p className="text-xs text-slate-500 mt-1">
          Search, filter, and inspect a balanced dashboard sample of 120 products from the full 684-product validated catalogue.
        </p>
      </div>

      {/* Filter Bar */}
      <FilterBar
        filters={filters}
        filterOptions={filterOptions}
        onFilterChange={handleFilterChange}
        onReset={handleResetFilters}
      />

      <div className="flex flex-wrap items-center gap-2 text-xs text-slate-600">
        <span className="font-semibold text-slate-800">Dashboard Sample: 120 products</span>
        <span>24 products per brand</span>
        <span className="text-slate-400">Full dataset: 684 validated products</span>
      </div>

      {/* Error state */}
      {error && (
        <EmptyState
          type="error"
          title="Product Retrieval Error"
          message={error}
          actionText="Retry Product Search"
          onAction={() => setPage(1)}
        />
      )}

      {/* Data Table */}
      {!error && (
        <DataTable
          products={products}
          total={totalProducts}
          page={page}
          pageSize={pageSize}
          onPageChange={setPage}
          onPageSizeChange={(newSize) => {
            setPageSize(newSize);
            setPage(1);
          }}
          isLoading={loadingProducts}
          diagnosticProducts={sampleProducts}
        />
      )}

      {/* Methodology notice */}
      <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-500 leading-relaxed">
        <span className="font-semibold text-slate-700">Data Integrity Notice: </span>
        All product records, pricing, discounts, and ratings represent publicly observed catalogue data extracted without modification. 
        Null values are explicitly rendered as "Not available" or "—" rather than zero to maintain strict analytical fidelity.
      </div>
    </div>
  );
}
