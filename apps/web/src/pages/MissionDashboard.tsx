import React, { useState, useEffect } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { CesiumMissionView } from '@/components/orbit/CesiumMissionView';
import { Card } from '@/components/common/Card';
import { KPICard } from '@/components/common/KPICard';
import { api } from '@/api/client';
import { MissionResult } from '@/types';
import { Sparkles, CheckCircle2 } from 'lucide-react';

export default function MissionDashboard() {
  const [name, setName] = useState('LEO-to-GEO Spiral');
  const [payload, setPayload] = useState(1000);
  const [startAlt, setStartAlt] = useState(400000);
  const [targetAlt, setTargetAlt] = useState(35786000);
  const [safetyFactor, setSafetyFactor] = useState(1.15);
  const [results, setResults] = useState<MissionResult | null>(null);

  const handleRun = async () => {
    const data = await api.computeMission({
      name,
      payload_mass_kg: payload,
      start_alt_m: startAlt,
      target_alt_m: targetAlt,
      safety_factor: safetyFactor,
      thruster_type: 'hall_thruster',
      isp_s: 2000,
      efficiency: 0.6,
      power_w: 5000,
    });
    setResults(data);
  };

  useEffect(() => {
    handleRun();
  }, [payload, startAlt, targetAlt, safetyFactor]);

  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Mission Profile Validation"
        subtitle="Sizing wet/dry spacecraft masses, calculating transfer times, and assessing success criteria"
      />

      {/* 3D Mission Globe */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 flex flex-col gap-4">
          <CesiumMissionView startAlt={startAlt} targetAlt={targetAlt} />
          
          {/* Mission Milestones Progress Bar */}
          <Card title="Mission Milestones">
            <div className="flex justify-between items-center gap-2 py-4 relative font-mono text-[10px] text-slate-500">
              <div className="flex flex-col items-center gap-1.5 z-10">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                <span className="font-sans font-bold text-slate-300">LAUNCH</span>
              </div>
              <div className="flex-1 h-0.5 bg-emerald-500/50" />
              <div className="flex flex-col items-center gap-1.5 z-10">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                <span className="font-sans font-bold text-slate-300">LEO INSERTION</span>
              </div>
              <div className="flex-1 h-0.5 bg-space-800" />
              <div className="flex flex-col items-center gap-1.5 z-10">
                <div className="w-5 h-5 rounded-full border border-space-700 bg-space-950 flex items-center justify-center font-bold text-[10px]">3</div>
                <span className="font-sans font-semibold">TRANSFER SPIRAL</span>
              </div>
              <div className="flex-1 h-0.5 bg-space-800" />
              <div className="flex flex-col items-center gap-1.5 z-10">
                <div className="w-5 h-5 rounded-full border border-space-700 bg-space-950 flex items-center justify-center font-bold text-[10px]">4</div>
                <span className="font-sans font-semibold">GEO OPERATIONS</span>
              </div>
            </div>
          </Card>
        </div>

        {/* Configurations Sidepanel */}
        <div className="lg:col-span-1 flex flex-col gap-4">
          <Card title="Spacecraft Sizing Inputs">
            <div className="flex flex-col gap-4 text-xs font-mono">
              <div className="flex flex-col gap-1.5">
                <div className="flex justify-between">
                  <label className="text-slate-400">PAYLOAD MASS</label>
                  <span className="text-plasma-400">{payload} kg</span>
                </div>
                <input
                  type="range" min="100" max="10000" step="100"
                  value={payload}
                  onChange={(e) => setPayload(Number(e.target.value))}
                  className="w-full h-1.5 bg-space-900 rounded-lg appearance-none cursor-pointer accent-plasma-400"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <div className="flex justify-between">
                  <label className="text-slate-400">SAFETY MARGIN FACTOR</label>
                  <span className="text-plasma-400">{safetyFactor.toFixed(2)}x</span>
                </div>
                <input
                  type="range" min="1.0" max="1.5" step="0.05"
                  value={safetyFactor}
                  onChange={(e) => setSafetyFactor(Number(e.target.value))}
                  className="w-full h-1.5 bg-space-900 rounded-lg appearance-none cursor-pointer accent-plasma-400"
                />
              </div>
            </div>
          </Card>

          <Card title="Calculated Mission Budgets">
            <div className="flex flex-col gap-3 font-mono text-xs text-slate-400">
              <div className="flex justify-between">
                <span>TOTAL DELTA-V</span>
                <span className="font-bold text-slate-300">{results?.delta_v_ms?.toFixed(1) ?? '4250.0'} m/s</span>
              </div>
              <div className="flex justify-between">
                <span>PROPELLANT MASS REQUIRED</span>
                <span className="font-bold text-plasma-400">{results?.propellant_mass_kg?.toFixed(1) ?? '240.0'} kg</span>
              </div>
              <div className="flex justify-between">
                <span>TRANSFER DURATION</span>
                <span className="font-bold text-slate-300">{results?.transfer_time_days?.toFixed(1) ?? '120.0'} days</span>
              </div>
              <div className="flex justify-between">
                <span>SUCCESS PROBABILITY</span>
                <span className="font-bold text-emerald-400">{( (results?.success_probability ?? 0.95) * 100).toFixed(0)}%</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
