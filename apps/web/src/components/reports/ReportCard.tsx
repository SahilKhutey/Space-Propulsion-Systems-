import React from 'react';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';
import { FileText, Download } from 'lucide-react';

export function ReportCard({ name, date, size, type, onDownload }:
  { name: string; date: string; size: string; type: string; onDownload: () => void }) {
  return (
    <Card>
      <div className="flex items-center justify-between font-mono text-xs">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded bg-space-800 border border-space-700 text-plasma-400">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <div className="font-sans font-semibold text-slate-200 text-sm">{name}</div>
            <div className="text-[10px] text-slate-500 mt-0.5">{date} | {size}</div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge color="slate">{type}</Badge>
          <button onClick={onDownload} className="p-1.5 rounded bg-space-850 hover:bg-space-800 text-slate-400 hover:text-white border border-space-800 transition">
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>
    </Card>
  );
}
