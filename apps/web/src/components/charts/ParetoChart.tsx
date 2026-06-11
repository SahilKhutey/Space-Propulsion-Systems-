import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Legend } from 'recharts';
import { chartPalette } from '@/theme/designSystem';

export function ParetoChart({ data, valueKey, nameKey }:
  { data: any[]; valueKey: string; nameKey: string }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid stroke="rgba(148,163,184,0.1)" strokeDasharray="3 3" />
        <XAxis dataKey={nameKey} tick={{ fontSize: 10, fill: '#94a3b8' }} angle={-20} textAnchor="end" height={60} />
        <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} />
        <Tooltip contentStyle={{ background: '#0a1142', border: '1px solid #1f2a99', fontSize: 12 }} />
        <Bar dataKey={valueKey} isAnimationActive={false}>
          {data.map((_, i) => <Cell key={i} fill={chartPalette[i % chartPalette.length]} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
