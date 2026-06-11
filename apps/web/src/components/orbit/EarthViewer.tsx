import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, useTexture } from '@react-three/drei';
import { useMemo, useRef } from 'react';
import * as THREE from 'three';

const EARTH_R = 6.371e6;
const SCALE = 1 / 1e5; // 1 unit = 100km in scene

function OrbitLine({ points, color = '#06b6d4' }: { points: number[][]; color?: string }) {
  const lineObj = useMemo(() => {
    const geom = new THREE.BufferGeometry();
    geom.setFromPoints(points.map(([x, y, z]) => new THREE.Vector3(x * SCALE, y * SCALE, z * SCALE)));
    const mat = new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.7 });
    return new THREE.Line(geom, mat);
  }, [points, color]);
  return <primitive object={lineObj} />;
}

function Earth() {
  let tex: any = null;
  try {
    tex = useTexture('/textures/earth_day.jpg');
  } catch (e) {
    // Texture fallback
  }
  return (
    <mesh>
      <sphereGeometry args={[EARTH_R * SCALE, 64, 64]} />
      {tex ? (
        <meshStandardMaterial map={tex} roughness={0.9} metalness={0.05} />
      ) : (
        <meshStandardMaterial color="#1e3a8a" roughness={0.9} metalness={0.05} />
      )}
    </mesh>
  );
}

function Sun() {
  return (
    <pointLight position={[20, 5, 10]} intensity={1.5} color="#fff5d6" />
  );
}

function Spacecraft({ position }: { position: [number, number, number] }) {
  const ref = useRef<THREE.Mesh>(null);
  return (
    <mesh ref={ref} position={position.map(p => p * SCALE) as [number, number, number]}>
      <coneGeometry args={[0.4, 1.2, 8]} />
      <meshStandardMaterial color="#06b6d4" emissive="#06b6d4" emissiveIntensity={0.4} />
    </mesh>
  );
}

export function EarthViewer({ orbitPoints, scPosition }:
  { orbitPoints?: number[][]; scPosition?: [number, number, number] }) {
  return (
    <div className="w-full h-[350px] relative rounded-xl overflow-hidden border border-space-800">
      <Canvas camera={{ position: [0, 50, 100], fov: 45 }} style={{ background: 'radial-gradient(ellipse at center, #050828, #000)' }}>
        <ambientLight intensity={0.15} />
        <Sun />
        <Stars radius={300} depth={50} count={8000} factor={4} fade speed={1} />
        <Earth />
        {orbitPoints && <OrbitLine points={orbitPoints} />}
        {scPosition && <Spacecraft position={scPosition} />}
        <OrbitControls enablePan enableZoom enableRotate minDistance={15} maxDistance={400} />
      </Canvas>
    </div>
  );
}
