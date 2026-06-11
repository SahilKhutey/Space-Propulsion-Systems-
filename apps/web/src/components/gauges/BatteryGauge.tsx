import { ProgressRing } from '@/components/common/ProgressRing';
export function BatteryGauge({ soc }: { soc: number }) {
  const color = soc < 0.2 ? '#ef4444' : soc < 0.5 ? '#f59e0b' : '#10b981';
  return <ProgressRing value={soc * 100} max={100} color={color} size={120} label="SOC" />;
}
