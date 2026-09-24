import React from 'react';
import { AlertTriangle, RotateCcw } from 'lucide-react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Dashboard caught error in component tree:", error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
          <div className="max-w-xl w-full bg-white rounded-xl shadow-lg border border-slate-200 p-8 text-center">
            <div className="w-14 h-14 bg-rose-50 text-rose-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <AlertTriangle className="w-8 h-8" />
            </div>
            <h2 className="text-xl font-bold text-slate-900 mb-2">Something went wrong</h2>
            <p className="text-sm text-slate-600 mb-6 leading-relaxed">
              An unexpected error occurred while rendering the dashboard. See the diagnostics below:
            </p>
            <div className="bg-slate-900 text-rose-300 font-mono text-xs text-left p-4 rounded-lg overflow-x-auto mb-6 max-h-48">
              {this.state.error?.toString()}
              {this.state.errorInfo?.componentStack && (
                <div className="mt-2 text-slate-400">
                  {this.state.errorInfo.componentStack}
                </div>
              )}
            </div>
            <button
              onClick={this.handleReload}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg text-sm transition-colors shadow-sm"
            >
              <RotateCcw className="w-4 h-4" />
              Reload Dashboard
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
