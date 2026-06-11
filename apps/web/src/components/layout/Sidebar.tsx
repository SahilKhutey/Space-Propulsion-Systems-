import { NavLink } from 'react-router-dom';
import {
  Home, Rocket, Thermometer, Zap, Orbit, Activity,
  Cpu, Brain, BarChart3, FileText, Settings, Layers,
} from 'lucide-react';
import clsx from 'clsx';

const items = [
  { to: '/',          label: 'Home',          icon: Home },
  { to: '/mission',   label: 'Mission',       icon: Layers },
  { to: '/propulsion',label: 'Propulsion',    icon: Rocket },
  { to: '/thermal',   label: 'Thermal',       icon: Thermometer },
  { to: '/power',     label: 'Power',         icon: Zap },
  { to: '/orbit',     label: 'Orbit',         icon: Orbit },
  { to: '/realtime',  label: 'Real-Time Sim', icon: Activity },
  { to: '/digitaltwin', label: 'Digital Twin', icon: Cpu },
  { to: '/ai',        label: 'AI Optimize',   icon: Brain },
  { to: '/sim',       label: 'Simulations',   icon: BarChart3 },
  { to: '/reports',   label: 'Reports',       icon: FileText },
  { to: '/settings',  label: 'Settings',      icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="w-56 border-r border-space-800/50 bg-space-950/50 backdrop-blur-md p-3 hidden md:flex flex-col gap-1">
      {items.map(({ to, label, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          end={to === '/'}
          className={({ isActive }) => clsx(
            'flex items-center gap-2 px-3 py-2 rounded-md text-sm transition',
            isActive
              ? 'bg-plasma-500/15 text-plasma-300 border-l-2 border-plasma-400'
              : 'text-slate-400 hover:text-slate-100 hover:bg-space-800/40'
          )}
        >
          <Icon className="w-4 h-4" />
          {label}
        </NavLink>
      ))}
    </aside>
  );
}
