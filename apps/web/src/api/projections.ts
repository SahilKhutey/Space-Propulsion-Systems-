import { api } from './client';

export const projectFuture = (state: any, horizon_s: number) =>
  api.post('/projection/future', { state, horizon_s }).then((r: any) => r.data);
export const predictFailures = (state: any, horizon_s: number) =>
  api.post('/projection/failures', { state, horizon_s }).then((r: any) => r.data);
export const runMonteCarlo = (cfg: any) =>
  api.post('/projection/monte-carlo', cfg).then((r: any) => r.data);
