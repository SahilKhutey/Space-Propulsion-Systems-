import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export function TrajectoryPlot({ data, refRadius }:
  { data: Array<{ x: number; y: number }>; refRadius?: number }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid stroke="rgba(148,163,184,0.1)" />
        <XAxis dataKey="x" tick={{ fontSize: 10, fill: '#94a3b8' }} unit=" m" type="number" />
        <YAxis dataKey="y" tick={{ fontSize: 10, fill: '#94a3b8' }} unit=" m" type="number" />
        <Tooltip contentStyle={{ background: '#0a1142', border: '1px solid #1f2a99', fontSize: 12 }} />
        <Line type="linear" dataKey="y" stroke="#06b6d4" dot={false} strokeWidth={2} isAnimationActive={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
