'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function PelerPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.error || 'Login gagal');
                setLoading(false);
                return;
            }

            // Login berhasil, redirect ke dashboard
            router.push('/dashboard');
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (_err) {
            setError('Terjadi kesalahan. Coba lagi.');
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center" style={{ backgroundImage: 'radial-gradient(circle at 20% 50%, rgba(0,255,136,0.1) 0%, transparent 50%)', backgroundAttachment: 'fixed' }}>
            {/* Scanlines effect */}
            <div className="fixed inset-0 pointer-events-none opacity-5" style={{ backgroundImage: 'repeating-linear-gradient(0deg, #000, #000 2px, transparent 2px, transparent 4px)' }}></div>

            <div className="w-full max-w-md px-4 relative z-10">
                {/* Header */}
                <div className="text-center mb-8">
                    <div className="flex items-center justify-center gap-2 mb-4">
                        <span className="text-4xl">⚡</span>
                        <h1 className="text-5xl font-bold font-mono text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-green-400 to-purple-500" style={{ textShadow: '0 0 20px rgba(0,255,255,0.5)' }}>
                            DORKER
                        </h1>
                        <span className="text-4xl">⚡</span>
                    </div>
                    <p className="text-green-300 font-mono text-sm" style={{ textShadow: '0 0 10px rgba(0,255,100,0.7)' }}>
                        &gt; Access Terminal v0.1
                    </p>
                </div>

                {/* Login Card */}
                <div className="bg-gray-950 border-2 border-cyan-500 rounded p-8" style={{ boxShadow: '0 0 30px rgba(0,255,255,0.3), inset 0 0 20px rgba(0,255,255,0.1)' }}>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Error Message */}
                        {error && (
                            <div className="bg-red-950 border-2 border-red-500 rounded p-3" style={{ boxShadow: '0 0 15px rgba(255,0,0,0.3)' }}>
                                <p className="text-red-300 font-mono text-sm">{error}</p>
                            </div>
                        )}

                        {/* Username Field */}
                        <div>
                            <label className="block text-cyan-400 text-xs font-mono uppercase tracking-widest mb-2" style={{ textShadow: '0 0 10px rgba(0,255,255,0.8)' }}>
                                $ USERNAME
                            </label>
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="admin"
                                disabled={loading}
                                className="w-full bg-gray-900 border-2 border-green-500 rounded px-4 py-3 text-green-300 placeholder-green-700 font-mono focus:outline-none focus:border-lime-400 transition-all"
                                style={{ boxShadow: '0 0 10px rgba(0,255,100,0.3)', color: '#00ff64' }}
                            />
                        </div>

                        {/* Password Field */}
                        <div>
                            <label className="block text-cyan-400 text-xs font-mono uppercase tracking-widest mb-2" style={{ textShadow: '0 0 10px rgba(0,255,255,0.8)' }}>
                                $ PASSWORD
                            </label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                disabled={loading}
                                className="w-full bg-gray-900 border-2 border-green-500 rounded px-4 py-3 text-green-300 placeholder-green-700 font-mono focus:outline-none focus:border-lime-400 transition-all"
                                style={{ boxShadow: '0 0 10px rgba(0,255,100,0.3)', color: '#00ff64' }}
                            />
                        </div>

                        {/* Login Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-cyan-500 to-green-500 text-black py-3 rounded border-2 border-green-400 font-mono font-bold uppercase text-sm hover:from-green-400 hover:to-cyan-400 transition-all disabled:opacity-50"
                            style={{ boxShadow: '0 0 20px rgba(0,255,100,0.6)' }}
                        >
                            {loading ? '🔓 ACCESSING...' : '🔐 LOGIN'}
                        </button>
                    </form>

                    {/* Footer Info */}

                </div>

                {/* System Status */}
                <div className="mt-6 text-center">
                    <div className="flex items-center justify-center gap-2">
                        <span className="inline-block w-2 h-2 rounded-full bg-lime-400 animate-pulse" style={{ boxShadow: '0 0 10px rgba(0,255,100,0.8)' }}></span>
                        <p className="text-lime-400 font-mono text-xs" style={{ textShadow: '0 0 10px rgba(0,255,100,0.6)' }}>SYSTEM READY</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
