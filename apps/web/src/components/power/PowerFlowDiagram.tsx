import React from 'react';
import { Card } from '../common/Card';

export function PowerFlowDiagram({ solar_w, load_w, battery_flow_w }:
  { solar_w: number; load_w: number; battery_flow_w: number }) {
  
  const batteryCharging = battery_flow_w >= 0;

  return (
    <Card title="Electrical System Power Flow">
      <div className="flex flex-col md:flex-row items-center justify-around gap-6 py-6 relative">
        <div className="panel p-4 flex flex-col items-center gap-1.5 bg-amber-500/10 border-amber-500/30 w-32 shadow-[0_0_8px_rgba(245,158,11,0.2)]">
          <span className="text-[10px] text-slate-500 uppercase font-mono font-bold">SOLAR ARRAYS</span>
          <span className="font-mono text-base font-bold text-amber-400">+{solar_w.toFixed(1)} W</span>
        </div>

        <div className="w-8 h-8 rounded-full bg-space-800 flex items-center justify-center font-mono text-xs text-slate-400 font-bold border border-space-700">
          BUS
        </div>

        <div className="flex flex-col gap-3">
          <div className={`panel p-3 flex flex-col items-center gap-1 w-32 ${batteryCharging ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-red-500/10 border-red-500/30'}`}>
            <span className="text-[10px] text-slate-500 uppercase font-mono font-bold">BATTERY</span>
            <span className={`font-mono text-sm font-bold ${batteryCharging ? 'text-emerald-400' : 'text-red-400'}`}>
              {batteryCharging ? `+${battery_flow_w.toFixed(1)} W` : `${battery_flow_w.toFixed(1)} W`}
            </span>
          </div>

          <div className="panel p-3 flex flex-col items-center gap-1 bg-cyan-500/10 border-cyan-500/30 w-32">
            <span className="text-[10px] text-slate-500 uppercase font-mono font-bold">SYSTEM LOAD</span>
            <span className="font-mono text-sm font-bold text-cyan-400">-{load_w.toFixed(1)} W</span>
          </div>
        </div>
      </div>
    </Card>
  );
}
