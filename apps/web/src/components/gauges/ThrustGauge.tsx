import { Gauge } from '@/components/common/Gauge';
export function ThrustGauge({ thrust_n }: { thrust_n: number }) {
  return <Gauge value={thrust_n} max={2} unit="N" label="Thrust" color="#f59e0b" size={160} />;
}
