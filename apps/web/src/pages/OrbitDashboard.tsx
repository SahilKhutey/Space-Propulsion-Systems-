import React, { useState } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import { OrbitRenderer } from '@/components/orbit/OrbitRenderer';
import { Card } from '@/components/common/Card';

export default function OrbitDashboard() {
  const [altitude, setAltitude] = useState(400000); // 400km LEO
  const [inclination, setInclination] = useState(28.5); // ISS inclination

  // Compute standard Keplerian variables
  const r_earth = 6371;
  const a_km = r_earth + (altitude / 1000);
  const mu = 3.986004418e5; // Earth mu
  const v_kms = Math.sqrt(mu / a_km);
  const period_min = 2 * Math.PI * Math.sqrt(Math.pow(a_km, 3) / mu) / 60;

  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title="Orbital Mechanics Viewer"
        subtitle="Propagate orbits dynamically, configure inclination angles, and monitor osculating elements"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* 3D WebGL Canvas */}
        <div className="lg:col-span-2">
          <OrbitRenderer altitude={altitude} inclination={inclination} />
        </div>

        {/* Configurations & Element Cards */}
        <div className="lg:col-span-1 flex flex-col gap-4">
          <Card title="Orbital Configuration">
            <div className="flex flex-col gap-4 text-xs font-mono">
              <div className="flex flex-col gap-1.5">
                <div className="flex justify-between">
                  <label className="text-slate-400">ALTITUDE (LEO)</label>
                  <span className="text-plasma-400">{altitude / 1000} km</span>
                </div>
                <input
                  type="range" min="200000" max="2000000" step="50000"
                  value={altitude}
                  onChange={(e) => setAltitude(Number(e.target.value))}
                  className="w-full h-1.5 bg-space-900 rounded-lg appearance-none cursor-pointer accent-plasma-400"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <div className="flex justify-between">
                  <label className="text-slate-400">INCLINATION (i)</label>
                  <span className="text-plasma-400">{inclination}°</span>
                </div>
                <input
                  type="range" min="0" max="90" step="0.5"
                  value={inclination}
                  onChange={(e) => setInclination(Number(e.target.value))}
                  className="w-full h-1.5 bg-space-900 rounded-lg appearance-none cursor-pointer accent-plasma-400"
                />
              </div>
            </div>
          </Card>

          <Card title="Keplerian Orbital Elements">
            <div className="flex flex-col gap-3 font-mono text-xs text-slate-400">
              <div className="flex justify-between">
                <span>SEMI-MAJOR AXIS (a)</span>
                <span className="font-bold text-slate-300">{a_km.toFixed(1)} km</span>
              </div>
              <div className="flex justify-between">
                <span>ECCENTRICITY (e)</span>
                <span className="font-bold text-slate-300">0.00000</span>
              </div>
              <div className="flex justify-between">
                <span>ORBITAL SPEED (v)</span>
                <span className="font-bold text-plasma-400">{v_kms.toFixed(3)} km/s</span>
              </div>
              <div className="flex justify-between">
                <span>ORBITAL PERIOD (T)</span>
                <span className="font-bold text-slate-300">{period_min.toFixed(2)} min</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
