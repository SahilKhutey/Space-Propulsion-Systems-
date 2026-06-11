import React, { useState } from 'react';
import { api } from '../api/client';
import { TradeStudyResult } from '../types';
import { Shield, Sparkles, Check, CheckCircle2, ShieldAlert } from 'lucide-react';

export const TradeStudy: React.FC = () => {
  const [payload, setPayload] = useState(1000);
  const [deltaV, setDeltaV] = useState(6000);
  const [duration, setDuration] = useState(5.0);
  const [powerBudget, setPowerBudget] = useState(5000.0);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TradeStudyResult | null>(null);
  const [error, setError] = useState('');

  const [optimizerLoading, setOptimizerLoading] = useState(false);
  const [optResult, setOptResult] = useState<any | null>(null);

  const runTradeStudy = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await api.runTradeStudy({
        payload_mass_kg: payload,
        delta_v_ms: deltaV,
        mission_duration_years: duration,
        power_budget_w: powerBudget,
        candidates: ['chemical_bipropellant', 'hall_thruster', 'ion_thruster', 'VASIMR']
      });
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Trade Study calculation failed.');
    } finally {
      setLoading(false);
    }
  };

  const runAIOptimizer = async () => {
    setOptimizerLoading(true);
    try {
      const data = await api.runOptimization({
        thruster_type: 'hall_thruster',
        target: 'efficiency',
        power_limit_w: powerBudget,
        mass_flow_limit_kg_s: 0.00008
      });
      setOptResult(data);
    } catch {
      // ignore
    } finally {
      setOptimizerLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 h-full">
      <div className="lg:col-span-4 flex flex-col gap-6">
        <form onSubmit={runTradeStudy} className="glass-panel p-6 rounded-xl flex flex-col gap-4">
          <div>
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Shield className="w-5 h-5 text-aerospace-cyan" />
              Trade Sizing Criteria
            </h3>
            <p className="text-xs text-slate-400">Configure parameters for sizing comparator scoring.</p>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-[10px] font-semibold text-slate-400 uppercase">Spacecraft Mass (kg)</label>
            <input
              type="number" value={payload} onChange={(e) => setPayload(Number(e.target.value))}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-[10px] font-semibold text-slate-400 uppercase">Required Mission Delta-V (m/s)</label>
            <input
              type="number" value={deltaV} onChange={(e) => setDeltaV(Number(e.target.value))}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-[10px] font-semibold text-slate-400 uppercase">Max Power Available (W)</label>
            <input
              type="number" value={powerBudget} onChange={(e) => setPowerBudget(Number(e.target.value))}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
            />
          </div>

          <button
            type="submit"
            className="w-full mt-2 py-2.5 bg-gradient-to-r from-aerospace-blue to-aerospace-cyan text-space-950 font-bold uppercase rounded-lg text-xs transition-all hover:opacity-90"
          >
            Run Sizing Study
          </button>
        </form>

        <div className="glass-panel p-6 rounded-xl flex flex-col gap-4">
          <div>
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-aerospace-cyan animate-pulse" />
              AI Geometric Optimizer
            </h3>
            <p className="text-[11px] text-slate-400">Perform parametric L-BFGS-B search on thruster boundaries.</p>
          </div>
          <button
            onClick={runAIOptimizer} disabled={optimizerLoading}
            className="w-full py-2 bg-slate-900 hover:border-aerospace-cyan border border-slate-800 text-slate-200 text-xs font-semibold rounded-lg uppercase transition-all"
          >
            {optimizerLoading ? 'Optimizing Fields...' : 'Execute Optimizer'}
          </button>

          {optResult && (
            <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-lg text-[10px] space-y-2">
              <div className="flex justify-between border-b border-slate-800/80 pb-1.5 font-bold text-aerospace-cyan">
                <span>Optimized Parameter</span>
                <span>Delta Value</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Power Level</span>
                <span className="text-slate-200 font-mono">{optResult.parameters.power_w.optimal.toFixed(0)} W</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Mass Flow Rate</span>
                <span className="text-slate-200 font-mono">{(optResult.parameters.mass_flow_rate_kg_s.optimal * 1e6).toFixed(1)} mg/s</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Thrust Efficiency</span>
                <span className="text-slate-200 font-mono">{(optResult.performance.efficiency.optimal * 100).toFixed(1)}% (+{optResult.performance.efficiency.improvement_pct.toFixed(0)}%)</span>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="lg:col-span-8 flex flex-col gap-6">
        {result ? (
          <div className="glass-panel p-6 rounded-xl flex-1 flex flex-col gap-6 animate-fade-in">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-lg font-bold text-slate-100">Evaluated Candidates</h3>
                <p className="text-xs text-slate-400">Weighted scores (Mass: 40%, Travel time: 40%, Maturity: 20%).</p>
              </div>
              <div className="px-3 py-1 bg-aerospace-cyan/15 text-aerospace-cyan border border-aerospace-cyan/35 rounded-full text-xs font-bold flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-aerospace-cyan" />
                <span>Winner: {result.winner.replace('_', ' ').toUpperCase()}</span>
              </div>
            </div>

            <div className="overflow-x-auto border border-slate-800/60 rounded-lg">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-slate-900/60 border-b border-slate-800 text-slate-400 font-semibold uppercase text-[9px] tracking-wider">
                    <th className="p-3">Thruster Class</th>
                    <th className="p-3">Isp (s)</th>
                    <th className="p-3">Propellant (kg)</th>
                    <th className="p-3">Time (days)</th>
                    <th className="p-3 text-right">Score</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {result.candidates.map((c, idx) => (
                    <tr key={idx} className={`hover:bg-slate-900/40 ${c.thruster_type === result.winner ? 'bg-aerospace-cyan/5 font-semibold' : ''}`}>
                      <td className="p-3 flex items-center gap-2">
                        {c.thruster_type === result.winner && <Check className="w-3.5 h-3.5 text-aerospace-cyan" />}
                        <span>{c.thruster_type.replace('_', ' ')}</span>
                      </td>
                      <td className="p-3 text-slate-300">{c.isp_s}</td>
                      <td className="p-3 text-slate-300">{c.propellant_mass_kg.toFixed(1)}</td>
                      <td className="p-3 text-slate-300">{c.transfer_time_days.toFixed(1)}</td>
                      <td className="p-3 text-right text-aerospace-cyan glow-text-cyan font-mono font-bold">{c.score.toFixed(1)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="p-4 bg-slate-950/60 rounded-lg border border-slate-800/80 mt-auto">
              <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Engineering Assessment</span>
              <p className="text-xs text-slate-300 mt-1.5 leading-relaxed">{result.rationale}</p>
            </div>
          </div>
        ) : (
          <div className="glass-panel p-6 rounded-xl flex-1 flex flex-col items-center justify-center text-slate-500 text-sm gap-2">
            <Shield className="w-10 h-10 text-slate-700 animate-pulse" />
            Perform sizing study to compare propulsion configurations.
          </div>
        )}
      </div>
    </div>
  );
};
