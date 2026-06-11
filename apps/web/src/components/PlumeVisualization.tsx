import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

export function PlumeVisualization({ thrust_n, isp_s, divergence = 15 }:
  { thrust_n: number; isp_s: number; divergence?: number }) {
  const len = Math.min(8, thrust_n * 4);
  const radius = len * Math.tan(THREE.MathUtils.degToRad(divergence));
  const color = new THREE.Color().setHSL(0.1 - 0.05 * Math.min(1, thrust_n), 1.0, 0.55);

  return (
    <Canvas camera={{ position: [6, 3, 8], fov: 50 }}>
      <ambientLight intensity={0.3} />
      <pointLight position={[5, 5, 5]} intensity={1.2} />
      <mesh>
        <sphereGeometry args={[0.7, 32, 32]} />
        <meshStandardMaterial color="#6478ff" metalness={0.7} roughness={0.2} />
      </mesh>
      {thrust_n > 0 && (
        <>
          <mesh position={[0, -len / 2 - 0.7, 0]}>
            <coneGeometry args={[radius, len, 32, 1, true]} />
            <meshBasicMaterial color={color} transparent opacity={0.65} side={THREE.DoubleSide} />
          </mesh>
          {/* Glow disc */}
          <mesh position={[0, -0.7, 0]} rotation={[Math.PI / 2, 0, 0]}>
            <ringGeometry args={[0.1, radius, 32]} />
            <meshBasicMaterial color={color} side={THREE.DoubleSide} transparent opacity={0.4} />
          </mesh>
        </>
      )}
      <gridHelper args={[20, 20, '#1f2a99', '#141c6e']} />
      <OrbitControls enablePan={false} />
    </Canvas>
  );
}
export default PlumeVisualization;
