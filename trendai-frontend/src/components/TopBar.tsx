import React from "react";
import { Search, Bell, Settings } from "lucide-react";

export default function Topbar() {
  return (
    <div className="flex items-center justify-between">
      <div className="w-full max-w-[900px]">
        <div className="relative">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"/>
          <input
            className="w-full pl-10 pr-4 py-3 bg-[#0b0f17] border border-white/6 rounded-lg text-sm placeholder:text-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            placeholder="Analyze a token or narrative..."
          />
        </div>
      </div>

      <div className="flex items-center gap-4 ml-6">
        <button className="w-9 h-9 rounded-md bg-panel flex items-center justify-center border border-white/6">
          <Bell size={16} className="text-slate-300"/>
        </button>
        <button className="w-9 h-9 rounded-md bg-panel flex items-center justify-center border border-white/6">
          <Settings size={16} className="text-slate-300"/>
        </button>
        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-purple-600 to-pink-500 flex items-center justify-center text-sm font-semibold text-white">A</div>
      </div>
    </div>
  );
}
