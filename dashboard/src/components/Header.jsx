import React from 'react';
import {
  LayoutDashboard,
  GitCompare,
  TrendingUp,
  PackageSearch,
  Lightbulb,
  Database
} from 'lucide-react';

export default function Header({
  activeTab,
  setActiveTab,
  apiStatus,
  systemMetadata,
  theme,
  onThemeChange
}) {
  const isConnected = apiStatus === 'healthy' || (systemMetadata?.status === 'ok' || systemMetadata?.status === 'healthy');

  const navItems = [
    { id: 'overview', label: 'Market Overview', icon: LayoutDashboard },
    { id: 'brands', label: 'Brand Comparison', icon: GitCompare },
    { id: 'pricing', label: 'Price Positioning', icon: TrendingUp },
    { id: 'products', label: 'Product Analysis', icon: PackageSearch },
    { id: 'insights', label: 'Business Insights', icon: Lightbulb },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
      {/* Top Brand Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 border-b border-slate-100">
          {/* Logo & Title */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white text-base shadow-sm">
              HF
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base sm:text-lg font-bold text-slate-900 leading-tight">
                  Home Fragrance Market Intelligence
                </h1>
                <span className="hidden md:inline-flex items-center text-[11px] font-semibold text-slate-600 bg-slate-50 px-2 py-0.5 rounded-full border border-slate-200">
                  Public Catalogue Analysis
                </span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">
                Competitive pricing, assortment and product positioning analysis
              </p>
            </div>
          </div>

          {/* Right Badges: API Status & Dataset Count */}
          <div className="flex items-center gap-2 sm:gap-3">
            <button
              type="button"
              onClick={() => onThemeChange(theme === 'dark' ? 'light' : 'dark')}
              className="theme-toggle inline-flex items-center gap-1.5 rounded-md border border-slate-200 bg-white px-2.5 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? 'Light' : 'Dark'}
            </button>
            {/* Connection Status Badge */}
            <div className={`
              flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border transition-colors
              ${isConnected
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                : 'bg-rose-50 text-rose-700 border-rose-200'}
            `}>
              <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
              <span className="hidden sm:inline">{isConnected ? 'FastAPI Connected' : 'API Disconnected'}</span>
              <span className="sm:hidden">{isConnected ? 'Live' : 'Offline'}</span>
            </div>

            {/* Database Indicator */}
            <div className="flex items-center gap-1.5 text-xs text-slate-600 bg-slate-100 px-2.5 py-1 rounded-md border border-slate-200 font-medium">
              <Database className="w-3.5 h-3.5 text-slate-500" />
              <span>Full Dataset: 684</span>
            </div>
            <div className="hidden lg:flex items-center text-xs text-blue-700 bg-blue-50 px-2.5 py-1 rounded-md border border-blue-200 font-semibold">
              Dashboard Sample: 120
            </div>
          </div>
        </div>

        {/* Top Navigation Tabs */}
        <nav className="flex space-x-1 sm:space-x-2 py-2 overflow-x-auto no-scrollbar" aria-label="Tabs">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`
                  flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all whitespace-nowrap
                  ${isActive
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}
                `}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
