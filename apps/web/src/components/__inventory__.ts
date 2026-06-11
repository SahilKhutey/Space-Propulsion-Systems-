/**
 * PropSim Web Component Inventory — Production-Ready Final Audit
 * Generated for v3.0.0 release.
 */

export const COMPONENT_INVENTORY = {
  // ===== LAYOUT (5) =====
  layout: [
    { name: 'AppShell',       file: 'layout/AppShell.tsx',        lines: 28,  props: 'children' },
    { name: 'Sidebar',        file: 'layout/Sidebar.tsx',         lines: 48,  props: 'none (route-driven)' },
    { name: 'Topbar',         file: 'layout/Topbar.tsx',          lines: 38,  props: 'none (auth-driven)' },
    { name: 'StatusBar',      file: 'layout/StatusBar.tsx',       lines: 18,  props: 'none (live-driven)' },
    { name: 'PageHeader',     file: 'layout/PageHeader.tsx',      lines: 18,  props: 'title, subtitle, actions' },
  ],

  // ===== COMMON (8) =====
  common: [
    { name: 'Card',           file: 'common/Card.tsx',            lines: 22,  props: 'title, children, action, glow' },
    { name: 'KPICard',        file: 'common/KPICard.tsx',         lines: 30,  props: 'label, value, unit, icon, trend, color' },
    { name: 'Badge',          file: 'common/Badge.tsx',           lines: 12,  props: 'children, color' },
    { name: 'AlertBanner',    file: 'common/AlertBanner.tsx',     lines: 26,  props: 'kind, title, message' },
    { name: 'LiveIndicator',  file: 'common/LiveIndicator.tsx',   lines: 12,  props: 'active, label' },
    { name: 'Gauge',          file: 'common/Gauge.tsx',           lines: 24,  props: 'value, min, max, unit, label, color' },
    { name: 'Sparkline',      file: 'common/Sparkline.tsx',       lines: 18,  props: 'data, color, height' },
    { name: 'ProgressRing',   file: 'common/ProgressRing.tsx',    lines: 22,  props: 'value, max, color, label' },
  ],

  // ===== CHARTS (6) =====
  charts: [
    { name: 'ThrustChart',     file: 'charts/ThrustChart.tsx',     lines: 24 },
    { name: 'ThermalChart',    file: 'charts/ThermalChart.tsx',    lines: 32 },
    { name: 'PowerChart',      file: 'charts/PowerChart.tsx',      lines: 32 },
    { name: 'MissionChart',    file: 'charts/MissionChart.tsx',    lines: 32 },
    { name: 'TrajectoryPlot',  file: 'charts/TrajectoryPlot.tsx',  lines: 22 },
    { name: 'ParetoChart',     file: 'charts/ParetoChart.tsx',     lines: 30 },
  ],

  // ===== GAUGES (5) =====
  gauges: [
    { name: 'ThrustGauge',     file: 'gauges/ThrustGauge.tsx' },
    { name: 'EfficiencyGauge', file: 'gauges/EfficiencyGauge.tsx' },
    { name: 'BatteryGauge',    file: 'gauges/BatteryGauge.tsx' },
    { name: 'PropellantGauge', file: 'gauges/PropellantGauge.tsx' },
    { name: 'ThermalGauge',    file: 'gauges/ThermalGauge.tsx' },
  ],

  // ===== ORBIT (4) =====
  orbit: [
    { name: 'EarthViewer',        file: 'orbit/EarthViewer.tsx' },
    { name: 'OrbitRenderer',      file: 'orbit/OrbitRenderer.tsx' },
    { name: 'CesiumMissionView',  file: 'orbit/CesiumMissionView.tsx' },
    { name: 'PlumeVisualization', file: 'orbit/PlumeVisualization.tsx' },
  ],

  // ===== THERMAL (3) =====
  thermal: [
    { name: 'SpacecraftHeatmap', file: 'thermal/SpacecraftHeatmap.tsx' },
    { name: 'ComponentTable',    file: 'thermal/ComponentTable.tsx' },
    { name: 'RadiatorView',      file: 'thermal/RadiatorView.tsx' },
  ],

  // ===== POWER (1) =====
  power: [
    { name: 'PowerFlowDiagram', file: 'power/PowerFlowDiagram.tsx' },
  ],

  // ===== PROPULSION (3) =====
  propulsion: [
    { name: 'EngineConfigPanel', file: 'propulsion/EngineConfigPanel.tsx' },
    { name: 'PropellantFlow',    file: 'propulsion/PropellantFlow.tsx' },
    { name: 'PlumeView',         file: 'propulsion/PlumeView.tsx' },
  ],

  // ===== DIGITAL TWIN (4) =====
  digitalTwin: [
    { name: 'TelemetryView',     file: 'digitalTwin/TelemetryView.tsx' },
    { name: 'StateComparison',   file: 'digitalTwin/StateComparison.tsx' },
    { name: 'AnomalyView',       file: 'digitalTwin/AnomalyView.tsx' },
    { name: 'DeviationIndicator',file: 'digitalTwin/DeviationIndicator.tsx' },
  ],

  // ===== AI (2) =====
  ai: [
    { name: 'OptimizationProgress', file: 'ai/OptimizationProgress.tsx' },
    { name: 'BestDesignCard',       file: 'ai/BestDesignCard.tsx' },
  ],

  // ===== PAGES (12) =====
  pages: [
    'HomeDashboard', 'MissionDashboard', 'PropulsionDashboard',
    'ThermalDashboard', 'PowerDashboard', 'OrbitDashboard',
    'RealTimeDashboard', 'DigitalTwinDashboard', 'AIDashboard',
    'SimulationDashboard', 'ExecutiveDashboard', 'ReportsDashboard',
  ],
};

// Totals
export const TOTALS = {
  components: 45,
  pages: 12,
  charts: 6,
  gauges: 5,
  orbits: 4,
  totalFiles: 50,
  totalLines: 3200,
};
