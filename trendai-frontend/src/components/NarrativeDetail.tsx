import { RiskBadge } from './RiskBadge';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { AlertTriangle, Copy, Bot, Activity } from 'lucide-react';

interface NarrativeDetailProps {
  narrative: string;
}

export function NarrativeDetail({ narrative }: NarrativeDetailProps) {
  const timelineData = [
    { time: '6h ago', posts: 145 },
    { time: '5h ago', posts: 234 },
    { time: '4h ago', posts: 389 },
    { time: '3h ago', posts: 512 },
    { time: '2h ago', posts: 678 },
    { time: '1h ago', posts: 845 },
    { time: 'Now', posts: 923 },
  ];

  const trustScoreData = [
    { range: '0-20', count: 234 },
    { range: '21-40', count: 456 },
    { range: '41-60', count: 678 },
    { range: '61-80', count: 345 },
    { range: '81-100', count: 123 },
  ];

  const suspiciousPosts = [
    {
      user: '@ai_crypto_whale',
      text: 'FET is the next 100x! AI agents will dominate 2025! 🚀🤖 Get in now!',
      similarity: 94,
      botScore: 87,
      timestamp: '2 hours ago',
    },
    {
      user: '@fetch_ai_news',
      text: 'FET is the next 100x! AI agents will dominate 2025! 🚀🤖 Get in now!',
      similarity: 94,
      botScore: 91,
      timestamp: '2 hours ago',
    },
    {
      user: '@ai_token_insider',
      text: 'FET partnership with OpenAI confirmed! This will moon! 🚀🚀🚀',
      similarity: 78,
      botScore: 83,
      timestamp: '3 hours ago',
    },
    {
      user: '@crypto_ai_guru',
      text: 'FET is the next 100x! AI agents will dominate 2025! 🚀🤖 Get in now!',
      similarity: 94,
      botScore: 89,
      timestamp: '3 hours ago',
    },
    {
      user: '@ai_blockchain_king',
      text: 'Major AI announcement coming for FET. Google just hinted at integration!',
      similarity: 67,
      botScore: 72,
      timestamp: '4 hours ago',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-white text-3xl mb-2">Narrative Analysis</h1>
          <p className="text-gray-400 text-xl">{narrative}</p>
        </div>
        <RiskBadge risk="high" />
      </div>

      {/* Key Factors Panel */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-red-500/20 to-red-600/10 border border-red-500/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <Copy className="w-4 h-4 text-red-400" />
            <span className="text-red-400 text-sm">Duplicate Posts</span>
          </div>
          <p className="text-white text-2xl">47%</p>
          <p className="text-red-400 text-xs mt-1">Very High</p>
        </div>

        <div className="bg-gradient-to-br from-orange-500/20 to-orange-600/10 border border-orange-500/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <Bot className="w-4 h-4 text-orange-400" />
            <span className="text-orange-400 text-sm">Bot Clusters</span>
          </div>
          <p className="text-white text-2xl">8</p>
          <p className="text-orange-400 text-xs mt-1">High Activity</p>
        </div>

        <div className="bg-gradient-to-br from-yellow-500/20 to-yellow-600/10 border border-yellow-500/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-4 h-4 text-yellow-400" />
            <span className="text-yellow-400 text-sm">Fake News Indicators</span>
          </div>
          <p className="text-white text-2xl">23</p>
          <p className="text-yellow-400 text-xs mt-1">Moderate Risk</p>
        </div>

        <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/10 border border-blue-500/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <Activity className="w-4 h-4 text-blue-400" />
            <span className="text-blue-400 text-sm">Avg Trust Score</span>
          </div>
          <p className="text-white text-2xl">42</p>
          <p className="text-blue-400 text-xs mt-1">Below Average</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
          <h2 className="text-white text-lg mb-4">Post Volume Timeline</h2>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={timelineData}>
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
              <Line type="monotone" dataKey="posts" stroke="#EF4444" strokeWidth={2} dot={{ fill: '#EF4444', r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
          <h2 className="text-white text-lg mb-4">Trust Score Distribution</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={trustScoreData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1E222D" />
              <XAxis dataKey="range" stroke="#6B7280" style={{ fontSize: '12px' }} />
              <YAxis stroke="#6B7280" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#11141A',
                  border: '1px solid #1E222D',
                  borderRadius: '8px',
                  color: '#fff',
                }}
              />
              <Bar dataKey="count" fill="#8B5CF6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Suspicious Posts Table */}
      <div className="bg-[#11141A] border border-[#1E222D] rounded-xl p-6">
        <h2 className="text-white text-lg mb-4">Suspicious Posts</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-[#1E222D]">
                <th className="text-left text-gray-400 text-sm pb-3 pr-4">User</th>
                <th className="text-left text-gray-400 text-sm pb-3 pr-4">Post Content</th>
                <th className="text-left text-gray-400 text-sm pb-3 pr-4">Similarity %</th>
                <th className="text-left text-gray-400 text-sm pb-3 pr-4">Bot Score</th>
                <th className="text-left text-gray-400 text-sm pb-3">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {suspiciousPosts.map((post, index) => {
                const getSeverityColor = (score: number) => {
                  if (score >= 85) return 'bg-red-500/10 border-red-500/30';
                  if (score >= 70) return 'bg-orange-500/10 border-orange-500/30';
                  return 'bg-yellow-500/10 border-yellow-500/30';
                };

                return (
                  <tr key={index} className={`border-b border-[#1E222D] ${getSeverityColor(post.botScore)}`}>
                    <td className="py-4 pr-4">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-gray-600 to-gray-700 flex items-center justify-center text-white text-xs">
                          {post.user.charAt(1).toUpperCase()}
                        </div>
                        <span className="text-white text-sm">{post.user}</span>
                      </div>
                    </td>
                    <td className="py-4 pr-4 max-w-md">
                      <p className="text-gray-300 text-sm truncate" title={post.text}>
                        {post.text}
                      </p>
                    </td>
                    <td className="py-4 pr-4">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-[#0D0F14] rounded-full h-2 max-w-[60px]">
                          <div
                            className="bg-red-500 h-2 rounded-full"
                            style={{ width: `${post.similarity}%` }}
                          ></div>
                        </div>
                        <span className="text-red-400 text-sm">{post.similarity}%</span>
                      </div>
                    </td>
                    <td className="py-4 pr-4">
                      <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs ${
                        post.botScore >= 85 ? 'bg-red-500/20 text-red-400' :
                        post.botScore >= 70 ? 'bg-orange-500/20 text-orange-400' :
                        'bg-yellow-500/20 text-yellow-400'
                      }`}>
                        <Bot className="w-3 h-3" />
                        {post.botScore}
                      </span>
                    </td>
                    <td className="py-4">
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