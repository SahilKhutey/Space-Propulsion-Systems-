import React, { useState, useEffect } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { PowerFlowDiagram } from '@/components/power/PowerFlowDiagram';
import { PowerChart } from '@/components/charts/PowerChart';
import { BatteryGauge } from '@/components/gauges/BatteryGauge';
import { Card } from '@/components/common/Card';

export default function PowerDashboard() {
  const [solar, setSolar] = useState(1500.0);
  const [load, setLoad] = useState(850.0);
  const [batteryFlow, setBatteryFlow] = useState(650.0);
  const [soc, setSoc] = useState(0.85);
  const [chartData, setChartData] = useState<any[]>([]);

  useEffect(() => {
    // Generate power chart data representing LEO orbital daylight and eclipses
    const list = [];
    for (let i = 0; i < 30; i++) {
      const isEclipse = i > 12 && i < 22;
      const sol = isEclipse ? 0.0 : 1500.0;
      const l = 800.0 + (i % 3 === 0 ? 400.0 : 0.0); // system loads
      const flow = sol - l;
      list.push({
        t: i * 3,
        solar: sol,
        load: l,
        soc: Math.max(20, Math.min(100, 85 + (flow * i) / 500)),
      });
    }
    setChartData(list);
  }, []);

  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Electrical Power Workspace"
        subtitle="Manage spacecraft power balances, eclipse shadow logs, and battery energy margins"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Power Flow Diagram & Recharts Area */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          <PowerFlowDiagram solar_w={solar} load_w={load} battery_flow_w={batteryFlow} />
          <Card title="LEO Orbital Power Profile (Daylight vs Eclipse)">
            <PowerChart data={chartData} />
          </Card>
        </div>

        {/* Battery Ring Widget */}
        <div className="lg:col-span-1 flex flex-col gap-4">
          <Card title="Battery Storage Unit" className="flex flex-col items-center justify-center py-6">
            <BatteryGauge soc={soc} />
            <div className="mt-4 font-mono text-xs text-slate-400 text-center flex flex-col gap-1 w-full border-t border-space-850 pt-4">
              <div className="flex justify-between px-4">
                <span>VOLTAGE</span>
                <span className="font-bold text-slate-300">28.4 V</span>
              </div>
              <div className="flex justify-between px-4">
                <span>CURRENT FLOW</span>
                <span className="font-bold text-slate-300">22.8 A</span>
              </div>
              <div className="flex justify-between px-4">
                <span>CAPACITY</span>
                <span className="font-bold text-slate-300">5000 Wh</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
