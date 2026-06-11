import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export function ThrustChart({ data }: { data: Array<{ t: number; thrust: number }> }) {
  return (
    <ResponsiveContainer width="100%" height={220}>
      <LineChart data={data} margin={{ left: 0, right: 8, top: 8, bottom: 0 }}>
        <CartesianGrid stroke="rgba(148,163,184,0.1)" strokeDasharray="3 3" />
        <XAxis dataKey="t" tick={{ fontSize: 10, fill: '#94a3b8' }}
               label={{ value: 't [s]', position: 'insideBottom', offset: -2, fill: '#94a3b8', fontSize: 10 }} />
        <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} unit=" N" width={60} />
        <Tooltip contentStyle={{ background: '#0a1142', border: '1px solid #1f2a99', borderRadius: 6, fontSize: 12 }} />
        <Line type="monotone" dataKey="thrust" stroke="#f59e0b" strokeWidth={2} dot={false} isAnimationActive={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
