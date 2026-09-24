import React from 'react';

export default function KpiCard({ title, value, subtitle, note, icon: Icon, color = "blue" }) {
  const colorMap = {
    blue: "text-blue-600 bg-blue-50 border-blue-100",
    emerald: "text-emerald-600 bg-emerald-50 border-emerald-100",
    amber: "text-amber-600 bg-amber-50 border-amber-100",
    indigo: "text-indigo-600 bg-indigo-50 border-indigo-100",
    slate: "text-slate-600 bg-slate-50 border-slate-200",
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow transition-shadow">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
          {title}
        </span>
        {Icon && (
          <div className={`p-2 rounded-lg border ${colorMap[color] || colorMap.blue}`}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="mt-3 flex items-baseline gap-2">
        <span className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
          {value !== null && value !== undefined ? value : "—"}
        </span>
        {subtitle && (
          <span className="text-xs text-slate-500 font-medium">
            {subtitle}
          </span>
        )}
      </div>

      {note && (
        <p className="mt-2 text-[11px] text-slate-400 leading-normal">
          {note}
        </p>
      )}
    </div>
  );
}
