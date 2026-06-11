import React from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card } from '@/components/common/Card';

export default function Settings() {
  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Settings & Parameters"
        subtitle="Configure system credentials and ground sync details"
      />

      <Card title="Ground Station Sync API">
        <div className="flex flex-col gap-3 font-mono text-xs text-slate-400">
          <div className="flex justify-between bg-space-950/30 p-2 rounded">
            <span>API SERVER BASE</span>
            <span className="font-bold text-slate-200">http://localhost:8000/api</span>
          </div>
          <div className="flex justify-between bg-space-950/30 p-2 rounded">
            <span>WEBSOCKET LINK</span>
            <span className="font-bold text-slate-200">ws://localhost:8000/ws/telemetry</span>
          </div>
        </div>
      </Card>
    </div>
  );
}
