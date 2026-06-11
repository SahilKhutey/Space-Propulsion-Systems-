import React, { useState, useEffect } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { SpacecraftHeatmap } from '@/components/thermal/SpacecraftHeatmap';
import { ThermalChart } from '@/components/charts/ThermalChart';
import { RadiatorView } from '@/components/thermal/RadiatorView';
import { ComponentTable, ThermalComponent } from '@/components/thermal/ComponentTable';
import { api } from '@/api/client';

export default function ThermalDashboard() {
  const [temps, setTemps] = useState<number[]>([295.15, 305.15, 320.15, 290.15, 298.15, 310.15, 335.15, 285.15]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [radiatorReq, setRadiatorReq] = useState(0.85);

  const components: ThermalComponent[] = [
    { name: 'Thruster Node 0', currentTemp: temps[0], maxTemp: 373.15 },
    { name: 'Core Avionics Node 1', currentTemp: temps[1], maxTemp: 343.15 },
    { name: 'Battery Array Node 2', currentTemp: temps[2], maxTemp: 323.15 },
    { name: 'Solar Junction Node 3', currentTemp: temps[3], maxTemp: 353.15 },
  ];

  useEffect(() => {
    // Generate transient chart data
    const list = [];
    for (let i = 0; i < 20; i++) {
      list.push({
        t: i * 60,
        node_0: 290 + 5 * Math.sin(i / 2) + i * 0.5,
        node_1: 300 + 3 * Math.cos(i / 3) + i * 0.3,
        node_2: 310 + 2 * Math.sin(i / 4) + i * 0.2,
        node_3: 285 + 4 * Math.cos(i / 2) + i * 0.1,
      });
    }
    setChartData(list);
  }, []);

  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Thermal Monitor Center"
        subtitle="Analyze spacecraft radiative heat balances, radiator area requirements, and critical component margins"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Heat Map and Component Table */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          <SpacecraftHeatmap temperatures={temps} />
          <div className="panel p-4">
            <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-3">Transient Node Temperature Curve</h3>
            <ThermalChart data={chartData} nodeNames={['node_0', 'node_1', 'node_2', 'node_3']} />
          </div>
        </div>

        {/* Radiator and Margins */}
        <div className="lg:col-span-1 flex flex-col gap-4">
          <RadiatorView reqArea={radiatorReq} activeArea={1.2} />
          <ComponentTable components={components} />
        </div>
      </div>
    </div>
  );
}
