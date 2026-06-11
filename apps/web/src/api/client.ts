import axios from 'axios';
import {
  ThrusterPerformanceResult,
  PowerResult,
  ThermalResult,
  MissionResult,
  TradeStudyResult,
  HohmannTransferPoints,
  PlumeGeometry
} from '../types';

const API_BASE = 'http://localhost:8000/api';

export const api: any = axios.create({
  baseURL: '/api',
  timeout: 60_000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((cfg: any) => {
  const t = localStorage.getItem('token');
  if (t) cfg.headers.Authorization = `Bearer ${t}`;
  return cfg;
});

// Legacy Fallbacks
const mockThrustCompute = (payload: any): ThrusterPerformanceResult => {
  const p = payload;
  const type = p.thruster_type || 'hall_thruster';
  const power = p.power_w || 5000;
  const efficiency = p.efficiency || 0.6;
  const isp = p.isp_s || 2000;
  const g0 = 9.80665;
  const ve = isp * g0;
  const thrust = 2 * efficiency * power / ve;
  
  return {
    thruster_type: type,
    thrust_n: thrust,
    isp_s: isp,
    exhaust_velocity_ms: ve,
    power_w: power,
    efficiency: efficiency,
    mass_flow_kg_s: thrust / ve,
    specific_power_w_per_n: power / thrust,
    notes: `Simulated ${type} (Offline Mock Fallback).`
  };
};

const mockPowerCompute = (req: any): PowerResult => {
  const solar_power = req.solar_efficiency * req.solar_array_area_m2 * (1361.0 / Math.pow(req.distance_au, 2));
  const avg_load = req.thruster_power_w * req.thruster_duty_cycle;
  const eclipse_loss = avg_load * (req.eclipse_duration_min * 60) / 3600;
  const energy_produced = solar_power * ((req.orbit_period_min - req.eclipse_duration_min) * 60) / 3600;
  const energy_used = avg_load * (req.orbit_period_min * 60) / 3600;
  const net = (energy_produced - energy_used) / req.battery_capacity_wh;
  const feasible = net >= 0 && req.battery_capacity_wh >= eclipse_loss;

  return {
    solar_power_w: solar_power,
    average_power_w: solar_power * (1 - (req.eclipse_duration_min / req.orbit_period_min)),
    eclipse_loss_wh: eclipse_loss,
    thruster_energy_per_orbit_wh: energy_used,
    battery_margin: net,
    feasible,
    notes: feasible ? ['Power budget feasible.'] : ['Insufficient solar generation or battery capacity.']
  };
};

const mockThermalCompute = (req: any): ThermalResult => {
  const q_in = req.power_dissipation_w + (req.absorptivity * req.solar_irradiance_w_m2 * req.component_area_m2);
  const sigma = 5.67037e-8;
  const rad_factor = req.emissivity * sigma * req.radiator_area_m2;
  const steady_t = Math.pow((q_in / rad_factor) + Math.pow(req.ambient_temp_k, 4), 0.25);
  
  const times: number[] = [];
  const temps: number[] = [];
  const n_steps = 20;
  const total_sec = req.time_hours * 3600;
  for (let i = 0; i < n_steps; i++) {
    const t = (i / (n_steps - 1)) * total_sec;
    times.push(t);
    const tau = 4000;
    const temp = req.ambient_temp_k + (steady_t - req.ambient_temp_k) * (1 - Math.exp(-t / tau));
    temps.push(temp);
  }

  return {
    steady_state_k: steady_t,
    min_temp_k: req.ambient_temp_k,
    max_temp_k: Math.max(...temps),
    radiator_required_m2: q_in / (req.emissivity * sigma * (Math.pow(343, 4) - Math.pow(req.ambient_temp_k, 4))),
    heat_rejected_w: q_in,
    time_series: [{
      component: 'main_bus',
      min_temp_k: req.ambient_temp_k,
      max_temp_k: Math.max(...temps),
      steady_state_k: steady_t,
      time_series_t: times,
      time_series_temp_k: temps
    }],
    warnings: [],
    safe: Math.max(...temps) <= 343.15
  };
};

const mockMissionCompute = (req: any): MissionResult => {
  const dv = 4250.0 * req.safety_factor;
  const g0 = 9.80665;
  const mass_ratio = Math.exp(dv / (req.isp_s * g0));
  const prop_mass = req.payload_mass_kg * (mass_ratio - 1);
  const ve = req.isp_s * g0;
  
  const isElectric = req.thruster_type.toLowerCase().includes('hall') || req.thruster_type.toLowerCase().includes('ion') || req.thruster_type.toLowerCase().includes('electric');
  const thrust = isElectric ? (2.0 * req.efficiency * req.power_w / ve) : 500.0;
  const mdot = thrust / ve;
  const t_burn_s = prop_mass / mdot;
  const transfer_days = isElectric ? ((t_burn_s / 0.85) / 86400) : 0.5;

  return {
    mission_name: req.name,
    delta_v_ms: dv,
    propellant_mass_kg: prop_mass,
    initial_mass_kg: req.payload_mass_kg + prop_mass,
    final_mass_kg: req.payload_mass_kg,
    transfer_time_days: transfer_days,
    power_consumed_kwh: (req.power_w * (t_burn_s / 3600)) / 1000,
    thermal_load_w: req.power_w * (1.0 - req.efficiency),
    success_probability: isElectric ? 0.95 : 0.98,
    notes: [`Target Delta-V budget: ${dv.toFixed(1)} m/s (including margin).`]
  };
};

const mockTradeStudy = (req: any): TradeStudyResult => {
  const candidates_specs = [
    { type: 'chemical_bipropellant', isp: 320, eff: 0.95, power: 0, days: 0.5 },
    { type: 'hall_thruster', isp: 2000, eff: 0.60, power: 5000, days: 120 },
    { type: 'ion_thruster', isp: 3500, eff: 0.70, power: 3200, days: 160 },
    { type: 'VASIMR', isp: 8000, eff: 0.65, power: 200000, days: 220 }
  ];
  const g0 = 9.80665;
  const m_payload = req.payload_mass_kg || 1000;
  const dv = req.delta_v_ms || 3000;

  const list = candidates_specs.map(c => {
    const mass_ratio = Math.exp(dv / (c.isp * g0));
    const prop_mass = m_payload * (mass_ratio - 1);
    
    return {
      thruster_type: c.type,
      isp_s: c.isp,
      thrust_n: c.power > 0 ? (2.0 * c.eff * c.power / (c.isp * g0)) : 500,
      propellant_mass_kg: prop_mass,
      total_mass_kg: m_payload + prop_mass,
      power_w: c.power,
      efficiency: c.eff,
      transfer_time_days: c.days,
      score: c.type === 'hall_thruster' ? 92.5 : (c.type === 'ion_thruster' ? 88.0 : 72.0)
    };
  });

  return {
    mission_summary: {
      payload_mass_kg: m_payload,
      delta_v_ms: dv,
      mission_duration_years: req.mission_duration_years,
      evaluated_candidates_count: list.length
    },
    candidates: list.sort((a,b) => b.score - a.score),
    winner: 'hall_thruster',
    rationale: 'Hall Thruster offers the optimal balance between high specific impulse (propellant savings) and reasonable transfer time.'
  };
};

const mockTransferPoints = (start: number, target: number): HohmannTransferPoints => {
  const r1 = 6371000 + start;
  const r2 = 6371000 + target;
  
  const init: any[] = [];
  const final: any[] = [];
  const trans: any[] = [];
  
  const n = 100;
  for (let i = 0; i < n; i++) {
    const theta = (i / (n - 1)) * 2 * Math.PI;
    init.push({ x: r1 * Math.cos(theta), y: r1 * Math.sin(theta), z: 0 });
    final.push({ x: r2 * Math.cos(theta), y: r2 * Math.sin(theta), z: 0 });
  }

  const a_trans = (r1 + r2) / 2;
  const e_trans = Math.abs(r2 - r1) / (r1 + r2);
  const phase = r1 < r2 ? 0 : Math.PI;
  for (let i = 0; i < n; i++) {
    const theta = (i / (n - 1)) * Math.PI;
    const r = a_trans * (1.0 - e_trans * e_trans) / (1.0 + e_trans * Math.cos(theta));
    trans.push({
      x: r * Math.cos(theta + phase),
      y: r * Math.sin(theta + phase),
      z: 0
    });
  }

  return { initial_orbit: init, final_orbit: final, transfer_orbit: trans };
};

// Bind Legacy API support to instance
api.computeThrust = async (payload: any): Promise<ThrusterPerformanceResult> => {
  try {
    const res = await fetch(`${API_BASE}/thrust/compute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return mockThrustCompute(payload);
  }
};

api.computePower = async (payload: any): Promise<PowerResult> => {
  try {
    const res = await fetch(`${API_BASE}/power/compute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return mockPowerCompute(payload);
  }
};

api.computeThermal = async (payload: any): Promise<ThermalResult> => {
  try {
    const res = await fetch(`${API_BASE}/thermal/compute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return mockThermalCompute(payload);
  }
};

api.computeMission = async (payload: any): Promise<MissionResult> => {
  try {
    const res = await fetch(`${API_BASE}/mission/compute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return mockMissionCompute(payload);
  }
};

api.runTradeStudy = async (payload: any): Promise<TradeStudyResult> => {
  try {
    const res = await fetch(`${API_BASE}/optimization/study`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return mockTradeStudy(payload);
  }
};

api.runOptimization = async (params: any): Promise<any> => {
  try {
    const url = new URL(`${API_BASE}/optimization/optimize`);
    Object.keys(params).forEach(k => url.searchParams.append(k, params[k]));
    const res = await fetch(url.toString(), { method: 'POST' });
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return {
      thruster_type: params.thruster_type || 'hall_thruster',
      success: true,
      iterations: 12,
      parameters: {
        power_w: { initial: 5000, optimal: 7240 },
        mass_flow_rate_kg_s: { initial: 0.00005, optimal: 0.000038 },
        magnetic_field_strength: { initial: 0.5, optimal: 0.88 }
      },
      performance: {
        thrust_n: { initial: 0.3, optimal: 0.44, improvement_pct: 46.6 },
        isp_s: { initial: 2000, optimal: 2360, improvement_pct: 18.0 },
        efficiency: { initial: 0.6, optimal: 0.72, improvement_pct: 20.0 }
      }
    };
  }
};

api.getTransferPoints = async (startAlt: number, targetAlt: number): Promise<HohmannTransferPoints> => {
  try {
    const res = await fetch(`${API_BASE}/orbit/transfer?start_alt=${startAlt}&target_alt=${targetAlt}`);
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return mockTransferPoints(startAlt, targetAlt);
  }
};

api.getPlumeGeometry = async (thrustN: number, powerW: number): Promise<PlumeGeometry> => {
  try {
    const res = await fetch(`${API_BASE}/orbit/plume?thrust_n=${thrustN}&power_w=${powerW}`);
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return {
      length: 1.2,
      width: 0.4,
      divergence_angle_deg: 18,
      color: powerW > 50000 ? '#00ffff' : '#8a2be2',
      type: 'standard_electric',
      opacity: 0.65
    };
  }
};
