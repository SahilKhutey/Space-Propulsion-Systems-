import clsx from 'clsx';

export function Badge({ children, color = 'plasma' }:
  { children: React.ReactNode; color?: 'plasma' | 'ok' | 'warn' | 'crit' | 'slate' }) {
  const map = {
    plasma: 'bg-plasma-500/15 text-plasma-300 border-plasma-500/30',
    ok: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    warn: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    crit: 'bg-red-500/15 text-red-300 border-red-500/30',
    slate: 'bg-slate-700/30 text-slate-300 border-slate-500/30',
  };
  return <span className={clsx('inline-block px-2 py-0.5 rounded text-[10px] font-mono uppercase border', map[color])}>{children}</span>;
}
