import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface Visualization3DProps {
  startAlt: number;
  targetAlt: number;
  thrust: number;
  power: number;
}

export const Visualization3D: React.FC<Visualization3DProps> = ({
  startAlt,
  targetAlt,
  thrust,
  power
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const paramsRef = useRef({ startAlt, targetAlt, thrust, power });
  
  useEffect(() => {
    paramsRef.current = { startAlt, targetAlt, thrust, power };
  }, [startAlt, targetAlt, thrust, power]);

  useEffect(() => {
    if (!containerRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight || 350;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color('#030712');

    const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.set(0, 15, 25);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    containerRef.current.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight1.position.set(5, 10, 7);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x06b6d4, 0.5);
    dirLight2.position.set(-5, -5, -5);
    scene.add(dirLight2);

    const gridHelper = new THREE.GridHelper(40, 40, '#1e293b', '#0f172a');
    gridHelper.position.y = -4;
    scene.add(gridHelper);

    const earthGeo = new THREE.SphereGeometry(3.5, 32, 32);
    const earthMat = new THREE.MeshPhongMaterial({ color: 0x1e293b, emissive: 0x0b0f19, shininess: 20 });
    const earthMesh = new THREE.Mesh(earthGeo, earthMat);
    scene.add(earthMesh);

    const wireMat = new THREE.MeshBasicMaterial({ color: 0x06b6d4, wireframe: true, transparent: true, opacity: 0.15 });
    const earthWire = new THREE.Mesh(earthGeo, wireMat);
    scene.add(earthWire);

    const satGroup = new THREE.Group();
    const satBodyGeo = new THREE.BoxGeometry(0.6, 0.6, 0.8);
    const satBodyMat = new THREE.MeshPhongMaterial({ color: 0x94a3b8, shininess: 80 });
    const satBody = new THREE.Mesh(satBodyGeo, satBodyMat);
    satGroup.add(satBody);

    const panelGeo = new THREE.BoxGeometry(1.6, 0.05, 0.4);
    const panelMat = new THREE.MeshPhongMaterial({ color: 0x0284c7, shininess: 90 });
    const leftPanel = new THREE.Mesh(panelGeo, panelMat);
    leftPanel.position.x = 1.1;
    satGroup.add(leftPanel);

    const rightPanel = new THREE.Mesh(panelGeo, panelMat);
    rightPanel.position.x = -1.1;
    satGroup.add(rightPanel);

    const plumeGeo = new THREE.ConeGeometry(0.25, 0.8, 16);
    plumeGeo.translate(0, -0.4, 0);
    plumeGeo.rotateX(Math.PI / 2);
    const plumeMat = new THREE.MeshBasicMaterial({
      color: 0x8a2be2,
      transparent: true,
      opacity: 0.7,
      blending: THREE.AdditiveBlending
    });
    const plumeMesh = new THREE.Mesh(plumeGeo, plumeMat);
    plumeMesh.position.z = 0.4;
    satGroup.add(plumeMesh);
    scene.add(satGroup);

    let orbitLineInit: THREE.Line | null = null;
    let orbitLineFinal: THREE.Line | null = null;
    let orbitLineTrans: THREE.Line | null = null;

    const minAlt = 400000;
    const maxAlt = 400000000;
    const scaleAlt = (alt: number) => {
      const logMin = Math.log10(minAlt);
      const logMax = Math.log10(maxAlt);
      const logVal = Math.log10(Math.max(minAlt, alt));
      const pct = (logVal - logMin) / (logMax - logMin);
      return 4.2 + pct * 7.3;
    };

    const updateOrbits = () => {
      const { startAlt: sAlt, targetAlt: tAlt, thrust: th, power: p } = paramsRef.current;
      const r1 = scaleAlt(sAlt);
      const r2 = scaleAlt(tAlt);

      if (orbitLineInit) scene.remove(orbitLineInit);
      if (orbitLineFinal) scene.remove(orbitLineFinal);
      if (orbitLineTrans) scene.remove(orbitLineTrans);

      const initPoints = [];
      for (let i = 0; i <= 64; i++) {
        const theta = (i / 64) * 2 * Math.PI;
        initPoints.push(new THREE.Vector3(r1 * Math.cos(theta), 0, r1 * Math.sin(theta)));
      }
      const initGeo = new THREE.BufferGeometry().setFromPoints(initPoints);
      const initMat = new THREE.LineBasicMaterial({ color: 0x2563eb, transparent: true, opacity: 0.4 });
      orbitLineInit = new THREE.Line(initGeo, initMat);
      scene.add(orbitLineInit);

      const finalPoints = [];
      for (let i = 0; i <= 64; i++) {
        const theta = (i / 64) * 2 * Math.PI;
        finalPoints.push(new THREE.Vector3(r2 * Math.cos(theta), 0, r2 * Math.sin(theta)));
      }
      const finalGeo = new THREE.BufferGeometry().setFromPoints(finalPoints);
      const finalMat = new THREE.LineBasicMaterial({ color: 0x06b6d4, transparent: true, opacity: 0.4 });
      orbitLineFinal = new THREE.Line(finalGeo, finalMat);
      scene.add(orbitLineFinal);

      const transPoints = [];
      const a_trans = (r1 + r2) / 2;
      const e_trans = Math.abs(r2 - r1) / (r1 + r2);
      const phase = r1 < r2 ? 0 : Math.PI;
      for (let i = 0; i <= 50; i++) {
        const theta = (i / 50) * Math.PI;
        const r = a_trans * (1 - e_trans * e_trans) / (1 + e_trans * Math.cos(theta));
        transPoints.push(new THREE.Vector3(r * Math.cos(theta + phase), 0, r * Math.sin(theta + phase)));
      }
      const transGeo = new THREE.BufferGeometry().setFromPoints(transPoints);
      const transMat = new THREE.LineDashedMaterial({ color: 0xf59e0b, dashSize: 0.5, gapSize: 0.3 });
      orbitLineTrans = new THREE.Line(transGeo, transMat);
      orbitLineTrans.computeLineDistances();
      scene.add(orbitLineTrans);

      if (th > 0) {
        plumeMesh.visible = true;
        plumeMesh.scale.set(1.0, 1.0, 0.5 + Math.log10(1 + th * 2.0));
        if (p === 0) plumeMat.color.setHex(0xff4500);
        else if (p > 50000) plumeMat.color.setHex(0x00ffff);
        else plumeMat.color.setHex(0x8a2be2);
      } else {
        plumeMesh.visible = false;
      }
    };

    updateOrbits();

    let angle = 0;
    let clock = new THREE.Clock();

    const animate = () => {
      requestAnimationFrame(animate);
      const delta = clock.getDelta();
      const { startAlt: sAlt, targetAlt: tAlt, thrust: th } = paramsRef.current;

      const r1 = scaleAlt(sAlt);
      const r2 = scaleAlt(tAlt);

      updateOrbits();

      earthMesh.rotation.y += 0.005;
      earthWire.rotation.y += 0.003;

      const speed = th > 0 ? 0.35 : 0.15;
      angle += speed * delta;

      const a_trans = (r1 + r2) / 2;
      const e_trans = Math.abs(r2 - r1) / (r1 + r2);
      const phase = r1 < r2 ? 0 : Math.PI;
      const theta = (angle % Math.PI);
      const r = a_trans * (1 - e_trans * e_trans) / (1 + e_trans * Math.cos(theta));

      const px = r * Math.cos(theta + phase);
      const pz = r * Math.sin(theta + phase);
      satGroup.position.set(px, 0, pz);

      const tangentX = -Math.sin(theta + phase);
      const tangentZ = Math.cos(theta + phase);
      satGroup.rotation.y = Math.atan2(-tangentZ, tangentX);

      if (plumeMesh.visible) {
        plumeMesh.scale.x = 0.9 + 0.2 * Math.sin(Date.now() * 0.05);
      }
      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight || 350;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (containerRef.current && renderer.domElement) {
        containerRef.current.removeChild(renderer.domElement);
      }
      earthGeo.dispose();
      earthMat.dispose();
      wireMat.dispose();
      satBodyGeo.dispose();
      satBodyMat.dispose();
      panelGeo.dispose();
      panelMat.dispose();
      plumeGeo.dispose();
      plumeMat.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div className="glass-panel p-4 rounded-xl flex flex-col h-full glow-border-cyan select-none relative overflow-hidden">
      <div className="absolute top-4 left-4 z-20 pointer-events-none">
        <h4 className="text-xs font-bold uppercase tracking-wider text-aerospace-cyan glow-text-cyan">
          3D Orbital Trajectory Planner
        </h4>
        <span className="text-[10px] text-slate-500 font-mono">Real-time digital twin visualization</span>
      </div>
      <div ref={containerRef} className="w-full h-80 lg:h-96 rounded-lg overflow-hidden border border-slate-900 bg-space-950/40 relative shadow-inner" />
    </div>
  );
};
