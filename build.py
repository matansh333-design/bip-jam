import json

with open('/home/claude/bipjam/cube_data_final.json') as f:
    cube_data = json.load(f)
print('data keys:', list(cube_data.keys()))

cube_data_json = json.dumps(cube_data, separators=(',', ':'))

html_template = r'''<style>
  .bipjam-root {
    --blue-deep: #4C5FD9;
    --blue-mid: #6C7EEE;
    --blue-light: #8FA0F7;
    --purple: #8B5CF6;
    --purple-glow: #A78BFA;
    --ink: #2A2F5C;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
  }
  .bipjam-viewport {
    position: relative;
    width: 100%;
    height: 640px;
    border-radius: 28px;
    overflow: hidden;
    background: radial-gradient(120% 140% at 30% 15%, var(--blue-light) 0%, var(--blue-mid) 45%, var(--blue-deep) 100%);
    box-shadow: 0 20px 60px rgba(40, 48, 130, 0.35), inset 0 1px 0 rgba(255,255,255,0.15);
    touch-action: none;
    cursor: grab;
  }
  .bipjam-viewport.dragging { cursor: grabbing; }
  .bipjam-viewport canvas { display: block; width: 100%; height: 100%; }

  .bipjam-hud {
    position: absolute;
    inset: 0;
    pointer-events: none;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 22px 26px;
  }
  .bipjam-logo {
    display: flex;
    flex-direction: column;
    line-height: 1;
    user-select: none;
  }
  .bipjam-logo .bip {
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
  }
  .bipjam-logo .jam {
    font-size: 12px;
    font-weight: 600;
    color: rgba(255,255,255,0.75);
    letter-spacing: 3px;
    margin-top: 2px;
  }
  .bipjam-hint {
    align-self: flex-start;
    background: rgba(255,255,255,0.14);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.25);
    color: #fff;
    font-size: 12.5px;
    font-weight: 500;
    padding: 8px 14px;
    border-radius: 999px;
    direction: rtl;
  }
  .bipjam-transport {
    align-self: flex-start;
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.16);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.28);
    padding: 8px 10px 8px 16px;
    border-radius: 999px;
    direction: ltr;
    pointer-events: auto;
  }
  .bipjam-play-btn {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    border: none;
    background: #fff;
    color: var(--purple);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    flex: none;
    transition: transform 0.15s ease;
  }
  .bipjam-play-btn:active { transform: scale(0.9); }
  .bipjam-play-btn svg { width: 15px; height: 15px; }
  .bipjam-bpm {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #fff;
    font-size: 12.5px;
    font-weight: 600;
    direction: rtl;
  }
  .bipjam-bpm-step {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.4);
    background: transparent;
    color: #fff;
    font-size: 13px;
    line-height: 1;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .bipjam-bars-toggle {
    display: flex;
    align-items: center;
    gap: 4px;
    direction: ltr;
  }
  .bipjam-bars-opt {
    min-width: 28px;
    height: 24px;
    padding: 0 8px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.4);
    background: transparent;
    color: #fff;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
  }
  .bipjam-bars-opt.active {
    background: #fff;
    color: var(--ink);
    border-color: #fff;
  }
  .bipjam-beat-dots {
    display: flex;
    gap: 4px;
    margin-inline-start: 4px;
  }
  .bipjam-beat-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: rgba(255,255,255,0.35);
    transition: background 0.1s ease, transform 0.1s ease;
  }
  .bipjam-beat-dot.on {
    background: #fff;
    transform: scale(1.35);
  }
  .bipjam-palette-item {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.92);
    color: var(--ink);
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 700;
    cursor: grab;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    touch-action: none;
    user-select: none;
    pointer-events: auto;
    direction: rtl;
  }
  .bipjam-palette-item:active { cursor: grabbing; transform: scale(0.96); }
  .bipjam-badge {
    align-self: flex-end;
    background: rgba(255,255,255,0.92);
    color: var(--ink);
    font-size: 12px;
    font-weight: 700;
    padding: 7px 14px;
    border-radius: 999px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    direction: rtl;
  }
  .bipjam-loading {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255,255,255,0.85);
    font-size: 14px;
    font-weight: 600;
    transition: opacity 0.4s ease;
  }
</style>

<div class="bipjam-root">
  <div class="bipjam-viewport" id="bipjam-viewport">
    <div class="bipjam-loading" id="bipjam-loading">טוען משטח…</div>
    <div class="bipjam-hud">
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div class="bipjam-logo"><span class="bip">bip</span><span class="jam">JAM</span></div>
        <div style="display:flex; flex-direction:column; align-items:flex-end; gap:8px; pointer-events:auto;">
          <div class="bipjam-badge" id="bipjam-counter">לחץ על קובייה כדי לעמוד עליה</div>
          <div class="bipjam-bars-toggle" id="bipjam-view-toggle">
            <button class="bipjam-bars-opt active" data-view="iso">איזו</button>
            <button class="bipjam-bars-opt" data-view="top">מעל</button>
            <button class="bipjam-bars-opt" data-view="side">צד</button>
            <button class="bipjam-bars-opt" data-view="front">חזית</button>
          </div>
        </div>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:flex-end;">
        <div class="bipjam-transport">
          <button class="bipjam-play-btn" id="bipjam-play-btn" aria-label="הפעל מטרונום">
            <svg id="bipjam-play-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
            <svg id="bipjam-pause-icon" viewBox="0 0 24 24" fill="currentColor" style="display:none"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg>
          </button>
          <div class="bipjam-bars-toggle" id="bipjam-bars-toggle">
            <button class="bipjam-bars-opt active" data-bars="4">4</button>
            <button class="bipjam-bars-opt" data-bars="8">8</button>
            <button class="bipjam-bars-opt" data-bars="12">12</button>
          </div>
          <div class="bipjam-bpm">
            <button class="bipjam-bpm-step" id="bipjam-bpm-minus">–</button>
            <span id="bipjam-bpm-label">120 BPM</span>
            <button class="bipjam-bpm-step" id="bipjam-bpm-plus">+</button>
          </div>
          <div class="bipjam-beat-dots" id="bipjam-beat-dots"></div>
        </div>
        <div style="display:flex; gap:8px;">
          <div class="bipjam-palette-item" id="bipjam-drum-chip" data-element-type="drum">
            <span style="font-size:16px;">🥁</span><span>תוף</span>
          </div>
          <div class="bipjam-palette-item" id="bipjam-tree-chip" data-element-type="tree">
            <span style="font-size:16px;">🌳</span><span>עץ</span>
          </div>
          <div class="bipjam-palette-item" id="bipjam-triangle-chip" data-element-type="triangle">
            <span style="font-size:16px;">🔺</span><span>משולש</span>
          </div>
        </div>
        <div class="bipjam-hint">גרור אלמנט למשטח &nbsp;·&nbsp; קליק על אלמנט = הסרה &nbsp;·&nbsp; קליק ריק = מעבר לקובייה</div>
      </div>
    </div>
  </div>
</div>

<script type="module">
import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/0.185.1/three.module.js';

const CUBE_DATA = __CUBE_DATA_JSON__;

let numBars = 4;
let GRID_COLS = numBars * 4;   // timeline steps
const GRID_ROWS = 4;    // lanes
const HIGHLIGHT_COLOR = 0x8B5CFF;

const viewport = document.getElementById('bipjam-viewport');
const loadingEl = document.getElementById('bipjam-loading');
const counterEl = document.getElementById('bipjam-counter');

// ---------- renderer / scene / camera ----------
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 500);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
viewport.appendChild(renderer.domElement);

// ---------- soft procedural environment (adds gentle reflections so materials don't look flat/plastic) ----------
function buildEnvironmentTexture() {
  const c = document.createElement('canvas');
  c.width = 64; c.height = 64;
  const ctx = c.getContext('2d');
  const grad = ctx.createLinearGradient(0, 0, 0, 64);
  grad.addColorStop(0, '#dfe6ff');
  grad.addColorStop(0.45, '#97a6f2');
  grad.addColorStop(0.75, '#6e79d6');
  grad.addColorStop(1, '#42407a');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 64, 64);
  const tex = new THREE.CanvasTexture(c);
  tex.mapping = THREE.EquirectangularReflectionMapping;
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}
scene.environment = buildEnvironmentTexture();

// ---------- lighting ----------
const hemi = new THREE.HemisphereLight(0xdfe8ff, 0x6a5a8a, 0.9);
scene.add(hemi);

const sun = new THREE.DirectionalLight(0xfff2d9, 1.6);
sun.position.set(9, 16, 7);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.left = -18;
sun.shadow.camera.right = 18;
sun.shadow.camera.top = 18;
sun.shadow.camera.bottom = -18;
sun.shadow.camera.near = 1;
sun.shadow.camera.far = 50;
sun.shadow.bias = -0.0025;
scene.add(sun);

const fill = new THREE.DirectionalLight(0xaab8ff, 0.35);
fill.position.set(-10, 6, -8);
scene.add(fill);

// ---------- decode helpers ----------
function b64ToFloat32(b64) {
  const bin = atob(b64);
  const buf = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
  return new Float32Array(buf.buffer);
}
function b64ToUint16(b64) {
  const bin = atob(b64);
  const buf = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
  return new Uint16Array(buf.buffer);
}
function b64ToUint32(b64) {
  const bin = atob(b64);
  const buf = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
  return new Uint32Array(buf.buffer);
}
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function clamp01(v) { return Math.min(1, Math.max(0, v)); }

// ---------- shared geometries (built once, reused by every tile) ----------
const baseColors = CUBE_DATA.materials.map(m => new THREE.Color().setRGB(m.color[0], m.color[1], m.color[2], THREE.LinearSRGBColorSpace));
const purpleBaseColor = new THREE.Color().setRGB(CUBE_DATA.purpleColor[0], CUBE_DATA.purpleColor[1], CUBE_DATA.purpleColor[2], THREE.LinearSRGBColorSpace);

const primGeometries = CUBE_DATA.primitives.map(prim => {
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(b64ToFloat32(prim.positions_b64), 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(b64ToFloat32(prim.normals_b64), 3));
  geo.setIndex(new THREE.BufferAttribute(b64ToUint16(prim.indices_b64), 1));
  geo.computeBoundingBox();
  geo.computeBoundingSphere();
  return { geo, materialIndex: prim.material };
});

const unionBox = new THREE.Box3();
primGeometries.forEach(p => unionBox.union(p.geo.boundingBox));
const tileSize = new THREE.Vector3();
unionBox.getSize(tileSize);
const tileCenter = new THREE.Vector3();
unionBox.getCenter(tileCenter);

const SPACING = Math.max(tileSize.x, tileSize.z);
// columns sit flush against each other, except at the divider boundaries where a tiny
// gap opens up just wide enough for the divider bar to sit without cutting into the cubes
const BAR_SIZE = 4; // columns per group
const DIVIDER_GAP = SPACING * 0.07;
function isGroupBoundary(colAfter) { return (colAfter + 1) % BAR_SIZE === 0 && (colAfter + 1) < GRID_COLS; }

const highlightGeo = new THREE.BoxGeometry(tileSize.x * 1.06, tileSize.y * 1.12, tileSize.z * 1.06);
highlightGeo.translate(tileCenter.x, tileCenter.y, tileCenter.z);

// gives each tile a slightly unique, hand-made material instead of a flat repeated color
function makeTileMaterial(baseColor, seed, opts) {
  opts = opts || {};
  const rand = mulberry32(seed);
  const hsl = { h: 0, s: 0, l: 0 };
  baseColor.getHSL(hsl);
  const hueJitter = opts.hueJitter != null ? opts.hueJitter : 0.015;
  const satJitter = opts.satJitter != null ? opts.satJitter : 0.1;
  const lightJitter = opts.lightJitter != null ? opts.lightJitter : 0.07;
  const h = clamp01(hsl.h + (rand() - 0.5) * hueJitter);
  const s = clamp01(hsl.s + (rand() - 0.5) * satJitter);
  const l = clamp01(hsl.l + (rand() - 0.5) * lightJitter);
  const c = new THREE.Color().setHSL(h, s, l);
  return new THREE.MeshStandardMaterial({
    color: c,
    roughness: 0.6 + rand() * 0.15,
    metalness: 0.04,
    envMapIntensity: opts.envMapIntensity != null ? opts.envMapIntensity : 0.55,
    emissive: opts.emissive || 0x000000,
    emissiveIntensity: opts.emissiveIntensity || 0,
  });
}

// ---------- build the grid (rebuildable so bars can be added/removed later) ----------
const gridGroup = new THREE.Group();
scene.add(gridGroup);
const shadowPlaneMat = new THREE.ShadowMaterial({ opacity: 0.18 });

let cubes = [];
let raycastTargets = [];
let dividerMeshes = [];
let shadowPlane = null;
let colCenters = [];
let colCenterOffset = 0;
let seedCounter = 1;

// ---------- bar dividers: shared geometry/material, instances rebuilt per bar count ----------
const dividerColor = new THREE.Color().setRGB(CUBE_DATA.divider.materials[0].color[0], CUBE_DATA.divider.materials[0].color[1], CUBE_DATA.divider.materials[0].color[2], THREE.LinearSRGBColorSpace);
const dividerPrim = CUBE_DATA.divider.primitives[0];
const dividerGeo = new THREE.BufferGeometry();
dividerGeo.setAttribute('position', new THREE.BufferAttribute(b64ToFloat32(dividerPrim.positions_b64), 3));
dividerGeo.setAttribute('normal', new THREE.BufferAttribute(b64ToFloat32(dividerPrim.normals_b64), 3));
dividerGeo.setIndex(new THREE.BufferAttribute(b64ToUint16(dividerPrim.indices_b64), 1));
dividerGeo.computeBoundingBox();
dividerGeo.computeBoundingSphere();

const dividerMat = new THREE.MeshStandardMaterial({
  color: dividerColor,
  roughness: 0.5,
  metalness: 0.05,
  envMapIntensity: 0.6,
});

// ---------- camera framing state (populated by rebuildScene) ----------
const target = new THREE.Vector3(0, tileSize.y * 0.55, 0);
const spherical = { radius: 30, theta: -Math.PI * 0.22, phi: Math.PI * 0.34 };
let MIN_RADIUS = 5, MAX_RADIUS = 100;
const MIN_PHI = 0.04;
const MAX_PHI = Math.PI * 0.5;

function updateCamera() {
  const r = spherical.radius, p = spherical.phi, t = spherical.theta;
  camera.position.set(
    target.x + r * Math.sin(p) * Math.sin(t),
    target.y + r * Math.cos(p),
    target.z + r * Math.sin(p) * Math.cos(t)
  );
  camera.lookAt(target);
}

function disposeCube(cube) {
  cube.highlightMat.dispose();
  cube.meshes.forEach(m => { m.normalMat.dispose(); m.purpleMat.dispose(); });
}

function rebuildScene(fitCamera) {
  if (typeof isPlaying !== 'undefined' && isPlaying) stopPlayback();
  currentIndex = -1;
  hoveredIndex = -1;

  if (typeof placedElements !== 'undefined') {
    placedElements.forEach(el => scene.remove(el.group));
    placedElements = [];
  }

  cubes.forEach(disposeCube);
  while (gridGroup.children.length) gridGroup.remove(gridGroup.children[0]);
  cubes = [];
  raycastTargets = [];

  dividerMeshes.forEach(m => scene.remove(m));
  dividerMeshes = [];

  colCenters = [0];
  for (let col = 1; col < GRID_COLS; col++) {
    const extra = isGroupBoundary(col - 1) ? DIVIDER_GAP : 0;
    colCenters.push(colCenters[col - 1] + SPACING + extra);
  }
  colCenterOffset = colCenters[GRID_COLS - 1] / 2;

  for (let row = 0; row < GRID_ROWS; row++) {
    for (let col = 0; col < GRID_COLS; col++) {
      const i = row * GRID_COLS + col;
      const tile = new THREE.Group();
      const x = colCenters[col] - colCenterOffset;
      const z = (row - (GRID_ROWS - 1) / 2) * SPACING;
      tile.position.set(x, 0, z);

      const meshes = [];
      primGeometries.forEach(p => {
        const seed = seedCounter++;
        const normalMat = makeTileMaterial(baseColors[p.materialIndex], seed);
        const purpleMat = makeTileMaterial(purpleBaseColor, seed + 9973, {
          hueJitter: 0.01, satJitter: 0.05, lightJitter: 0.05,
          envMapIntensity: 0.8, emissive: HIGHLIGHT_COLOR, emissiveIntensity: 0.12,
        });
        const mesh = new THREE.Mesh(p.geo, normalMat);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        mesh.userData.tileIndex = i;
        tile.add(mesh);
        raycastTargets.push(mesh);
        meshes.push({ mesh, normalMat, purpleMat });
      });

      const highlightMat = new THREE.MeshBasicMaterial({
        color: HIGHLIGHT_COLOR,
        transparent: true,
        opacity: 0,
        depthWrite: false,
      });
      const highlightMesh = new THREE.Mesh(highlightGeo, highlightMat);
      tile.add(highlightMesh);

      gridGroup.add(tile);
      cubes.push({ tile, meshes, highlightMat, row, col, index: i, isCurrent: false });
    }
  }

  if (shadowPlane) { scene.remove(shadowPlane); shadowPlane.geometry.dispose(); }
  const shadowPlaneGeo = new THREE.PlaneGeometry(SPACING * (GRID_COLS + 6), SPACING * (GRID_ROWS + 6));
  shadowPlaneGeo.rotateX(-Math.PI / 2);
  shadowPlane = new THREE.Mesh(shadowPlaneGeo, shadowPlaneMat);
  shadowPlane.position.y = 0.001;
  shadowPlane.receiveShadow = true;
  scene.add(shadowPlane);

  for (let c = BAR_SIZE - 1; c < GRID_COLS - 1; c += BAR_SIZE) {
    const boundaryX = (colCenters[c] + colCenters[c + 1]) / 2 - colCenterOffset;
    const bar = new THREE.Mesh(dividerGeo, dividerMat);
    bar.position.set(boundaryX, 0, 0);
    bar.castShadow = true;
    bar.receiveShadow = true;
    scene.add(bar);
    dividerMeshes.push(bar);
  }

  const gridWidth = colCenters[GRID_COLS - 1] + SPACING;
  const gridDepth = GRID_ROWS * SPACING;
  const gridDiag = Math.hypot(gridWidth, gridDepth);
  MIN_RADIUS = SPACING * 3;
  MAX_RADIUS = gridDiag * 1.8;
  spherical.radius = fitCamera ? gridDiag * 0.62 : clamp(spherical.radius, MIN_RADIUS, MAX_RADIUS);
  updateCamera();

  if (typeof updateBarsLabel === 'function') updateBarsLabel();
}

// ---------- resize ----------
function resize() {
  const w = viewport.clientWidth, h = viewport.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h, false);
}
new ResizeObserver(resize).observe(viewport);
resize();


// ---------- pointer interaction: orbit, zoom, hover, single-tile "standing" selection ----------
const pointers = new Map();
let dragging = false;
let lastDragMid = { x: 0, y: 0 };
let lastPinchDist = null;
let moved = false;

const raycaster = new THREE.Raycaster();
const ndc = new THREE.Vector2();
let hoveredIndex = -1;
let currentIndex = -1; // the single tile currently "stood on"

function refreshHighlight(i) {
  if (i < 0 || i >= cubes.length) return;
  const c = cubes[i];
  // the current tile is fully repainted purple (see setCurrentState), so the
  // translucent overlay is reserved for hovering a *different*, non-current tile
  if (i === currentIndex) c.highlightMat.opacity = 0.0;
  else if (i === hoveredIndex) c.highlightMat.opacity = 0.22;
  else c.highlightMat.opacity = 0.0;
}

function setCurrentState(i, isCurrent) {
  if (i < 0 || i >= cubes.length) return;
  const c = cubes[i];
  c.isCurrent = isCurrent;
  c.meshes.forEach(m => { m.mesh.material = isCurrent ? m.purpleMat : m.normalMat; });
}

function moveTo(i) {
  const prev = currentIndex;
  currentIndex = i;
  if (prev >= 0) setCurrentState(prev, false);
  setCurrentState(i, true);
  refreshHighlight(prev);
  refreshHighlight(currentIndex);
  const c = cubes[i];
  counterEl.textContent = 'עומד על טור ' + (c.col + 1) + ' · שורה ' + (c.row + 1);
}

function pickTile(clientX, clientY) {
  const rect = viewport.getBoundingClientRect();
  ndc.x = ((clientX - rect.left) / rect.width) * 2 - 1;
  ndc.y = -((clientY - rect.top) / rect.height) * 2 + 1;
  raycaster.setFromCamera(ndc, camera);
  const hits = raycaster.intersectObjects(raycastTargets, false);
  if (hits.length === 0) return -1;
  return hits[0].object.userData.tileIndex;
}

function onPointerDown(e) {
  if (e.target.closest('.bipjam-transport') || e.target.closest('.bipjam-palette-item') || e.target.closest('#bipjam-view-toggle')) return; // let UI controls handle their own clicks
  viewport.setPointerCapture(e.pointerId);
  pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  moved = false;
  if (pointers.size === 1) {
    dragging = true;
    viewport.classList.add('dragging');
    lastDragMid = { x: e.clientX, y: e.clientY };
  } else if (pointers.size === 2) {
    dragging = false;
    lastPinchDist = getPinchDist();
  }
}
function onPointerMove(e) {
  if (pointers.has(e.pointerId)) pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });

  if (pointers.size === 2) {
    const dist = getPinchDist();
    if (lastPinchDist != null) {
      const delta = dist - lastPinchDist;
      spherical.radius = clamp(spherical.radius - delta * 0.05, MIN_RADIUS, MAX_RADIUS);
      updateCamera();
    }
    lastPinchDist = dist;
    return;
  }

  if (dragging && pointers.size === 1) {
    const dx = e.clientX - lastDragMid.x;
    const dy = e.clientY - lastDragMid.y;
    if (Math.abs(dx) + Math.abs(dy) > 2) moved = true;
    spherical.theta -= dx * 0.006;
    spherical.phi = clamp(spherical.phi - dy * 0.005, MIN_PHI, MAX_PHI);
    lastDragMid = { x: e.clientX, y: e.clientY };
    updateCamera();
    return;
  }

  const idx = pickTile(e.clientX, e.clientY);
  if (idx !== hoveredIndex) {
    const prev = hoveredIndex;
    hoveredIndex = idx;
    refreshHighlight(prev);
    refreshHighlight(hoveredIndex);
  }
}
function onPointerUp(e) {
  pointers.delete(e.pointerId);
  if (pointers.size === 0) {
    dragging = false;
    viewport.classList.remove('dragging');
    lastPinchDist = null;
    if (!moved && !isPlaying) {
      const idx = pickTile(e.clientX, e.clientY);
      if (idx >= 0) {
        if (!removeElementAt(idx) && idx !== currentIndex) moveTo(idx);
      }
    }
  } else if (pointers.size === 1) {
    lastPinchDist = null;
    dragging = true;
    const [remaining] = pointers.values();
    lastDragMid = { x: remaining.x, y: remaining.y };
  }
}
function onPointerLeave() {
  if (hoveredIndex !== -1) {
    const prev = hoveredIndex;
    hoveredIndex = -1;
    refreshHighlight(prev);
  }
}
function onWheel(e) {
  e.preventDefault();
  spherical.radius = clamp(spherical.radius + e.deltaY * 0.03, MIN_RADIUS, MAX_RADIUS);
  updateCamera();
}
function getPinchDist() {
  const pts = [...pointers.values()];
  const dx = pts[0].x - pts[1].x, dy = pts[0].y - pts[1].y;
  return Math.hypot(dx, dy);
}
function clamp(v, lo, hi) { return Math.min(hi, Math.max(lo, v)); }

viewport.addEventListener('pointerdown', onPointerDown);
viewport.addEventListener('pointermove', onPointerMove);
viewport.addEventListener('pointerup', onPointerUp);
viewport.addEventListener('pointercancel', onPointerUp);
viewport.addEventListener('pointerleave', onPointerLeave);
viewport.addEventListener('wheel', onWheel, { passive: false });

// ---------- metronome / timeline playhead ----------
// each column = one quarter-note beat; every BAR_SIZE (4) columns = one bar.
// the 4 beat-dots always show position within the current 16-column block, however many bars exist.
const DOTS_PER_BLOCK = 4;

const playBtn = document.getElementById('bipjam-play-btn');
const playIcon = document.getElementById('bipjam-play-icon');
const pauseIcon = document.getElementById('bipjam-pause-icon');
const bpmLabel = document.getElementById('bipjam-bpm-label');
const bpmMinus = document.getElementById('bipjam-bpm-minus');
const bpmPlus = document.getElementById('bipjam-bpm-plus');
const beatDotsEl = document.getElementById('bipjam-beat-dots');

for (let b = 0; b < DOTS_PER_BLOCK; b++) {
  const dot = document.createElement('div');
  dot.className = 'bipjam-beat-dot';
  beatDotsEl.appendChild(dot);
}
const beatDots = [...beatDotsEl.children];

let bpm = 120;
let isPlaying = false;
let playheadCol = -1;
let lastStepAt = 0;

function stepDurationMs() { return 60000 / bpm; } // each column IS a quarter note

// ---------- audio: metronome click (synthesized) + per-element samples ----------
let audioCtx = null;
const elementAudioBuffers = {};
function ensureAudio() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    Object.entries(ELEMENT_TYPES).forEach(([key, type]) => {
      const bin = atob(type.audio.data_b64);
      const buf = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
      audioCtx.decodeAudioData(buf.buffer, (decoded) => { elementAudioBuffers[key] = decoded; });
    });
  }
  if (audioCtx.state === 'suspended') audioCtx.resume();
}
function playElementSound(typeKey) {
  const buffer = elementAudioBuffers[typeKey];
  if (!audioCtx || !buffer) return;
  const src = audioCtx.createBufferSource();
  src.buffer = buffer;
  const gain = audioCtx.createGain();
  gain.gain.value = 0.85;
  src.connect(gain);
  gain.connect(audioCtx.destination);
  src.start(0, ELEMENT_TYPES[typeKey].audioOffset); // skip the near-silent lead-in baked into the sample
}
function playClick(accent) {
  if (!audioCtx) return;
  const now = audioCtx.currentTime;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'sine';
  osc.frequency.value = accent ? 1300 : 950;
  gain.gain.setValueAtTime(accent ? 0.22 : 0.14, now);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.09);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start(now);
  osc.stop(now + 0.1);
}

function setColumnHighlight(col, on) {
  for (let row = 0; row < GRID_ROWS; row++) setCurrentState(row * GRID_COLS + col, on);
}

function advancePlayhead() {
  if (playheadCol >= 0) setColumnHighlight(playheadCol, false);
  playheadCol = (playheadCol + 1) % GRID_COLS;
  setColumnHighlight(playheadCol, true);
  playClick(playheadCol % BAR_SIZE === 0);
  placedElements.forEach(el => {
    if (el.tileIndex % GRID_COLS === playheadCol) {
      el.hitAt = performance.now();
      playElementSound(el.type);
    }
  });
  beatDots.forEach((d, b) => d.classList.toggle('on', b === Math.floor((playheadCol % 16) / BAR_SIZE)));
  counterEl.textContent = 'טור ' + (playheadCol + 1) + ' מתוך ' + GRID_COLS;
}

function stopPlayback() {
  isPlaying = false;
  playIcon.style.display = '';
  pauseIcon.style.display = 'none';
  if (playheadCol >= 0) setColumnHighlight(playheadCol, false);
  playheadCol = -1;
  beatDots.forEach(d => d.classList.remove('on'));
  if (currentIndex >= 0) {
    const c = cubes[currentIndex];
    counterEl.textContent = 'עומד על טור ' + (c.col + 1) + ' · שורה ' + (c.row + 1);
  } else {
    counterEl.textContent = 'לחץ על קובייה כדי לעמוד עליה';
  }
}

function startPlayback() {
  ensureAudio();
  if (currentIndex >= 0) { setCurrentState(currentIndex, false); refreshHighlight(currentIndex); currentIndex = -1; }
  isPlaying = true;
  playIcon.style.display = 'none';
  pauseIcon.style.display = '';
  lastStepAt = performance.now();
  playheadCol = -1;
  advancePlayhead();
}

playBtn.addEventListener('click', () => { isPlaying ? stopPlayback() : startPlayback(); });
bpmMinus.addEventListener('click', () => { bpm = Math.max(60, bpm - 4); bpmLabel.textContent = bpm + ' BPM'; });
bpmPlus.addEventListener('click', () => { bpm = Math.min(200, bpm + 4); bpmLabel.textContent = bpm + ' BPM'; });

// ---------- bars (loop length): fixed presets - 4 / 8 / 12 bars, each bar = one divider + 4 columns ----------
const barsToggle = document.getElementById('bipjam-bars-toggle');
const barsOpts = [...barsToggle.querySelectorAll('.bipjam-bars-opt')];

function updateBarsLabel() {
  barsOpts.forEach(btn => btn.classList.toggle('active', parseInt(btn.dataset.bars, 10) === numBars));
}
barsOpts.forEach(btn => {
  btn.addEventListener('click', () => {
    const n = parseInt(btn.dataset.bars, 10);
    if (n === numBars) return;
    numBars = n;
    GRID_COLS = numBars * 4;
    rebuildScene(false);
  });
});

// ---------- draggable elements: generic registry, driven by CUBE_DATA ----------
const ELEMENT_TYPES = {
  drum: { emoji: '🥁', label: 'תוף', data: CUBE_DATA.drum, audio: CUBE_DATA.snareAudio, audioOffset: 0.02, scale: 1, rotationY: 0 },
  tree: { emoji: '🌳', label: 'עץ', data: CUBE_DATA.tree, audio: CUBE_DATA.kickAudio, audioOffset: 0.03, scale: 1, rotationY: 0 },
  triangle: { emoji: '🔺', label: 'משולש', data: CUBE_DATA.triangle, audio: CUBE_DATA.triangleAudio, audioOffset: 0, scale: 0.21, rotationY: -Math.PI / 2 },
};

Object.entries(ELEMENT_TYPES).forEach(([key, type]) => {
  type.materials = type.data.materials.map(m => {
    if (m.hasTexture) {
      const img = new Image();
      img.src = 'data:' + type.data.texture_mime + ';base64,' + type.data.texture_b64;
      const tex = new THREE.Texture(img);
      tex.flipY = false; // raw glTF UVs are already top-left origin; GLTFLoader would normally set this for us
      tex.colorSpace = THREE.SRGBColorSpace;
      img.onload = () => { tex.needsUpdate = true; };
      return new THREE.MeshStandardMaterial({ map: tex, roughness: 0.6, metalness: 0.05, envMapIntensity: 0.5 });
    }
    const c = new THREE.Color().setRGB(m.color[0], m.color[1], m.color[2], THREE.LinearSRGBColorSpace);
    return new THREE.MeshStandardMaterial({ color: c, roughness: 0.55, metalness: 0.08, envMapIntensity: 0.5 });
  });

  type.geometries = type.data.primitives.map(prim => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(b64ToFloat32(prim.positions_b64), 3));
    geo.setAttribute('normal', new THREE.BufferAttribute(b64ToFloat32(prim.normals_b64), 3));
    if (prim.uvs_b64) geo.setAttribute('uv', new THREE.BufferAttribute(b64ToFloat32(prim.uvs_b64), 2));
    geo.setIndex(new THREE.BufferAttribute(b64ToUint32(prim.indices_b64), 1));
    geo.computeBoundingBox();
    geo.computeBoundingSphere();
    return { geo, materialIndex: prim.material };
  });
});

function createElementInstance(typeKey) {
  const type = ELEMENT_TYPES[typeKey];
  const group = new THREE.Group();
  type.geometries.forEach(p => {
    const mesh = new THREE.Mesh(p.geo, type.materials[p.materialIndex]);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    group.add(mesh);
  });
  group.scale.setScalar(type.scale || 1);
  group.rotation.y = type.rotationY || 0;
  return group;
}

let placedElements = [];

function placeElement(typeKey, tileIndex) {
  if (tileIndex < 0 || tileIndex >= cubes.length) return;
  if (placedElements.some(el => el.tileIndex === tileIndex)) return;
  const cube = cubes[tileIndex];
  const inst = createElementInstance(typeKey);
  inst.position.set(cube.tile.position.x, tileSize.y, cube.tile.position.z);
  scene.add(inst);
  placedElements.push({ tileIndex, type: typeKey, group: inst, hitAt: -1 });
}

function removeElementAt(tileIndex) {
  const i = placedElements.findIndex(el => el.tileIndex === tileIndex);
  if (i === -1) return false;
  scene.remove(placedElements[i].group);
  placedElements.splice(i, 1);
  return true;
}

// custom drag from a palette chip onto the 3D grid (native HTML5 DnD is unreliable on touch)
let dragPreviewIndex = -1;

function makeDragHandlers(typeKey) {
  function dragPointerMove(e) {
    const rect = viewport.getBoundingClientRect();
    const inside = e.clientX >= rect.left && e.clientX <= rect.right && e.clientY >= rect.top && e.clientY <= rect.bottom;
    const idx = inside ? pickTile(e.clientX, e.clientY) : -1;
    if (idx !== dragPreviewIndex) {
      if (dragPreviewIndex >= 0) refreshHighlight(dragPreviewIndex);
      dragPreviewIndex = idx;
      if (dragPreviewIndex >= 0) cubes[dragPreviewIndex].highlightMat.opacity = 0.3;
    }
  }
  function dragPointerUp() {
    document.removeEventListener('pointermove', dragPointerMove);
    document.removeEventListener('pointerup', dragPointerUp);
    if (dragPreviewIndex >= 0) {
      placeElement(typeKey, dragPreviewIndex);
      refreshHighlight(dragPreviewIndex);
    }
    dragPreviewIndex = -1;
  }
  return (e) => {
    e.preventDefault();
    document.addEventListener('pointermove', dragPointerMove);
    document.addEventListener('pointerup', dragPointerUp);
  };
}

document.querySelectorAll('.bipjam-palette-item').forEach(chip => {
  chip.addEventListener('pointerdown', makeDragHandlers(chip.dataset.elementType));
});

// ---------- camera view presets ----------
const VIEW_PRESETS = {
  iso: { theta: -Math.PI * 0.22, phi: Math.PI * 0.34 },
  top: { theta: 0, phi: 0.06 },
  side: { theta: -Math.PI / 2, phi: Math.PI * 0.4 },
  front: { theta: 0, phi: Math.PI * 0.4 },
};
const viewOpts = [...document.querySelectorAll('#bipjam-view-toggle .bipjam-bars-opt')];
viewOpts.forEach(btn => {
  btn.addEventListener('click', () => {
    const preset = VIEW_PRESETS[btn.dataset.view];
    if (!preset) return;
    spherical.theta = preset.theta;
    spherical.phi = preset.phi;
    updateCamera();
    viewOpts.forEach(b => b.classList.toggle('active', b === btn));
  });
});

// ---------- initial build ----------
rebuildScene(true);

// ---------- render loop ----------
function tick(now) {
  if (isPlaying && now - lastStepAt >= stepDurationMs()) {
    lastStepAt += stepDurationMs();
    advancePlayhead();
  }
  placedElements.forEach(el => {
    if (el.hitAt >= 0) {
      const t = (now - el.hitAt) / 160;
      const s = t < 1 ? 1 + (1 - t) * 0.35 : 1;
      el.group.scale.setScalar(s);
    }
  });
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);

loadingEl.style.opacity = '0';
setTimeout(() => loadingEl.remove(), 400);
</script>
'''

html_out = html_template.replace('__CUBE_DATA_JSON__', cube_data_json)

with open('/mnt/user-data/outputs/bip_jam_studio.html', 'w') as f:
    f.write(html_out)

print('written, size KB:', len(html_out) / 1024)
