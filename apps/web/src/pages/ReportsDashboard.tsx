import React, { useState } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { ReportCard } from '@/components/reports/ReportCard';
import { ReportViewer } from '@/components/reports/ReportViewer';

export default function ReportsDashboard() {
  const [content] = useState(
    '# Executive Mission Report Summary\n## GEO Spiraling Feasibility\n* Propulsion: Hall Effect Thruster (Nominal)\n* Propellant Mass: 240.2 kg\n* Transfer Time: 120.5 days\n* Status: FEASIBLE\n\nThis mission design spiraling is calculated with full J2 orbital drift coordinates and Stefan-Boltzmann radiative cooling constants.'
  );

  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Engineering Reports & Documents"
        subtitle="Manage compile-logs, sizing summaries, and trade study reports"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-1 flex flex-col gap-3">
          <ReportCard
            name="GEO Orbit Raising Study"
            date="2026-06-11"
            size="24 KB"
            type="PDF"
            onDownload={() => console.log('Downloading...')}
          />
          <ReportCard
            name="VASIMR Deep Space Study"
            date="2026-06-10"
            size="42 KB"
            type="LaTeX"
            onDownload={() => console.log('Downloading...')}
          />
        </div>

        <div className="lg:col-span-2">
          <ReportViewer markdownContent={content} />
        </div>
      </div>
    </div>
  );
}
