import React from 'react';
import { Shield, Radio, Database, Cpu, Compass, Flame, Sun, Thermometer, Activity, Settings, TrendingUp } from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Layout: React.FC<LayoutProps> = ({ children, activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'thrust', label: 'Thrust Engine', icon: Flame },
    { id: 'isp', label: 'Isp & Fuel', icon: TrendingUp },
    { id: 'power', label: 'Power Grid', icon: Sun },
    { id: 'thermal', label: 'Thermal Nodes', icon: Thermometer },
    { id: 'mission', label: 'Mission Planner', icon: Compass },
    { id: 'trade', label: 'Trade Study', icon: Shield },
  ];

  return (
    <div className="flex h-screen bg-space-950 text-slate-100 overflow-hidden font-sans relative">
      <div className="absolute inset-0 bg-grid-pattern bg-[size:30px_30px] opacity-[0.03] pointer-events-none" />
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-aerospace-cyan/5 rounded-full blur-[150px] pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-aerospace-blue/5 rounded-full blur-[150px] pointer-events-none" />

      <aside className="w-80 glass-panel border-r border-slate-800 flex flex-col z-10 shrink-0">
        <div className="p-6 border-b border-slate-800/80 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-tr from-aerospace-blue to-aerospace-cyan flex items-center justify-center glow-border-cyan">
            <Cpu className="w-6 h-6 text-space-950 stroke-[2.5]" />
          </div>
          <div>
            <h1 className="font-bold text-xl tracking-wide font-sans text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-100 to-slate-400">
              PROPSIM
            </h1>
            <span className="text-[10px] uppercase tracking-widest text-aerospace-cyan font-bold glow-text-cyan">
              Digital Twin v1.0
            </span>
          </div>
        </div>

        <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
          <p className="text-[10px] uppercase font-bold text-slate-500 tracking-wider px-3 mb-2">Simulation Suites</p>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3.5 px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-aerospace-cyan/15 text-aerospace-cyan border border-aerospace-cyan/35 shadow-[0_0_15px_rgba(6,182,212,0.1)]'
                    : 'text-slate-400 hover:bg-slate-900/60 hover:text-slate-100 border border-transparent'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-aerospace-cyan' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="p-4 border-t border-slate-800/80 space-y-3 bg-slate-950/40">
          <p className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">System Telemetry</p>
          <div className="grid grid-cols-2 gap-2 text-[11px]">
            <div className="flex items-center gap-1.5 text-slate-400">
              <Database className="w-3.5 h-3.5 text-aerospace-emerald" />
              <span>DB: <b className="text-slate-300">Online</b></span>
            </div>
            <div className="flex items-center gap-1.5 text-slate-400">
              <Radio className="w-3.5 h-3.5 text-aerospace-emerald" />
              <span>Core: <b className="text-slate-300">Ready</b></span>
            </div>
            <div className="flex items-center gap-1.5 text-slate-400 col-span-2">
              <Activity className="w-3.5 h-3.5 text-aerospace-cyan animate-pulse" />
              <span>API Gateway: <b className="text-slate-300">Connected</b></span>
            </div>
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col overflow-hidden z-10">
        <header className="h-20 border-b border-slate-800/80 flex items-center justify-between px-8 bg-slate-950/20 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-aerospace-cyan animate-pulse" />
            <h2 className="text-lg font-semibold text-slate-200 uppercase tracking-wide">
              {navItems.find(n => n.id === activeTab)?.label || 'Console'}
            </h2>
          </div>
          <div className="flex items-center gap-4">
            <div className="px-4 py-1.5 rounded-full bg-slate-900 border border-slate-800 flex items-center gap-2 text-xs text-slate-400">
              <Settings className="w-3.5 h-3.5" />
              <span>Node Environment: <b className="text-slate-300">Localhost</b></span>
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-8 bg-space-950/30">
          <div className="max-w-7xl mx-auto h-full flex flex-col">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
};
