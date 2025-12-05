import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid } from "recharts";

const data = [
  { time: "00:00", BTC: 300, DOGE: 200, ETH: 250, SOL: 180 },
  { time: "04:00", BTC: 280, DOGE: 220, ETH: 260, SOL: 190 },
  { time: "08:00", BTC: 350, DOGE: 300, ETH: 280, SOL: 230 },
  { time: "12:00", BTC: 520, DOGE: 420, ETH: 330, SOL: 260 },
  { time: "16:00", BTC: 700, DOGE: 500, ETH: 420, SOL: 300 },
  { time: "20:00", BTC: 820, DOGE: 540, ETH: 460, SOL: 320 },
  { time: "23:59", BTC: 770, DOGE: 500, ETH: 450, SOL: 310 }
];

export default function NarrativeChart() {
  return (
    <div style={{ height: 360 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 30, left: 8, bottom: 0 }}>
          <CartesianGrid stroke="rgba(255,255,255,0.03)" />
          <XAxis dataKey="time" tick={{ fill: "#94a3b8" }} axisLine={{ stroke: "rgba(255,255,255,0.04)" }} />
          <YAxis tick={{ fill: "#94a3b8" }} axisLine={{ stroke: "rgba(255,255,255,0.04)" }} />
          <Tooltip wrapperStyle={{ background: "#0b1220", border: "1px solid rgba(255,255,255,0.06)" }} />
          <Legend wrapperStyle={{ color: "#94a3b8" }} />
          <Line type="monotone" dataKey="BTC" stroke="#ef4444" strokeWidth={2.2} dot={{ r: 3 }} />
          <Line type="monotone" dataKey="DOGE" stroke="#f97316" strokeWidth={2.2} dot={{ r: 3 }} />
          <Line type="monotone" dataKey="ETH" stroke="#60a5fa" strokeWidth={2.2} dot={{ r: 3 }} />
          <Line type="monotone" dataKey="SOL" stroke="#34d399" strokeWidth={2.2} dot={{ r: 3 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
