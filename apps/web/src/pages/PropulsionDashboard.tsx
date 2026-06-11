import React, { useState, useEffect } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { EngineConfigPanel } from '@/components/propulsion/EngineConfigPanel';
import { ThrustGauge } from '@/components/gauges/ThrustGauge';
import { EfficiencyGauge } from '@/components/gauges/EfficiencyGauge';
import { PropellantFlow } from '@/components/propulsion/PropellantFlow';
import { PlumeVisualization } from '@/components/orbit/PlumeVisualization';
import { api } from '@/api/client';
import { ThrusterPerformanceResult } from '@/types';

export default function PropulsionDashboard() {
  const [type, setType] = useState('hall_thruster');
  const [power, setPower] = useState(5000);
  const [isp, setIsp] = useState(2000);
  const [efficiency, setEfficiency] = useState(0.60);
  const [results, setResults] = useState<ThrusterPerformanceResult | null>(null);

  const handleCompute = async () => {
    const data = await api.computeThrust({
      thruster_type: type,
      power_w: power,
      isp_s: isp,
      efficiency: efficiency,
    });
    setResults(data);
  };

  useEffect(() => {
    handleCompute();
  }, [type, power, isp, efficiency]);

  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Propulsion Design Workspace"
        subtitle="Configure physical thruster designs and evaluate performance metrics"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Sliders Panel */}
        <div className="lg:col-span-1">
          <EngineConfigPanel
            type={type} setType={setType}
            power={power} setPower={setPower}
            isp={isp} setIsp={setIsp}
            efficiency={efficiency} setEfficiency={setEfficiency}
            onRun={handleCompute}
          />
        </div>

        {/* Live Gauges & Plume */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="panel p-4 flex items-center justify-center">
              <ThrustGauge thrust_n={results?.thrust_n ?? 0.0} />
            </div>
            <div className="panel p-4 flex items-center justify-center">
              <EfficiencyGauge eta={results?.efficiency ?? 0.6} />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4">
            <PropellantFlow mdot={results?.mass_flow_kg_s ?? 0.0} />
            <PlumeVisualization thrust_n={results?.thrust_n ?? 0.0} power_w={power} />
          </div>
        </div>
      </div>
    </div>
  );
}
