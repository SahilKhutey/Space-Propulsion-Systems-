import { EarthViewer } from './EarthViewer';

export function TrajectoryRenderer({ history }: { history: Array<{ position_m: number[] }> }) {
  const points = history.map(h => h.position_m);
  const currentPos = points.length > 0 ? points[points.length - 1] : [7000000.0, 0, 0];
  return <EarthViewer orbitPoints={points} scPosition={currentPos as [number, number, number]} />;
}
