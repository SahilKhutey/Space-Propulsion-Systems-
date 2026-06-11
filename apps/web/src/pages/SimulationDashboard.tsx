import React from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card } from '@/components/common/Card';
import { Badge } from '@/components/common/Badge';

export default function SimulationDashboard() {
  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Simulation Logs"
        subtitle="View and download historical simulation trajectories"
      />

      <Card title="Completed Simulations">
        <div className="flex flex-col gap-3 font-mono text-xs">
          <div className="panel p-3 bg-space-950/40 border-space-850 hover:bg-space-900/30 flex justify-between items-center transition">
            <div>
              <div className="font-sans font-bold text-slate-200">GEO Orbit Raising Study #SIM-4029</div>
              <div className="text-[10px] text-slate-500 mt-0.5">HET / Xenon / 5.0 kW | 2026-06-11</div>
            </div>
            <Badge color="ok">COMPLETED</Badge>
          </div>

          <div className="panel p-3 bg-space-950/40 border-space-850 hover:bg-space-900/30 flex justify-between items-center transition">
            <div>
              <div className="font-sans font-bold text-slate-200">VASIMR Spirals #SIM-4028</div>
              <div className="text-[10px] text-slate-500 mt-0.5">VASIMR / Argon / 200.0 kW | 2026-06-10</div>
            </div>
            <Badge color="ok">COMPLETED</Badge>
          </div>
        </div>
      </Card>
    </div>
  );
}
