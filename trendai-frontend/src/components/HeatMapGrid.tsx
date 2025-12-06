import React from "react";

const tokens = ["BTC","ETH","SOL","DOGE","PEPE","SHIB","ARB","MATIC","AVAX","LINK","UNI","AAVE"];
const metrics = ["Bot Activity","Duplicate Posts","Viral Spread"];

const fixedSample: Record<string, ("low"|"medium"|"high")[]> = {
  BTC: ["low","medium","low"],
  ETH: ["low","low","low"],
  SOL: ["medium","medium","low"],
  DOGE: ["high","high","high"],
  PEPE: ["high","high","high"],
  SHIB: ["high","high","high"],
  ARB: ["medium","medium","medium"],
  MATIC: ["low","low","low"],
  AVAX: ["medium","medium","medium"],
  LINK: ["low","high","medium"],
  UNI: ["low","low","low"],
  AAVE: ["low","low","low"]
};

function cellClass(state: "low"|"medium"|"high") {
  if(state === "low") return "bg-[#1f7a4c]";       // green-ish
  if(state === "medium") return "bg-[#b5801a]";    // gold-ish
  return "bg-[#8b1f2d]";                           // red-ish
}

export default function HeatmapGrid() {
  return (
    <div className="text-slate-200">
      <div className="flex justify-end mb-4">
        <select className="bg-[#0b0f17] border border-white/6 px-3 py-1 rounded-md text-sm text-slate-300">
          <option>Last 24 hours</option>
          <option>Last 7 days</option>
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full table-fixed">
          <thead>
            <tr className="text-left text-sm text-slate-400">
              <th className="w-48 py-2"></th>
              {tokens.map(t => <th key={t} className="px-2 py-2">{t}</th>)}
            </tr>
          </thead>
          <tbody>
            {metrics.map((m, rowIndex) => (
              <tr key={m} className="align-middle">
                <td className="py-3 text-sm text-slate-300">{m}</td>
                {tokens.map(t => {
                  const state = fixedSample[t][rowIndex] ?? "low";
                  return (
                    <td key={t + m} className="p-2">
                      <div className={`${cellClass(state)} w-12 h-8 rounded-md shadow-inner border border-white/6`}></div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex items-center gap-6 mt-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-sm bg-[#1f7a4c]"></div>
          <div className="text-sm text-slate-400">Low</div>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-sm bg-[#b5801a]"></div>
          <div className="text-sm text-slate-400">Medium</div>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-sm bg-[#8b1f2d]"></div>
          <div className="text-sm text-slate-400">High</div>
        </div>
      </div>
    </div>
  );
}
