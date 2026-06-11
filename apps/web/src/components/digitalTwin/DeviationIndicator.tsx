import React from 'react';
import { Card } from '../common/Card';

export function DeviationIndicator({ distance_error_km }: { distance_error_km: number }) {
  const pct = Math.min(100, (distance_error_km / 3.0) * 100);
  const color = distance_error_km > 2.0 ? 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.5)]' : distance_error_km > 0.5 ? 'bg-amber-500' : 'bg-emerald-500';

  return (
    <Card title="Orbit Position Error (Deviation)">
      <div className="flex flex-col gap-3 font-mono text-xs py-2">
        <div className="flex justify-between items-baseline">
          <span className="text-slate-500">DEVIATION DISTANCE</span>
          <span className="font-bold text-sm text-slate-300">{distance_error_km.toFixed(3)} km</span>
        </div>
        
        <div className="w-full h-3 bg-space-900 rounded-full overflow-hidden border border-space-800">
          <div className={`h-full rounded-full transition-all duration-500 ${color}`} style={{ width: `${pct}%` }} />
        </div>

        <div className="flex justify-between text-[10px] text-slate-600">
          <span>0 km</span>
          <span>1 km</span>
          <span>2 km</span>
          <span>3 km+</span>
        </div>
      </div>
    </Card>
  );
}
