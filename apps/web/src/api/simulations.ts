import { api } from './client';

export const runThrust = (params: any) => api.post('/simulation/thrust', params).then((r: any) => r.data);
export const runMission = (params: any) => api.post('/simulation/mission', params).then((r: any) => r.data);
export const runThermal = (params: any) => api.post('/simulation/thermal', params).then((r: any) => r.data);
export const runPower = (params: any) => api.post('/simulation/power', params).then((r: any) => r.data);
export const runTradeStudy = (params: any) => api.post('/trade/compare', params).then((r: any) => r.data);
