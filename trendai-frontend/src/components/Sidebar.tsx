import { LayoutDashboard, FileText, AlertTriangle, Network, Shield } from 'lucide-react';

interface SidebarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

export function Sidebar({ currentPage, onNavigate }: SidebarProps) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'narratives', label: 'Narratives', icon: FileText },
    { id: 'suspicious-posts', label: 'Suspicious Posts', icon: AlertTriangle },
    { id: 'spread-map', label: 'Spread Map', icon: Network },
    { id: 'watchdog-agent', label: 'Watchdog Agent', icon: Shield },
  ];

  return (
    <div className="w-64 bg-[#11141A] border-r border-[#1E222D] flex flex-col">
      <div className="p-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-white">TrendAI</h1>
            <p className="text-xs text-gray-400">Narrative Watchdog</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 px-3">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-1 transition-all ${
                isActive
                  ? 'bg-gradient-to-r from-blue-500/20 to-purple-500/20 text-blue-400 border border-blue-500/30'
                  : 'text-gray-400 hover:text-white hover:bg-[#1E222D]'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-[#1E222D]">
        <div className="bg-gradient-to-br from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 rounded-full bg-green-500"></div>
            <span className="text-xs text-gray-400">System Status</span>
          </div>
          <p className="text-xs text-white">All monitors active</p>
        </div>
      </div>
    </div>
  );
}
