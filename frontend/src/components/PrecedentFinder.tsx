import React, { useState, useEffect } from 'react';
import {
  Search,
  BookOpen,
  Filter,
  Copy,
  Check,
  Scale,
  Calendar,
  Building,
} from 'lucide-react';
import api from '../api/client';

export const PrecedentFinder: React.FC = () => {
  const [query, setQuery] = useState('');
  const [courtFilter, setCourtFilter] = useState('');
  const [sourceType, setSourceType] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const fetchPrecedents = async (searchParam?: string) => {
    setLoading(true);
    try {
      const params: any = {};
      if (searchParam !== undefined ? searchParam : query) {
        params.q = searchParam !== undefined ? searchParam : query;
      }
      if (courtFilter) params.court = courtFilter;
      if (sourceType) params.source_type = sourceType;

      const res = await api.get('/precedents/search', { params });
      setResults(res.data);
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrecedents('');
  }, [courtFilter, sourceType]);

  const handleCopy = (citation: string, id: string) => {
    navigator.clipboard.writeText(citation);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const quickTopics = [
    { label: 'Bail & Personal Liberty', q: 'bail personal liberty Satender Kumar Antil' },
    { label: 'Right to Privacy (Art. 21)', q: 'privacy Puttaswamy fundamental right' },
    { label: 'Mandatory FIR (Sec 173 BNSS)', q: 'FIR Lalita Kumari cognizable' },
    { label: 'Arrest Safeguards (Arnesh Kumar)', q: 'Arnesh Kumar notice arrest 41A' },
    { label: 'Electronic Evidence (Sec 63 BSA)', q: 'electronic evidence certificate 65B' },
  ];

  return (
    <div className="flex-1 p-6 max-w-6xl mx-auto w-full space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-amber-400" />
          Judicial Precedents & Landmark Case Law Repository
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Semantic search across Constitution Benches, Supreme Court rulings, and High Court precedents.
        </p>
      </div>

      {/* Search & Filter Controls */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3 shadow-md">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            fetchPrecedents();
          }}
          className="flex items-center gap-3"
        >
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by legal issue, case name, citation, or section (e.g., 'triple test for bail', 'Section 303')..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-xs text-slate-100 placeholder-slate-400 focus:outline-none focus:border-amber-400"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 text-slate-950 font-bold text-xs rounded-xl flex items-center gap-2 transition-all shadow-md shadow-yellow-500/20"
          >
            <Search className="w-4 h-4" />
            <span>{loading ? 'Searching...' : 'Search'}</span>
          </button>
        </form>

        {/* Quick Topic Chips */}
        <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
          <span className="text-slate-400 font-medium flex items-center gap-1">
            <Filter className="w-3.5 h-3.5 text-amber-400" />
            Quick Topics:
          </span>
          {quickTopics.map((topic, i) => (
            <button
              key={i}
              onClick={() => {
                setQuery(topic.q);
                fetchPrecedents(topic.q);
              }}
              className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700/80 border border-slate-700 text-slate-300 rounded-lg text-xs transition-colors"
            >
              {topic.label}
            </button>
          ))}
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-4 pt-2 border-t border-slate-800/80 text-xs">
          <div className="flex items-center gap-2">
            <span className="text-slate-400">Court:</span>
            <select
              value={courtFilter}
              onChange={(e) => setCourtFilter(e.target.value)}
              className="bg-slate-950 border border-slate-800 text-slate-300 rounded-lg px-2.5 py-1 focus:outline-none focus:border-amber-400"
            >
              <option value="">All Courts</option>
              <option value="Supreme Court">Supreme Court of India</option>
              <option value="High Court">High Courts</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-slate-400">Source Type:</span>
            <select
              value={sourceType}
              onChange={(e) => setSourceType(e.target.value)}
              className="bg-slate-950 border border-slate-800 text-slate-300 rounded-lg px-2.5 py-1 focus:outline-none focus:border-amber-400"
            >
              <option value="">All Sources</option>
              <option value="precedent">Judicial Precedents</option>
              <option value="statute">Statutes & Codes</option>
              <option value="constitution">Constitution</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results List */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs text-slate-400 px-1">
          <span>Found {results.length} legal records</span>
          <span>Ranked by Hybrid Semantic Relevance</span>
        </div>

        {results.map((item) => (
          <div
            key={item.id}
            className="bg-slate-900 border border-slate-800/80 hover:border-slate-700 rounded-xl p-5 space-y-3 transition-colors shadow-md"
          >
            <div className="flex flex-wrap items-start justify-between gap-2">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span
                    className={`text-[10px] px-2 py-0.5 rounded font-mono font-bold uppercase ${
                      item.source_type === 'precedent'
                        ? 'bg-amber-500/10 border border-amber-500/30 text-amber-300'
                        : item.source_type === 'constitution'
                        ? 'bg-purple-500/10 border border-purple-500/30 text-purple-300'
                        : 'bg-blue-500/10 border border-blue-500/30 text-blue-300'
                    }`}
                  >
                    {item.source_type}
                  </span>
                  <h3 className="text-sm font-bold text-slate-100">{item.title}</h3>
                </div>

                <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 font-mono">
                  <span className="text-amber-400 font-bold">{item.citation}</span>
                  {item.court && (
                    <span className="flex items-center gap-1 text-slate-400">
                      <Building className="w-3 h-3 text-slate-500" />
                      {item.court}
                    </span>
                  )}
                  {item.enactment_year && (
                    <span className="flex items-center gap-1 text-slate-400">
                      <Calendar className="w-3 h-3 text-slate-500" />
                      {item.enactment_year}
                    </span>
                  )}
                  {item.bench && (
                    <span className="text-slate-400">Bench: {item.bench}</span>
                  )}
                </div>
              </div>

              <button
                onClick={() => handleCopy(item.citation, item.id)}
                className="flex items-center gap-1 px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs transition-colors"
                title="Copy Citation"
              >
                {copiedId === item.id ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
                <span>{copiedId === item.id ? 'Copied' : 'Cite'}</span>
              </button>
            </div>

            {/* Ratio Decidendi Highlight */}
            {item.ratio_decidendi && (
              <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800/80 text-xs">
                <span className="text-amber-400 font-bold">Ratio Decidendi: </span>
                <span className="text-slate-300 leading-relaxed">{item.ratio_decidendi}</span>
              </div>
            )}

            {/* Statutory Text Excerpt */}
            <p className="text-xs text-slate-400 leading-relaxed bg-slate-950/40 p-3 rounded-lg font-mono">
              {item.legal_text}
            </p>
          </div>
        ))}

        {results.length === 0 && !loading && (
          <div className="p-12 text-center text-slate-500 text-xs bg-slate-900/40 rounded-xl border border-slate-800">
            No legal precedents matching your criteria. Try adjusting keywords or filters.
          </div>
        )}
      </div>
    </div>
  );
};
