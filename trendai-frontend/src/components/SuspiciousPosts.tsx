import { useState } from 'react';
import { Filter, Bot, Copy, AlertTriangle } from 'lucide-react';

export function SuspiciousPosts() {
  const [activeFilter, setActiveFilter] = useState('all');

  const posts = [
    {
      account: '@ai_moon_shots',
      credibility: 23,
      content: 'BREAKING: Google announces partnership with FET AI agents! Buy now before it\'s too late! 🚀🤖',
      botScore: 94,
      similarity: 97,
      timestamp: '5 min ago',
      severity: 'high',
    },
    {
      account: '@fetch_insider_news',
      credibility: 18,
      content: 'BREAKING: Google announces partnership with FET AI agents! Buy now before it\'s too late! 🚀🤖',
      botScore: 96,
      similarity: 97,
      timestamp: '7 min ago',
      severity: 'high',
    },
    {
      account: '@ai_whale_alerts',
      credibility: 31,
      content: 'Sam Altman just tweeted about AGIX integration with ChatGPT-5!',
      botScore: 88,
      similarity: 84,
      timestamp: '12 min ago',
      severity: 'high',
    },
    {
      account: '@ai_trade_master',
      credibility: 45,
      content: 'My AI predicts TAO will 50x in 48 hours with Bittensor upgrade!',
      botScore: 79,
      similarity: 72,
      timestamp: '18 min ago',
      severity: 'medium',
    },
    {
      account: '@render_network_daily',
      credibility: 52,
      content: 'RNDR GPU rendering partnership with NVIDIA confirmed for Q1 2025.',
      botScore: 71,
      similarity: 58,
      timestamp: '23 min ago',
      severity: 'medium',
    },
    {
      account: '@invest_ai_crypto',
      credibility: 38,
      content: 'BREAKING: Google announces partnership with FET AI agents! Buy now before it\'s too late! 🚀🤖',
      botScore: 92,
      similarity: 97,
      timestamp: '31 min ago',
      severity: 'high',
    },
    {
      account: '@ai_gem_hunter',
      credibility: 41,
      content: 'Just discovered PAAL AI! 1000x potential with LLM integration! Link in bio!',
      botScore: 85,
      similarity: 79,
      timestamp: '45 min ago',
      severity: 'high',
    },
    {
      account: '@ocean_protocol_pro',
      credibility: 29,
      content: 'OCEAN data marketplace is the next big thing! AI data economy starts here!',
      botScore: 76,
      similarity: 65,
      timestamp: '1 hour ago',
      severity: 'medium',
    },
  ];

  const filteredPosts = posts.filter(post => {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'high-bot') return post.botScore >= 85;
    if (activeFilter === 'duplicate') return post.similarity >= 90;
    if (activeFilter === 'fake-news') return post.credibility < 40;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-white text-3xl mb-2">Suspicious Posts</h1>
          <p className="text-gray-400">Detected posts with high risk indicators</p>
        </div>
        <div className="flex items-center gap-3">
          <Filter className="w-5 h-5 text-gray-400" />
          <button
            onClick={() => setActiveFilter('all')}
            className={`px-4 py-2 rounded-lg text-sm transition-all ${
              activeFilter === 'all'
                ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                : 'bg-[#11141A] text-gray-400 border border-[#1E222D] hover:border-blue-500/30'
            }`}
          >
            All Posts
          </button>
          <button
            onClick={() => setActiveFilter('high-bot')}
            className={`px-4 py-2 rounded-lg text-sm transition-all ${
              activeFilter === 'high-bot'
                ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                : 'bg-[#11141A] text-gray-400 border border-[#1E222D] hover:border-red-500/30'
            }`}
          >
            High Bot Score
          </button>
          <button
            onClick={() => setActiveFilter('duplicate')}
            className={`px-4 py-2 rounded-lg text-sm transition-all ${
              activeFilter === 'duplicate'
                ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
                : 'bg-[#11141A] text-gray-400 border border-[#1E222D] hover:border-orange-500/30'
            }`}
          >
            Duplicate Text
          </button>
          <button
            onClick={() => setActiveFilter('fake-news')}
            className={`px-4 py-2 rounded-lg text-sm transition-all ${
              activeFilter === 'fake-news'
                ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                : 'bg-[#11141A] text-gray-400 border border-[#1E222D] hover:border-yellow-500/30'
            }`}
          >
            Fake News Claims
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-4">
          <p className="text-gray-400 text-sm mb-1">Total Flagged</p>
          <p className="text-white text-2xl">{posts.length}</p>
        </div>
        <div className="bg-[#11141A] border border-red-500/30 rounded-xl p-4">
          <p className="text-gray-400 text-sm mb-1">High Risk</p>
          <p className="text-red-400 text-2xl">{posts.filter(p => p.severity === 'high').length}</p>
        </div>
        <div className="bg-[#11141A] border border-orange-500/30 rounded-xl p-4">
          <p className="text-gray-400 text-sm mb-1">Duplicate Content</p>
          <p className="text-orange-400 text-2xl">{posts.filter(p => p.similarity >= 90).length}</p>
        </div>
        <div className="bg-[#11141A] border border-purple-500/30 rounded-xl p-4">
          <p className="text-gray-400 text-sm mb-1">Bot Accounts</p>
          <p className="text-purple-400 text-2xl">{posts.filter(p => p.botScore >= 85).length}</p>
        </div>
      </div>

      {/* Table */}
      <div className="bg-[#11141A] border border-[#1E222D] rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-[#0D0F14]">
              <tr className="border-b border-[#1E222D]">
                <th className="text-left text-gray-400 text-sm p-4">Account</th>
                <th className="text-left text-gray-400 text-sm p-4">Credibility Score</th>
                <th className="text-left text-gray-400 text-sm p-4">Post Content</th>
                <th className="text-left text-gray-400 text-sm p-4">Bot Score</th>
                <th className="text-left text-gray-400 text-sm p-4">Duplicate Similarity</th>
                <th className="text-left text-gray-400 text-sm p-4">Post Time</th>
              </tr>
            </thead>
            <tbody>
              {filteredPosts.map((post, index) => {
                const rowColor = post.severity === 'high' 
                  ? 'bg-red-500/5 border-l-4 border-l-red-500' 
                  : 'bg-orange-500/5 border-l-4 border-l-orange-500';

                return (
                  <tr key={index} className={`border-b border-[#1E222D] ${rowColor} hover:bg-[#0D0F14]/50`}>
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-600 to-gray-700 flex items-center justify-center text-white">
                          {post.account.charAt(1).toUpperCase()}
                        </div>
                        <span className="text-white text-sm">{post.account}</span>
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-[#0D0F14] rounded-full h-2 max-w-[80px]">
                          <div
                            className={`h-2 rounded-full ${
                              post.credibility >= 50 ? 'bg-green-500' :
                              post.credibility >= 30 ? 'bg-yellow-500' :
                              'bg-red-500'
                            }`}
                            style={{ width: `${post.credibility}%` }}
                          ></div>
                        </div>
                        <span className={`text-sm ${
                          post.credibility >= 50 ? 'text-green-400' :
                          post.credibility >= 30 ? 'text-yellow-400' :
                          'text-red-400'
                        }`}>
                          {post.credibility}
                        </span>
                      </div>
                    </td>
                    <td className="p-4 max-w-md">
                      <div className="flex items-start gap-2">
                        {post.similarity >= 90 && <Copy className="w-4 h-4 text-orange-400 mt-0.5 flex-shrink-0" />}
                        {post.credibility < 40 && <AlertTriangle className="w-4 h-4 text-yellow-400 mt-0.5 flex-shrink-0" />}
                        <p className="text-gray-300 text-sm line-clamp-2" title={post.content}>
                          {post.content}
                        </p>
                      </div>
                    </td>
                    <td className="p-4">
                      <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-lg text-sm ${
                        post.botScore >= 85 ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                        'bg-orange-500/20 text-orange-400 border border-orange-500/30'
                      }`}>
                        <Bot className="w-4 h-4" />
                        {post.botScore}
                      </span>
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-[#0D0F14] rounded-full h-2 max-w-[80px]">
                          <div
                            className="bg-orange-500 h-2 rounded-full"
                            style={{ width: `${post.similarity}%` }}
                          ></div>
                        </div>
                        <span className="text-orange-400 text-sm">{post.similarity}%</span>
                      </div>
                    </td>
                    <td className="p-4">
                      <span className="text-gray-400 text-sm">{post.timestamp}</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}