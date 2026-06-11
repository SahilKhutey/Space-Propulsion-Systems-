export function ProgressRing({ value, max, color = '#06b6d4', size = 100, label }:
  { value: number; max: number; color?: string; size?: number; label?: string }) {
  const pct = max > 0 ? value / max : 0;
  const r = size / 2 - 8;
  const C = 2 * Math.PI * r;
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="rgba(148,163,184,0.15)" strokeWidth="6"/>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth="6"
                strokeDasharray={`${C * pct} ${C}`} strokeLinecap="round"
                style={{ transition: 'stroke-dasharray 0.6s ease' }}/>
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="font-mono text-lg font-bold">{Math.round(pct * 100)}%</span>
        {label && <span className="text-[10px] text-slate-400 uppercase tracking-wider">{label}</span>}
      </div>
    </div>
  );
}
