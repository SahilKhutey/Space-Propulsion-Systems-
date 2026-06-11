import React from 'react';
import { Card } from '../common/Card';

export function StateComparison({ label, actual, simulated }:
  { label: string; actual: number; simulated: number }) {
  const diff = Math.abs(actual - simulated);
  const diffPct = simulated > 0 ? (diff / simulated) * 100 : 0;

  return (
    <Card title={`${label} Twin Comparison`}>
      <div className="flex flex-col gap-3 font-mono text-xs">
        <div className="flex justify-between">
          <span className="text-slate-500">TELEMETRY</span>
          <span className="font-bold text-slate-300">{actual.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">SIMULATION MODEL</span>
          <span className="font-bold text-slate-300">{simulated.toFixed(2)}</span>
        </div>
        <div className="h-px bg-space-800" />
        <div className="flex justify-between items-center">
          <span className="text-slate-500">ABS DEVIATION</span>
          <span className={`font-bold ${diffPct > 5 ? 'text-red-400 animate-pulse' : 'text-emerald-400'}`}>
            {diff.toFixed(2)} ({diffPct.toFixed(1)}%)
          </span>
        </div>
      </div>
    </Card>
  );
}
