import React, { useState, useEffect } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { TelemetryView } from '@/components/digitalTwin/TelemetryView';
import { DeviationIndicator } from '@/components/digitalTwin/DeviationIndicator';
import { AnomalyView } from '@/components/digitalTwin/AnomalyView';
import { StateComparison } from '@/components/digitalTwin/StateComparison';

export default function DigitalTwinDashboard() {
  const [actualPos, setActualPos] = useState<number[]>([7000210.0, 150.0, 20.0]);
  const [estPos, setEstPos] = useState<number[]>([7000208.5, 149.0, 19.5]);
  const [deviation, setDeviation] = useState(0.002); // 2 meters
  const [anomalies, setAnomalies] = useState<string[]>([]);

  useEffect(() => {
    const interval = setInterval(() => {
      // Add small mock telemetry drift/fluctuations
      const drift = 0.5 * Math.random();
      const newDev = deviation + (Math.random() > 0.5 ? drift : -drift);
      setDeviation(Math.max(0.001, newDev));

      const newActual = [
        actualPos[0] + (Math.random() - 0.5) * 5,
        actualPos[1] + (Math.random() - 0.5) * 5,
        actualPos[2] + (Math.random() - 0.5) * 2,
      ];
      setActualPos(newActual);

      setEstPos([
        newActual[0] + (Math.random() - 0.5) * 1.5,
        newActual[1] + (Math.random() - 0.5) * 1.5,
        newActual[2] + (Math.random() - 0.5) * 0.8,
      ]);

      if (newDev > 2.0) {
        setAnomalies(['Positional trajectory drift exceeded threshold limit of 2.0 km.']);
      } else {
        setAnomalies([]);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [actualPos, deviation]);

  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Predictive Digital Twin Space"
        subtitle="Compare actual ground telemetry streams with state estimates and numerical prediction models"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Telemetry Comparison & Anomaly Log */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          <TelemetryView actual={actualPos} estimated={estPos} />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <StateComparison label="X-Position" actual={actualPos[0]} simulated={estPos[0]} />
            <StateComparison label="Y-Position" actual={actualPos[1]} simulated={estPos[1]} />
          </div>
        </div>

        {/* Deviation Indicators */}
        <div className="lg:col-span-1 flex flex-col gap-4">
          <DeviationIndicator distance_error_km={deviation} />
          <AnomalyView anomalies={anomalies} />
        </div>
      </div>
    </div>
  );
}
