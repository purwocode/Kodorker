import { ReactNode } from 'react';

export default function StatsCard({
    title,
    value,
    icon,
    trend,
}: {
    title: string;
    value: number;
    icon: string | ReactNode;
    trend?: 'up' | 'down';
}) {
    return (
        <div className="bg-gray-950 border-2 border-cyan-500 rounded p-6 hover:border-green-400 transition-all group overflow-hidden relative" style={{ boxShadow: '0 0 20px rgba(0,255,255,0.3), inset 0 0 10px rgba(0,255,255,0.1)' }}>
            {/* Glow effect */}
            <div className="absolute -inset-full bg-gradient-to-r from-cyan-500 via-green-500 to-purple-500 opacity-0 group-hover:opacity-20 transition-opacity duration-500 blur-2xl"></div>

            <div className="relative flex items-center justify-between">
                <div>
                    <p className="text-cyan-400 text-xs font-mono uppercase tracking-widest" style={{ textShadow: '0 0 10px rgba(0,255,255,0.8)' }}>{title}</p>
                    <p className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-cyan-400 mt-2 font-mono" style={{ textShadow: '0 0 20px rgba(0,255,100,0.5)' }}>{value.toLocaleString()}</p>
                    {trend && (
                        <p className={`text-xs font-semibold mt-2 font-mono ${trend === 'up' ? 'text-lime-400' : 'text-orange-400'}`}>
                            {trend === 'up' ? '📈 INCREASING' : '📉 DECREASING'}
                        </p>
                    )}
                </div>
                <div className="text-6xl opacity-80 group-hover:opacity-100 transition-opacity">{icon}</div>
            </div>
        </div>
    );
}
