import React, { useState } from 'react';
import { api } from '../api/client';
import { ThermalResult } from '../types';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Thermometer, ShieldAlert, CheckCircle } from 'lucide-react';

export const ThermalModule: React.FC = () => {
  const [power, setPower] = useState(600.0);
  const [area, setArea] = useState(0.85);
  const [emissivity, setEmissivity] = useState(0.85);
  const [solarFlux, setSolarFlux] = useState(1361.0);
  const [absorptivity, setAbsorptivity] = useState(0.3);
  const [duration, setDuration] = useState(24.0);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ThermalResult | null>(null);
  const [error, setError] = useState('');

  const handleSimulateThermal = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await api.computeThermal({
        power_dissipation_w: power,
        ambient_temp_k: 3.0,
        component_area_m2: 0.1,
        emissivity,
        radiator_area_m2: area,
        radiator_emissivity: emissivity,
        solar_irradiance_w_m2: solarFlux,
        absorptivity,
        time_hours: duration,
        time_step_s: 300.0
      });
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Thermal transient simulation failed.');
    } finally {
      setLoading(false);
    }
  };

  const getChartData = () => {
    if (!result || result.time_series.length === 0) return [];
    const node = result.time_series[0];
    return node.time_series_t.map((t, idx) => ({
      hour: (t / 3600).toFixed(1),
      temp: parseFloat((node.time_series_temp_k[idx] - 273.15).toFixed(2))
    }));
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 h-full">
      <div className="lg:col-span-5 flex flex-col">
        <form onSubmit={handleSimulateThermal} className="glass-panel p-6 rounded-xl flex flex-col gap-5 h-full">
          <div>
            <h3 className="text-lg font-bold text-slate-100 mb-1 flex items-center gap-2">
              <Thermometer className="w-5 h-5 text-aerospace-cyan" />
              Thermal Node Config
            </h3>
            <p className="text-xs text-slate-400">Model spacecraft radiative/conductive surface parameters.</p>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-slate-300">Internal Dissipation Power (W)</label>
            <input
              type="number" value={power} onChange={(e) => setPower(Number(e.target.value))}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-slate-300">Radiator Surface Area ($m^2$)</label>
            <input
              type="number" value={area} onChange={(e) => setArea(Number(e.target.value))}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-300">Emissivity ($\epsilon$)</label>
              <input
                type="number" step="0.05" value={emissivity} onChange={(e) => setEmissivity(Number(e.target.value))}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-300">Absorptivity ($\alpha$)</label>
              <input
                type="number" step="0.05" value={absorptivity} onChange={(e) => setAbsorptivity(Number(e.target.value))}
                className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
              />
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-slate-300">External Solar Irradiance ($W/m^2$)</label>
            <input
              type="number" value={solarFlux} onChange={(e) => setSolarFlux(Number(e.target.value))}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none"
            />
          </div>

          <button
            type="submit" disabled={loading}
            className="w-full mt-auto py-3 bg-gradient-to-r from-aerospace-blue to-aerospace-cyan text-space-950 font-bold uppercase rounded-lg text-sm transition-all hover:opacity-90 active:scale-95"
          >
            Solve Thermal Balance
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
                <h3 className="text-lg font-bold text-slate-100">Solver Output</h3>
                <p className="text-xs text-slate-400">Transient temperature curve computed over {duration} hours.</p>
              </div>
              <div className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1.5 ${result.safe ? 'bg-aerospace-emerald/10 text-aerospace-emerald border border-aerospace-emerald/30' : 'bg-aerospace-crimson/10 text-aerospace-crimson border border-aerospace-crimson/30'}`}>
                {result.safe ? (
                  <>
                    <CheckCircle className="w-4 h-4" />
                    <span>Safe Limits</span>
                  </>
                ) : (
                  <>
                    <ShieldAlert className="w-4 h-4" />
                    <span>Limit Exceeded</span>
                  </>
                )}
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="p-3 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[9px] uppercase font-bold text-slate-400">Min Temp</span>
                <span className="text-lg font-bold text-slate-200 mt-1">{(result.min_temp_k - 273.15).toFixed(1)}°C</span>
              </div>
              <div className="p-3 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[9px] uppercase font-bold text-slate-400">Max Temp</span>
                <span className="text-lg font-bold text-slate-200 mt-1">{(result.max_temp_k - 273.15).toFixed(1)}°C</span>
              </div>
              <div className="p-3 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[9px] uppercase font-bold text-slate-400">Steady State</span>
                <span className="text-lg font-bold text-slate-200 mt-1">{(result.steady_state_k - 273.15).toFixed(1)}°C</span>
              </div>
            </div>

            <div className="flex-1 min-h-[220px] w-full text-[10px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={getChartData()} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                  <XAxis dataKey="hour" stroke="#64748b" />
                  <YAxis stroke="#64748b" />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1f2937' }} />
                  <Line type="monotone" dataKey="temp" stroke="#06b6d4" strokeWidth={2.5} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        ) : (
          <div className="glass-panel p-6 rounded-xl flex-1 flex flex-col items-center justify-center text-slate-500 text-sm gap-2">
            <Thermometer className="w-10 h-10 text-slate-700 animate-pulse" />
            Perform simulations to solve transient thermal nodes.
          </div>
        )}
      </div>
    </div>
  );
};
