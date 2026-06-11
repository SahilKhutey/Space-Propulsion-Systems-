import React, { useState } from 'react';
import { api } from '../api/client';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { ShieldCheck, Flame, Cpu } from 'lucide-react';

export const IspModule: React.FC = () => {
  const [propellantMass, setPropellantMass] = useState(250);
  const [dryMass, setDryMass] = useState(800);
  const [thrust, setThrust] = useState(0.25);
  const [isp, setIsp] = useState(2500);

  const [loading, setLoading] = useState(false);
  const [lifetimeYears, setLifetimeYears] = useState<number | null>(null);
  const [deltaV, setDeltaV] = useState<number | null>(null);

  const runCalculations = async () => {
    setLoading(true);
    try {
      const years = propellantMass / (thrust / (isp * 9.80665)) / (365.25 * 24 * 3600);
      const dv = isp * 9.80665 * Math.log((propellantMass + dryMass) / dryMass);
      setLifetimeYears(years);
      setDeltaV(dv);
    } finally {
      setLoading(false);
    }
  };

  const chartData = [
    { name: 'Chemical Biprop', isp: 310 },
    { name: 'NTR', isp: 900 },
    { name: 'Hall Effect', isp: 2000 },
    { name: 'Gridded Ion', isp: 3500 },
    { name: 'VASIMR', isp: 8000 }
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 h-full">
      <div className="lg:col-span-5 flex flex-col gap-6">
        <div className="glass-panel p-6 rounded-xl flex flex-col gap-5 flex-1">
          <div>
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Cpu className="w-5 h-5 text-aerospace-cyan" />
              Efficiency & Fuel Sizing
            </h3>
            <p className="text-xs text-slate-400">Calculate propellant lifecycle and delta-V potential.</p>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-slate-300">Propellant Budget (kg)</label>
            <input
              type="number" value={propellantMass} onChange={(e) => setPropellantMass(Number(e.target.value))}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-aerospace-cyan"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-slate-300">Dry Spacecraft Mass (kg)</label>
            <input
              type="number" value={dryMass} onChange={(e) => setDryMass(Number(e.target.value))}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-slate-300">Specific Impulse (Isp - seconds)</label>
            <input
              type="number" value={isp} onChange={(e) => setIsp(Number(e.target.value))}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-slate-300">Thrust Level (N)</label>
            <input
              type="number" step="0.01" value={thrust} onChange={(e) => setThrust(Number(e.target.value))}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2.5 text-sm text-slate-200 focus:outline-none"
            />
          </div>

          <button
            onClick={runCalculations} disabled={loading}
            className="w-full mt-auto py-3 bg-gradient-to-r from-aerospace-blue to-aerospace-cyan text-space-950 font-bold uppercase rounded-lg text-sm transition-all hover:opacity-90 active:scale-95"
          >
            Compute Sizing Curves
          </button>
        </div>
      </div>

      <div className="lg:col-span-7 flex flex-col gap-6">
        {deltaV !== null && lifetimeYears !== null && (
          <div className="glass-panel p-6 rounded-xl flex flex-col gap-6 animate-fade-in">
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-aerospace-cyan" />
              Sizing Outcomes
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[10px] uppercase font-bold text-slate-400">Total Delta-V Achievable</span>
                <span className="text-2xl font-black text-slate-200 mt-1">{deltaV.toFixed(1)} m/s</span>
              </div>
              <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-lg flex flex-col">
                <span className="text-[10px] uppercase font-bold text-slate-400">Max Active Thrust Lifetime</span>
                <span className="text-2xl font-black text-slate-200 mt-1">{lifetimeYears.toFixed(2)} years</span>
              </div>
            </div>
          </div>
        )}

        <div className="glass-panel p-6 rounded-xl flex-1 flex flex-col gap-4">
          <div>
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Flame className="w-5 h-5 text-aerospace-cyan" />
              Technology Isp Comparison
            </h3>
            <p className="text-xs text-slate-400">Specific Impulse curves across chemical, nuclear, and electric propulsion technologies.</p>
          </div>
          <div className="flex-1 min-h-[200px] w-full text-xs">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                <XAxis dataKey="name" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1f2937' }} />
                <Bar dataKey="isp" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
