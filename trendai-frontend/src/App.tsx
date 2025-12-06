import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { Dashboard } from './components/Dashboard';
import { NarrativeDetail } from './components/NarrativeDetail';
import { SuspiciousPosts } from './components/SuspiciousPosts';
import { SpreadMap } from './components/SpreadMap';
import { WatchdogAgent } from './components/WatchdogAgent';

export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [selectedNarrative, setSelectedNarrative] = useState('FET AI Agent Narrative');

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard onNarrativeClick={(narrative) => {
          setSelectedNarrative(narrative);
          setCurrentPage('narrative-detail');
        }} />;
      case 'narratives':
        return <NarrativeDetail narrative={selectedNarrative} />;
      case 'narrative-detail':
        return <NarrativeDetail narrative={selectedNarrative} />;
      case 'suspicious-posts':
        return <SuspiciousPosts />;
      case 'spread-map':
        return <SpreadMap />;
      case 'watchdog-agent':
        return <WatchdogAgent />;
      default:
        return <Dashboard onNarrativeClick={(narrative) => {
          setSelectedNarrative(narrative);
          setCurrentPage('narrative-detail');
        }} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0D0F14]">
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 p-8">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}