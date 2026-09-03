import React, { useState } from 'react';
import {
  Send,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  BookOpen,
  Copy,
  Check,
  Languages,
  Scale,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import api from '../api/client';

interface LegalAdvisorChatProps {
  currentLanguage: string;
}

export const LegalAdvisorChat: React.FC<LegalAdvisorChatProps> = ({ currentLanguage }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);
  const [copied, setCopied] = useState(false);
  const [showSources, setShowSources] = useState(true);

  const samplePrompts = [
    'What is the punishment for theft under the new BNS code?',
    'चोरी की सजा क्या है और जमानत कैसे मिलेगी?',
    'Does the right to privacy fall under Article 21 of the Constitution?',
    'What are the mandatory bail guidelines under Satender Kumar Antil v. CBI?',
    'What are the mandatory security safeguards under DPDP Act 2023?',
  ];

  const handleSend = async (textToSend?: string) => {
    const text = textToSend || query;
    if (!text.trim()) return;

    setLoading(true);
    setResponse(null);

    try {
      const res = await api.post('/qa/query', {
        query: text,
        target_language: currentLanguage,
      });
      setResponse(res.data);
    } catch (err: any) {
      console.error(err);
      alert('Failed to process legal query. Ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (!response) return;
    navigator.clipboard.writeText(response.answer);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-65px)] overflow-hidden bg-slate-950">
      {/* Top Bar */}
      <div className="border-b border-slate-800/80 px-6 py-3 bg-slate-900/40 flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-slate-100 flex items-center gap-2">
            <Scale className="w-4 h-4 text-amber-400" />
            AI Legal Consultation & Grounded IRAC Research
          </h2>
          <p className="text-xs text-slate-400">
            Authoritative legal reasoning with zero-trust citation verification & BNS/IPC cross-mapping.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Target Output:</span>
          <span className="text-xs px-2 py-0.5 rounded bg-slate-800 border border-slate-700 font-mono text-amber-300 uppercase">
            {currentLanguage}
          </span>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 max-w-5xl mx-auto w-full">
        {/* Sample Prompts when empty */}
        {!response && !loading && (
          <div className="py-8 text-center space-y-6">
            <div className="w-16 h-16 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center mx-auto text-amber-400 shadow-xl shadow-amber-500/5">
              <Sparkles className="w-8 h-8" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-slate-100 tracking-tight">
                Ask Any Indian Legal Question
              </h3>
              <p className="text-sm text-slate-400 max-w-lg mx-auto mt-1">
                Enter your query in English, Hindi, Tamil, Telugu, Marathi, etc. The platform retrieves relevant statutes, verifies citations, and produces a complete IRAC legal memorandum.
              </p>
            </div>

            <div className="grid sm:grid-cols-2 gap-2.5 max-w-2xl mx-auto text-left">
              {samplePrompts.map((prompt, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setQuery(prompt);
                    handleSend(prompt);
                  }}
                  className="p-3 bg-slate-900 border border-slate-800 hover:border-amber-500/50 hover:bg-slate-800/80 rounded-xl text-xs text-slate-300 transition-all flex items-start gap-2.5 group"
                >
                  <span className="text-amber-400 font-mono font-bold mt-0.5 group-hover:translate-x-0.5 transition-transform">
                    →
                  </span>
                  <span>{prompt}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Loading Spinner */}
        {loading && (
          <div className="p-12 text-center space-y-4">
            <div className="inline-block w-8 h-8 border-2 border-amber-400 border-t-transparent rounded-full animate-spin" />
            <div className="space-y-1">
              <p className="text-sm font-medium text-slate-200">
                Executing Hybrid Retrieval & Citation Verification...
              </p>
              <p className="text-xs text-slate-400">
                Scanning FAISS dense vector space + BM25 statutory indices for BNS 2023 & SC Precedents
              </p>
            </div>
          </div>
        )}

        {/* Legal Response Presentation */}
        {response && !loading && (
          <div className="space-y-5 animate-in fade-in duration-200">
            {/* Query Header & Metadata Bar */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center justify-between gap-3 shadow-md">
              <div className="space-y-1">
                <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">User Query:</span>
                <p className="text-sm font-medium text-amber-200">"{response.query}"</p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <div className="flex items-center gap-1 text-xs px-2.5 py-1 bg-slate-800 border border-slate-700 rounded-md text-slate-300">
                  <Languages className="w-3.5 h-3.5 text-amber-400" />
                  <span>{response.detected_language_name}</span>
                </div>

                <div className="text-xs px-2.5 py-1 bg-blue-500/10 border border-blue-500/30 text-blue-400 rounded-md font-mono">
                  Intent: {response.intent} ({Math.round(response.intent_confidence * 100)}%)
                </div>

                {response.verification_summary.is_verified ? (
                  <div className="flex items-center gap-1 text-xs px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-md font-medium">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Citations Verified ({response.verification_summary.verification_rate}%)</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-1 text-xs px-2.5 py-1 bg-amber-500/10 border border-amber-500/30 text-amber-400 rounded-md font-medium">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    <span>Review Citations</span>
                  </div>
                )}
              </div>
            </div>

            {/* Extracted Legal Entities */}
            {response.entities && (
              <div className="flex flex-wrap items-center gap-1.5 px-1 text-xs">
                <span className="text-slate-400 font-medium">Extracted Legal Entities:</span>
                {response.entities.statutes?.map((s: string, i: number) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-purple-500/10 border border-purple-500/30 text-purple-300 font-mono text-[11px]">
                    {s}
                  </span>
                ))}
                {response.entities.provisions?.map((p: string, i: number) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-300 font-mono text-[11px]">
                    {p}
                  </span>
                ))}
                {response.entities.offences?.map((o: string, i: number) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-red-500/10 border border-red-500/30 text-red-300 font-mono text-[11px]">
                    {o}
                  </span>
                ))}
              </div>
            )}

            {/* IRAC Memorandum Content */}
            <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-amber-400" />
                  <span className="text-sm font-bold tracking-wide uppercase text-amber-300">
                    Authoritative Legal Memorandum
                  </span>
                </div>
                <button
                  onClick={copyToClipboard}
                  className="flex items-center gap-1.5 px-3 py-1 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-xs text-slate-200 transition-colors"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
                  <span>{copied ? 'Copied' : 'Copy Memorandum'}</span>
                </button>
              </div>

              {/* Formatted Markdown/Text */}
              <div className="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap font-sans">
                {response.answer}
              </div>
            </div>

            {/* Zero-Trust Citation Verification Breakdown */}
            {response.citations && response.citations.length > 0 && (
              <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-3">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  Statutory Citation Verification & BNS/IPC Cross-Reference
                </h4>

                <div className="grid gap-2">
                  {response.citations.map((c: any, idx: number) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg border text-xs flex flex-col gap-1.5 ${
                        c.status === 'VERIFIED'
                          ? 'bg-emerald-500/5 border-emerald-500/30'
                          : c.status === 'REPLACED_BY_NEW_CODE'
                          ? 'bg-amber-500/5 border-amber-500/30'
                          : 'bg-red-500/5 border-red-500/30'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-slate-200 font-mono text-sm">{c.citation}</span>
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            c.status === 'VERIFIED'
                              ? 'bg-emerald-500/20 text-emerald-300'
                              : c.status === 'REPLACED_BY_NEW_CODE'
                              ? 'bg-amber-500/20 text-amber-300'
                              : 'bg-red-500/20 text-red-300'
                          }`}
                        >
                          {c.status}
                        </span>
                      </div>
                      <p className="text-slate-300">{c.message}</p>
                      {c.ground_truth && (
                        <p className="text-[11px] text-slate-400 bg-slate-950/60 p-2 rounded border border-slate-800/80 font-mono leading-relaxed">
                          <span className="text-amber-400 font-bold">Statutory Ground Truth: </span>
                          {c.ground_truth}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Retrieved Sources Accordion */}
            {response.retrieved_sources && response.retrieved_sources.length > 0 && (
              <div className="bg-slate-900/40 border border-slate-800 rounded-xl overflow-hidden">
                <button
                  onClick={() => setShowSources(!showSources)}
                  className="w-full px-4 py-3 bg-slate-900/70 flex items-center justify-between text-xs font-semibold text-slate-300 hover:text-slate-100"
                >
                  <span className="flex items-center gap-2">
                    <BookOpen className="w-4 h-4 text-blue-400" />
                    Retrieved Authoritative Sources ({response.retrieved_sources.length} matches)
                  </span>
                  {showSources ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </button>

                {showSources && (
                  <div className="p-4 grid md:grid-cols-2 gap-3">
                    {response.retrieved_sources.map((src: any, i: number) => (
                      <div key={i} className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg text-xs space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="font-semibold text-amber-300">{src.title}</span>
                          <span className="text-[10px] text-slate-400 font-mono">{src.citation}</span>
                        </div>
                        <p className="text-slate-400 leading-relaxed line-clamp-3">{src.excerpt}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Input Bar */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-900/70 backdrop-blur-md">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="max-w-5xl mx-auto flex items-center gap-3"
        >
          <div className="relative flex-1">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask any legal question in English, हिन्दी, தமிழ், తెలుగు, etc. (e.g. 'What is the punishment for theft under BNS?')"
              className="w-full bg-slate-800/90 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:border-amber-400 transition-colors shadow-inner"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="px-5 py-3 bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 disabled:opacity-50 text-slate-950 font-bold text-sm rounded-xl flex items-center gap-2 transition-all shadow-md shadow-yellow-500/20"
          >
            <Send className="w-4 h-4" />
            <span>Consult</span>
          </button>
        </form>
      </div>
    </div>
  );
};
