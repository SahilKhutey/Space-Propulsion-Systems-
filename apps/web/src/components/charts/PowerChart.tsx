import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export function PowerChart({ data }: { data: Array<{ t: number; solar: number; load: number; soc: number }> }) {
  return (
    <ResponsiveContainer width="100%" height={220}>
      <AreaChart data={data} margin={{ left: 0, right: 8, top: 8, bottom: 0 }}>
        <CartesianGrid stroke="rgba(148,163,184,0.1)" strokeDasharray="3 3" />
        <XAxis dataKey="t" tick={{ fontSize: 10, fill: '#94a3b8' }} />
        <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} unit=" W" width={60} />
        <Tooltip contentStyle={{ background: '#0a1142', border: '1px solid #1f2a99', fontSize: 12 }} />
        <Legend wrapperStyle={{ fontSize: 10 }} />
        <Area type="monotone" dataKey="solar" stackId="1" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.3} isAnimationActive={false} />
        <Area type="monotone" dataKey="load" stackId="2" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.3} isAnimationActive={false} />
        <Area type="monotone" dataKey="soc" stackId="3" stroke="#10b981" fill="#10b981" fillOpacity={0.2} isAnimationActive={false} />
      </AreaChart>
    </ResponsiveContainer>
  );
}
