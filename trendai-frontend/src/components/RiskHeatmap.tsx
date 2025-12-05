interface RiskHeatmapProps {
  onTokenClick: (token: string) => void;
}

export function RiskHeatmap({ onTokenClick }: RiskHeatmapProps) {
  const tokens = [
    { name: 'FET', risk: 'high' },
    { name: 'AGIX', risk: 'high' },
    { name: 'RNDR', risk: 'medium' },
    { name: 'TAO', risk: 'low' },
    { name: 'OCEAN', risk: 'medium' },
    { name: 'GRT', risk: 'low' },
    { name: 'ARKM', risk: 'high' },
    { name: 'NMR', risk: 'low' },
    { name: 'AIOZ', risk: 'medium' },
    { name: 'ROSE', risk: 'low' },
    { name: 'PAAL', risk: 'high' },
    { name: 'ALI', risk: 'medium' },
  ];

  const narratives = [
    'Bot Activity',
    'Duplicate Posts',
    'Trust Score',
    'Viral Spread',
  ];

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low':
        return 'bg-green-500/30 hover:bg-green-500/50 border-green-500/50';
      case 'medium':
        return 'bg-yellow-500/30 hover:bg-yellow-500/50 border-yellow-500/50';
      case 'high':
        return 'bg-red-500/30 hover:bg-red-500/50 border-red-500/50';
      default:
        return 'bg-gray-500/30 hover:bg-gray-500/50 border-gray-500/50';
    }
  };

  const getRandomRisk = () => {
    const risks = ['low', 'low', 'medium', 'high'];
    return risks[Math.floor(Math.random() * risks.length)];
  };

  return (
    <div className="overflow-x-auto">
      <div className="min-w-max">
        <div className="grid grid-cols-[120px_repeat(12,1fr)] gap-2">
          {/* Header */}
          <div></div>
          {tokens.map((token) => (
            <div key={token.name} className="text-center text-gray-400 text-sm pb-2">
              {token.name}
            </div>
          ))}

          {/* Rows */}
          {narratives.map((narrative) => (
            <>
              <div key={`label-${narrative}`} className="flex items-center text-gray-400 text-sm">
                {narrative}
              </div>
              {tokens.map((token) => {
                const risk = narrative === 'Bot Activity' ? token.risk : getRandomRisk();
                return (
                  <button
                    key={`${narrative}-${token.name}`}
                    onClick={() => onTokenClick(`${token.name} - ${narrative}`)}
                    className={`h-12 rounded border ${getRiskColor(risk)} transition-all cursor-pointer`}
                    title={`${token.name} - ${narrative}: ${risk} risk`}
                  />
                );
              })}
            </>
          ))}
        </div>

        {/* Legend */}
        <div className="flex items-center gap-6 mt-6 pt-4 border-t border-[#1E222D]">
          <span className="text-gray-400 text-sm">Risk Level:</span>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-green-500/30 border border-green-500/50"></div>
            <span className="text-gray-400 text-sm">Low</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-yellow-500/30 border border-yellow-500/50"></div>
            <span className="text-gray-400 text-sm">Medium</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-red-500/30 border border-red-500/50"></div>
            <span className="text-gray-400 text-sm">High</span>
          </div>
        </div>
      </div>
    </div>
  );
}