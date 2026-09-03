import React from 'react';
import {
  MessageSquareText,
  FileSearch,
  BookOpen,
  FileEdit,
  TrendingUp,
  CheckCircle2,
  ShieldCheck,
} from 'lucide-react';

export type TabType = 'chat' | 'documents' | 'precedents' | 'drafter' | 'outcomes' | 'citations' | 'compliance';

interface SidebarProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, onTabChange }) => {
  const menuItems = [
    {
      id: 'chat' as TabType,
      label: 'AI Legal Advisor',
      desc: 'Multilingual Q&A & IRAC Research',
      icon: MessageSquareText,
      badge: 'Core'
    },
    {
      id: 'documents' as TabType,
      label: 'Document Summarizer',
      desc: 'Clause Analysis & Risk Radar',
      icon: FileSearch,
      badge: 'CLAUSE'
    },
    {
      id: 'precedents' as TabType,
      label: 'Precedent Finder',
      desc: 'Supreme Court & High Court Judgments',
      icon: BookOpen,
      badge: 'RAG'
    },
    {
      id: 'drafter' as TabType,
      label: 'Structured Drafter',
      desc: 'Court Petitions & Notices',
      icon: FileEdit,
      badge: 'Templates'
    },
    {
      id: 'outcomes' as TabType,
      label: 'Case Outcome Predictor',
      desc: 'Bail & Relief Probability Gauge',
      icon: TrendingUp,
      badge: 'BNSS §479'
    },
    {
      id: 'citations' as TabType,
      label: 'Citation Verifier',
      desc: 'Zero-Trust Statute Cross-Check',
      icon: CheckCircle2,
      badge: 'Verified'
    },
    {
      id: 'compliance' as TabType,
      label: 'DPDP Security Vault',
      desc: 'Audit Trail & Retention Logs',
      icon: ShieldCheck,
      badge: 'Pillars'
    },
  ];

  return (
    <aside className="w-72 bg-slate-900/60 border-r border-slate-800 flex flex-col p-4 shrink-0">
      <div className="text-[11px] font-semibold tracking-wider text-slate-400 uppercase mb-3 px-2">
        Judicial Modules
      </div>
      <nav className="space-y-1.5 flex-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`w-full flex items-start gap-3 p-3 rounded-xl text-left transition-all duration-150 ${
                isActive
                  ? 'bg-amber-500/10 border border-amber-500/40 text-amber-300 shadow-md shadow-amber-500/5'
                  : 'text-slate-300 hover:bg-slate-800/80 hover:text-slate-100 border border-transparent'
              }`}
            >
              <div
                className={`p-2 rounded-lg mt-0.5 ${
                  isActive ? 'bg-amber-500/20 text-amber-400' : 'bg-slate-800 text-slate-400'
                }`}
              >
                <Icon className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium truncate">{item.label}</span>
                  <span
                    className={`text-[10px] px-1.5 py-0.5 rounded font-mono ${
                      isActive
                        ? 'bg-amber-400/20 text-amber-300'
                        : 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {item.badge}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 truncate mt-0.5">{item.desc}</p>
              </div>
            </button>
          );
        })}
      </nav>

      {/* Footer Banner */}
      <div className="mt-auto pt-4 border-t border-slate-800/80 px-2 text-[11px] text-slate-400">
        <div className="flex items-center justify-between font-mono">
          <span>Nyaya Core v2.0</span>
          <span className="text-emerald-400">FAISS Dense + BM25</span>
        </div>
        <p className="mt-1 text-[10px] leading-relaxed text-slate-400">
          Statutory grounding under BNS, BNSS, BSA 2023 & Constitution of India.
        </p>
      </div>
    </aside>
  );
};
