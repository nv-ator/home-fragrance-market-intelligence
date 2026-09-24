import React from 'react';
import { AlertCircle, RotateCcw, Database } from 'lucide-react';

export default function EmptyState({ 
  title = "No Data Available", 
  message = "No records match the selected parameters or filters.", 
  onRetry, 
  onAction,
  isError = false,
  type = "info",
  actionText = "Retry Request"
}) {
  const isErr = isError || type === "error";
  const handleAction = onRetry || onAction;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-12 text-center shadow-sm flex flex-col items-center justify-center my-6">
      <div className={`p-3 rounded-full mb-3 ${isErr ? 'bg-rose-50 text-rose-600' : 'bg-slate-100 text-slate-500'}`}>
        {isErr ? <AlertCircle className="w-8 h-8" /> : <Database className="w-8 h-8" />}
      </div>
      <h3 className="text-base font-semibold text-slate-900 mb-1">
        {title}
      </h3>
      <p className="text-sm text-slate-500 max-w-md mx-auto mb-5 leading-relaxed">
        {message}
      </p>
      {handleAction && (
        <button
          onClick={handleAction}
          className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium rounded-lg shadow-sm transition-colors"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          {actionText}
        </button>
      )}
    </div>
  );
}

