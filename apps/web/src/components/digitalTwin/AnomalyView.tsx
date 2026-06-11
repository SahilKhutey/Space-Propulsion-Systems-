import React from 'react';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';

export function AnomalyView({ anomalies }: { anomalies: string[] }) {
  return (
    <Card title="Signal Anomaly Log">
      <div className="flex flex-col gap-2 max-h-48 overflow-y-auto font-mono text-xs pr-1">
        {anomalies.length === 0 ? (
          <div className="text-slate-500 text-center py-4 uppercase">No anomalies detected. Signals nominal.</div>
        ) : (
          anomalies.map((a, i) => (
            <div key={i} className="panel p-2 bg-red-500/10 border-red-500/30 flex justify-between items-center">
              <span className="text-red-400 font-semibold">{a}</span>
              <Badge color="crit">CRITICAL</Badge>
            </div>
          ))
        )}
      </div>
    </Card>
  );
}
