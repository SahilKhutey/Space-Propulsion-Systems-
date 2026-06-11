import { useSimulationStore } from '@/store/useSimulationStore';
import { useTelemetryStore } from '@/store/useTelemetryStore';

export function StatusBar() {
  const live = useSimulationStore((s) => s.live);
  const uncertainty = useTelemetryStore((s) => s.uncertaintyTrace);
  return (
    <footer className="h-7 border-t border-space-800/50 bg-space-950/70 backdrop-blur-md
                       flex items-center justify-between px-4 text-[11px] text-slate-500 font-mono">
      <div className="flex gap-4">
        <span>UTC {new Date().toISOString().slice(11, 19)}</span>
        <span>T+{live?.time?.toFixed(1) ?? '0.0'}s</span>
        <span>ESTIMATOR σ² = {uncertainty.toFixed(2)}</span>
      </div>
      <div className="flex gap-4">
        <span>API ● connected</span>
        <span>WS ● telemetry</span>
        <span>Build 1.0.0</span>
      </div>
    </footer>
  );
}
