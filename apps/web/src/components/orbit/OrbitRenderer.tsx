import { useEffect, useState } from 'react';
import { EarthViewer } from './EarthViewer';

export function OrbitRenderer({ altitude, inclination = 0 }:
  { altitude: number; inclination?: number }) {
  const [points, setPoints] = useState<number[][]>([]);
  useEffect(() => {
    const r = 6371000 + altitude;
    const pts = [];
    const rad = inclination * Math.PI / 180;
    for (let i = 0; i <= 100; i++) {
      const theta = (i / 100) * 2 * Math.PI;
      const x = r * Math.cos(theta);
      const y = r * Math.sin(theta) * Math.cos(rad);
      const z = r * Math.sin(theta) * Math.sin(rad);
      pts.push([x, y, z]);
    }
    setPoints(pts);
  }, [altitude, inclination]);

  return <EarthViewer orbitPoints={points} scPosition={points[0] as [number, number, number]} />;
}
