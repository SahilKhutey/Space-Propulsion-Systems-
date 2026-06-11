import { Gauge } from '@/components/common/Gauge';
export function ThermalGauge({ temp_k }: { temp_k: number }) {
  const t_c = temp_k - 273.15;
  const color = temp_k > 343.15 ? '#ef4444' : temp_k > 313.15 ? '#f59e0b' : '#10b981';
  return <Gauge value={t_c} min={-50} max={150} unit="°C" label="Temp" color={color} size={140} />;
}
