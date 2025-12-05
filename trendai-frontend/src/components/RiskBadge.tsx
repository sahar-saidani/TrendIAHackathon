import { Shield, AlertTriangle, ShieldAlert } from 'lucide-react';

interface RiskBadgeProps {
  risk: 'safe' | 'suspicious' | 'high';
}

export function RiskBadge({ risk }: RiskBadgeProps) {
  const configs = {
    safe: {
      icon: Shield,
      label: 'Safe',
      classes: 'bg-green-500/20 text-green-400 border-green-500/30',
    },
    suspicious: {
      icon: AlertTriangle,
      label: 'Suspicious',
      classes: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    },
    high: {
      icon: ShieldAlert,
      label: 'High Risk',
      classes: 'bg-red-500/20 text-red-400 border-red-500/30',
    },
  };

  const config = configs[risk];
  const Icon = config.icon;

  return (
    <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg border ${config.classes}`}>
      <Icon className="w-5 h-5" />
      <span>{config.label}</span>
    </div>
  );
}
