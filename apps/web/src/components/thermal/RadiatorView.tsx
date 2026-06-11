import React from 'react';
import { Card } from '../common/Card';

export function RadiatorView({ reqArea, activeArea }: { reqArea: number; activeArea: number }) {
  const margin = activeArea - reqArea;
  const status = margin >= 0 ? 'ok' : 'crit';

  return (
    <Card title="Radiator Heat Rejection">
      <div className="flex flex-col gap-3 font-mono text-xs">
        <div className="flex justify-between">
          <span className="text-slate-500">REQUIRED AREA</span>
          <span className="font-bold text-slate-300">{reqArea.toFixed(2)} m²</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">INSTALLED RADIATOR</span>
          <span className="font-bold text-slate-300">{activeArea.toFixed(2)} m²</span>
        </div>
        <div className="h-px bg-space-800" />
        <div className="flex justify-between items-center">
          <span className="text-slate-500">THERMAL AREA MARGIN</span>
          <span className={`font-bold text-sm ${status === 'ok' ? 'text-emerald-400' : 'text-red-400'}`}>
            {margin >= 0 ? `+${margin.toFixed(2)} m²` : `${margin.toFixed(2)} m²`}
          </span>
        </div>
      </div>
    </Card>
  );
}
