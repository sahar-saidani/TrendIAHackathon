import { Search } from "lucide-react";

export default function Navbar() {
  return (
    <div className="w-full bg-[#11141A] border-b border-gray-800 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center w-full max-w-xl bg-[#0D0F14] border border-gray-700 px-4 py-2 rounded-lg">
        <Search className="text-gray-400 mr-2"/>
        <input 
          placeholder="Analyze a token or narrative..."
          className="w-full bg-transparent outline-none text-gray-300"
        />
      </div>

      <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-white ml-4 font-semibold">
        A
      </div>
    </div>
  );
}
