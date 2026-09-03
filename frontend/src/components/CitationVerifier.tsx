import React, { useState } from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Sparkles,
  BookOpen,
} from 'lucide-react';
import api from '../api/client';

export const CitationVerifier: React.FC = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const sampleCitationText = `In the instant case, the prosecution asserts that the accused committed murder punishable under IPC Section 302 and theft under IPC Section 378. However, following the 2024 reform codes, the applicable statute is BNS Section 103 and BNS Section 303 respectively. 
Furthermore, pursuant to Satender Kumar Antil v. CBI and Arnesh Kumar v. State of Bihar, pre-trial custody for offences punishable under 7 years requires strict compliance with notice provisions. Under Article 21, personal liberty and the right to privacy as laid down in Puttaswamy remain fundamental.`;

  const handleVerify = async (textToVerify?: string) => {
    const content = textToVerify || text;
    if (!content.trim()) return;

    setLoading(true);
    try {
      const res = await api.post('/citations/verify', { text: content });
      setResults(res.data);
    } catch (err) {
      console.error(err);
      alert('Verification failed. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const loadSample = () => {
    setText(sampleCitationText);
    handleVerify(sampleCitationText);
  };

  return (
    <div className="flex-1 p-6 max-w-5xl mx-auto w-full space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-amber-400" />
            Zero-Trust Citation Verifier
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Cross-checks cited statutory provisions and judicial precedents against the authoritative legal database, identifying repealed IPC/CrPC sections and hallucinated references.
          </p>
        </div>

        <button
          onClick={loadSample}
          className="px-3.5 py-1.5 bg-amber-500/10 border border-amber-500/30 hover:bg-amber-500/20 text-amber-300 rounded-lg text-xs font-medium transition-all"
        >
          Load Mixed Sample Text
        </button>
      </div>

      {/* Input Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 shadow-lg">
        <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
          Paste Legal Brief, Petition, or Judgment Text:
        </label>
        <textarea
          rows={6}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste legal argument or citations to verify against BNS, BNSS, BSA, and Supreme Court rulings..."
          className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:border-amber-400 transition-colors leading-relaxed"
        />

        <button
          onClick={() => handleVerify()}
          disabled={loading || !text.trim()}
          className="px-5 py-2.5 bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 text-slate-950 font-bold text-xs rounded-xl flex items-center gap-2 disabled:opacity-50 transition-all shadow-md shadow-yellow-500/20"
        >
          <Sparkles className="w-4 h-4" />
          <span>{loading ? 'Verifying Citations...' : 'Verify Citations Against Database'}</span>
        </button>
      </div>

      {/* Verification Output */}
      {results && (
        <div className="space-y-4 animate-in fade-in duration-200">
          {/* Summary Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-3">
              <span className="text-slate-400">Total Citations Detected:</span>
              <span className="font-mono font-bold text-slate-100 text-sm">{results.total_citations}</span>
            </div>

            <div className="flex items-center gap-3">
              <span className="text-slate-400">Verification Accuracy:</span>
              <span className="font-mono font-bold text-emerald-400 text-sm">
                {results.verification_rate}%
              </span>
            </div>

            <div className="flex items-center gap-1.5">
              {results.is_verified ? (
                <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-lg font-bold flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> All References Validated
                </span>
              ) : (
                <span className="px-3 py-1 bg-amber-500/10 border border-amber-500/30 text-amber-300 rounded-lg font-bold flex items-center gap-1">
                  <AlertTriangle className="w-3.5 h-3.5" /> Legacy / Outdated Provisions Detected
                </span>
              )}
            </div>
          </div>

          {/* Cards */}
          <div className="grid gap-3">
            {results.verifications.map((item: any, idx: number) => (
              <div
                key={idx}
                className={`p-4 rounded-xl border text-xs space-y-2 shadow-md ${
                  item.status === 'VERIFIED'
                    ? 'bg-emerald-500/5 border-emerald-500/30'
                    : item.status === 'REPLACED_BY_NEW_CODE'
                    ? 'bg-amber-500/5 border-amber-500/30'
                    : 'bg-red-500/5 border-red-500/30'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono font-bold text-sm text-slate-100">{item.citation}</span>
                  <span
                    className={`px-2.5 py-0.5 rounded text-[11px] font-bold font-mono ${
                      item.status === 'VERIFIED'
                        ? 'bg-emerald-500/20 text-emerald-300'
                        : item.status === 'REPLACED_BY_NEW_CODE'
                        ? 'bg-amber-500/20 text-amber-300'
                        : 'bg-red-500/20 text-red-300'
                    }`}
                  >
                    {item.status}
                  </span>
                </div>

                <p className="text-slate-300 leading-relaxed">{item.message}</p>

                {item.replacement_code && (
                  <div className="bg-slate-900 p-2.5 rounded-lg border border-slate-800 text-slate-300">
                    <span className="text-amber-400 font-bold">Bharatiya Nyaya Sanhita Replacement: </span>
                    <span className="font-mono text-amber-300 font-bold">{item.replacement_code}</span>
                  </div>
                )}

                {item.ground_truth && (
                  <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800/80 text-[11px] text-slate-400 font-mono leading-relaxed">
                    <span className="text-slate-300 font-bold">Authoritative Statutory Record: </span>
                    {item.ground_truth}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
