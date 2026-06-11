import clsx from 'clsx';

export function LiveIndicator({ active, label = 'LIVE' }: { active: boolean; label?: string }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className={clsx(
        'w-2 h-2 rounded-full',
        active ? 'bg-red-500 animate-pulse shadow-[0_0_8px_rgba(239,68,68,0.8)]' : 'bg-slate-600'
      )} />
      <span className="text-[10px] font-mono uppercase tracking-widest text-slate-400">{label}</span>
    </div>
  );
}
