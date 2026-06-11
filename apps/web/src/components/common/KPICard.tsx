import clsx from 'clsx';
import { LucideIcon } from 'lucide-react';
import { ReactNode } from 'react';

export function KPICard({ label, value, unit, icon: Icon, trend, color = 'plasma' }:
  { label: string; value: string | number; unit?: string; icon?: LucideIcon;
    trend?: ReactNode; color?: 'plasma' | 'thrust' | 'ok' | 'warn' | 'crit' }) {
  const colorMap = {
    plasma: 'text-plasma-300',
    thrust: 'text-thrust-400',
    ok: 'text-emerald-400',
    warn: 'text-amber-400',
    crit: 'text-red-400',
  };
  return (
    <div className="kpi">
      <div className="flex justify-between items-start">
        <span className="text-xs text-slate-400 uppercase tracking-wider">{label}</span>
        {Icon && <Icon className={clsx('w-4 h-4', colorMap[color])} />}
      </div>
      <div className="flex items-baseline gap-1">
        <span className={clsx('font-mono text-2xl font-bold tabular-nums', colorMap[color])}>
          {value}
        </span>
        {unit && <span className="text-sm text-slate-500">{unit}</span>}
      </div>
      {trend && <div className="text-xs">{trend}</div>}
    </div>
  );
}
