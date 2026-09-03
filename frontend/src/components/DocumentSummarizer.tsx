import React, { useState } from 'react';
import {
  Upload,
  FileText,
  AlertTriangle,
  ShieldAlert,
  CheckCircle,
  FileSearch,
  BookOpen,
} from 'lucide-react';
import api from '../api/client';

export const DocumentSummarizer: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'upload' | 'text'>('text');
  const [rawText, setRawText] = useState('');
  const [docTitle, setDocTitle] = useState('Master Service Agreement');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);

  const sampleAgreement = `MASTER SERVICES AGREEMENT

1. SERVICES AND DELIVERABLES:
Supplier shall provide cloud data management services to Client. Supplier may process user personal data, customer financial records, and identifying documents.

2. TERMINATION:
Client shall have the exclusive unilateral right to terminate this Agreement at any time without cause upon 24 hours written notice. Supplier shall not have any corresponding right to terminate without cause.

3. LIMITATION OF LIABILITY AND INDEMNITY:
Supplier agrees to defend, indemnify, and hold harmless Client against all losses, penalties, and damages arising out of performance of services, without any monetary cap or exclusion of indirect damages.

4. DISPUTE RESOLUTION:
In the event of any dispute arising out of this agreement, the parties agree to resolve the dispute through arbitration. The venue of arbitration shall be New Delhi.

5. CONFIDENTIALITY:
Each party agrees to maintain confidentiality of proprietary trade secrets.`;

  const handleAnalyzeText = async (textToUse?: string) => {
    const text = textToUse || rawText;
    if (!text.trim()) return;

    setLoading(true);
    try {
      const res = await api.post('/documents/analyze-text', {
        title: docTitle,
        text: text,
      });
      setAnalysis(res.data);
    } catch (err: any) {
      console.error(err);
      alert('Failed to analyze document. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setAnalysis(res.data);
    } catch (err: any) {
      console.error(err);
      alert('Upload failed. Please upload a PDF or TXT file.');
    } finally {
      setLoading(false);
    }
  };

  const loadSample = () => {
    setRawText(sampleAgreement);
    handleAnalyzeText(sampleAgreement);
  };

  return (
    <div className="flex-1 p-6 max-w-6xl mx-auto w-full space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <FileSearch className="w-5 h-5 text-amber-400" />
            Legal Document Summarizer & CLAUSE Loophole Auditor
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Extracts critical contractual clauses, verifies DPDP 2023 compliance covenants, and scores legal liabilities.
          </p>
        </div>

        <button
          onClick={loadSample}
          className="px-3.5 py-1.5 bg-amber-500/10 border border-amber-500/30 hover:bg-amber-500/20 text-amber-300 rounded-lg text-xs font-medium transition-all"
        >
          Load Vulnerable Sample Contract
        </button>
      </div>

      {/* Input Section */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-3 text-xs">
          <button
            onClick={() => setActiveTab('text')}
            className={`px-3 py-1.5 rounded-lg font-medium transition-colors ${
              activeTab === 'text'
                ? 'bg-amber-500 text-slate-950 font-bold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Paste Agreement Text
          </button>
          <button
            onClick={() => setActiveTab('upload')}
            className={`px-3 py-1.5 rounded-lg font-medium transition-colors ${
              activeTab === 'upload'
                ? 'bg-amber-500 text-slate-950 font-bold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Upload Document (PDF / TXT)
          </button>
        </div>

        {activeTab === 'text' ? (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">Document Title:</span>
              <input
                type="text"
                value={docTitle}
                onChange={(e) => setDocTitle(e.target.value)}
                className="bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-slate-200 focus:outline-none focus:border-amber-400"
              />
            </div>
            <textarea
              rows={8}
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              placeholder="Paste contract, agreement, FIR, or legal brief text here..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:border-amber-400 transition-colors leading-relaxed"
            />
            <button
              onClick={() => handleAnalyzeText()}
              disabled={loading || !rawText.trim()}
              className="px-5 py-2.5 bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 text-slate-950 font-bold text-xs rounded-xl flex items-center gap-2 disabled:opacity-50 transition-all shadow-md shadow-yellow-500/20"
            >
              <FileSearch className="w-4 h-4" />
              <span>{loading ? 'Analyzing...' : 'Run CLAUSE Vulnerability Audit'}</span>
            </button>
          </div>
        ) : (
          <div className="p-8 border-2 border-dashed border-slate-700 hover:border-amber-500/50 rounded-xl text-center space-y-3 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center mx-auto text-amber-400">
              <Upload className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-200">Upload Legal File (PDF, TXT)</p>
              <p className="text-xs text-slate-400 mt-0.5">Supports contracts, agreements, charge sheets, and court orders.</p>
            </div>
            <label className="inline-block px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-600 text-xs font-medium text-slate-200 rounded-lg cursor-pointer transition-colors">
              Choose File
              <input type="file" accept=".pdf,.txt,.docx" onChange={handleFileUpload} className="hidden" />
            </label>
          </div>
        )}
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="space-y-6 animate-in fade-in duration-200">
          {/* Executive Overview & Risk Score */}
          <div className="grid md:grid-cols-3 gap-4">
            <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-2 shadow-md">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <BookOpen className="w-3.5 h-3.5 text-amber-400" />
                Executive Summary
              </span>
              <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">
                {analysis.summary}
              </p>
            </div>

            {/* Risk Gauge */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between shadow-md">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <ShieldAlert className="w-3.5 h-3.5 text-red-400" />
                Liability & Risk Index
              </span>

              <div className="my-3 text-center">
                <div className="text-4xl font-extrabold text-amber-400 font-mono tracking-tight">
                  {analysis.risk_score} <span className="text-sm text-slate-400 font-normal">/ 10</span>
                </div>
                <div className="mt-1">
                  <span
                    className={`inline-block px-2.5 py-0.5 rounded text-[11px] font-bold ${
                      analysis.risk_score >= 7
                        ? 'bg-red-500/20 text-red-300 border border-red-500/30'
                        : analysis.risk_score >= 4
                        ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    }`}
                  >
                    {analysis.risk_score >= 7
                      ? 'High Legal Risk'
                      : analysis.risk_score >= 4
                      ? 'Moderate Exposure'
                      : 'Low Risk'}
                  </span>
                </div>
              </div>

              <p className="text-[11px] text-slate-400 leading-relaxed text-center">
                Calculated across statutory compliance, unilateral clauses & financial exposures.
              </p>
            </div>
          </div>

          {/* Vulnerabilities & Loopholes */}
          {analysis.vulnerabilities && analysis.vulnerabilities.length > 0 && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-md">
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                Adversarial Vulnerabilities & Loopholes Detected ({analysis.vulnerabilities.length})
              </h3>

              <div className="grid gap-3">
                {analysis.vulnerabilities.map((v: any, idx: number) => (
                  <div
                    key={idx}
                    className="p-4 bg-slate-950/80 border border-slate-800/90 rounded-xl space-y-2 text-xs"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-200 text-sm">{v.title}</span>
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold font-mono ${
                          v.severity === 'HIGH'
                            ? 'bg-red-500/20 text-red-300 border border-red-500/30'
                            : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        }`}
                      >
                        {v.severity} SEVERITY
                      </span>
                    </div>
                    <p className="text-slate-300 leading-relaxed">{v.description}</p>
                    <div className="bg-slate-900 p-2.5 rounded-lg border border-slate-800 text-slate-300">
                      <span className="text-emerald-400 font-bold">Recommended Judicial Remedy: </span>
                      {v.remedy}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Key Clauses Extracted */}
          {analysis.key_clauses && Object.keys(analysis.key_clauses).length > 0 && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-md">
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-400" />
                Classified Contractual Covenants
              </h3>

              <div className="grid md:grid-cols-2 gap-3">
                {Object.entries(analysis.key_clauses).map(([category, clauses]: [string, any], idx) => (
                  <div key={idx} className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl text-xs space-y-1.5">
                    <span className="font-bold text-amber-300 capitalize">
                      {category.replace('_', ' ')}
                    </span>
                    {clauses.length > 0 ? (
                      clauses.map((c: string, ci: number) => (
                        <p key={ci} className="text-slate-400 leading-relaxed line-clamp-3 bg-slate-900/60 p-2 rounded border border-slate-800/60 font-mono text-[11px]">
                          "{c}"
                        </p>
                      ))
                    ) : (
                      <p className="text-slate-500 italic">No specific clause identified.</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
