import { ReactNode } from 'react';
import clsx from 'clsx';

export function Card({ title, children, className, action, glow }:
  { title?: string; children: ReactNode; className?: string; action?: ReactNode; glow?: 'cyan' | 'amber' | 'red' }) {
  return (
    <div className={clsx('panel p-4', className, glow === 'cyan' && 'glow-cyan', glow === 'amber' && 'glow-amber', glow === 'red' && 'glow-red')}>
      {(title || action) && (
        <div className="flex justify-between items-center mb-3">
          {title && <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider">{title}</h3>}
          {action}
        </div>
      )}
      {children}
    </div>
  );
}
