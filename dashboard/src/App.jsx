import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Overview from './pages/Overview';
import BrandComparison from './pages/BrandComparison';
import PricePositioning from './pages/PricePositioning';
import ProductAnalysis from './pages/ProductAnalysis';
import BusinessInsights from './pages/BusinessInsights';
import { getHealth } from './api/client';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [apiStatus, setApiStatus] = useState('checking'); // 'healthy' | 'unhealthy' | 'checking'
  const [systemMetadata, setSystemMetadata] = useState(null);
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('dashboard-theme');
    return savedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  });

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
    localStorage.setItem('dashboard-theme', theme);
  }, [theme]);

  // Check backend health periodically
  useEffect(() => {
    async function checkHealth() {
      try {
        const health = await getHealth();
        if (health && (health.status === 'ok' || health.status === 'healthy')) {
          setApiStatus('healthy');
          setSystemMetadata(health);
        } else {
          setApiStatus('unhealthy');
        }
      } catch (err) {
        console.error('API health check error:', err);
        setApiStatus('unhealthy');
      }
    }

    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const renderActivePage = () => {
    switch (activeTab) {
      case 'overview':
        return <Overview />;
      case 'brands':
        return <BrandComparison />;
      case 'pricing':
        return <PricePositioning />;
      case 'products':
        return <ProductAnalysis />;
      case 'insights':
        return <BusinessInsights />;
      default:
        return <Overview />;
    }
  };

  return (
    <div className={`min-h-screen bg-slate-50 text-slate-900 font-sans flex flex-col ${theme === 'dark' ? 'dark-theme' : ''}`}>
      {/* Top Navbar Header with tabs */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        apiStatus={apiStatus}
        systemMetadata={systemMetadata}
        theme={theme}
        onThemeChange={setTheme}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        {renderActivePage()}
      </main>
    </div>
  );
}
