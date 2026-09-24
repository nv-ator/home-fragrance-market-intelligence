import React from 'react';

export default function ChartCard({ title, subtitle, note, children, action }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between gap-4 mb-1">
          <div>
            <h3 className="text-sm font-semibold text-slate-900 leading-snug">
              {title}
            </h3>
            {subtitle && (
              <p className="text-xs text-slate-500 mt-0.5">
                {subtitle}
              </p>
            )}
          </div>
          {action && <div>{action}</div>}
        </div>

        <div className="mt-4 w-full">
          {children}
        </div>
      </div>

      {note && (
        <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-400 leading-relaxed italic">
          {note}
        </div>
      )}
    </div>
  );
}
