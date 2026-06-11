import React from 'react';
import { Card } from '../common/Card';

export function OptimizationProgress({ currentGen, totalGen }:
  { currentGen: number; totalGen: number }) {
  const pct = Math.min(100, (currentGen / totalGen) * 100);

  return (
    <Card title="Genetic Optimization Search">
      <div className="flex flex-col gap-3 font-mono text-xs py-2">
        <div className="flex justify-between items-baseline">
          <span className="text-slate-500">SEARCH GENERATION</span>
          <span className="font-bold text-slate-300">GEN {currentGen} / {totalGen}</span>
        </div>
        
        <div className="w-full h-2 bg-space-900 rounded-full overflow-hidden border border-space-800">
          <div className="h-full bg-plasma-500 rounded-full transition-all duration-300 shadow-[0_0_8px_rgba(6,182,212,0.4)]" style={{ width: `${pct}%` }} />
        </div>
      </div>
    </Card>
  );
}
