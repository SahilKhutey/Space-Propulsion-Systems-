import React from 'react';
import { Card } from '../common/Card';

export interface ThermalComponent {
  name: string;
  currentTemp: number;
  maxTemp: number;
}

export function ComponentTable({ components }: { components: ThermalComponent[] }) {
  return (
    <Card title="Spacecraft Components Thermal Margin">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse font-mono text-xs">
          <thead>
            <tr className="border-b border-space-800 text-slate-500">
              <th className="py-2">COMPONENT</th>
              <th className="py-2">TEMP</th>
              <th className="py-2">LIMIT</th>
              <th className="py-2 text-right">MARGIN</th>
            </tr>
          </thead>
          <tbody>
            {components.map((c) => {
              const margin = c.maxTemp - c.currentTemp;
              const color = margin < 10 ? 'text-red-400 font-bold animate-pulse' : margin < 25 ? 'text-amber-400' : 'text-emerald-400';
              return (
                <tr key={c.name} className="border-b border-space-850 hover:bg-space-900/30">
                  <td className="py-2 font-sans font-semibold text-slate-200">{c.name}</td>
                  <td className="py-2 text-slate-300">{c.currentTemp.toFixed(1)} K</td>
                  <td className="py-2 text-slate-400">{c.maxTemp.toFixed(1)} K</td>
                  <td className={`py-2 text-right ${color}`}>{margin.toFixed(1)} K</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
