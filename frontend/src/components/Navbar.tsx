import React from 'react';
import { Scale, Globe, ShieldCheck, UserCheck } from 'lucide-react';

interface NavbarProps {
  currentLanguage: string;
  onLanguageChange: (lang: string) => void;
  userRole: string;
}

export const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'hi', name: 'हिन्दी (Hindi)' },
  { code: 'ta', name: 'தமிழ் (Tamil)' },
  { code: 'te', name: 'తెలుగు (Telugu)' },
  { code: 'bn', name: 'বাংলা (Bengali)' },
  { code: 'mr', name: 'मराठी (Marathi)' },
  { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
  { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
];

export const Navbar: React.FC<NavbarProps> = ({ currentLanguage, onLanguageChange, userRole }) => {
  return (
    <header className="bg-slate-900/90 backdrop-blur-md border-b border-slate-800 sticky top-0 z-50 px-6 py-3.5">
      <div className="flex items-center justify-between max-w-7xl mx-auto">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 to-yellow-300 p-0.5 shadow-lg shadow-yellow-500/20">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Scale className="w-5 h-5 text-amber-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-amber-200 via-yellow-400 to-amber-500 bg-clip-text text-transparent">
                NYAYA AI
              </span>
              <span className="text-xs px-2 py-0.5 bg-amber-500/10 border border-amber-500/30 text-amber-300 rounded-full font-medium">
                LEGAL ADVISOR
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">
              Multilingual Indian Judicial AI Platform • BNS, BNSS & BSA 2023 Ready
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          {/* DPDP Compliance Pill */}
          <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>DPDP 2025 Compliant</span>
          </div>

          {/* Language Selector */}
          <div className="flex items-center gap-1.5 bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 hover:border-slate-600 transition-colors">
            <Globe className="w-4 h-4 text-amber-400" />
            <select
              value={currentLanguage}
              onChange={(e) => onLanguageChange(e.target.value)}
              className="bg-transparent text-slate-200 focus:outline-none cursor-pointer pr-1"
            >
              {LANGUAGES.map((l) => (
                <option key={l.code} value={l.code} className="bg-slate-900 text-slate-200">
                  {l.name}
                </option>
              ))}
            </select>
          </div>

          {/* Role Pill */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-xs font-medium text-slate-300">
            <UserCheck className="w-3.5 h-3.5 text-blue-400" />
            <span className="capitalize">{userRole}</span>
          </div>
        </div>
      </div>
    </header>
  );
};
