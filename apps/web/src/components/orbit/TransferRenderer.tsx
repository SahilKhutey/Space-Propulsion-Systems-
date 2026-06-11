import { useEffect, useState } from 'react';
import { api } from '@/api/client';
import { EarthViewer } from './EarthViewer';

export function TransferRenderer({ startAlt, targetAlt }:
  { startAlt: number; targetAlt: number }) {
  const [points, setPoints] = useState<number[][]>([]);
  useEffect(() => {
    async function load() {
      const data = await api.getTransferPoints(startAlt, targetAlt);
      if (data && data.transfer_orbit) {
        setPoints(data.transfer_orbit.map((p: any) => [p.x, p.y, p.z]));
      }
    }
    load();
  }, [startAlt, targetAlt]);

  return <EarthViewer orbitPoints={points} scPosition={points[0] as [number, number, number]} />;
}
