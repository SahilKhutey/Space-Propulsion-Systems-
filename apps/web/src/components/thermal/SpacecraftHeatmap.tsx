import React from 'react';

export function SpacecraftHeatmap({ temperatures }: { temperatures: number[] }) {
  const getTempColor = (t: number) => {
    if (!t) return 'bg-slate-700';
    const c = t - 273.15;
    if (c > 70) return 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)] border border-red-400';
    if (c > 40) return 'bg-amber-500 border border-amber-400';
    if (c > 10) return 'bg-emerald-500 border border-emerald-400';
    return 'bg-blue-500 border border-blue-400';
  };

  const getTempLabel = (t: number) => {
    if (!t) return 'N/A';
    return `${(t - 273.15).toFixed(1)}°C`;
  };

  return (
    <div className="w-full p-4 bg-space-900/40 rounded-xl border border-space-800 flex flex-col gap-4">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {temperatures.map((t, idx) => (
          <div key={idx} className="panel p-3 flex flex-col items-center gap-1.5 bg-space-950/40">
            <span className="text-[10px] text-slate-500 font-mono font-bold">NODE_{idx}</span>
            <div className={`w-6 h-6 rounded-full ${getTempColor(t)}`} />
            <span className="font-mono text-xs text-slate-300 font-semibold">{getTempLabel(t)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
