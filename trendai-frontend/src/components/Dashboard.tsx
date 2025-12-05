import { KpiCard } from './KpiCard';
import { RiskHeatmap } from './RiskHeatmap';
import { TimelineChart } from './TimelineChart';
import { ShieldCheck, Activity, Bot } from 'lucide-react';

interface DashboardProps {
  onNarrativeClick: (narrative: string) => void;
}

export function Dashboard({ onNarrativeClick }: DashboardProps) {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-white text-3xl mb-2">Dashboard</h1>
        <p className="text-gray-400">Real-time AI crypto token narrative monitoring and analysis</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-3 gap-6">
        <KpiCard
          title="Narrative Risk"
          value="Suspicious"
          icon={ShieldCheck}
          trend="+12% from yesterday"
          trendUp={true}
          color="yellow"
        />
        <KpiCard
          title="Average Trust Score"
          value="67"
          icon={Activity}
          trend="-5 pts from yesterday"
          trendUp={false}
          color="blue"
        />
        <KpiCard
          title="Bot Activity Level"
          value="Medium"
          icon={Bot}
          trend="3 new clusters detected"
          trendUp={true}
          color="purple"
        />
      </div>

      {/* Risk Heatmap */}
      <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-white text-xl mb-1">Risk Heatmap per AI Token</h2>
            <p className="text-gray-400 text-sm">Real-time risk assessment across monitored AI crypto tokens</p>
          </div>
          <select className="bg-[#0D0F14] border border-[#1E222D] rounded-lg px-4 py-2 text-white text-sm focus:outline-none focus:border-blue-500/50">
            <option>Last 24 hours</option>
            <option>Last 7 days</option>
            <option>Last 30 days</option>
          </select>
        </div>
        <RiskHeatmap onTokenClick={onNarrativeClick} />
      </div>

      {/* Timeline Chart */}
      <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
        <div className="mb-6">
          <h2 className="text-white text-xl mb-1">AI Token Narrative Spread Timeline</h2>
          <p className="text-gray-400 text-sm">Post volume over time across key AI token narratives</p>
        </div>
        <TimelineChart />
      </div>
    </div>
  );
}