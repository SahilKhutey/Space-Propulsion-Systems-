import { Rocket, User, LogOut, Bell } from 'lucide-react';
import { useAuthStore } from '@/store/useAuthStore';
import { LiveIndicator } from '@/components/common/LiveIndicator';
import { useSimulationStore } from '@/store/useSimulationStore';

export function Topbar() {
  const { user, logout } = useAuthStore();
  const isRunning = useSimulationStore((s) => s.isRunning);
  return (
    <header className="h-12 border-b border-space-800/50 bg-space-950/70 backdrop-blur-md
                       flex items-center justify-between px-4">
      <div className="flex items-center gap-2">
        <Rocket className="w-5 h-5 text-plasma-400" />
        <span className="font-display font-bold text-plasma-300 tracking-wide">PropSim</span>
        <span className="text-slate-500 text-xs">Mission Control</span>
      </div>
      <div className="flex items-center gap-3">
        <LiveIndicator active={isRunning} label="LIVE" />
        <Bell className="w-4 h-4 text-slate-400 cursor-pointer" />
        {user ? (
          <div className="flex items-center gap-2 text-sm text-slate-300">
            <User className="w-4 h-4" />
            {user.username}
            <button onClick={logout} className="ml-2 text-slate-500 hover:text-red-400">
              <LogOut className="w-3.5 h-3.5" />
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2 text-sm text-slate-300">
            <User className="w-4 h-4" />
            Guest
          </div>
        )}
      </div>
    </header>
  );
}
