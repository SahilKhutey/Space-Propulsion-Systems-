import { useState } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card } from '@/components/common/Card';
import { KPICard } from '@/components/common/KPICard';
import { Badge } from '@/components/common/Badge';
import { FileText, Download, Eye, Calendar, FileBarChart } from 'lucide-react';
import { api } from '@/api/client';

interface Report {
  id: string;
  name: string;
  type: 'propulsion' | 'mission' | 'thermal' | 'power' | 'optimization' | 'executive';
  generated: string;
  size_kb: number;
  status: 'ready' | 'generating' | 'failed';
  mission_id?: string;
}

const SAMPLE_REPORTS: Report[] = [
  { id: 'r1', name: 'DemoSat-LEO2GEO-Full-Analysis', type: 'mission',
    generated: '2024-12-19T14:23:00Z', size_kb: 1240, status: 'ready' },
  { id: 'r2', name: 'Hall-5kW-Trade-Study', type: 'propulsion',
    generated: '2024-12-19T10:15:00Z', size_kb: 580, status: 'ready' },
  { id: 'r3', name: 'Mars-Transfer-Mission-Plan', type: 'mission',
    generated: '2024-12-18T16:45:00Z', size_kb: 2100, status: 'ready' },
  { id: 'r4', name: 'Thermal-Equilibrium-Analysis', type: 'thermal',
    generated: '2024-12-18T11:20:00Z', size_kb: 720, status: 'ready' },
  { id: 'r5', name: 'Power-Budget-LEO', type: 'power',
    generated: '2024-12-17T09:00:00Z', size_kb: 410, status: 'ready' },
  { id: 'r6', name: 'Q4-Executive-Summary', type: 'executive',
    generated: '2024-12-15T18:00:00Z', size_kb: 3400, status: 'ready' },
  { id: 'r7', name: 'AI-Optimization-Run-47', type: 'optimization',
    generated: '2024-12-19T15:00:00Z', size_kb: 0, status: 'generating' },
];

const typeColor = {
  propulsion: 'thrust', mission: 'plasma', thermal: 'warn',
  power: 'thrust', optimization: 'ok', executive: 'plasma'
} as const;

export default function ReportsDashboard() {
  const [filter, setFilter] = useState<string>('all');

  const filtered = filter === 'all'
    ? SAMPLE_REPORTS
    : SAMPLE_REPORTS.filter(r => r.type === filter);

  const download = async (r: Report) => {
    try {
      const res = await api.get(`/reports/${r.id}/download`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement('a');
      a.href = url; a.download = `${r.name}.pdf`;
      a.click();
    } catch (e) { console.error(e); }
  };

  const generate = async (type: string) => {
    const res = await api.post('/reports/generate', { type, name: `New-${type}-Report` });
    console.log('Generated:', res.data);
  };

  return (
    <div>
      <PageHeader
        title="Engineering Reports"
        subtitle="Auto-generated PDFs and JSON for mission analysis, trade studies, and executive review"
        actions={
          <select value={filter} onChange={e => setFilter(e.target.value)}
                  className="bg-space-800 border border-space-700 rounded p-2 text-sm text-white">
            <option value="all">All Types</option>
            <option value="mission">Mission</option>
            <option value="propulsion">Propulsion</option>
            <option value="thermal">Thermal</option>
            <option value="power">Power</option>
            <option value="optimization">Optimization</option>
            <option value="executive">Executive</option>
          </select>
        }
      />

      <div className="grid grid-cols-2 md:grid-cols-6 gap-3 mb-4">
        {(['mission', 'propulsion', 'thermal', 'power', 'optimization', 'executive'] as const).map(t => {
          const count = SAMPLE_REPORTS.filter(r => r.type === t).length;
          return (
            <KPICard key={t} label={t.charAt(0).toUpperCase() + t.slice(1)} value={count}
                     icon={FileText} color={typeColor[t]} />
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card title="Report Library" className="lg:col-span-2">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs text-slate-400 uppercase tracking-wider border-b border-space-800/50">
                <th className="py-2">Name</th>
                <th>Type</th>
                <th>Generated</th>
                <th>Size</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((r) => (
                <tr key={r.id} className="border-b border-space-800/30 hover:bg-space-900/30">
                  <td className="py-2 font-medium">{r.name}</td>
                  <td><Badge color={typeColor[r.type]}>{r.type.toUpperCase()}</Badge></td>
                  <td className="text-slate-500 font-mono text-xs">
                    {new Date(r.generated).toLocaleString()}
                  </td>
                  <td className="text-slate-400 font-mono text-xs">
                    {r.size_kb > 0 ? `${(r.size_kb / 1024).toFixed(2)} MB` : '—'}
                  </td>
                  <td>
                    {r.status === 'ready' && <Badge color="ok">READY</Badge>}
                    {r.status === 'generating' && <Badge color="warn">GENERATING</Badge>}
                    {r.status === 'failed' && <Badge color="crit">FAILED</Badge>}
                  </td>
                  <td>
                    <div className="flex gap-1">
                      <button className="p-1 hover:bg-space-700 rounded"
                              title="View"><Eye className="w-3.5 h-3.5 text-slate-400" /></button>
                      <button onClick={() => download(r)} className="p-1 hover:bg-space-700 rounded"
                              title="Download"><Download className="w-3.5 h-3.5 text-slate-400" /></button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>

        <Card title="Generate New Report">
          <div className="space-y-2">
            {(['mission', 'propulsion', 'thermal', 'power', 'executive'] as const).map(t => (
              <button key={t} onClick={() => generate(t)}
                      className="w-full p-2 rounded bg-space-800/50 hover:bg-space-700/50
                                 border border-space-700 text-left text-sm transition flex items-center gap-2 text-white">
                <FileBarChart className="w-4 h-4 text-plasma-400" />
                <span>Generate {t.charAt(0).toUpperCase() + t.slice(1)} Report</span>
              </button>
            ))}
          </div>
          <div className="mt-4 text-xs text-slate-500">
            Reports include: mission analysis, propulsion trade studies, thermal maps,
            power budgets, and executive summaries.
          </div>
        </Card>
      </div>
    </div>
  );
}
