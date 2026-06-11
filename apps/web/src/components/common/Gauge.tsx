interface GaugeProps { value: number; min?: number; max: number;
  unit?: string; label?: string; color?: string; size?: number; }
export function Gauge({ value, min = 0, max, unit, label, color = '#06b6d4', size = 140 }: GaugeProps) {
  const pct = Math.max(0, Math.min(1, (value - min) / (max - min)));
  return (
    <div className="flex flex-col items-center" style={{ width: size }}>
      <svg viewBox="0 0 100 100" width={size} height={size}>
        <path d="M 15 85 A 35 35 0 1 1 85 85" fill="none" stroke="rgba(148,163,184,0.15)" strokeWidth="6" strokeLinecap="round"/>
        <path d="M 15 85 A 35 35 0 1 1 85 85" fill="none" stroke={color} strokeWidth="6" strokeLinecap="round"
              strokeDasharray={`${pct * 138} 138`} style={{ transition: 'stroke-dasharray 0.6s ease' }} />
        <text x="50" y="55" textAnchor="middle" className="font-mono" fontSize="14" fontWeight="700" fill="#e2e8f0">
          {value.toFixed(2)}
        </text>
        {unit && <text x="50" y="70" textAnchor="middle" fontSize="8" fill="#94a3b8">{unit}</text>}
        {label && <text x="50" y="95" textAnchor="middle" fontSize="7" fill="#94a3b8" style={{ textTransform: 'uppercase' }}>{label}</text>}
      </svg>
    </div>
  );
}
