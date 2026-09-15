'use client';

interface UsageMetric {
    usage: number;
    limit: number;
}

interface UsageStatsProps {
    egress: UsageMetric;
    database_size: UsageMetric;
    monthly_active_users: UsageMetric;
    storage_size: UsageMetric;
}

interface UsageCardProps {
    title: string;
    icon: string;
    metric: UsageMetric;
    unit: string;
}

const getPercentage = (usage: number, limit: number) => {
    return Math.min((usage / limit) * 100, 100);
};

const getColor = (percentage: number) => {
    if (percentage >= 90) return 'from-red-500 to-red-600';
    if (percentage >= 70) return 'from-orange-500 to-orange-600';
    return 'from-lime-400 to-cyan-400';
};

// Extracted component - defined outside render
function UsageCard({ title, icon, metric, unit }: UsageCardProps) {
    const percentage = getPercentage(metric.usage, metric.limit);

    return (
        <div className="bg-gray-950 border-2 border-cyan-500 rounded-lg p-5" style={{ boxShadow: '0 0 15px rgba(0,255,255,0.2)' }}>
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                    <span className="text-xl">{icon}</span>
                    <h3 className="font-mono text-sm font-bold text-cyan-400 uppercase">{title}</h3>
                </div>
                <span className={`text-xs font-bold px-2 py-1 rounded border ${percentage >= 90 ? 'border-red-500 text-red-400' : percentage >= 70 ? 'border-orange-500 text-orange-400' : 'border-lime-400 text-lime-400'}`}>
                    {percentage.toFixed(1)}%
                </span>
            </div>

            {/* Progress Bar */}
            <div className="mb-2 h-2 bg-gray-900 rounded overflow-hidden border border-gray-800">
                <div
                    className={`h-full bg-gradient-to-r ${getColor(percentage)} transition-all duration-300`}
                    style={{ width: `${Math.min(percentage, 100)}%`, boxShadow: `0 0 10px rgba(0,255,100,0.5)` }}
                ></div>
            </div>

            {/* Usage Text */}
            <div className="text-xs font-mono text-gray-300">
                <span className="text-lime-400 font-bold">{metric.usage.toFixed(2)}</span>
                <span className="text-gray-500"> / </span>
                <span className="text-cyan-400">{metric.limit}</span>
                <span className="text-gray-600"> {unit}</span>
            </div>
        </div>
    );
}

export default function UsageStats({
    egress,
    database_size,
    monthly_active_users,
    storage_size,
}: UsageStatsProps) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <UsageCard title="Egress" icon="📊" metric={egress} unit="GB" />
            <UsageCard title="Database Size" icon="🗄️" metric={database_size} unit="MB" />
            <UsageCard title="Monthly Active Users" icon="👥" metric={monthly_active_users} unit="" />
            <UsageCard title="File Storage" icon="💾" metric={storage_size} unit="GB" />
        </div>
    );
}
