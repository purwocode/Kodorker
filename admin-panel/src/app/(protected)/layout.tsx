'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const router = useRouter();
    const [isLoggingOut, setIsLoggingOut] = useState(false);

    const handleLogout = async () => {
        setIsLoggingOut(true);
        try {
            const response = await fetch('/api/auth/logout', {
                method: 'POST',
            });

            if (response.ok) {
                router.push('/peler');
            }
        } catch (error) {
            console.error('Logout error:', error);
            setIsLoggingOut(false);
        }
    };

    return (
        <>
            <nav className="bg-black border-b-2 border-cyan-500 sticky top-0 z-40" style={{ boxShadow: '0 0 20px rgba(0,255,255,0.5), inset 0 0 20px rgba(0,255,255,0.1)' }}>
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <span className="text-2xl">⚡</span>
                        <h1 className="text-2xl font-bold font-mono text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-green-400" style={{ textShadow: '0 0 20px rgba(0,255,100,0.5)' }}>
                            [DORKER_DASHBOARD]
                        </h1>
                    </div>
                    <button
                        onClick={handleLogout}
                        disabled={isLoggingOut}
                        className="px-4 py-2 bg-gradient-to-r from-red-600 to-orange-600 text-white rounded border-2 border-red-400 font-mono font-bold text-sm hover:from-orange-600 hover:to-red-600 transition-all disabled:opacity-50"
                        style={{ boxShadow: '0 0 15px rgba(255,0,0,0.6)' }}
                    >
                        {isLoggingOut ? '🔒 LOGGING OUT...' : '🔒 LOGOUT'}
                    </button>
                </div>
            </nav>

            <main className="min-h-screen bg-black" style={{ backgroundImage: 'radial-gradient(circle at 20% 50%, rgba(0,255,136,0.1) 0%, transparent 50%)', backgroundAttachment: 'fixed' }}>
                {/* Scanlines effect */}
                <div className="fixed inset-0 pointer-events-none opacity-5 z-0" style={{ backgroundImage: 'repeating-linear-gradient(0deg, #000, #000 2px, transparent 2px, transparent 4px)' }}></div>
                <div className="relative z-10">
                    {children}
                </div>
            </main>
        </>
    );
}
