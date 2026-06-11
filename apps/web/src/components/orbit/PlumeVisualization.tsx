import React from 'react';

export function PlumeVisualization({ thrust_n, power_w }: { thrust_n: number; power_w: number }) {
  const plumeLength = Math.min(200, 50 + thrust_n * 150);
  const opacity = Math.min(1.0, 0.2 + power_w / 100000);
  const color = power_w > 50000 ? 'from-cyan-400 to-transparent' : 'from-indigo-400 to-transparent';

  return (
    <div className="w-full h-40 bg-space-900/50 rounded-xl border border-space-800 flex items-center justify-center relative overflow-hidden grid-bg">
      <div className="absolute left-8 flex items-center gap-2">
        <div className="w-16 h-16 bg-slate-800 border-2 border-slate-700 rounded-md flex items-center justify-center font-mono text-[10px] text-slate-400">
          THRUSTER
        </div>
        <div className="flex flex-col gap-0.5">
          <div
            className={`h-6 rounded-r-full bg-gradient-to-r ${color}`}
            style={{ width: `${plumeLength}px`, opacity }}
          />
        </div>
      </div>
      <div className="absolute right-4 bottom-2 text-right font-mono text-[10px] text-slate-500">
        <div>Plume Length: {(plumeLength / 100).toFixed(2)} m</div>
        <div>Intensity: {Math.round(opacity * 100)}%</div>
      </div>
    </div>
  );
}
