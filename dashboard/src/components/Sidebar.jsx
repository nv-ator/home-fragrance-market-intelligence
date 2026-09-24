import React from 'react';
import { 
  LayoutDashboard, 
  GitCompare, 
  TrendingUp, 
  PackageSearch, 
  Lightbulb, 
  X,
  ShieldCheck
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, activePage, setActivePage, isOpen, setIsOpen }) {
  const currentTab = activeTab || activePage || 'overview';
  const handleSelect = setActiveTab || setActivePage || (() => {});

  const navItems = [
    { id: 'overview', label: 'Market Overview', icon: LayoutDashboard },
    { id: 'brands', label: 'Brand Comparison', icon: GitCompare },
    { id: 'pricing', label: 'Price Positioning', icon: TrendingUp },
    { id: 'products', label: 'Product Analysis', icon: PackageSearch },
    { id: 'insights', label: 'Business Insights', icon: Lightbulb },
  ];


  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40 bg-slate-900/60 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar Container */}
      <aside className={`
        fixed top-0 bottom-0 left-0 z-50 w-64 bg-slate-900 text-slate-100 flex flex-col transition-transform duration-200 ease-in-out
        lg:translate-x-0 ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        {/* Brand Header */}
        <div className="h-16 px-6 flex items-center justify-between border-b border-slate-800">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-sm">
              HF
            </div>
            <div>
              <span className="font-semibold text-sm tracking-wide text-white block">Market Intelligence</span>
              <span className="text-[10px] text-slate-400 block tracking-wider uppercase">Portfolio Analysis</span>
            </div>
          </div>
          <button 
            className="lg:hidden text-slate-400 hover:text-white p-1"
            onClick={() => setIsOpen(false)}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 py-6 px-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  handleSelect(item.id);
                  setIsOpen(false);
                }}
                className={`
                  w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-left
                  ${isActive 
                    ? 'bg-blue-600 text-white shadow-sm' 
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'}
                `}
              >

                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                {item.label}
              </button>
            );
          })}
        </nav>

        {/* Audit Provenance Badge */}
        <div className="p-4 border-t border-slate-800 text-xs text-slate-400">
          <div className="flex items-center gap-1.5 text-emerald-400 font-medium mb-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Public Catalogue Dataset</span>
          </div>
          <p className="text-[11px] leading-relaxed text-slate-400">
            767 validated products across 5 competitor brands.
          </p>
        </div>
      </aside>
    </>
  );
}
