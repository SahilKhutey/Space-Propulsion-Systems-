import { create } from 'zustand';

export interface Telemetry {
  t: number;
  position: number[];
  velocity: number[];
  estimated: number[];
  covariance_diag: number[];
  anomalies: string[];
}

interface TelemetryState {
  packets: Telemetry[];
  lastAnomaly: string | null;
  uncertaintyTrace: number;
  push: (p: Telemetry) => void;
}

export const useTelemetryStore = create<TelemetryState>((set) => ({
  packets: [],
  lastAnomaly: null,
  uncertaintyTrace: 0,
  push: (p) => set((s) => ({
    packets: [...s.packets.slice(-9999), p],
    lastAnomaly: p.anomalies.length > 0 ? p.anomalies[p.anomalies.length - 1] : s.lastAnomaly,
    uncertaintyTrace: p.covariance_diag.reduce((a, b) => a + b, 0),
  })),
}));
