import { AlertTriangle, Info, CheckCircle, XCircle } from 'lucide-react';
import clsx from 'clsx';

const icons = { info: Info, ok: CheckCircle, warn: AlertTriangle, crit: XCircle };
const map = {
  info: 'bg-plasma-500/10 border-plasma-500/30 text-plasma-200',
  ok:   'bg-emerald-500/10 border-emerald-500/30 text-emerald-200',
  warn: 'bg-amber-500/10 border-amber-500/30 text-amber-200',
  crit: 'bg-red-500/10 border-red-500/30 text-red-200',
};

export function AlertBanner({ kind = 'info', title, message }:
  { kind?: 'info' | 'ok' | 'warn' | 'crit'; title?: string; message: string }) {
  const Icon = icons[kind];
  return (
    <div className={clsx('flex items-start gap-2 p-3 rounded-md border', map[kind])}>
      <Icon className="w-4 h-4 mt-0.5 flex-shrink-0" />
      <div className="text-sm">
        {title && <div className="font-semibold">{title}</div>}
        <div className="opacity-90">{message}</div>
      </div>
    </div>
  );
}
