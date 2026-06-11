import { api } from './client';

export const syncTelemetry = (telemetry: any) =>
  api.post('/twin/sync', telemetry).then((r: any) => r.data);
export const getTwinEstimation = () =>
  api.get('/twin/estimate').then((r: any) => r.data);
