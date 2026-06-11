import { useEffect, useState } from 'react';
import { api } from '@/api/client';
import { Card } from '@/components/common/Card';
import { Badge } from '@/components/common/Badge';
import { Activity, Cpu, Database, Zap } from 'lucide-react';

interface HealthData {
  status: string;
  uptime_s: number;
  version: string;
}

interface SystemMetrics {
  cpu_pct: number;
  mem_mb: number;
  mem_pct: number;
  threads: number;
  load_avg: number[] | null;
}

export function SystemHealth() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [sys, setSys] = useState<SystemMetrics | null>(null);
  const [latency, setLatency] = useState<number>(0);

  useEffect(() => {
    const check = async () => {
      const t0 = performance.now();
      try {
        const h = await api.get<HealthData>('/health/');
        const s = await api.get<SystemMetrics>('/health/system');
        setHealth(h.data);
        setSys(s.data);
        setLatency(performance.now() - t0);
      } catch (e) { console.error(e); }
    };
    check();
    const i = setInterval(check, 5000);
    return () => clearInterval(i);
  }, []);

  return (
    <Card title="System Health" glow={health?.status === 'healthy' ? 'cyan' : 'red'}>
      <div className="grid grid-cols-2 gap-3 text-sm text-white">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-emerald-400" />
          <span>Status:</span>
          <Badge color={health?.status === 'healthy' ? 'ok' : 'crit'}>
            {health?.status?.toUpperCase() ?? 'CHECKING'}
          </Badge>
        </div>
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-plasma-400" />
          <span>API Latency:</span>
          <span className="font-mono text-slate-300">{latency.toFixed(0)} ms</span>
        </div>
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-amber-400" />
          <span>CPU:</span>
          <span className="font-mono text-slate-300">{sys?.cpu_pct?.toFixed(1) ?? '—'}%</span>
        </div>
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-purple-400" />
          <span>Memory:</span>
          <span className="font-mono text-slate-300">{sys?.mem_mb?.toFixed(0) ?? '—'} MB</span>
        </div>
        <div className="col-span-2 text-xs text-slate-500 font-mono mt-2 pt-2 border-t border-space-800/50">
          v{health?.version ?? '—'} · uptime {Math.floor((health?.uptime_s ?? 0) / 60)}m
        </div>
      </div>
    </Card>
  );
}
export default SystemHealth;
