import React from "react";

export default function StatCard({ title, value, hint, tone = "blue" }: { title: string; value: string | number; hint?: string; tone?: "blue" | "gold" | "purple" }) {
  const toneColor = tone === "gold" ? "from-yellow-700 to-yellow-600" : tone === "purple" ? "from-purple-700 to-purple-500" : "from-blue-700 to-blue-500";
  return (
    <div className="rounded-xl p-6" style={{ background: "linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01))" }}>
      <div className={`w-full rounded-lg p-4 bg-gradient-to-br ${toneColor} text-white/95`}>
        <div className="text-xs">{title}</div>
        <div className="text-2xl font-semibold mt-2">{value}</div>
        {hint && <div className="text-sm text-white/70 mt-1">{hint}</div>}
      </div>
    </div>
  );
}
