import React from 'react';

export function CesiumMissionView({ startAlt, targetAlt }: { startAlt: number; targetAlt: number }) {
  return (
    <div className="w-full h-[350px] bg-space-900 border border-space-800 rounded-xl flex flex-col items-center justify-center p-4 text-center">
      <div className="w-8 h-8 rounded-full border-2 border-plasma-400 border-t-transparent animate-spin mb-3"></div>
      <div className="font-mono text-sm text-plasma-300">CESIUM MISSION VIEW (SIMULATOR MODE)</div>
      <div className="text-xs text-slate-500 mt-1">LEO Start: {startAlt / 1000} km | GEO Target: {targetAlt / 1000} km</div>
      <div className="text-[10px] text-slate-600 mt-2 font-mono">Synchronizing 3D ellipsoid coordinate assets...</div>
    </div>
  );
}
