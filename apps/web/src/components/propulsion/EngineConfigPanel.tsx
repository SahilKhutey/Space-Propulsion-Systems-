import React from 'react';
import { Card } from '../common/Card';

interface EngineConfigPanelProps {
  type: string;
  setType: (v: string) => void;
  power: number;
  setPower: (v: number) => void;
  isp: number;
  setIsp: (v: number) => void;
  efficiency: number;
  setEfficiency: (v: number) => void;
  onRun: () => void;
}

export function EngineConfigPanel({
  type, setType,
  power, setPower,
  isp, setIsp,
  efficiency, setEfficiency,
  onRun
}: EngineConfigPanelProps) {
  return (
    <Card title="Engine Design Configuration">
      <div className="flex flex-col gap-4 text-xs font-mono">
        <div className="flex flex-col gap-1.5">
          <label className="text-slate-400">THRUSTER TYPE</label>
          <select
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="panel p-2 bg-space-950 text-slate-200 border-space-800"
          >
            <option value="hall_thruster">Hall Effect Thruster</option>
            <option value="ion_thruster">Gridded Ion Engine</option>
            <option value="VASIMR">VASIMR Plasma Thruster</option>
            <option value="MPD">MPD Magnetoplasmadynamic</option>
          </select>
        </div>

        <div className="flex flex-col gap-1.5">
          <div className="flex justify-between">
            <label className="text-slate-400">POWER LEVEL</label>
            <span className="text-plasma-400">{power} W</span>
          </div>
          <input
            type="range" min="100" max="50000" step="100"
            value={power}
            onChange={(e) => setPower(Number(e.target.value))}
            className="w-full h-1.5 bg-space-900 rounded-lg appearance-none cursor-pointer accent-plasma-400"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <div className="flex justify-between">
            <label className="text-slate-400">SPECIFIC IMPULSE (ISP)</label>
            <span className="text-plasma-400">{isp} s</span>
          </div>
          <input
            type="range" min="1000" max="8000" step="50"
            value={isp}
            onChange={(e) => setIsp(Number(e.target.value))}
            className="w-full h-1.5 bg-space-900 rounded-lg appearance-none cursor-pointer accent-plasma-400"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <div className="flex justify-between">
            <label className="text-slate-400">EFFICIENCY (η)</label>
            <span className="text-plasma-400">{Math.round(efficiency * 100)} %</span>
          </div>
          <input
            type="range" min="0.1" max="0.9" step="0.01"
            value={efficiency}
            onChange={(e) => setEfficiency(Number(e.target.value))}
            className="w-full h-1.5 bg-space-900 rounded-lg appearance-none cursor-pointer accent-plasma-400"
          />
        </div>

        <button
          onClick={onRun}
          className="btn btn-primary w-full mt-2 font-display text-sm flex items-center justify-center gap-1 hover:brightness-110"
        >
          EXECUTE DESIGN STUDY
        </button>
      </div>
    </Card>
  );
}
