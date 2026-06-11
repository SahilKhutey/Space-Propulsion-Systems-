import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Legend } from 'recharts';
const nodeColors = ['#06b6d4', '#f59e0b', '#10b981', '#a78bfa', '#f472b6', '#fb923c', '#60a5fa', '#fb7185'];

export function ThermalChart({ data, nodeNames }:
  { data: Array<Record<string, any>>; nodeNames: string[] }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data} margin={{ left: 0, right: 8, top: 8, bottom: 0 }}>
        <CartesianGrid stroke="rgba(148,163,184,0.1)" strokeDasharray="3 3" />
        <XAxis dataKey="t" tick={{ fontSize: 10, fill: '#94a3b8' }} />
        <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} domain={['dataMin - 5', 'dataMax + 5']} unit=" K" width={60} />
        <Tooltip contentStyle={{ background: '#0a1142', border: '1px solid #1f2a99', fontSize: 12 }} />
        <Legend wrapperStyle={{ fontSize: 10 }} />
        <ReferenceLine y={343.15} stroke="#ef4444" strokeDasharray="2 2" label={{ value: 'T_crit', fill: '#ef4444', fontSize: 9 }} />
        {nodeNames.map((name, i) => (
          <Line key={name} type="monotone" dataKey={name} stroke={nodeColors[i % nodeColors.length]}
                dot={false} strokeWidth={1.5} isAnimationActive={false} />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
