import { Gauge } from '@/components/common/Gauge';
export function EfficiencyGauge({ eta }: { eta: number }) {
  return <Gauge value={eta * 100} max={100} unit="%" label="η" color="#10b981" size={140} />;
}
