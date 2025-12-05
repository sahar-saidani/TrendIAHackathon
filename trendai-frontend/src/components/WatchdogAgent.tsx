import { useState } from 'react';
import { Search, Bot, AlertTriangle, TrendingUp, Copy } from 'lucide-react';
import { RiskBadge } from './RiskBadge';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export function WatchdogAgent() {
  const [query, setQuery] = useState('');
  const [analyzed, setAnalyzed] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  const handleAnalyze = () => {
    if (!query) return;
    setAnalyzing(true);
    setTimeout(() => {
      setAnalyzing(false);
      setAnalyzed(true);
    }, 1500);
  };

  const duplicateData = [
    { time: '6h ago', percentage: 12 },
    { time: '5h ago', percentage: 18 },
    { time: '4h ago', percentage: 28 },
    { time: '3h ago', percentage: 35 },
    { time: '2h ago', percentage: 42 },
    { time: '1h ago', percentage: 47 },
    { time: 'Now', percentage: 47 },
  ];

  const suspiciousPosts = [
    {
      user: '@crypto_whale_88',
      text: 'DOGE to the moon! 🚀 This is the next 100x! Don\'t miss out!!!',
      botScore: 94,
    },
    {
      user: '@moon_hunter_2024',
      text: 'DOGE to the moon! 🚀 This is the next 100x! Don\'t miss out!!!',
      botScore: 96,
    },
    {
      user: '@invest_guru_pro',
      text: 'DOGE pumping hard! Get in now before it\'s too late! 🚀🚀🚀',
      botScore: 88,
    },
  ];

  const suspiciousAccounts = [
    { name: '@crypto_whale_88', botScore: 94, followers: '1.2K', created: '2 weeks ago' },
    { name: '@moon_hunter_2024', botScore: 96, followers: '890', created: '1 week ago' },
    { name: '@invest_guru_pro', botScore: 88, followers: '2.3K', created: '3 weeks ago' },
    { name: '@trade_signals_x', botScore: 91, followers: '1.5K', created: '10 days ago' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-white text-3xl mb-2">Watchdog Agent</h1>
        <p className="text-gray-400">Real-time narrative and token analysis powered by AI</p>
      </div>

      {/* Input Section */}
      <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-8">
        <div className="max-w-3xl mx-auto">
          <label className="block text-white mb-3">Enter a token or narrative to analyze</label>
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
                placeholder="e.g., FET, AGIX, TAO, AI Agents..."
                className="w-full bg-[#0D0F14] border border-[#1E222D] rounded-lg pl-12 pr-4 py-4 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50"
              />
            </div>
            <button
              onClick={handleAnalyze}
              disabled={!query || analyzing}
              className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white hover:from-blue-600 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {analyzing ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
          
          {/* Suggestions */}
          <div className="flex items-center gap-2 mt-4">
            <span className="text-gray-400 text-sm">Quick analyze:</span>
            {['FET', 'AGIX', 'TAO AI Agents'].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => {
                  setQuery(suggestion);
                  setTimeout(() => {
                    setAnalyzing(true);
                    setTimeout(() => {
                      setAnalyzing(false);
                      setAnalyzed(true);
                    }, 1500);
                  }, 100);
                }}
                className="px-3 py-1 bg-[#0D0F14] border border-[#1E222D] rounded-lg text-gray-400 text-sm hover:border-blue-500/30 hover:text-blue-400 transition-all"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results */}
      {analyzing && (
        <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-12">
          <div className="max-w-md mx-auto text-center">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 border border-blue-500/30 flex items-center justify-center">
              <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <p className="text-white text-lg mb-2">Analyzing narrative...</p>
            <p className="text-gray-400 text-sm">Scanning social media posts, checking bot activity, and analyzing sentiment</p>
          </div>
        </div>
      )}

      {analyzed && !analyzing && (
        <>
          {/* Risk Card */}
          <div className="bg-gradient-to-br from-red-500/10 to-red-600/5 border border-red-500/30 rounded-xl p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-white text-xl mb-2">Analysis Results for "{query}"</h2>
                <p className="text-gray-400">Last updated: just now</p>
              </div>
              <RiskBadge risk="high" />
            </div>

            <div className="grid grid-cols-4 gap-4 mt-6">
              <div className="bg-[#11141A]/50 rounded-lg p-4 border border-red-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="w-4 h-4 text-red-400" />
                  <span className="text-red-400 text-sm">Risk Score</span>
                </div>
                <p className="text-white text-2xl">87/100</p>
              </div>

              <div className="bg-[#11141A]/50 rounded-lg p-4 border border-orange-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <Copy className="w-4 h-4 text-orange-400" />
                  <span className="text-orange-400 text-sm">Duplicate Posts</span>
                </div>
                <p className="text-white text-2xl">47%</p>
              </div>

              <div className="bg-[#11141A]/50 rounded-lg p-4 border border-purple-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <Bot className="w-4 h-4 text-purple-400" />
                  <span className="text-purple-400 text-sm">Bot Accounts</span>
                </div>
                <p className="text-white text-2xl">12</p>
              </div>

              <div className="bg-[#11141A]/50 rounded-lg p-4 border border-blue-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-4 h-4 text-blue-400" />
                  <span className="text-blue-400 text-sm">Total Posts</span>
                </div>
                <p className="text-white text-2xl">923</p>
              </div>
            </div>

            <div className="mt-6 p-4 bg-[#11141A]/50 rounded-lg border border-red-500/20">
              <h3 className="text-white mb-2">Summary</h3>
              <p className="text-gray-300 text-sm leading-relaxed">
                High risk AI token narrative detected. Analysis shows significant bot activity with 47% duplicate content across 923 posts. 
                Multiple bot clusters identified spreading identical messaging about FET AI agents and fake partnership announcements. Trust score is low at 42/100. 
                The narrative appears to be artificially amplified with coordinated inauthentic behavior targeting AI crypto investors.
              </p>
            </div>
          </div>

          {/* Charts and Lists */}
          <div className="grid grid-cols-2 gap-6">
            {/* Chart */}
            <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
              <h2 className="text-white text-lg mb-4">Duplicate Content Trend</h2>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={duplicateData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1E222D" />
                  <XAxis dataKey="time" stroke="#6B7280" style={{ fontSize: '12px' }} />
                  <YAxis stroke="#6B7280" style={{ fontSize: '12px' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#11141A',
                      border: '1px solid #1E222D',
                      borderRadius: '8px',
                      color: '#fff',
                    }}
                  />
                  <Bar dataKey="percentage" fill="#F97316" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Top Suspicious Posts */}
            <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
              <h2 className="text-white text-lg mb-4">Top Suspicious Posts</h2>
              <div className="space-y-3">
                {suspiciousPosts.map((post, index) => (
                  <div key={index} className="p-3 bg-[#0D0F14] rounded-lg border border-red-500/20">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-gray-600 to-gray-700 flex items-center justify-center text-white text-xs">
                          {post.user.charAt(1).toUpperCase()}
                        </div>
                        <span className="text-white text-sm">{post.user}</span>
                      </div>
                      <span className="inline-flex items-center gap-1 px-2 py-1 bg-red-500/20 text-red-400 rounded text-xs">
                        <Bot className="w-3 h-3" />
                        {post.botScore}
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm">{post.text}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Suspicious Accounts */}
          <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
            <h2 className="text-white text-lg mb-4">Suspicious Accounts</h2>
            <div className="grid grid-cols-2 gap-4">
              {suspiciousAccounts.map((account, index) => (
                <div key={index} className="p-4 bg-[#0D0F14] rounded-lg border border-red-500/20">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-red-600 to-red-700 flex items-center justify-center text-white">
                        {account.name.charAt(1).toUpperCase()}
                      </div>
                      <div>
                        <p className="text-white">{account.name}</p>
                        <p className="text-gray-400 text-xs">{account.followers} followers</p>
                      </div>
                    </div>
                    <span className="inline-flex items-center gap-1 px-2 py-1 bg-red-500/20 text-red-400 rounded text-xs">
                      <Bot className="w-3 h-3" />
                      {account.botScore}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-gray-400">
                    <span>Created {account.created}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}