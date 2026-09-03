import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar, TabType } from './components/Sidebar';
import { LegalAdvisorChat } from './components/LegalAdvisorChat';
import { DocumentSummarizer } from './components/DocumentSummarizer';
import { PrecedentFinder } from './components/PrecedentFinder';
import { LegalDrafter } from './components/LegalDrafter';
import { OutcomeAnalyzer } from './components/OutcomeAnalyzer';
import { CitationVerifier } from './components/CitationVerifier';
import { ComplianceVault } from './components/ComplianceVault';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('chat');
  const [currentLanguage, setCurrentLanguage] = useState<string>('en');
  const [userRole, setUserRole] = useState<string>('citizen');

  return (
    <div className="flex flex-col h-screen w-screen bg-[#0b1329] text-slate-100 overflow-hidden font-sans">
      {/* Top Navigation */}
      <Navbar
        currentLanguage={currentLanguage}
        onLanguageChange={setCurrentLanguage}
        userRole={userRole}
      />

      {/* Main App Workspace */}
      <div className="flex flex-1 overflow-hidden">
        {/* Navigation Sidebar */}
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

        {/* Tab Viewport */}
        <main className="flex-1 flex flex-col overflow-hidden bg-slate-950/40">
          {activeTab === 'chat' && <LegalAdvisorChat currentLanguage={currentLanguage} />}
          {activeTab === 'documents' && <DocumentSummarizer />}
          {activeTab === 'precedents' && <PrecedentFinder />}
          {activeTab === 'drafter' && <LegalDrafter />}
          {activeTab === 'outcomes' && <OutcomeAnalyzer />}
          {activeTab === 'citations' && <CitationVerifier />}
          {activeTab === 'compliance' && <ComplianceVault />}
        </main>
      </div>
    </div>
  );
};

export default App;
