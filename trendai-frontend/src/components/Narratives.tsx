import React from "react";
import { AlertTriangle, Bot, Copy, BarChart3 } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function Narratives() {
  /* Sample Data */
  const volumeData = [
    { time: "6h", value: 120 },
    { time: "5h", value: 180 },
    { time: "4h", value: 330 },
    { time: "3h", value: 420 },
    { time: "2h", value: 610 },
    { time: "1h", value: 780 },
    { time: "Now", value: 910 },
  ];

  const trustData = [
    { score: "0-20", count: 150 },
    { score: "21-40", count: 300 },
    { score: "41-60", count: 520 },
    { score: "61-80", count: 400 },
    { score: "81-100", count: 120 },
  ];

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Narrative Analysis</h1>
          <p className="text-sm text-muted">Bitcoin ETF Approval</p>
        </div>

        <div className="px-4 py-2 rounded-md bg-red-900/40 text-red-400 font-medium">
          High Risk
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <StatCard
          icon={<Copy size={18} />}
          title="Duplicate Posts"
          value="47%"
          risk="Very High"
          color="from-red-800 to-red-600"
        />

        <StatCard
          icon={<Bot size={18} />}
          title="Bot Clusters"
          value="8"
          risk="High Activity"
          color="from-orange-800 to-orange-600"
        />

        <StatCard
          icon={<AlertTriangle size={18} />}
          title="Fake News Indicators"
          value="23"
          risk="Moderate Risk"
          color="from-yellow-700 to-yellow-500"
        />

        <StatCard
          icon={<BarChart3 size={18} />}
          title="Avg Trust Score"
          value="42"
          risk="Below Average"
          color="from-blue-800 to-blue-600"
        />
      </div>

      {/* Graphs */}
      <div className="grid grid-cols-2 gap-4">
        {/* Line Chart */}
        <div className="bg-panel p-5 rounded-lg">
          <h2 className="font-medium mb-3">Post Volume Timeline</h2>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={volumeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis dataKey="time" stroke="#ccc" />
                <YAxis stroke="#ccc" />
                <Tooltip contentStyle={{ background: "#1f2937", border: "none" }} />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#ef4444"
                  strokeWidth={2}
                  dot={{ fill: "#ef4444", r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bar Chart */}
        <div className="bg-panel p-5 rounded-lg">
          <h2 className="font-medium mb-3">Trust Score Distribution</h2>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={trustData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis dataKey="score" stroke="#ccc" />
                <YAxis stroke="#ccc" />
                <Tooltip contentStyle={{ background: "#1f2937", border: "none" }} />
                <Bar dataKey="count" fill="#a78bfa" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Suspicious Posts */}
      <div className="bg-panel p-5 rounded-lg">
        <h2 className="font-medium mb-4">Suspicious Posts</h2>

        <div className="space-y-3">
          {[
            { user: "@crypto_whale_88", text: "DOGE to the moon!", sim: 94, bot: 87, time: "2 hours ago" },
            { user: "@moon_hunter_2024", text: "DOGE to the moon!", sim: 94, bot: 91, time: "2 hours ago" },
            { user: "@invest_guru_pro", text: "DOGE pumping hard!", sim: 78, bot: 83, time: "3 hours ago" },
          ].map((p, i) => (
            <PostRow key={i} {...p} />
          ))}
        </div>
      </div>
    </div>
  );
}

/* Components */

function StatCard({ icon, title, value, risk, color }: any) {
  return (
    <div className={`p-4 rounded-lg bg-gradient-to-br ${color} text-white`}>
      <div className="flex items-center gap-2 mb-3">
        {icon}
        <span className="text-sm">{title}</span>
      </div>
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-xs opacity-70">{risk}</div>
    </div>
  );
}

function PostRow({ user, text, sim, bot, time }: any) {
  return (
    <div className="flex justify-between items-center bg-gray-800/30 p-3 rounded-md">
      <div>
        <div className="font-medium">{user}</div>
        <div className="text-sm text-muted">{text}</div>
      </div>

      <div className="flex items-center gap-6">
        <div className="text-sm text-red-400">Similarity {sim}%</div>
        <div className="text-sm text-orange-400">Bot Score {bot}</div>
        <div className="text-xs text-muted">{time}</div>
      </div>
    </div>
  );
}
