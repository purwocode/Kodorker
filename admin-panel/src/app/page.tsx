'use client';

import { useCallback, useEffect, useState } from 'react';
import StatsCard from '@/components/StatsCard';
import LoadingSpinner from '@/components/LoadingSpinner';

interface ScraperStats {
  total_domains: number;
  total_results: number;
  total_queries: number;
  unique_titles: number;
}



export default function HomePage() {
  const [stats, setStats] = useState<ScraperStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = useCallback(async () => {
    try {
      const statsRes = await fetch('/api/public/stats');

      if (!statsRes.ok) throw new Error('Failed to fetch stats');
      const statsData = await statsRes.json();
      setStats(statsData);

      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, []);

  /* eslint-disable react-hooks/exhaustive-deps, react-hooks/set-state-in-effect */
  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);
  /* eslint-enable react-hooks/exhaustive-deps, react-hooks/set-state-in-effect */

  if (loading) return <LoadingSpinner />;

  if (error) {
    return (
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="bg-gray-950 border-2 border-red-500 rounded-lg p-6" style={{ boxShadow: '0 0 20px rgba(255,0,0,0.3)' }}>
          <h3 className="text-red-400 font-semibold font-mono text-lg">⚠️ ERROR DETECTED</h3>
          <p className="text-red-300 text-sm mt-1 font-mono">{error}</p>
          <button
            onClick={fetchStats}
            className="mt-3 px-4 py-2 bg-gradient-to-r from-red-600 to-orange-600 text-white rounded border-2 border-red-400 font-mono font-bold hover:from-orange-600 hover:to-red-600 transition-all" style={{ boxShadow: '0 0 10px rgba(255,0,0,0.6)' }}
          >
            🔄 RETRY
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-7xl">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatsCard
            title="DOMAINS_INDEXED"
            value={stats?.total_domains || 0}
            icon={
              <svg viewBox="-0.5 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-16 h-16">
                <path d="M22 11.8201C22 9.84228 21.4135 7.90885 20.3147 6.26436C19.2159 4.61987 17.6542 3.33813 15.8269 2.58126C13.9996 1.82438 11.9889 1.62637 10.0491 2.01223C8.10927 2.39808 6.32748 3.35052 4.92896 4.74904C3.53043 6.14757 2.578 7.92935 2.19214 9.86916C1.80629 11.809 2.00436 13.8197 2.76123 15.6469C3.51811 17.4742 4.79985 19.036 6.44434 20.1348C8.08883 21.2336 10.0222 21.8201 12 21.8201" stroke="#00ff64" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M2 11.8201H22" stroke="#00ff64" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M12 21.8201C10.07 21.8201 8.5 17.3401 8.5 11.8201C8.5 6.30007 10.07 1.82007 12 1.82007C13.93 1.82007 15.5 6.30007 15.5 11.8201" stroke="#00ff64" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M18.3691 21.6901C20.3021 21.6901 21.8691 20.1231 21.8691 18.1901C21.8691 16.2571 20.3021 14.6901 18.3691 14.6901C16.4361 14.6901 14.8691 16.2571 14.8691 18.1901C14.8691 20.1231 16.4361 21.6901 18.3691 21.6901Z" stroke="#00ff64" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M22.9998 22.8202L20.8398 20.6702" stroke="#00ff64" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            }
            trend="up"
          />
          <StatsCard
            title="RESULTS_CACHED"
            value={stats?.total_results || 0}
            icon={
              <svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" className="w-16 h-16" fill="none">
                <defs>
                  <style>{`.chart-green{fill:#00ff64;}`}</style>
                </defs>
                <path className="chart-green" d="M42.33,38H5.67l-.25-.63a20,20,0,1,1,37.16,0ZM7,36H41A18,18,0,1,0,6,30,17.87,17.87,0,0,0,7,36Z" />
                <path className="chart-green" d="M39,31a1,1,0,0,1-1-1,14,14,0,0,0-26.83-5.6A13.78,13.78,0,0,0,10,30a1,1,0,0,1-2,0,15.8,15.8,0,0,1,1.34-6.4A16,16,0,0,1,40,30,1,1,0,0,1,39,31Z" />
                <path className="chart-green" d="M28,38a1,1,0,0,1-1-1,3,3,0,0,0-6,0,1,1,0,0,1-2,0,5,5,0,0,1,10,0A1,1,0,0,1,28,38Z" />
                <path className="chart-green" d="M26.8,34a1,1,0,0,1-.62-.22,1,1,0,0,1-.16-1.4l6.4-8A1,1,0,1,1,34,25.63l-6.4,8A1,1,0,0,1,26.8,34Z" />
              </svg>
            }
            trend="up"
          />
          <StatsCard
            title="QUERIES_EXECUTED"
            value={stats?.total_queries || 0}
            icon={
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-16 h-16">
                <circle cx="11" cy="11" r="7" stroke="#00ff64" strokeWidth="2"></circle>
                <path d="M11 8C10.606 8 10.2159 8.0776 9.85195 8.22836C9.48797 8.37913 9.15726 8.6001 8.87868 8.87868C8.6001 9.15726 8.37913 9.48797 8.22836 9.85195C8.0776 10.2159 8 10.606 8 11" stroke="#00ff64" strokeWidth="2" strokeLinecap="round"></path>
                <path d="M20 20L17 17" stroke="#00ff64" strokeWidth="2" strokeLinecap="round"></path>
              </svg>
            }
            trend="up"
          />
          <StatsCard
            title="TITLES_EXTRACTED"
            value={stats?.unique_titles || 0}
            icon={
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-16 h-16">
                <path fillRule="evenodd" clipRule="evenodd" d="M13 10V14H9V12.5H10.4497C9.81799 11.881 8.95313 11.5 8 11.5C6.067 11.5 4.5 13.067 4.5 15H3C3 12.2386 5.23858 10 8 10C9.36334 10 10.5985 10.5456 11.5 11.4295V10H13Z" fill="#00ff64"></path>
                <path d="M11.5 15C11.5 15.9667 11.1091 16.8407 10.4749 17.4749C9.84067 18.1091 8.9667 18.5 8 18.5C7.04687 18.5 6.18201 18.119 5.55033 17.5H7V16H3V20H4.5V18.5705C5.40148 19.4544 6.63666 20 8 20C9.10981 20 10.136 19.6378 10.9654 19.026L12.9393 21L14 19.9393L12.026 17.9654C12.6378 17.136 13 16.1098 13 15H11.5Z" fill="#00ff64"></path>
                <path fillRule="evenodd" clipRule="evenodd" d="M9 5.5H14V10H18.5V18.5H15.0607V20H20V8.93934L15.0607 4H7.5V9H9V5.5ZM17.4393 8.5L15.5 6.56066V8.5H17.4393Z" fill="#00ff64"></path>
              </svg>
            }
            trend="up"
          />
        </div>
      </div>
    </div>
  );
}
