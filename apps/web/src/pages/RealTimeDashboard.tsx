import React, { useEffect } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card } from '@/components/common/Card';
import { KPICard } from '@/components/common/KPICard';
import { useSimulationStore } from '@/store/useSimulationStore';
import { Play, Square, RefreshCw } from 'lucide-react';

export default function RealTimeDashboard() {
  const { live, isRunning, setRunning, setLive } = useSimulationStore();

  const handleToggle = () => {
    setRunning(!isRunning);
  };

  useEffect(() => {
    let interval: any = null;
    if (isRunning) {
      interval = setInterval(() => {
        // Mock ticking state vector increments
        setLive({
          time: (live?.time ?? 0) + 1.0,
          position_m: [
            (live?.position_m[0] ?? 7000000.0) + (live?.velocity_m_s[0] ?? 0.0) * 1.0,
            (live?.position_m[1] ?? 0.0) + (live?.velocity_m_s[1] ?? 7500.0) * 1.0,
            (live?.position_m[2] ?? 0.0) + (live?.velocity_m_s[2] ?? 0.0) * 1.0,
          ],
          velocity_m_s: [
            live?.velocity_m_s[0] ?? -5.0,
            live?.velocity_m_s[1] ?? 7498.0,
            live?.velocity_m_s[2] ?? 0.0,
          ],
          mass_total_kg: (live?.mass_total_kg ?? 1000.0) - 0.0001,
          mass_propellant_kg: (live?.mass_propellant_kg ?? 500.0) - 0.0001,
          thermal_k: (live?.thermal_k ?? [290.0]).map(t => t + 0.05 * Math.random()),
          battery_wh: Math.max(0, (live?.battery_wh ?? 5000.0) - 0.15),
          thruster_on: live?.thruster_on ?? true,
          thruster_hours: (live?.thruster_hours ?? 0) + 1.0 / 3600.0,
          delta_v_used_ms: (live?.delta_v_used_ms ?? 0) + 0.02,
        });
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isRunning, live]);

  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Real-Time Simulation Core"
        subtitle="Manage and execute active simulation clock loops, and monitor dynamic spacecraft state vectors"
        actions={
          <button
            onClick={handleToggle}
            className={`btn flex items-center gap-1.5 px-4 py-2 ${
              isRunning ? 'bg-red-500/20 text-red-300 border border-red-500/30' : 'bg-plasma-500 text-space-950 font-bold hover:brightness-115'
            }`}
          >
            {isRunning ? (
              <>
                <Square className="w-4 h-4" />
                ABORT SIMULATION
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                START SIMULATION
              </>
            )}
          </button>
        }
      />

      {/* KPI Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard label="Elapsed Time (T+)" value={`${live?.time?.toFixed(1) ?? '0.0'}`} unit="s" icon={RefreshCw} color="plasma" />
        <KPICard label="Total Wet Mass" value={`${live?.mass_total_kg?.toFixed(2) ?? '1000.00'}`} unit="kg" color="plasma" />
        <KPICard label="Remaining Fuel" value={`${live?.mass_propellant_kg?.toFixed(2) ?? '500.00'}`} unit="kg" color="thrust" />
        <KPICard label="Delta-V Expended" value={`${live?.delta_v_used_ms?.toFixed(2) ?? '0.00'}`} unit="m/s" color="ok" />
      </div>

      {/* State Vector Display */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card title="Kinematic States [Position & Velocity]">
          <div className="flex flex-col gap-3 font-mono text-xs text-slate-400">
            <div className="flex justify-between bg-space-950/30 p-2 rounded">
              <span>POSITION X / Y / Z</span>
              <span className="font-bold text-slate-300">
                {live?.position_m[0]?.toFixed(1) ?? '7000000.0'} / {live?.position_m[1]?.toFixed(1) ?? '0.0'} / {live?.position_m[2]?.toFixed(1) ?? '0.0'} m
              </span>
            </div>
            <div className="flex justify-between bg-space-950/30 p-2 rounded">
              <span>VELOCITY X / Y / Z</span>
              <span className="font-bold text-slate-300">
                {live?.velocity_m_s[0]?.toFixed(2) ?? '0.00'} / {live?.velocity_m_s[1]?.toFixed(2) ?? '7500.00'} / {live?.velocity_m_s[2]?.toFixed(2) ?? '0.00'} m/s
              </span>
            </div>
          </div>
        </Card>

        <Card title="System Margins [Battery & Thermal]">
          <div className="flex flex-col gap-3 font-mono text-xs text-slate-400">
            <div className="flex justify-between bg-space-950/30 p-2 rounded">
              <span>BATTERY CAPACITY</span>
              <span className="font-bold text-slate-300">{live?.battery_wh?.toFixed(1) ?? '5000.0'} Wh</span>
            </div>
            <div className="flex justify-between bg-space-950/30 p-2 rounded">
              <span>CORE TEMPERATURE</span>
              <span className="font-bold text-slate-300">{live?.thermal_k[0]?.toFixed(1) ?? '290.0'} K</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
