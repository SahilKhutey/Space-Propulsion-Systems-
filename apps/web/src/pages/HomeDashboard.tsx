import React from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card } from '@/components/common/Card';
import { KPICard } from '@/components/common/KPICard';
import { AlertBanner } from '@/components/common/AlertBanner';
import { Activity, Layers, Cpu, Bell } from 'lucide-react';

export default function HomeDashboard() {
  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Mission Control Center"
        subtitle="PropSim System Overview & Telemetry Monitor"
      />

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard label="Active Projects" value="4" icon={Layers} color="plasma" />
        <KPICard label="Running Missions" value="2" icon={Activity} color="ok" />
        <KPICard label="Simulations Run" value="142" icon={Cpu} color="thrust" />
        <KPICard label="Active Anomalies" value="0" icon={Bell} color="ok" />
      </div>

      {/* Main Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Active Projects Widget */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          <Card title="Active Engineering Projects">
            <div className="flex flex-col gap-3 font-mono text-xs">
              <div className="panel p-3 bg-space-950/40 border-space-850 hover:bg-space-900/30 flex justify-between items-center transition">
                <div>
                  <div className="font-sans font-bold text-slate-200">GEO Orbit Raising spiraling</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">HET / Xenon / 5.0 kW</div>
                </div>
                <span className="text-emerald-400 font-semibold">LEO → GEO Spiraling (45%)</span>
              </div>

              <div className="panel p-3 bg-space-950/40 border-space-850 hover:bg-space-900/30 flex justify-between items-center transition">
                <div>
                  <div className="font-sans font-bold text-slate-200">Deep Space Gateway Stationkeeping</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Ion / Krypton / 3.2 kW</div>
                </div>
                <span className="text-emerald-400 font-semibold">Halo Orbit Nominal</span>
              </div>
            </div>
          </Card>

          <Card title="Recent Simulation Runs">
            <div className="overflow-x-auto font-mono text-xs">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-space-800 text-slate-500">
                    <th className="py-2">RUN ID</th>
                    <th className="py-2">ENGINE</th>
                    <th className="py-2">ISP</th>
                    <th className="py-2">THRUST</th>
                    <th className="py-2 text-right">STATUS</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-space-850 text-slate-300">
                    <td className="py-2">#SIM-4029</td>
                    <td>Hall Effect V2</td>
                    <td>2150 s</td>
                    <td>0.385 N</td>
                    <td className="py-2 text-right text-emerald-400">NOMINAL</td>
                  </tr>
                  <tr className="border-b border-space-850 text-slate-300">
                    <td className="py-2">#SIM-4028</td>
                    <td>VASIMR spirals</td>
                    <td>5000 s</td>
                    <td>1.250 N</td>
                    <td className="py-2 text-right text-emerald-400">NOMINAL</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </Card>
        </div>

        {/* Alert Log Widget */}
        <div className="lg:col-span-1">
          <Card title="System Telemetry Alert Log">
            <div className="flex flex-col gap-2">
              <AlertBanner
                kind="ok"
                title="Ground Sync Nominal"
                message="WebSocket telemetry connection synchronized successfully with UKF state estimator."
              />
              <AlertBanner
                kind="info"
                title="Simulation Engine V3.0"
                message="Predictive J2 propagation solver active. Precision bounds capped at 1.0e-6."
              />
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
