import * as THREE from "three";
import { MapControls } from "three/addons/controls/MapControls.js";
import { cityPoint } from "./geo";

type Segment = { start: number; count: number };
type Tile = { surface: Segment; edges: Segment };
type Manifest = {
  version: number;
  quantization: number;
  buildings: number;
  tiles: Tile[];
  water: Segment;
  parks: Segment;
  roads: Segment;
  rail: Segment;
  bounds: number[];
  surfaceFloats: number;
  edgeFloats: number;
  geometry: string;
};
type Fly = {
  start: number;
  duration: number;
  fromTarget: THREE.Vector3;
  toTarget: THREE.Vector3;
  fromOffset: THREE.Vector3;
  toOffset: THREE.Vector3;
  fromZoom: number;
  toZoom: number;
};
const PAPER = {
  background: 0xeceee7,
  ground: 0xe9eae1,
  building: 0xfaf9f2,
  edge: 0x505951,
  water: 0xb4c4c2,
  park: 0xd1dbc2,
  road: 0xf7f6ef,
  rail: 0x9fa89e,
  ambient: 0xd4e1e3,
  sun: 0xffffff,
};
const INK = {
  background: 0x1b303b,
  ground: 0x243c46,
  building: 0xe0b191,
  edge: 0x8b7062,
  water: 0x142b38,
  park: 0x314d48,
  road: 0x506269,
  rail: 0x77858a,
  ambient: 0xc0d6ef,
  sun: 0xffddbd,
};
export class CityRenderer {
  private scene = new THREE.Scene();
  private renderer: THREE.WebGLRenderer;
  private camera: THREE.OrthographicCamera;
  private controls: MapControls;
  private observer: ResizeObserver;
  private ground: THREE.Mesh;
  private materials: {
    building: THREE.MeshLambertMaterial;
    edge: THREE.LineBasicMaterial;
    water: THREE.MeshLambertMaterial;
    park: THREE.MeshLambertMaterial;
    road: THREE.MeshBasicMaterial;
    rail: THREE.LineBasicMaterial;
  };
  private sun = new THREE.DirectionalLight(PAPER.sun, 1.55);
  private ambient = new THREE.HemisphereLight(0xffffff, PAPER.ambient, 1.2);
  private fly: Fly | null = null;
  private raf = 0;
  private running = true;
  private dirty = true;
  private idleFrames = 0;
  private reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  private abort = new AbortController();
  private pins: HTMLButtonElement[];
  private labels = true;
  private activeHalo: THREE.Mesh;
  private meshes: THREE.Object3D[] = [];
  private tickTime = 0;
  constructor(
    private host: HTMLElement,
    private onChange: (zoom: number, angle: number) => void,
  ) {
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: false,
      powerPreference: "high-performance",
    });
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, 1.7));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.05;
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFShadowMap;
    this.renderer.shadowMap.autoUpdate = false;
    this.renderer.setClearColor(PAPER.background);
    this.renderer.domElement.setAttribute(
      "aria-label",
      "Berlin 3D map. Drag to pan, right-drag to rotate, scroll to zoom. Use the labelled map controls or project list for keyboard navigation.",
    );
    this.renderer.domElement.tabIndex = 0;
    this.host.prepend(this.renderer.domElement);
    this.camera = new THREE.OrthographicCamera(
      -2400,
      2400,
      1600,
      -1600,
      1,
      70000,
    );
    const center = cityPoint(13.38, 52.521);
    this.camera.zoom = 1.35;
    this.camera.position.set(center[0] + 1400, 2000, center[1] + 2800);
    this.controls = new MapControls(this.camera, this.renderer.domElement);
    this.controls.target.set(center[0], 0, center[1]);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.085;
    this.controls.screenSpacePanning = false;
    this.controls.minZoom = 0.13;
    this.controls.maxZoom = 16;
    this.controls.minPolarAngle = 0.02;
    this.controls.maxPolarAngle = Math.PI * 0.43;
    this.controls.zoomSpeed = 0.8;
    this.controls.rotateSpeed = 0.6;
    this.controls.listenToKeyEvents(this.renderer.domElement);
    this.controls.addEventListener("start", () => {
      this.fly = null;
      this.setOrbit(false);
      this.wake();
    });
    this.controls.addEventListener("change", () => {
      this.dirty = true;
      this.idleFrames = 0;
      this.placePins();
      this.onChange(this.camera.zoom, this.controls.getAzimuthalAngle());
    });
    this.scene.background = new THREE.Color(PAPER.background);
    this.scene.add(this.sun, this.ambient);
    this.sun.position.set(-4000, 6000, 2500);
    this.sun.castShadow = true;
    this.sun.shadow.mapSize.set(4096, 4096);
    Object.assign(this.sun.shadow.camera, {
      left: -8000,
      right: 8000,
      top: 8000,
      bottom: -8000,
      near: 100,
      far: 20000,
    });
    this.sun.shadow.bias = -0.00006;
    this.sun.shadow.normalBias = 0.4;
    this.materials = {
      building: new THREE.MeshLambertMaterial({
        color: PAPER.building,
        side: THREE.DoubleSide,
      }),
      edge: new THREE.LineBasicMaterial({
        color: PAPER.edge,
        transparent: true,
        opacity: 0.48,
      }),
      water: new THREE.MeshLambertMaterial({
        color: PAPER.water,
        side: THREE.DoubleSide,
      }),
      park: new THREE.MeshLambertMaterial({
        color: PAPER.park,
        side: THREE.DoubleSide,
      }),
      road: new THREE.MeshBasicMaterial({
        color: PAPER.road,
        side: THREE.DoubleSide,
      }),
      rail: new THREE.LineBasicMaterial({
        color: PAPER.rail,
        transparent: true,
        opacity: 0.55,
      }),
    };
    this.ground = new THREE.Mesh(
      new THREE.PlaneGeometry(80000, 80000),
      new THREE.MeshLambertMaterial({ color: PAPER.ground }),
    );
    this.ground.rotation.x = -Math.PI / 2;
    this.ground.position.y = -1;
    this.ground.receiveShadow = true;
    this.scene.add(this.ground);
    this.activeHalo = new THREE.Mesh(
      new THREE.RingGeometry(32, 38, 64),
      new THREE.MeshBasicMaterial({
        color: 0xdf662f,
        transparent: true,
        opacity: 0.9,
        side: THREE.DoubleSide,
        depthTest: false,
      }),
    );
    this.activeHalo.rotation.x = -Math.PI / 2;
    this.activeHalo.position.y = 3;
    this.activeHalo.visible = false;
    this.activeHalo.renderOrder = 5;
    this.scene.add(this.activeHalo);
    this.pins = [...host.querySelectorAll<HTMLButtonElement>(".project-pin")];
    this.observer = new ResizeObserver(() => this.resize());
    this.observer.observe(host);
    document.addEventListener(
      "visibilitychange",
      () => {
        if (!document.hidden) this.wake();
      },
      { signal: this.abort.signal },
    );
    this.renderer.domElement.addEventListener(
      "webglcontextlost",
      (e) => {
        e.preventDefault();
        this.running = false;
        cancelAnimationFrame(this.raf);
        this.host.dispatchEvent(
          new CustomEvent("atlas-error", {
            detail:
              "The graphics context was interrupted. Reload the atlas or use the project index.",
          }),
        );
      },
      { signal: this.abort.signal },
    );
    this.controls.update();
    this.resize();
    this.wake();
  }
  async load(onProgress: (message: string) => void) {
    const response = await fetch("/atlas/model.json", {
      signal: this.abort.signal,
    });
    if (!response.ok) throw new Error("The city model is unavailable.");
    const manifest = (await response.json()) as Manifest;
    if (manifest.version !== 1 || !manifest.geometry.startsWith("/atlas/"))
      throw new Error("Unsupported city model.");
    onProgress("Loading the architectural model");
    const res = await fetch(manifest.geometry, { signal: this.abort.signal });
    if (!res.ok || !res.body)
      throw new Error("The city geometry could not be downloaded.");
    const buffer = await new Response(
      res.body.pipeThrough(new DecompressionStream("gzip")),
    ).arrayBuffer();
    if (
      buffer.byteLength !==
      (manifest.surfaceFloats + manifest.edgeFloats) * 2
    )
      throw new Error("Incomplete model download. Please try again.");
    const decoded = Float32Array.from(
      new Int16Array(buffer),
      (v) => v / manifest.quantization,
    );
    const surfaces = decoded.subarray(0, manifest.surfaceFloats);
    const edges = decoded.subarray(manifest.surfaceFloats);
    const geometry = (source: Float32Array, s: Segment) => {
      const g = new THREE.BufferGeometry();
      g.setAttribute(
        "position",
        new THREE.BufferAttribute(
          source.subarray(s.start, s.start + s.count),
          3,
        ),
      );
      g.computeBoundingSphere();
      return g;
    };
    onProgress("Tracing the city’s outlines");
    const addMesh = (segment: Segment, mat: THREE.Material) => {
      if (!segment.count) return;
      const g = geometry(surfaces, segment);
      g.computeVertexNormals();
      const m = new THREE.Mesh(g, mat);
      m.castShadow = mat === this.materials.building;
      this.scene.add(m);
      this.meshes.push(m);
    };
    for (let i = 0; i < manifest.tiles.length; i++) {
      const t = manifest.tiles[i];
      addMesh(t.surface, this.materials.building);
      if (t.edges.count) {
        const lines = new THREE.LineSegments(
          geometry(edges, t.edges),
          this.materials.edge,
        );
        this.scene.add(lines);
        this.meshes.push(lines);
      }
      if (i % 15 === 0) {
        await new Promise<void>((r) => requestAnimationFrame(() => r()));
      }
    }
    addMesh(manifest.water, this.materials.water);
    addMesh(manifest.parks, this.materials.park);
    addMesh(manifest.roads, this.materials.road);
    if (manifest.rail.count) {
      const rail = new THREE.LineSegments(
        geometry(edges, manifest.rail),
        this.materials.rail,
      );
      this.scene.add(rail);
      this.meshes.push(rail);
    }
    this.renderer.shadowMap.needsUpdate = true;
    this.pins.forEach((p) => (p.hidden = false));
    this.placePins();
    this.wake();
    return manifest;
  }
  private resize() {
    const { width, height } = this.host.getBoundingClientRect();
    if (!width || !height) return;
    const aspect = width / height;
    const half = width < 700 ? 1350 : 1600;
    this.camera.left = -half * aspect;
    this.camera.right = half * aspect;
    this.camera.top = half;
    this.camera.bottom = -half;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
    this.wake();
  }
  private placePins() {
    const r = this.host.getBoundingClientRect();
    for (const p of this.pins) {
      const [x, z] = cityPoint(Number(p.dataset.lon), Number(p.dataset.lat));
      const v = new THREE.Vector3(x, 55, z).project(this.camera);
      const visible =
        this.labels &&
        v.z >= -1 &&
        v.z <= 1 &&
        Math.abs(v.x) < 1.1 &&
        Math.abs(v.y) < 1.1;
      p.classList.toggle("label-left", v.x > 0.3);
      p.style.visibility = visible ? "visible" : "hidden";
      p.style.transform = `translate(${(v.x * 0.5 + 0.5) * r.width - 14}px,${(-v.y * 0.5 + 0.5) * r.height - 14}px)`;
    }
  }
  private wake() {
    if (!this.running) return;
    this.dirty = true;
    this.idleFrames = 0;
    if (!this.raf) this.raf = requestAnimationFrame((t) => this.frame(t));
  }
  private frame(now: number) {
    this.raf = 0;
    if (!this.running || document.hidden) return;
    const delta = Math.min((now - this.tickTime) / 1000, 0.05);
    this.tickTime = now;
    if (this.fly) {
      const f = this.fly;
      const progress = Math.min(1, (now - f.start) / f.duration);
      const t =
        progress < 0.5 ? 4 * progress ** 3 : 1 - (-2 * progress + 2) ** 3 / 2;
      this.controls.target.lerpVectors(f.fromTarget, f.toTarget, t);
      const offset = f.fromOffset.clone().lerp(f.toOffset, t);
      this.camera.position.copy(this.controls.target).add(offset);
      this.camera.zoom = THREE.MathUtils.lerp(f.fromZoom, f.toZoom, t);
      this.camera.updateProjectionMatrix();
      if (progress === 1) this.fly = null;
      this.dirty = true;
    }
    this.controls.update(delta);
    this.clampTarget();
    if (this.dirty || this.controls.autoRotate || this.fly) {
      this.renderer.render(this.scene, this.camera);
      this.placePins();
      this.dirty = false;
      this.idleFrames = 0;
    } else this.idleFrames++;
    if (this.idleFrames < 90 || this.controls.autoRotate || this.fly)
      this.raf = requestAnimationFrame((t) => this.frame(t));
  }
  private clampTarget() {
    const t = this.controls.target;
    const x = THREE.MathUtils.clamp(t.x, -8500, 9000),
      z = THREE.MathUtils.clamp(t.z, -5000, 6500);
    if (x !== t.x || z !== t.z) {
      this.camera.position.x += x - t.x;
      this.camera.position.z += z - t.z;
      t.x = x;
      t.z = z;
    }
  }
  private move(target: THREE.Vector3, zoom: number, offset?: THREE.Vector3) {
    this.setOrbit(false);
    this.fly = {
      start: performance.now(),
      duration: this.reduced ? 1 : 1350,
      fromTarget: this.controls.target.clone(),
      toTarget: target,
      fromOffset: this.camera.position.clone().sub(this.controls.target),
      toOffset:
        offset ?? this.camera.position.clone().sub(this.controls.target),
      fromZoom: this.camera.zoom,
      toZoom: zoom,
    };
    this.wake();
  }
  select(lon: number, lat: number) {
    const [x, z] = cityPoint(lon, lat);
    this.activeHalo.position.set(x, 3, z);
    this.activeHalo.visible = true;
    const shift = innerWidth <= 700 ? 180 : innerWidth > 1000 ? 240 : 0;
    this.move(
      new THREE.Vector3(x + shift, 0, z + (innerWidth <= 700 ? 400 : 0)),
      2.2,
      new THREE.Vector3(1000, 2200, 2200),
    );
  }
  clearSelection() {
    this.activeHalo.visible = false;
    this.wake();
  }
  overview() {
    const [x, z] = cityPoint(13.385, 52.5175);
    this.move(
      new THREE.Vector3(x, 0, z),
      0.7,
      new THREE.Vector3(1400, 2400, 2200),
    );
  }
  zoom(factor: number) {
    this.move(
      this.controls.target.clone(),
      THREE.MathUtils.clamp(
        this.camera.zoom * factor,
        this.controls.minZoom,
        this.controls.maxZoom,
      ),
    );
  }
  north() {
    const offset = this.camera.position.clone().sub(this.controls.target);
    const d = offset.length();
    this.move(
      this.controls.target.clone(),
      this.camera.zoom,
      new THREE.Vector3(0, d * 0.72, d * 0.694),
    );
  }
  setPlan(value: boolean) {
    const d = this.camera.position.distanceTo(this.controls.target);
    this.move(
      this.controls.target.clone(),
      this.camera.zoom,
      value
        ? new THREE.Vector3(0, d, 0.01)
        : new THREE.Vector3(d * 0.35, d * 0.7, d * 0.62),
    );
  }
  setOrbit(value: boolean) {
    this.controls.autoRotate = value && !this.reduced;
    this.controls.autoRotateSpeed = 0.38;
    this.host.dispatchEvent(
      new CustomEvent("atlas-orbit", { detail: this.controls.autoRotate }),
    );
    this.wake();
  }
  setLabels(value: boolean) {
    this.labels = value;
    this.placePins();
    this.wake();
  }
  theme(ink: boolean) {
    const p = ink ? INK : PAPER;
    this.scene.background = new THREE.Color(p.background);
    (this.ground.material as THREE.MeshLambertMaterial).color.set(p.ground);
    this.materials.building.color.set(p.building);
    this.materials.edge.color.set(p.edge);
    this.materials.edge.opacity = ink ? 0.42 : 0.48;
    this.materials.water.color.set(p.water);
    this.materials.park.color.set(p.park);
    this.materials.road.color.set(p.road);
    this.materials.rail.color.set(p.rail);
    this.renderer.shadowMap.needsUpdate = true;
    this.sun.color.set(p.sun);
    this.ambient.groundColor.set(p.ambient);
    this.wake();
  }
  dispose() {
    this.running = false;
    this.abort.abort();
    cancelAnimationFrame(this.raf);
    this.observer.disconnect();
    this.controls.dispose();
    this.scene.traverse((o) => {
      if (o instanceof THREE.Mesh || o instanceof THREE.LineSegments)
        o.geometry.dispose();
    });
    Object.values(this.materials).forEach((m) => m.dispose());
    (this.ground.material as THREE.Material).dispose();
    (this.activeHalo.material as THREE.Material).dispose();
    this.renderer.dispose();
    this.renderer.domElement.remove();
  }
}
