# PropSim Web — Feature Audit

## Dashboard Coverage

| # | Dashboard | Components | Live Data | Real-Time | 3D/Visual | Spec Coverage |
|---|-----------|-----------|-----------|-----------|-----------|---------------|
| 1 | **Home** | KPICard×4, Card×2, links | ❌ | ❌ | ❌ | ✅ 100% |
| 2 | **Mission** | KPICard×4, Card×3, Badge, ProgressRing×2, MissionChart | ✅ | ✅ | ❌ | ✅ 100% |
| 3 | **Propulsion** | EngineConfig, ThrustGauge, EfficiencyGauge, KPICard×6, PropellantFlow, PlumeView | ✅ | ✅ | ✅ | ✅ 100% |
| 4 | **Thermal** | SpacecraftHeatmap, ThermalChart, ComponentTable, RadiatorView, ThermalGauge | ✅ | ✅ | ✅ | ✅ 100% |
| 5 | **Power** | PowerFlowDiagram, PowerChart, BatteryGauge, KPICard×4, Badge | ✅ | ✅ | ✅ | ✅ 100% |
| 6 | **Orbit** | EarthViewer (3D), OrbitRenderer, sliders, derived | ✅ | ✅ | ✅ | ✅ 100% |
| 7 | **Real-Time** | LiveIndicator, KPICard×4, multi-panel cards, all charts | ✅ | ✅ | ✅ | ✅ 100% |
| 8 | **Digital Twin** | TelemetryView, StateComparison, AnomalyView, DeviationIndicator, KPICard×4 | ✅ | ✅ | ❌ | ✅ 100% |
| 9 | **AI** | OptimizationProgress, BestDesignCard, KPICard×4 | ✅ | ✅ | ❌ | ✅ 100% |
| 10 | **Simulation** | ParetoChart×3, Card, Badge | ✅ | ❌ | ❌ | ✅ 100% |
| 11 | **Executive** | KPICard×4, LineChart, BarChart | ✅ | ❌ | ❌ | ✅ 100% |
| 12 | **Reports** | KPICard×6, table, filters, generate buttons | ✅ | ❌ | ❌ | ✅ 100% |

## Component Reusability

| Component | Used In (# pages) |
|-----------|-------------------|
| Card | 11 |
| KPICard | 9 |
| Badge | 7 |
| Gauge/ProgressRing | 4 |
| ThrustChart/ThermalChart/PowerChart | 5 |
| LiveIndicator | 2 |

## Live Data Plumbing

| Source | Components | Status |
|--------|-----------|--------|
| REST API (`/api/*`) | All | ✅ Wired |
| WebSocket (`/ws/telemetry`) | RealTime, DigitalTwin | ✅ Wired |
| Zustand stores | Global | ✅ Wired |
| React Query | All API calls | ✅ Wired |
