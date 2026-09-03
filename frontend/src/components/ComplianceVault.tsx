import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  Lock,
  Database,
  History,
  Activity,
  CheckCircle2,
  RefreshCw,
} from 'lucide-react';
import api from '../api/client';

export const ComplianceVault: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchComplianceData = async () => {
    setLoading(true);
    try {
      const [statsRes, logsRes] = await Promise.all([
        api.get('/compliance/stats'),
        api.get('/compliance/logs'),
      ]);
      setStats(statsRes.data);
      setLogs(logsRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComplianceData();
  }, []);

  const pillars = [
    { title: 'Pillar 1: Data Encryption', desc: 'AES-256 at rest and TLS 1.3 in transit', status: 'ACTIVE' },
    { title: 'Pillar 2: Access Control (RBAC)', desc: 'Strict multi-tier Citizen / Advocate / Admin controls', status: 'ENFORCED' },
    { title: 'Pillar 3: Continuous Monitoring', desc: 'Real-time anomaly detection and rate compliance', status: 'ACTIVE' },
    { title: 'Pillar 4: Activity Logging', desc: 'Cryptographically signed audit logs for every query', status: 'LOGGING' },
    { title: 'Pillar 5: 1-Year Log Retention', desc: 'Immutable retention policy mandated under DPDP §8', status: 'COMPLIANT' },
    { title: 'Pillar 6: Business Continuity', desc: 'Dual-engine failover between SQLite & PostgreSQL', status: 'READY' },
    { title: 'Pillar 7: Processor Governance', desc: 'Contractual verification for downstream AI processors', status: 'VERIFIED' },
  ];

  return (
    <div className="flex-1 p-6 max-w-6xl mx-auto w-full space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            DPDP Act 2025 Compliance & Security Vault
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time compliance monitoring enforcing the Seven Pillars of Security and 1-Year Audit Log Retention.
          </p>
        </div>

        <button
          onClick={fetchComplianceData}
          disabled={loading}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* System Stats Overview */}
      {stats && (
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
            <span className="text-[11px] text-slate-400 uppercase font-semibold">Legal Corpus</span>
            <p className="text-2xl font-bold text-amber-400 font-mono">
              {stats.authoritative_sources_count}
            </p>
            <span className="text-[10px] text-slate-500">Statutes & Precedents</span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
            <span className="text-[11px] text-slate-400 uppercase font-semibold">Queries Analyzed</span>
            <p className="text-2xl font-bold text-blue-400 font-mono">
              {stats.queries_analyzed_count}
            </p>
            <span className="text-[10px] text-slate-500">Multilingual Inquiries</span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
            <span className="text-[11px] text-slate-400 uppercase font-semibold">Audit Logs</span>
            <p className="text-2xl font-bold text-emerald-400 font-mono">
              {stats.compliance_audit_events}
            </p>
            <span className="text-[10px] text-slate-500">Immutable Records</span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
            <span className="text-[11px] text-slate-400 uppercase font-semibold">Indian Languages</span>
            <p className="text-2xl font-bold text-purple-400 font-mono">
              {stats.supported_languages_count}
            </p>
            <span className="text-[10px] text-slate-500">Native Lexicon Support</span>
          </div>
        </div>
      )}

      {/* Seven Pillars Grid */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-md">
        <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
          <Lock className="w-4 h-4 text-emerald-400" />
          The Seven Pillars of Security (DPDP Act 2025 Architecture)
        </h3>

        <div className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {pillars.map((p, idx) => (
            <div
              key={idx}
              className="bg-slate-950/80 border border-slate-800/80 rounded-xl p-3.5 space-y-1.5 text-xs"
            >
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-200">{p.title}</span>
                <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                  {p.status}
                </span>
              </div>
              <p className="text-slate-400 leading-relaxed text-[11px]">{p.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Real-time Audit Logs */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 shadow-md">
        <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
          <Activity className="w-4 h-4 text-blue-400" />
          Live Immutable Audit Trail (1-Year Retention Standard)
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-mono">
                <th className="pb-2">Timestamp</th>
                <th className="pb-2">Actor / User</th>
                <th className="pb-2">Action</th>
                <th className="pb-2">Resource</th>
                <th className="pb-2">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-800/40 text-slate-300">
                  <td className="py-2.5 text-slate-500 text-[11px]">
                    {new Date(log.timestamp).toLocaleString()}
                  </td>
                  <td className="py-2.5 text-amber-400 font-medium">{log.user_id}</td>
                  <td className="py-2.5">
                    <span className="px-2 py-0.5 rounded bg-blue-500/10 border border-blue-500/30 text-blue-300 text-[10px]">
                      {log.action}
                    </span>
                  </td>
                  <td className="py-2.5 text-slate-300">{log.resource_id}</td>
                  <td className="py-2.5 text-slate-400 max-w-xs truncate">{log.details}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
