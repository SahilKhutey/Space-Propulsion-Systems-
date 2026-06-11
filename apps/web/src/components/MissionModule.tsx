import React, { useState } from 'react';
import { api } from '../api/client';
import { MissionResult } from '../types';
import { Compass, ShieldAlert, FileText, CheckCircle } from 'lucide-react';

interface MissionModuleProps {
  onSimulationRun: (startAlt: number, targetAlt: number, thrust: number, power: number) => void;
}

export const MissionModule: React.FC<MissionModuleProps> = ({ onSimulationRun }) => {
  const [name, setName] = useState('GEO Insertion Mission');
  const [initialOrbit, setInitialOrbit] = useState<'LEO' | 'SSO' | 'MEO' | 'GEO' | 'HEO' | 'LUNAR'>('LEO');
  const [targetOrbit, setTargetOrbit] = useState<'LEO' | 'SSO' | 'MEO' | 'GEO' | 'HEO' | 'LUNAR' | 'MARS_TRANSFER' | 'ASTEROID'>('GEO');
  const [payload, setPayload] = useState(1000.0);
  const [thrusterType, setThrusterType] = useState('hall_thruster');
  const [isp, setIsp] = useState(2200.0);
  const [efficiency, setEfficiency] = useState(0.62);
  const [power, setPower] = useState(4500.0);
  const [safetyFactor, setSafetyFactor] = useState(1.2);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<MissionResult | null>(null);
  const [error, setError] = useState('');

  const orbitAltitudes = {
    LEO: 400000,
    SSO: 800000,
    MEO: 20000000,
    GEO: 35786000,
    HEO: 100000000,
    LUNAR: 384400000,
    MARS_TRANSFER: 225000000000,
    ASTEROID: 350000000000,
  };

  const handleSimulateMission = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await api.computeMission({
        name,
        initial_orbit: initialOrbit,
        target_orbit: targetOrbit,
        payload_mass_kg: payload,
        thruster_type: thrusterType,
        isp_s: isp,
        efficiency,
        power_w: power,
        duration_years: 5.0,
        safety_factor: safetyFactor
      });
      setResult(data);

      const startAlt = orbitAltitudes[initialOrbit];
      const rawTargetAlt = orbitAltitudes[targetOrbit];
      const targetAlt = rawTargetAlt > 400000000 ? 400000000 : rawTargetAlt;
      
      const g0 = 9.80665;
      const ve = isp * g0;
      const computedThrust = 2 * efficiency * power / ve;
      
      onSimulationRun(startAlt, targetAlt, computedThrust, power);
    } catch (err: any) {
      setError(err.message || 'Mission simulation failed.');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = () => {
    if (!result) return;
    const jsonStr = JSON.stringify(result, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${name.replace(/\s+/g, '_')}_brief.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 h-full">
      <div className="lg:col-span-5 flex flex-col">
        <form onSubmit={handleSimulateMission} className="glass-panel p-6 rounded-xl flex flex-col gap-4 h-full overflow-y-auto">
          <div>
            <h3 className="text-lg font-bold text-slate-100 mb-1 flex items-center gap-2">
              <Compass className="w-5 h-5 text-aerospace-cyan" />
              Mission Planner
            </h3>
            <p className="text-xs text-slate-400">Validate spacecraft trajectory envelopes and orbital delta-V.</p>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-[10px] font-semibold text-slate-400 uppercase">Mission Title</label>
            <input
              type="text" value={name} onChange={(e) => setName(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="flex flex-col gap-1">
              <label className="text-[10px] font-semibold text-slate-400 uppercase">Initial Orbit</label>
              <select
                value={initialOrbit} onChange={(e) => setInitialOrbit(e.target.value as any)}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              >
                <option value="LEO">LEO (400 km)</option>
                <option value="SSO">SSO (800 km)</option>
                <option value="MEO">MEO (20,000 km)</option>
                <option value="GEO">GEO (35,786 km)</option>
                <option value="LUNAR">Lunar Orbit</option>
              </select>
            </div>
            <div className="flex flex-col gap-1">
              <label className="text-[10px] font-semibold text-slate-400 uppercase">Target Orbit</label>
              <select
                value={targetOrbit} onChange={(e) => setTargetOrbit(e.target.value as any)}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              >
                <option value="GEO">GEO (35,786 km)</option>
                <option value="MEO">MEO (20,000 km)</option>
                <option value="LUNAR">Lunar Orbit</option>
                <option value="MARS_TRANSFER">Mars Transfer</option>
                <option value="ASTEROID">Asteroid Belt</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="flex flex-col gap-1">
              <label className="text-[10px] font-semibold text-slate-400 uppercase">Payload Mass (kg)</label>
              <input
                type="number" value={payload} onChange={(e) => setPayload(Number(e.target.value))}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              />
            </div>
            <div className="flex flex-col gap-1">
              <label className="text-[10px] font-semibold text-slate-400 uppercase">Safety Factor</label>
              <input
                type="number" step="0.05" value={safetyFactor} onChange={(e) => setSafetyFactor(Number(e.target.value))}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              />
            </div>
          </div>

          <div className="border-t border-slate-800/80 pt-3 flex flex-col gap-3">
            <span className="text-[10px] font-bold text-aerospace-cyan uppercase">Thruster Design Inputs</span>
            
            <div className="flex flex-col gap-1">
              <label className="text-[9px] font-semibold text-slate-400 uppercase">System Class</label>
              <select
                value={thrusterType} onChange={(e) => setThrusterType(e.target.value)}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              >
                <option value="hall_thruster">Hall Effect Thruster</option>
                <option value="ion_thruster">Gridded Ion Engine</option>
                <option value="VASIMR">VASIMR Plasma Engine</option>
                <option value="chemical">Bipropellant Chemical</option>
              </select>
            </div>

            <div className="grid grid-cols-3 gap-2">
              <div className="flex flex-col gap-1">
                <label className="text-[9px] font-semibold text-slate-400 uppercase">Isp (s)</label>
                <input
                  type="number" value={isp} onChange={(e) => setIsp(Number(e.target.value))}
                  className="bg-slate-900 border border-slate-800 rounded-lg px-2 py-1.5 text-xs text-slate-200 focus:outline-none"
                />
              </div>
              <div className="flex flex-col gap-1">
                <label className="text-[9px] font-semibold text-slate-400 uppercase">Eff ($\eta$)</label>
                <input
                  type="number" step="0.05" value={efficiency} onChange={(e) => setEfficiency(Number(e.target.value))}
                  className="bg-slate-900 border border-slate-800 rounded-lg px-2 py-1.5 text-xs text-slate-200 focus:outline-none"
                />
              </div>
              <div className="flex flex-col gap-1">
                <label className="text-[9px] font-semibold text-slate-400 uppercase">Power (W)</label>
                <input
                  type="number" value={power} onChange={(e) => setPower(Number(e.target.value))}
                  className="bg-slate-900 border border-slate-800 rounded-lg px-2 py-1.5 text-xs text-slate-200 focus:outline-none"
                />
              </div>
            </div>
          </div>

          <button
            type="submit" disabled={loading}
            className="w-full mt-auto py-3 bg-gradient-to-r from-aerospace-blue to-aerospace-cyan text-space-950 font-bold uppercase rounded-lg text-sm transition-all hover:opacity-90 active:scale-95"
          >
            Run Trajectory Analysis
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
                <h3 className="text-lg font-bold text-slate-100">Flight Validation Outcomes</h3>
                <p className="text-xs text-slate-400">Validated orbital parameters and dry mass ratios.</p>
              </div>
              <button
                onClick={downloadReport}
                className="py-1.5 px-3 bg-slate-900 border border-slate-800 hover:border-aerospace-cyan text-slate-300 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5"
              >
                <FileText className="w-4 h-4 text-aerospace-cyan" />
                <span>Download Report</span>
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[10px] uppercase font-bold text-slate-400">Total Propellant Mass</span>
                <span className="text-2xl font-black text-slate-200 mt-1">{result.propellant_mass_kg.toFixed(1)} kg</span>
              </div>
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[10px] uppercase font-bold text-slate-400">Trip Transfer Duration</span>
                <span className="text-2xl font-black text-slate-200 mt-1">{result.transfer_time_days.toFixed(2)} days</span>
              </div>
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[10px] uppercase font-bold text-slate-400">Total Firing Energy</span>
                <span className="text-xl font-bold text-slate-200 mt-1">{result.power_consumed_kwh.toFixed(1)} kWh</span>
              </div>
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[10px] uppercase font-bold text-slate-400">Thermal Output</span>
                <span className="text-xl font-bold text-slate-200 mt-1">{result.thermal_load_w.toFixed(1)} W</span>
              </div>
            </div>

            <div className="p-4 bg-slate-950/60 rounded-lg border border-slate-800/80 mt-auto flex items-start gap-3">
              <div className="p-2 bg-aerospace-emerald/10 rounded border border-aerospace-emerald/30 text-aerospace-emerald">
                <CheckCircle className="w-5 h-5" />
              </div>
              <div>
                <span className="text-[10px] uppercase font-bold text-slate-400">Trajectory Probability Success</span>
                <div className="text-xl font-black text-slate-200">{(result.success_probability * 100).toFixed(1)}%</div>
                <p className="text-[11px] text-slate-400 mt-0.5">Calculated using operational hours degradation and safety margins.</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="glass-panel p-6 rounded-xl flex-1 flex flex-col items-center justify-center text-slate-500 text-sm gap-2">
            <Compass className="w-10 h-10 text-slate-700 animate-pulse" />
            Perform simulations to solve transfer trajectories.
          </div>
        )}
      </div>
    </div>
  );
};
