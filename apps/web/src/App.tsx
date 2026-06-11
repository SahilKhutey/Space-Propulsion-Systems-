import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import { AppShell } from './components/layout/AppShell';

import HomeDashboard from './pages/HomeDashboard';
import MissionDashboard from './pages/MissionDashboard';
import PropulsionDashboard from './pages/PropulsionDashboard';
import ThermalDashboard from './pages/ThermalDashboard';
import PowerDashboard from './pages/PowerDashboard';
import OrbitDashboard from './pages/OrbitDashboard';
import RealTimeDashboard from './pages/RealTimeDashboard';
import DigitalTwinDashboard from './pages/DigitalTwinDashboard';
import AIDashboard from './pages/AIDashboard';
import SimulationDashboard from './pages/SimulationDashboard';
import ReportsDashboard from './pages/ReportsDashboard';
import Settings from './pages/Settings';

const App: React.FC = () => {
  return (
    <HashRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<HomeDashboard />} />
          <Route path="/mission" element={<MissionDashboard />} />
          <Route path="/propulsion" element={<PropulsionDashboard />} />
          <Route path="/thermal" element={<ThermalDashboard />} />
          <Route path="/power" element={<PowerDashboard />} />
          <Route path="/orbit" element={<OrbitDashboard />} />
          <Route path="/realtime" element={<RealTimeDashboard />} />
          <Route path="/digitaltwin" element={<DigitalTwinDashboard />} />
          <Route path="/ai" element={<AIDashboard />} />
          <Route path="/sim" element={<SimulationDashboard />} />
          <Route path="/reports" element={<ReportsDashboard />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </HashRouter>
  );
};

export default App;
export { App };
