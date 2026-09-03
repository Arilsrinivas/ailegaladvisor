import React, { useState } from 'react';
import {
  TrendingUp,
  ShieldCheck,
  AlertOctagon,
  Scale,
  Sparkles,
  BookOpen,
} from 'lucide-react';
import api from '../api/client';

export const OutcomeAnalyzer: React.FC = () => {
  const [caseTitle, setCaseTitle] = useState('State (NCT of Delhi) v. Ramesh Kumar');
  const [offenceName, setOffenceName] = useState('Theft / Dishonest Misappropriation');
  const [sections, setSections] = useState('BNS Section 303, BNS Section 318');
  const [maxYears, setMaxYears] = useState(3);
  const [custodyDays, setCustodyDays] = useState(120);
  const [isFirstOffender, setIsFirstOffender] = useState(true);
  const [isVulnerable, setIsVulnerable] = useState(false);
  const [noticeIssued, setNoticeIssued] = useState(false);
  const [coAccusedBailed, setCoAccusedBailed] = useState(true);
  const [chargeSheetFiled, setChargeSheetFiled] = useState(true);
  const [flightRisk, setFlightRisk] = useState('low');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const res = await api.post('/outcomes/predict', {
        case_title: caseTitle,
        offence_name: offenceName,
        applied_sections: sections.split(',').map((s) => s.trim()),
        max_punishment_years: Number(maxYears),
        is_first_offender: isFirstOffender,
        days_in_custody: Number(custodyDays),
        is_vulnerable: isVulnerable,
        notice_issued: noticeIssued,
        co_accused_bailed: coAccusedBailed,
        charge_sheet_filed: chargeSheetFiled,
        flight_risk: flightRisk,
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert('Prediction failed. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-6 max-w-6xl mx-auto w-full space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-amber-400" />
          Case Outcome & Bail Likelihood Estimator
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Judicial factor analysis applying BNSS Section 479 (Undertrial Detentions), Satender Kumar Antil categories, and Supreme Court bail jurisprudence.
        </p>
      </div>

      <div className="grid lg:grid-cols-12 gap-6">
        {/* Factors Input Panel (5 cols) */}
        <div className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-lg text-xs">
          <h3 className="font-bold text-slate-200 uppercase tracking-wider text-[11px] border-b border-slate-800 pb-2">
            Case Parameters
          </h3>

          <div className="space-y-3">
            <div>
              <label className="block text-slate-400 mb-1">Case Title:</label>
              <input
                type="text"
                value={caseTitle}
                onChange={(e) => setCaseTitle(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-200 focus:outline-none focus:border-amber-400"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Alleged Offence:</label>
              <input
                type="text"
                value={offenceName}
                onChange={(e) => setOffenceName(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-200 focus:outline-none focus:border-amber-400"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Applied Sections:</label>
              <input
                type="text"
                value={sections}
                onChange={(e) => setSections(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-200 focus:outline-none focus:border-amber-400"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-400 mb-1">Max Penalty (Years): {maxYears}</label>
                <input
                  type="range"
                  min={1}
                  max={20}
                  value={maxYears}
                  onChange={(e) => setMaxYears(Number(e.target.value))}
                  className="w-full accent-amber-400 cursor-pointer"
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Custody Days: {custodyDays}</label>
                <input
                  type="number"
                  value={custodyDays}
                  onChange={(e) => setCustodyDays(Number(e.target.value))}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-1.5 text-xs text-slate-200 focus:outline-none focus:border-amber-400"
                />
              </div>
            </div>

            {/* Checkbox Options */}
            <div className="space-y-2 pt-2 border-t border-slate-800/80">
              <label className="flex items-center gap-2 cursor-pointer text-slate-300">
                <input
                  type="checkbox"
                  checked={isFirstOffender}
                  onChange={(e) => setIsFirstOffender(e.target.checked)}
                  className="rounded border-slate-700 text-amber-500 focus:ring-0"
                />
                <span>First-time Offender (Qualifies for 1/3 threshold under BNSS §479)</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer text-slate-300">
                <input
                  type="checkbox"
                  checked={isVulnerable}
                  onChange={(e) => setIsVulnerable(e.target.checked)}
                  className="rounded border-slate-700 text-amber-500 focus:ring-0"
                />
                <span>Woman / Minor / Sick / Infirm (BNSS §480 Proviso)</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer text-slate-300">
                <input
                  type="checkbox"
                  checked={noticeIssued}
                  onChange={(e) => setNoticeIssued(e.target.checked)}
                  className="rounded border-slate-700 text-amber-500 focus:ring-0"
                />
                <span>Notice of Appearance Issued (Sec 35 BNSS / 41A CrPC)</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer text-slate-300">
                <input
                  type="checkbox"
                  checked={coAccusedBailed}
                  onChange={(e) => setCoAccusedBailed(e.target.checked)}
                  className="rounded border-slate-700 text-amber-500 focus:ring-0"
                />
                <span>Co-accused with similar role already granted bail (Parity)</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer text-slate-300">
                <input
                  type="checkbox"
                  checked={chargeSheetFiled}
                  onChange={(e) => setChargeSheetFiled(e.target.checked)}
                  className="rounded border-slate-700 text-amber-500 focus:ring-0"
                />
                <span>Charge Sheet Filed (Investigation Complete)</span>
              </label>
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Flight Risk & Evidence Tampering Apprehension:</label>
              <select
                value={flightRisk}
                onChange={(e) => setFlightRisk(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-200 focus:outline-none focus:border-amber-400"
              >
                <option value="low">Low Risk (Local resident, roots in society)</option>
                <option value="medium">Medium Risk (Requires surety/conditions)</option>
                <option value="high">High Risk (Absconding history/influential)</option>
              </select>
            </div>
          </div>

          <button
            onClick={handlePredict}
            disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 text-slate-950 font-bold text-xs rounded-xl flex items-center justify-center gap-2 transition-all shadow-md shadow-yellow-500/20"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? 'Evaluating Precedents...' : 'Calculate Relief Likelihood'}</span>
          </button>
        </div>

        {/* Prediction Results Panel (7 cols) */}
        <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col shadow-lg space-y-5">
          {result ? (
            <div className="space-y-5 animate-in fade-in duration-200 text-xs">
              {/* Top Score Gauge */}
              <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 text-center space-y-3">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Estimated Probability of Bail / Pre-Trial Relief
                </span>

                <div className="text-5xl font-extrabold font-mono tracking-tight text-amber-400">
                  {result.probability_score}%
                </div>

                <div className="inline-block px-3 py-1 rounded-full text-xs font-bold border border-amber-500/30 bg-amber-500/10 text-amber-300">
                  {result.predicted_outcome}
                </div>

                <p className="text-xs text-slate-300 max-w-lg mx-auto leading-relaxed pt-2">
                  <span className="text-amber-400 font-bold">Judicial Strategy: </span>
                  {result.recommendation}
                </p>
              </div>

              {/* Favorable Factors */}
              {result.favorable_factors?.length > 0 && (
                <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2">
                  <h4 className="font-bold text-emerald-400 flex items-center gap-1.5 uppercase text-[11px]">
                    <ShieldCheck className="w-4 h-4" />
                    Statutory & Factual Favorable Grounds ({result.favorable_factors.length})
                  </h4>
                  <ul className="space-y-1.5">
                    {result.favorable_factors.map((f: string, i: number) => (
                      <li key={i} className="text-slate-300 leading-relaxed flex items-start gap-2">
                        <span className="text-emerald-400 font-bold">✓</span>
                        <span>{f}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Adverse Factors */}
              {result.adverse_factors?.length > 0 && (
                <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2">
                  <h4 className="font-bold text-red-400 flex items-center gap-1.5 uppercase text-[11px]">
                    <AlertOctagon className="w-4 h-4" />
                    Prosecution Adverse Factors & Potential Objections ({result.adverse_factors.length})
                  </h4>
                  <ul className="space-y-1.5">
                    {result.adverse_factors.map((a: string, i: number) => (
                      <li key={i} className="text-slate-300 leading-relaxed flex items-start gap-2">
                        <span className="text-red-400 font-bold">✗</span>
                        <span>{a}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Guidelines Applied */}
              {result.guidelines_applied?.length > 0 && (
                <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2">
                  <h4 className="font-bold text-amber-300 flex items-center gap-1.5 uppercase text-[11px]">
                    <Scale className="w-4 h-4" />
                    Supreme Court Guidelines & Statutes Applied
                  </h4>
                  <div className="grid gap-2">
                    {result.guidelines_applied.map((g: any, i: number) => (
                      <div key={i} className="p-2.5 bg-slate-900 rounded-lg border border-slate-800">
                        <span className="font-bold text-slate-200">
                          {g.precedent || g.statute}:
                        </span>{' '}
                        <span className="text-slate-400">{g.principle}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full min-h-[350px] flex flex-col items-center justify-center text-center text-slate-500 space-y-3">
              <Scale className="w-12 h-12 text-slate-700" />
              <div>
                <p className="text-sm font-medium text-slate-300">No Outcome Prediction Run Yet</p>
                <p className="text-xs text-slate-500 max-w-sm mt-1">
                  Adjust the case factors on the left and click "Calculate Relief Likelihood" to view quantitative probabilities and precedents.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
