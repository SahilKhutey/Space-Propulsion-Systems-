interface SparklineProps { data: number[]; color?: string; height?: number; }
export function Sparkline({ data, color = '#06b6d4', height = 40 }: SparklineProps) {
  if (data.length < 2) return <div style={{ height }} />;
  const min = Math.min(...data), max = Math.max(...data);
  const range = max - min || 1;
  const pts = data.map((v, i) =>
    `${(i / (data.length - 1)) * 100},${height - ((v - min) / range) * height}`
  ).join(' ');
  return (
    <svg viewBox={`0 0 100 ${height}`} preserveAspectRatio="none" style={{ width: '100%', height }}>
      <polyline points={pts} fill="none" stroke={color} strokeWidth="1.5" />
    </svg>
  );
}
