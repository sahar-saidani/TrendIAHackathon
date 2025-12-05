import { Search, Bell, Settings } from 'lucide-react';

export function Header() {
  return (
    <header className="h-20 bg-[#11141A] border-b border-[#1E222D] flex items-center px-8">
      <div className="flex-1 max-w-2xl">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder=""
          />
        </div>
      </div>

      <div className="flex items-center gap-4 ml-8">
        <button className="p-2 rounded-lg hover:bg-[#1E222D] text-gray-400 hover:text-white transition-colors relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
        <button className="p-2 rounded-lg hover:bg-[#1E222D] text-gray-400 hover:text-white transition-colors">
          <Settings className="w-5 h-5" />
        </button>
        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white">
          <span>A</span>
        </div>
      </div>
    </header>
  );
}