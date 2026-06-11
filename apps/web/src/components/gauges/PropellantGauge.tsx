import { ProgressRing } from '@/components/common/ProgressRing';
export function PropellantGauge({ fraction }: { fraction: number }) {
  return <ProgressRing value={fraction * 100} max={100} color="#f59e0b" size={120} label="Fuel" />;
}
