import React from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card } from '@/components/common/Card';
import { KPICard } from '@/components/common/KPICard';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Layers, CheckCircle2, TrendingUp, DollarSign } from 'lucide-react';

const performanceData = [
  { year: '2023', savings: 120000, efficiency: 62 },
  { year: '2024', savings: 240000, efficiency: 68 },
  { year: '2025', savings: 450000, efficiency: 74 },
  { year: '2026', savings: 680000, efficiency: 82 },
];

export default function ExecutiveDashboard() {
  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Executive Portfolio Dashboard"
        subtitle="Evaluate propulsion R&D return-on-investment, mission budgets, and platform metrics"
      />

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard label="Active Programs" value="6" icon={Layers} color="plasma" />
        <KPICard label="Mission Success Rate" value="98.2" unit="%" icon={CheckCircle2} color="ok" />
        <KPICard label="Average Efficiency Gain" value="+46.6" unit="%" icon={TrendingUp} color="ok" />
        <KPICard label="Estimated Cost Savings" value="$680k" icon={DollarSign} color="thrust" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card title="Program Cost Savings Profile ($ USD)">
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={performanceData}>
              <CartesianGrid stroke="rgba(148,163,184,0.1)" strokeDasharray="3 3" />
              <XAxis dataKey="year" tick={{ fontSize: 10, fill: '#94a3b8' }} />
              <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} unit=" $" />
              <Tooltip contentStyle={{ background: '#0a1142', border: '1px solid #1f2a99', fontSize: 12 }} />
              <Area type="monotone" dataKey="savings" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.2} isAnimationActive={false} />
            </AreaChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Average Engine Efficiency Gains">
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={performanceData}>
              <CartesianGrid stroke="rgba(148,163,184,0.1)" strokeDasharray="3 3" />
              <XAxis dataKey="year" tick={{ fontSize: 10, fill: '#94a3b8' }} />
              <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} unit=" %" />
              <Tooltip contentStyle={{ background: '#0a1142', border: '1px solid #1f2a99', fontSize: 12 }} />
              <Area type="monotone" dataKey="efficiency" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.2} isAnimationActive={false} />
            </AreaChart>
          </ResponsiveContainer>
        </Card>
      </div>
    </div>
  );
}
