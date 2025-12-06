import {TrendingUp, TrendingDown, type LucideIcon } from 'lucide-react';

interface KpiCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend: string;
  trendUp: boolean;
  color: 'blue' | 'purple' | 'green' | 'yellow' | 'red';
}

export function KpiCard({ title, value, icon: Icon, trend, trendUp, color }: KpiCardProps) {
  const colorClasses = {
    blue: 'from-blue-500/20 to-blue-600/10 border-blue-500/30 text-blue-400',
    purple: 'from-purple-500/20 to-purple-600/10 border-purple-500/30 text-purple-400',
    green: 'from-green-500/20 to-green-600/10 border-green-500/30 text-green-400',
    yellow: 'from-yellow-500/20 to-yellow-600/10 border-yellow-500/30 text-yellow-400',
    red: 'from-red-500/20 to-red-600/10 border-red-500/30 text-red-400',
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} border rounded-xl p-6`}>
      <div className="flex items-start justify-between mb-4">
        <div className="p-3 rounded-lg bg-[#0D0F14]/50">
          <Icon className="w-6 h-6" />
        </div>
      </div>
      <div className="mb-2">
        <p className="text-gray-400 text-sm mb-1">{title}</p>
        <p className="text-white text-3xl">{value}</p>
      </div>
      <div className="flex items-center gap-1 text-xs">
        {trendUp ? (
          <TrendingUp className="w-3 h-3" />
        ) : (
          <TrendingDown className="w-3 h-3" />
        )}
        <span>{trend}</span>
      </div>
    </div>
  );
}
