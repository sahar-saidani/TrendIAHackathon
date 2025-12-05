import React from "react";
import StatCard from "./StatCard";

export default function StatsCards() {
  return (
    <div className="grid grid-cols-3 gap-6">
      <StatCard
        title="Narrative Risk"
        value="Suspicious"
        hint="+12% from yesterday"
        tone="gold"
      />
      <StatCard
        title="Average Trust Score"
        value="67"
        hint="~5 pts from yesterday"
        tone="blue"
      />
      <StatCard
        title="Bot Activity Level"
        value="Medium"
        hint="~3 new clusters detected"
        tone="purple"
      />
    </div>
  );
}
