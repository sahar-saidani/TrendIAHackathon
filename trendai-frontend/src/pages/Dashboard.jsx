

export default function Dashboard() {
  const tokens = ["BTC","ETH","SOL","DOGE","PEPE","SHIB","ARB","MATIC","AVAX","LINK"];

  const metrics = [
    { metric: "Bot Activity", values: ["low","medium","high","high","low","medium","low","medium","high","low"] },
    { metric: "Duplicate Posts", values: ["medium","high","high","medium","low","low","medium","high","medium","low"] },
    { metric: "Viral Spread", values: ["low","low","medium","high","low","medium","low","medium","high","low"] },
  ];

  const timelineData = [
    { time: "00:00", BTC: 200, ETH: 150, DOGE: 400 },
    { time: "06:00", BTC: 220, ETH: 180, DOGE: 450 },
    { time: "12:00", BTC: 280, ETH: 200, DOGE: 600 },
    { time: "18:00", BTC: 300, ETH: 210, DOGE: 750 },
    { time: "23:59", BTC: 280, ETH: 190, DOGE: 700 },
  ];

  return (
    <div className="flex">
      <Sidebar/>

      <div className="flex-1 bg-[#0D0F14] min-h-screen text-white">
        <Navbar/>

        <div className="p-8">

          <h1 className="text-2xl font-semibold">Dashboard</h1>
          <p className="text-gray-400 mb-6">Real-time crypto narrative monitoring and analysis</p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <KpiCard title="Narrative Risk" value="Suspicious" trend="+12% from yesterday"
              gradient="bg-gradient-to-br from-yellow-600 to-yellow-800"/>
            <KpiCard title="Average Trust Score" value="67" trend="+5 pts from yesterday"
              gradient="bg-gradient-to-br from-blue-700 to-blue-900"/>
            <KpiCard title="Bot Activity Level" value="Medium" trend="3 new clusters detected"
              gradient="bg-gradient-to-br from-purple-700 to-purple-900"/>
          </div>

          <Heatmap tokens={tokens} metrics={metrics}/>
          <TimelineChart data={timelineData}/>

        </div>
      </div>
    </div>
  );
}
