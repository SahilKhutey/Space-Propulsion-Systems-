import React, { useState } from 'react';
import { api } from '../api/client';
import { ThrusterPerformanceResult } from '../types';
import { Zap, Flame, ShieldAlert, Cpu } from 'lucide-react';

export const ThrustModule: React.FC = () => {
  const [thrusterType, setThrusterType] = useState('hall_thruster');
  const [power, setPower] = useState(5000);
  const [efficiency, setEfficiency] = useState(0.6);
  const [isp, setIsp] = useState(2000);
  const [massFlow, setMassFlow] = useState(1.5);
  const [propellant, setPropellant] = useState('LOX_LH2');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ThrusterPerformanceResult | null>(null);
  const [error, setError] = useState('');

  const handleRunSimulation = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    let payload: any = {};
    if (thrusterType === 'hall_thruster') {
      payload = { thruster_type: 'hall_thruster', power_w: power, efficiency, isp_s: isp };
    } else if (thrusterType === 'ion_thruster') {
      payload = { thruster_type: 'ion_thruster', power_w: power, efficiency, isp_s: isp };
    } else if (thrusterType === 'chemical') {
      payload = { thruster_type: 'chemical', propellant, mass_flow_kg_s: massFlow, isp_s: 450.0 };
    } else if (thrusterType === 'VASIMR') {
      payload = { thruster_type: 'VASIMR', power_w: power, efficiency, isp_s: isp };
    } else {
      payload = { thruster_type: 'NTR', power_w: power, efficiency, isp_s: isp, mass_flow_kg_s: massFlow };
    }

    try {
      const data = await api.computeThrust(payload);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Simulation error.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 h-full">
      <div className="lg:col-span-5 flex flex-col">
        <form onSubmit={handleRunSimulation} className="glass-panel p-6 rounded-xl flex flex-col gap-5 h-full">
          <div>
            <h3 className="text-lg font-bold text-slate-100 mb-1 flex items-center gap-2">
              <Cpu className="w-5 h-5 text-aerospace-cyan" />
              Engine Configuration
            </h3>
            <p className="text-xs text-slate-400">Design parameters for active thruster simulations.</p>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-slate-300">Thruster Concept Type</label>
            <select
              value={thrusterType}
              onChange={(e) => setThrusterType(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-aerospace-cyan"
            >
              <option value="hall_thruster">Hall Effect Thruster (Electric)</option>
              <option value="ion_thruster">Gridded Ion Engine (Electric)</option>
              <option value="chemical">Chemical Propulsion (Liquid/Solid)</option>
              <option value="VASIMR">VASIMR Plasma Rocket (Electric)</option>
              <option value="NTR">Nuclear Thermal Rocket (Nuclear)</option>
            </select>
          </div>

          {thrusterType !== 'chemical' && (
            <div className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <div className="flex justify-between text-xs">
                  <label className="font-semibold text-slate-300">Input Firing Power: <b className="text-aerospace-cyan">{power.toLocaleString()} W</b></label>
                </div>
                <input
                  type="range" min="100" max="250000" step="500" value={power}
                  onChange={(e) => setPower(Number(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-aerospace-cyan"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <div className="flex justify-between text-xs">
                  <label className="font-semibold text-slate-300">Specific Impulse (Isp): <b className="text-aerospace-cyan">{isp.toLocaleString()} s</b></label>
                </div>
                <input
                  type="range" min="300" max="15000" step="100" value={isp}
                  onChange={(e) => setIsp(Number(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-aerospace-cyan"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <div className="flex justify-between text-xs">
                  <label className="font-semibold text-slate-300">Efficiency ($\eta$): <b className="text-aerospace-cyan">{(efficiency * 100).toFixed(0)}%</b></label>
                </div>
                <input
                  type="range" min="0.1" max="0.85" step="0.05" value={efficiency}
                  onChange={(e) => setEfficiency(Number(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-aerospace-cyan"
                />
              </div>
            </div>
          )}

          {thrusterType === 'chemical' && (
            <div className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-semibold text-slate-300">Propellant Combination</label>
                <select
                  value={propellant}
                  onChange={(e) => setPropellant(e.target.value)}
                  className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-aerospace-cyan"
                >
                  <option value="LOX_LH2">LOX / LH2 (Isp ~ 450s)</option>
                  <option value="LOX_methane">LOX / Methane (Isp ~ 360s)</option>
                  <option value="bipropellant">Hydrazine biprop (Isp ~ 310s)</option>
                  <option value="monopropellant">Hydrazine monoprop (Isp ~ 220s)</option>
                  <option value="solid">Solid (Isp ~ 280s)</option>
                </select>
              </div>

              <div className="flex flex-col gap-1.5">
                <div className="flex justify-between text-xs">
                  <label className="font-semibold text-slate-300">Mass Flow Rate: <b className="text-aerospace-cyan">{massFlow.toFixed(1)} kg/s</b></label>
                </div>
                <input
                  type="range" min="0.1" max="50" step="0.1" value={massFlow}
                  onChange={(e) => setMassFlow(Number(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-aerospace-cyan"
                />
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-auto py-3 bg-gradient-to-r from-aerospace-blue to-aerospace-cyan text-space-950 font-bold uppercase rounded-lg text-sm transition-all hover:opacity-90 active:scale-95 disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loading ? 'Solving Fields...' : 'Launch Solver'}
          </button>
        </form>
      </div>

      <div className="lg:col-span-7 flex flex-col gap-6">
        {error && (
          <div className="p-4 bg-aerospace-crimson/10 border border-aerospace-crimson/30 rounded-lg flex items-center gap-3 text-aerospace-crimson">
            <ShieldAlert className="w-5 h-5" />
            <span className="text-xs font-semibold">{error}</span>
          </div>
        )}

        {result ? (
          <div className="glass-panel p-6 rounded-xl flex-1 flex flex-col gap-6">
            <div>
              <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <Flame className="w-5 h-5 text-aerospace-cyan animate-pulse" />
                Performance Telemetry
              </h3>
              <p className="text-xs text-slate-400">Calculated characteristics based on pure physics algorithms.</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col gap-1 hover:border-aerospace-cyan/40 transition-all">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Total Thrust</span>
                <span className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-200">
                  {result.thrust_n.toFixed(4)} N
                </span>
              </div>

              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col gap-1 hover:border-aerospace-cyan/40 transition-all">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Specific Impulse</span>
                <span className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-200">
                  {result.isp_s.toLocaleString()} s
                </span>
              </div>

              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col gap-1">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Exhaust Velocity</span>
                <span className="text-xl font-bold text-slate-200">
                  {result.exhaust_velocity_ms.toLocaleString()} m/s
                </span>
              </div>

              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col gap-1">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Mass Flow Rate</span>
                <span className="text-xl font-bold text-slate-200 font-mono">
                  {(result.mass_flow_kg_s * 1e6).toFixed(2)} mg/s
                </span>
              </div>

              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col gap-1 col-span-2">
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Specific Firing Power Requirement</span>
                <span className="text-lg font-bold text-slate-200">
                  {result.specific_power_w_per_n === Infinity ? '0.0 W/N' : `${(result.specific_power_w_per_n / 1000).toFixed(2)} kW / N`}
                </span>
              </div>
            </div>

            <div className="mt-auto p-4 bg-slate-950/60 rounded-lg border border-slate-800/80">
              <span className="text-[10px] uppercase font-bold text-aerospace-cyan glow-text-cyan tracking-wider">Analysis Notes</span>
              <p className="text-xs text-slate-300 mt-1.5 leading-relaxed">{result.notes}</p>
            </div>
          </div>
        ) : (
          <div className="glass-panel p-6 rounded-xl flex-1 flex flex-col items-center justify-center text-slate-500 text-sm gap-2">
            <Flame className="w-10 h-10 text-slate-700 animate-pulse" />
            Configure parameters and launch solver to display telemetry.
          </div>
        )}
      </div>
    </div>
  );
};
