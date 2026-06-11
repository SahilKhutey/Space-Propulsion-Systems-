import React, { useState } from 'react';
import { api } from '../api/client';
import { PowerResult } from '../types';
import { Sun, ShieldAlert, CheckCircle, Info } from 'lucide-react';

export const PowerModule: React.FC = () => {
  const [area, setArea] = useState(15.0);
  const [efficiency, setEfficiency] = useState(0.28);
  const [distance, setDistance] = useState(1.0);
  const [battery, setBattery] = useState(1500.0);
  const [thrusterPower, setThrusterPower] = useState(2500.0);
  const [dutyCycle, setDutyCycle] = useState(0.25);
  const [orbitPeriod, setOrbitPeriod] = useState(90.0);
  const [eclipseDuration, setEclipseDuration] = useState(35.0);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PowerResult | null>(null);
  const [error, setError] = useState('');

  const handleSimulatePower = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await api.computePower({
        solar_array_area_m2: area,
        solar_efficiency: efficiency,
        distance_au: distance,
        battery_capacity_wh: battery,
        eclipse_duration_min: eclipseDuration,
        orbit_period_min: orbitPeriod,
        thruster_power_w: thrusterPower,
        thruster_duty_cycle: dutyCycle
      });
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Power simulation failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 h-full">
      <div className="lg:col-span-5 flex flex-col">
        <form onSubmit={handleSimulatePower} className="glass-panel p-6 rounded-xl flex flex-col gap-5 h-full">
          <div>
            <h3 className="text-lg font-bold text-slate-100 mb-1 flex items-center gap-2">
              <Sun className="w-5 h-5 text-aerospace-cyan" />
              Power Grid Configuration
            </h3>
            <p className="text-xs text-slate-400">Configure arrays, battery cells, and solar distances.</p>
          </div>

          <div className="flex gap-2">
            <button type="button" onClick={() => setDistance(1.0)} className={`flex-1 py-1.5 px-2 text-xs font-semibold rounded ${distance === 1.0 ? 'bg-aerospace-cyan text-space-950' : 'bg-slate-900 border border-slate-800'}`}>Earth</button>
            <button type="button" onClick={() => setDistance(1.524)} className={`flex-1 py-1.5 px-2 text-xs font-semibold rounded ${distance === 1.524 ? 'bg-aerospace-cyan text-space-950' : 'bg-slate-900 border border-slate-800'}`}>Mars</button>
            <button type="button" onClick={() => setDistance(5.203)} className={`flex-1 py-1.5 px-2 text-xs font-semibold rounded ${distance === 5.203 ? 'bg-aerospace-cyan text-space-950' : 'bg-slate-900 border border-slate-800'}`}>Jupiter</button>
            <button type="button" onClick={() => setDistance(9.582)} className={`flex-1 py-1.5 px-2 text-xs font-semibold rounded ${distance === 9.582 ? 'bg-aerospace-cyan text-space-950' : 'bg-slate-900 border border-slate-800'}`}>Saturn</button>
          </div>

          <div className="flex flex-col gap-1.5">
            <div className="flex justify-between text-xs">
              <label className="font-semibold text-slate-300">Distance from Sun: <b className="text-aerospace-cyan">{distance.toFixed(3)} AU</b></label>
            </div>
            <input
              type="range" min="0.3" max="35.0" step="0.1" value={distance}
              onChange={(e) => setDistance(Number(e.target.value))}
              className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-aerospace-cyan"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-300">Solar Array Area ($m^2$)</label>
              <input
                type="number" value={area} onChange={(e) => setArea(Number(e.target.value))}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-300">Battery Capacity (Wh)</label>
              <input
                type="number" value={battery} onChange={(e) => setBattery(Number(e.target.value))}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-300">Thruster Power (W)</label>
              <input
                type="number" value={thrusterPower} onChange={(e) => setThrusterPower(Number(e.target.value))}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-300">Duty Cycle (0-1)</label>
              <input
                type="number" step="0.05" value={dutyCycle} onChange={(e) => setDutyCycle(Number(e.target.value))}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit" disabled={loading}
            className="w-full mt-auto py-3 bg-gradient-to-r from-aerospace-blue to-aerospace-cyan text-space-950 font-bold uppercase rounded-lg text-sm transition-all hover:opacity-90 active:scale-95"
          >
            Compute Energy Balance
          </button>
        </form>
      </div>

      <div className="lg:col-span-7 flex flex-col gap-6">
        {error && (
          <div className="p-4 bg-aerospace-crimson/10 border border-aerospace-crimson/30 rounded-lg flex items-center gap-3 text-aerospace-crimson text-xs font-semibold">
            <ShieldAlert className="w-5 h-5" />
            <span>{error}</span>
          </div>
        )}

        {result ? (
          <div className="glass-panel p-6 rounded-xl flex-1 flex flex-col gap-6 animate-fade-in">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-slate-100">Telemetry Summary</h3>
                <p className="text-xs text-slate-400">Power flow calculations for the spacecraft power grid.</p>
              </div>
              <div className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1.5 ${result.feasible ? 'bg-aerospace-emerald/10 text-aerospace-emerald border border-aerospace-emerald/30' : 'bg-aerospace-crimson/10 text-aerospace-crimson border border-aerospace-crimson/30'}`}>
                {result.feasible ? (
                  <>
                    <CheckCircle className="w-4 h-4" />
                    <span>Feasible</span>
                  </>
                ) : (
                  <>
                    <ShieldAlert className="w-4 h-4" />
                    <span>Infeasible</span>
                  </>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[10px] uppercase font-bold text-slate-400">Solar Generation</span>
                <span className="text-2xl font-black text-slate-200 mt-1">{result.solar_power_w.toFixed(1)} W</span>
              </div>
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[10px] uppercase font-bold text-slate-400">Average Orbital Power</span>
                <span className="text-2xl font-black text-slate-200 mt-1">{result.average_power_w.toFixed(1)} W</span>
              </div>
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[10px] uppercase font-bold text-slate-400">Eclipse Power Loss</span>
                <span className="text-xl font-bold text-slate-200 mt-1">{result.eclipse_loss_wh.toFixed(1)} Wh</span>
              </div>
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[10px] uppercase font-bold text-slate-400">Battery Margin</span>
                <span className={`text-xl font-bold mt-1 ${(result.battery_margin * 100) >= 0 ? 'text-aerospace-emerald' : 'text-aerospace-crimson'}`}>
                  {(result.battery_margin * 100).toFixed(1)}%
                </span>
              </div>
            </div>

            <div className="p-4 bg-slate-950/60 rounded-lg border border-slate-800/80 mt-auto">
              <span className="text-[10px] uppercase font-bold text-aerospace-cyan tracking-wider flex items-center gap-1.5">
                <Info className="w-3.5 h-3.5" />
                Engineering Insights
              </span>
              <ul className="text-xs text-slate-300 mt-2 space-y-1.5">
                {result.notes.map((n, i) => (
                  <li key={i} className="flex gap-1.5 items-start">
                    <span className="text-aerospace-cyan font-bold">•</span>
                    <span>{n}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ) : (
          <div className="glass-panel p-6 rounded-xl flex-1 flex flex-col items-center justify-center text-slate-500 text-sm gap-2">
            <Sun className="w-10 h-10 text-slate-700 animate-pulse" />
            Perform simulations to compute power grid metrics.
          </div>
        )}
      </div>
    </div>
  );
};
