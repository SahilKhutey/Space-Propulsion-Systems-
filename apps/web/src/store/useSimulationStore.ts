import { create } from 'zustand';

export interface SpacecraftState {
  time: number;
  position_m: number[];
  velocity_m_s: number[];
  mass_total_kg: number;
  mass_propellant_kg: number;
  thermal_k: number[];
  battery_wh: number;
  thruster_on: boolean;
  thruster_hours: number;
  delta_v_used_ms: number;
  power_solar_w?: number;
  power_load_w?: number;
  power_battery_flow_w?: number;
}

export interface Projection {
  horizon_s: number;
  state: Partial<SpacecraftState>;
}

interface SimState {
  live: SpacecraftState | null;
  history: SpacecraftState[];
  projections: Record<string, Projection>;
  isRunning: boolean;
  failures: any | null;
  setLive: (s: SpacecraftState) => void;
  appendHistory: (s: SpacecraftState) => void;
  setProjections: (p: Record<string, Projection>) => void;
  setFailures: (f: any) => void;
  setRunning: (b: boolean) => void;
}

export const useSimulationStore = create<SimState>((set) => ({
  live: null,
  history: [],
  projections: {},
  isRunning: false,
  failures: null,
  setLive: (live) => set({ live }),
  appendHistory: (s) => set((st) => ({ history: [...st.history.slice(-9999), s] })),
  setProjections: (projections) => set({ projections }),
  setFailures: (failures) => set({ failures }),
  setRunning: (isRunning) => set({ isRunning }),
}));
