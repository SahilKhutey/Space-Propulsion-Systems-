import { useTelemetryStore } from '@/store/useTelemetryStore';

let ws: WebSocket | null = null;

export function connectTelemetry() {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  const url = `${proto}://${location.host}/ws/telemetry`;
  ws = new WebSocket(url);

  ws.onopen = () => console.log('[telemetry] connected');
  ws.onmessage = (ev) => {
    try {
      const p = JSON.parse(ev.data);
      useTelemetryStore.getState().push(p);
    } catch (e) { console.warn('[telemetry] parse error', e); }
  };
  ws.onclose = () => {
    console.log('[telemetry] disconnected; retrying in 3s');
    setTimeout(connectTelemetry, 3000);
  };
  ws.onerror = (e) => console.error('[telemetry] error', e);
}

export function disconnectTelemetry() { ws?.close(); ws = null; }
