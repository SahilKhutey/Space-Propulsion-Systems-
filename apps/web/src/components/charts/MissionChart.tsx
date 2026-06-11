import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export function MissionChart({ data }:
  { data: Array<{ t: number; radius: number; mass: number; battery: number; thrust: number }> }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data} margin={{ left: 0, right: 8, top: 8, bottom: 0 }}>
        <CartesianGrid stroke="rgba(148,163,184,0.1)" strokeDasharray="3 3" />
        <XAxis dataKey="t" tick={{ fontSize: 10, fill: '#94a3b8' }} label={{ value: 'mission time [h]', position: 'insideBottom', offset: -2, fill: '#94a3b8', fontSize: 10 }} />
        <YAxis yAxisId="left" tick={{ fontSize: 10, fill: '#94a3b8' }} />
        <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 10, fill: '#94a3b8' }} />
        <Tooltip contentStyle={{ background: '#0a1142', border: '1px solid #1f2a99', fontSize: 12 }} />
        <Legend wrapperStyle={{ fontSize: 10 }} />
        <Line yAxisId="left" dataKey="radius" stroke="#06b6d4" dot={false} name="Orbit [km]" isAnimationActive={false} />
        <Line yAxisId="left" dataKey="mass" stroke="#f59e0b" dot={false} name="Mass [kg]" isAnimationActive={false} />
        <Line yAxisId="right" dataKey="battery" stroke="#10b981" dot={false} name="Battery [Wh]" isAnimationActive={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
