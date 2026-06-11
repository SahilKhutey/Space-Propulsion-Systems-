import React from 'react';
import { Card } from '../common/Card';

export function TelemetryView({ actual, estimated }: { actual: number[]; estimated: number[] }) {
  return (
    <Card title="Live Telemetry Vectors [X, Y, Z]">
      <div className="flex flex-col gap-4 font-mono text-xs">
        <div className="flex flex-col gap-1.5">
          <span className="text-slate-500 uppercase font-bold text-[10px]">Actual Spacecraft telemetry</span>
          <div className="panel p-2 bg-space-950/40 text-slate-300 flex justify-between">
            <span>X: {actual[0]?.toFixed(1) ?? '0.0'} m</span>
            <span>Y: {actual[1]?.toFixed(1) ?? '0.0'} m</span>
            <span>Z: {actual[2]?.toFixed(1) ?? '0.0'} m</span>
          </div>
        </div>

        <div className="flex flex-col gap-1.5">
          <span className="text-plasma-400 uppercase font-bold text-[10px]">Unscented Kalman Filter state estimate</span>
          <div className="panel p-2 bg-plasma-950/10 border-plasma-500/20 text-plasma-300 flex justify-between">
            <span>X: {estimated[0]?.toFixed(1) ?? '0.0'} m</span>
            <span>Y: {estimated[1]?.toFixed(1) ?? '0.0'} m</span>
            <span>Z: {estimated[2]?.toFixed(1) ?? '0.0'} m</span>
          </div>
        </div>
      </div>
    </Card>
  );
}
