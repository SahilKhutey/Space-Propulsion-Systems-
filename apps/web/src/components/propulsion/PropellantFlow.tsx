import React from 'react';
import { Card } from '../common/Card';

export function PropellantFlow({ mdot }: { mdot: number }) {
  const flow_mg = mdot * 1e6;

  return (
    <Card title="Propellant Supply Channel">
      <div className="flex flex-col gap-4 py-3 text-xs font-mono">
        <div className="flex items-center justify-between">
          <span className="text-slate-500">PROPELLANT TYPE</span>
          <span className="font-bold text-slate-300">Xenon (Xe)</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-slate-500">MASS FLOW RATE</span>
          <span className="font-bold text-plasma-400">{flow_mg.toFixed(3)} mg/s</span>
        </div>
        
        <div className="w-full h-3 bg-space-900 rounded-full overflow-hidden border border-space-800 relative">
          {flow_mg > 0 && (
            <div className="h-full bg-gradient-to-r from-plasma-400 to-cyan-500 rounded-full animate-flow w-full"
                 style={{
                   backgroundSize: '30px 100%',
                   backgroundImage: 'linear-gradient(90deg, rgba(6,182,212,0.6) 25%, transparent 25%, transparent 50%, rgba(6,182,212,0.6) 50%, rgba(6,182,212,0.6) 75%, transparent 75%, transparent)'
                 }}
            />
          )}
        </div>
      </div>
    </Card>
  );
}
