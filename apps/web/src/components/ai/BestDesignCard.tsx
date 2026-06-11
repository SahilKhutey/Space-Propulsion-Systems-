import React from 'react';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';

export interface OptimizedParameters {
  thruster_type: string;
  efficiency: number;
  isp_s: number;
  power_w: number;
  thrust_n: number;
}

export function BestDesignCard({ params }: { params: OptimizedParameters }) {
  return (
    <Card title="Optimal Design Candidate" glow="cyan">
      <div className="flex flex-col gap-3 font-mono text-xs">
        <div className="flex justify-between items-center">
          <span className="text-slate-500">ENGINE MODEL</span>
          <Badge color="plasma">{params.thruster_type}</Badge>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">EFFICIENCY (η)</span>
          <span className="font-bold text-emerald-400">{Math.round(params.efficiency * 100)}%</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">SPECIFIC IMPULSE</span>
          <span className="font-bold text-slate-300">{Math.round(params.isp_s)} s</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">POWER ALLOCATION</span>
          <span className="font-bold text-slate-300">{Math.round(params.power_w)} W</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">OPTIMIZED THRUST</span>
          <span className="font-bold text-amber-400">{params.thrust_n.toFixed(4)} N</span>
        </div>
      </div>
    </Card>
  );
}
