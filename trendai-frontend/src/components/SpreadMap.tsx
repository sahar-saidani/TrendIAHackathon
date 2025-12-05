import { Network, Users, AlertCircle, TrendingUp } from 'lucide-react';

export function SpreadMap() {
  const nodes = [
    { id: 1, x: 50, y: 30, size: 40, botScore: 95, label: '@ai_crypto_bot' },
    { id: 2, x: 30, y: 50, size: 35, botScore: 92, label: '@fetch_hunter' },
    { id: 3, x: 70, y: 50, size: 35, botScore: 89, label: '@agix_whale' },
    { id: 4, x: 20, y: 70, size: 25, botScore: 78, label: '@ai_trade_signals' },
    { id: 5, x: 40, y: 75, size: 25, botScore: 72, label: '@render_news_x' },
    { id: 6, x: 60, y: 75, size: 25, botScore: 81, label: '@tao_invest_pro' },
    { id: 7, x: 80, y: 70, size: 25, botScore: 68, label: '@ai_defi_tracker' },
    { id: 8, x: 15, y: 35, size: 20, botScore: 55, label: '@ai_hodler_123' },
    { id: 9, x: 85, y: 35, size: 20, botScore: 52, label: '@ocean_fan' },
    { id: 10, x: 50, y: 15, size: 30, botScore: 88, label: '@ai_pump_central' },
  ];

  const edges = [
    { from: 1, to: 2 },
    { from: 1, to: 3 },
    { from: 1, to: 10 },
    { from: 2, to: 4 },
    { from: 2, to: 5 },
    { from: 3, to: 6 },
    { from: 3, to: 7 },
    { from: 1, to: 8 },
    { from: 1, to: 9 },
    { from: 10, to: 2 },
    { from: 10, to: 3 },
  ];

  const getNodeColor = (botScore: number) => {
    if (botScore >= 85) return '#EF4444';
    if (botScore >= 70) return '#F97316';
    if (botScore >= 50) return '#EAB308';
    return '#10B981';
  };

  const clusters = [
    { id: 1, name: 'FET AI Agent Hype', size: 47, risk: 'High', accounts: 12 },
    { id: 2, name: 'AGIX-OpenAI Partnership', size: 38, risk: 'High', accounts: 8 },
    { id: 3, name: 'TAO Network Upgrade', size: 29, risk: 'Medium', accounts: 15 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-white text-3xl mb-2">Narrative Spread Map</h1>
        <p className="text-gray-400">Visual representation of how narratives propagate through social networks</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Network Visualization */}
        <div className="col-span-2 bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-white text-lg">Network Graph</h2>
            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <span className="text-gray-400">High Bot</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-orange-500"></div>
                <span className="text-gray-400">Medium Bot</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <span className="text-gray-400">Low Bot</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span className="text-gray-400">Human</span>
              </div>
            </div>
          </div>

          <div className="relative h-[500px] bg-[#0D0F14] rounded-lg border border-[#1E222D] overflow-hidden">
            <svg width="100%" height="100%" className="absolute inset-0">
              {/* Draw edges */}
              {edges.map((edge, index) => {
                const fromNode = nodes.find(n => n.id === edge.from);
                const toNode = nodes.find(n => n.id === edge.to);
                if (!fromNode || !toNode) return null;

                return (
                  <line
                    key={index}
                    x1={`${fromNode.x}%`}
                    y1={`${fromNode.y}%`}
                    x2={`${toNode.x}%`}
                    y2={`${toNode.y}%`}
                    stroke="#1E222D"
                    strokeWidth="2"
                    opacity="0.5"
                  />
                );
              })}

              {/* Draw nodes */}
              {nodes.map((node) => (
                <g key={node.id}>
                  <circle
                    cx={`${node.x}%`}
                    cy={`${node.y}%`}
                    r={node.size / 2}
                    fill={getNodeColor(node.botScore)}
                    opacity="0.8"
                    className="cursor-pointer hover:opacity-100 transition-opacity"
                  >
                    <title>{`${node.label}\nBot Score: ${node.botScore}`}</title>
                  </circle>
                  <circle
                    cx={`${node.x}%`}
                    cy={`${node.y}%`}
                    r={node.size / 2}
                    fill="none"
                    stroke={getNodeColor(node.botScore)}
                    strokeWidth="2"
                    opacity="0.3"
                    className="animate-pulse"
                  />
                </g>
              ))}
            </svg>

            {/* Node labels */}
            {nodes.slice(0, 5).map((node) => (
              <div
                key={`label-${node.id}`}
                className="absolute text-xs text-gray-400 pointer-events-none"
                style={{
                  left: `${node.x}%`,
                  top: `${node.y}%`,
                  transform: 'translate(-50%, calc(-50% - 35px))',
                }}
              >
                {node.label}
              </div>
            ))}
          </div>

          <div className="mt-4 grid grid-cols-3 gap-4">
            <div className="bg-[#0D0F14] rounded-lg p-3 border border-[#1E222D]">
              <p className="text-gray-400 text-xs mb-1">Total Nodes</p>
              <p className="text-white text-xl">{nodes.length}</p>
            </div>
            <div className="bg-[#0D0F14] rounded-lg p-3 border border-[#1E222D]">
              <p className="text-gray-400 text-xs mb-1">Connections</p>
              <p className="text-white text-xl">{edges.length}</p>
            </div>
            <div className="bg-[#0D0F14] rounded-lg p-3 border border-red-500/30">
              <p className="text-gray-400 text-xs mb-1">High-Risk Nodes</p>
              <p className="text-red-400 text-xl">{nodes.filter(n => n.botScore >= 85).length}</p>
            </div>
          </div>
        </div>

        {/* Side Panel */}
        <div className="space-y-4">
          <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <Network className="w-5 h-5 text-blue-400" />
              <h2 className="text-white text-lg">Network Summary</h2>
            </div>

            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-400 text-sm">Number of Clusters</span>
                  <span className="text-white">{clusters.length}</span>
                </div>
                <div className="h-1 bg-[#0D0F14] rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 w-3/4"></div>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-400 text-sm">Avg Bot Score</span>
                  <span className="text-orange-400">76.8</span>
                </div>
                <div className="h-1 bg-[#0D0F14] rounded-full overflow-hidden">
                  <div className="h-full bg-orange-500 w-[76.8%]"></div>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-400 text-sm">Network Density</span>
                  <span className="text-purple-400">High</span>
                </div>
                <div className="h-1 bg-[#0D0F14] rounded-full overflow-hidden">
                  <div className="h-full bg-purple-500 w-5/6"></div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertCircle className="w-5 h-5 text-red-400" />
              <h2 className="text-white text-lg">Top Clusters</h2>
            </div>

            <div className="space-y-3">
              {clusters.map((cluster) => (
                <div
                  key={cluster.id}
                  className={`p-3 rounded-lg border ${
                    cluster.risk === 'High'
                      ? 'bg-red-500/10 border-red-500/30'
                      : 'bg-orange-500/10 border-orange-500/30'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <p className="text-white text-sm">{cluster.name}</p>
                    <span className={`text-xs px-2 py-0.5 rounded ${
                      cluster.risk === 'High' ? 'bg-red-500/20 text-red-400' : 'bg-orange-500/20 text-orange-400'
                    }`}>
                      {cluster.risk}
                    </span>
                  </div>
                  <div className="flex items-center gap-4 text-xs text-gray-400">
                    <div className="flex items-center gap-1">
                      <Users className="w-3 h-3" />
                      <span>{cluster.accounts} accounts</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <TrendingUp className="w-3 h-3" />
                      <span>{cluster.size} posts</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
            <h2 className="text-white text-lg mb-4">Suspicious Accounts</h2>
            <div className="space-y-2">
              {nodes
                .filter(n => n.botScore >= 85)
                .sort((a, b) => b.botScore - a.botScore)
                .slice(0, 5)
                .map((node) => (
                  <div key={node.id} className="flex items-center justify-between p-2 rounded bg-[#0D0F14]">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-red-500"></div>
                      <span className="text-white text-sm">{node.label}</span>
                    </div>
                    <span className="text-red-400 text-xs">{node.botScore}</span>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}