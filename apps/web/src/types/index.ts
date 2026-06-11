export interface ThrusterPerformanceResult {
  thruster_type: string;
  thrust_n: number;
  isp_s: number;
  exhaust_velocity_ms: number;
  power_w: number;
  efficiency: number;
  mass_flow_kg_s: number;
  specific_power_w_per_n: number;
  notes: string;
}

export interface PowerResult {
  solar_power_w: number;
  average_power_w: number;
  eclipse_loss_wh: number;
  thruster_energy_per_orbit_wh: number;
  battery_margin: number;
  feasible: boolean;
  notes: string[];
}

export interface ThermalNodeResult {
  component: string;
  min_temp_k: number;
  max_temp_k: number;
  steady_state_k: number;
  time_series_t: number[];
  time_series_temp_k: number[];
}

export interface ThermalResult {
  steady_state_k: number;
  min_temp_k: number;
  max_temp_k: number;
  radiator_required_m2: number;
  heat_rejected_w: number;
  time_series: ThermalNodeResult[];
  warnings: string[];
  safe: boolean;
}

export interface MissionResult {
  mission_name: string;
  delta_v_ms: number;
  propellant_mass_kg: number;
  initial_mass_kg: number;
  final_mass_kg: number;
  transfer_time_days: number;
  power_consumed_kwh: number;
  thermal_load_w: number;
  success_probability: number;
  notes: string[];
}

export interface TradeStudyCandidate {
  thruster_type: string;
  isp_s: number;
  thrust_n: number;
  propellant_mass_kg: number;
  total_mass_kg: number;
  power_w: number;
  efficiency: number;
  transfer_time_days: number;
  score: number;
}

export interface TradeStudyResult {
  mission_summary: {
    payload_mass_kg: number;
    delta_v_ms: number;
    mission_duration_years: number;
    evaluated_candidates_count: number;
  };
  candidates: TradeStudyCandidate[];
  winner: string;
  rationale: string;
}

export interface Point3D {
  x: number;
  y: number;
  z: number;
}

export interface HohmannTransferPoints {
  initial_orbit: Point3D[];
  final_orbit: Point3D[];
  transfer_orbit: Point3D[];
}

export interface PlumeGeometry {
  length: number;
  width: number;
  divergence_angle_deg: number;
  color: string;
  type: string;
  opacity: number;
}
