import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';
import { StatusBar } from './StatusBar';

export function AppShell() {
  return (
    <div className="min-h-screen flex flex-col">
      <Topbar />
      <div className="flex-1 flex">
        <Sidebar />
        <main className="flex-1 overflow-auto p-4">
          <Outlet />
        </main>
      </div>
      <StatusBar />
    </div>
  );
}
