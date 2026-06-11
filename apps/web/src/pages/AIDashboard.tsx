import React, { useState, useEffect } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { OptimizationProgress } from '@/components/ai/OptimizationProgress';
import { BestDesignCard, OptimizedParameters } from '@/components/ai/BestDesignCard';
import { ParetoChart } from '@/components/charts/ParetoChart';
import { Card } from '@/components/common/Card';
import { api } from '@/api/client';

export default function AIDashboard() {
  const [gen, setGen] = useState(1);
  const [candidates, setCandidates] = useState<any[]>([]);
  const [best, setBest] = useState<OptimizedParameters>({
    thruster_type: 'hall_thruster',
    efficiency: 0.72,
    isp_s: 2360,
    power_w: 7240,
    thrust_n: 0.442,
  });

  const handleRun = async () => {
    setGen(1);
    const result = await api.runOptimization({
      thruster_type: 'hall_thruster',
      power_w: 5000,
    });
    
    // Simulate generation ticks
    const interval = setInterval(() => {
      setGen((g) => {
        if (g >= 12) {
          clearInterval(interval);
          return 12;
        }
        return g + 1;
      });
    }, 300);
  };

  useEffect(() => {
    // Populate candidate list
    setCandidates([
      { name: 'Hall Candidate A', score: 92.5 },
      { name: 'Ion Candidate B', score: 88.0 },
      { name: 'VASIMR Candidate C', score: 72.0 },
      { name: 'Chemical Candidate D', score: 65.0 },
    ]);
  }, []);

  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="AI Optimization Studio"
        subtitle="Execute machine-learning genetic searches and find optimal thruster designs along Pareto frontiers"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Pareto Charts & Progress */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          <OptimizationProgress currentGen={gen} totalGen={12} />
          <Card title="Candidate Scores comparison">
            <ParetoChart data={candidates} valueKey="score" nameKey="name" />
          </Card>
        </div>

        {/* Best Design Profile */}
        <div className="lg:col-span-1 flex flex-col gap-4">
          <button
            onClick={handleRun}
            className="btn btn-primary w-full py-3 font-display font-bold uppercase tracking-wider hover:brightness-110"
          >
            RUN GENETIC OPTIMIZER
          </button>
          <BestDesignCard params={best} />
        </div>
      </div>
    </div>
  );
}
