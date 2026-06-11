import React from 'react';
import { Card } from '../common/Card';

export function ReportViewer({ markdownContent }: { markdownContent: string }) {
  return (
    <Card title="Report Summary Preview">
      <div className="panel p-4 bg-space-950/40 min-h-[300px] font-sans text-xs text-slate-300 leading-relaxed border border-space-850 overflow-y-auto">
        <div className="prose prose-invert max-w-none">
          {markdownContent.split('\n').map((line, idx) => {
            if (line.startsWith('# ')) return <h1 key={idx} className="text-lg font-bold text-white mb-3 mt-4">{line.replace('# ', '')}</h1>;
            if (line.startsWith('## ')) return <h2 key={idx} className="text-base font-bold text-white mb-2 mt-3">{line.replace('## ', '')}</h2>;
            if (line.startsWith('* ') || line.startsWith('- ')) return <li key={idx} className="ml-4 list-disc mb-1">{line.substring(2)}</li>;
            return <p key={idx} className="mb-2">{line}</p>;
          })}
        </div>
      </div>
    </Card>
  );
}
