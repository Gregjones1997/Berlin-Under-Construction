import * as THREE from "three";
import { MapControls } from "three/addons/controls/MapControls.js";
import { cityPoint } from "./geo";

type Segment = { start: number; count: number };
type Payload = {
  geometry: string;
  quantization: number;
  surfaceFloats: number;
  edgeFloats: number;
  offset: number[];
  bytes: number;
};
type Tile = Payload & {
  id: string;
  bounds: number[];
  maxHeight: number;
  buildings: number;
};
type Manifest = Payload & {
  version: number;
  buildings: number;
  tiles: Tile[];
  overview: Segment;
  water: Segment;
  parks: Segment;
  roads: Segment;
  rail: Segment;
  bounds: number[];
};
export type MapView = { target: number[]; offset: number[]; zoom: number };
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
  private orbitAfterArrival = false;
  private raf = 0;
  private running = true;
  private dirty = true;
  private idleFrames = 0;
  private reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  private abort = new AbortController();
  private pins: HTMLButtonElement[];
  private labels = { projects: true, water: false, parks: false };
  private contextLabels: HTMLElement[];
  private activeHalo: THREE.Mesh;
  private tickTime = 0;
  private manifest: Manifest | null = null;
  private loaded = new Map<string, THREE.Group>();
  private fading = new Map<THREE.Group, number>();
  private pending = new Set<string>();
  private failed = new Map<string, number>();
  private wanted: Tile[] = [];
  private tileTimer: ReturnType<typeof setTimeout> | undefined;
  private mapBounds = [-8500, -5000, 9000, 6500];
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
      200000,
    );
    const center = cityPoint(13.38, 52.521);
    this.camera.zoom = 1.35;
    this.camera.position.set(center[0] + 1400, 2000, center[1] + 2800);
    this.controls = new MapControls(this.camera, this.renderer.domElement);
    this.controls.target.set(center[0], 0, center[1]);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.085;
    this.controls.screenSpacePanning = false;
    this.controls.minZoom = 0.045;
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
      this.scheduleTiles();
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
      new THREE.PlaneGeometry(240000, 240000),
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
    this.contextLabels = [
      ...host.querySelectorAll<HTMLElement>(".context-label"),
    ];
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
  private async decode(payload: Payload) {
    if (!/^\/atlas\/berlin-[a-f0-9]{12}\.bin\.gz$/.test(payload.geometry))
      throw new Error("Invalid model asset path");
    const res = await fetch(payload.geometry, { signal: this.abort.signal });
    if (!res.ok || !res.body)
      throw new Error("The city geometry could not be downloaded.");
    const buffer = await new Response(
      res.body.pipeThrough(new DecompressionStream("gzip")),
    ).arrayBuffer();
    if (buffer.byteLength !== (payload.surfaceFloats + payload.edgeFloats) * 2)
      throw new Error("Incomplete model download. Please try again.");
    return Float32Array.from(
      new Int16Array(buffer),
      (v) => v / payload.quantization,
    );
  }
  private geometry(source: Float32Array, segment: Segment) {
    const g = new THREE.BufferGeometry();
    g.setAttribute(
      "position",
      new THREE.BufferAttribute(
        source.subarray(segment.start, segment.start + segment.count),
        3,
      ),
    );
    g.computeBoundingSphere();
    return g;
  }
  private mesh(
    group: THREE.Group,
    source: Float32Array,
    segment: Segment,
    material: THREE.Material,
  ) {
    if (!segment.count) return;
    const geometry = this.geometry(source, segment);
    geometry.computeVertexNormals();
    const mesh = new THREE.Mesh(geometry, material);
    mesh.castShadow = material === this.materials.building;
    group.add(mesh);
  }
  async load(onProgress: (message: string) => void) {
    const response = await fetch("/atlas/model.json", {
      signal: this.abort.signal,
    });
    if (!response.ok) throw new Error("The city model is unavailable.");
    const manifest = (await response.json()) as Manifest;
    if (manifest.version !== 2) throw new Error("Unsupported city model.");
    onProgress("Unfolding the whole city");
    const decoded = await this.decode(manifest);
    if (!this.running) return manifest;
    const surfaces = decoded.subarray(0, manifest.surfaceFloats);
    const edges = decoded.subarray(manifest.surfaceFloats);
    const group = new THREE.Group();
    this.mesh(group, surfaces, manifest.overview, this.materials.building);
    this.mesh(group, surfaces, manifest.water, this.materials.water);
    this.mesh(group, surfaces, manifest.parks, this.materials.park);
    this.mesh(group, surfaces, manifest.roads, this.materials.road);
    if (manifest.rail.count)
      group.add(
        new THREE.LineSegments(
          this.geometry(edges, manifest.rail),
          this.materials.rail,
        ),
      );
    this.scene.add(group);
    this.manifest = manifest;
    this.mapBounds = manifest.bounds;
    this.fitZoomLimit();
    this.pins.forEach((p) => (p.hidden = false));
    this.updateTiles();
    // The overview is immediately usable; detail arrives without blocking navigation.
    this.placePins();
    this.wake();
    return manifest;
  }
  private scheduleTiles() {
    if (!this.manifest) return;
    if (this.tileTimer) return;
    this.tileTimer = setTimeout(() => {
      this.tileTimer = undefined;
      this.updateTiles();
    }, 180);
  }
  private updateTiles() {
    if (!this.manifest || !this.running) return;
    this.camera.updateMatrixWorld();
    const frustum = new THREE.Frustum().setFromProjectionMatrix(
      new THREE.Matrix4().multiplyMatrices(
        this.camera.projectionMatrix,
        this.camera.matrixWorldInverse,
      ),
    );
    const target = this.controls.target;
    this.wanted =
      this.camera.zoom < 0.45
        ? []
        : this.manifest.tiles
            .filter((t) =>
              frustum.intersectsBox(
                new THREE.Box3(
                  new THREE.Vector3(t.bounds[0], 0, t.bounds[1]),
                  new THREE.Vector3(t.bounds[2], t.maxHeight, t.bounds[3]),
                ),
              ),
            )
            .sort((a, b) => {
              const distance = (t: Tile) =>
                Math.hypot(
                  (t.bounds[0] + t.bounds[2]) / 2 - target.x,
                  (t.bounds[1] + t.bounds[3]) / 2 - target.z,
                );
              return distance(a) - distance(b);
            })
            .slice(0, 32);
    const wanted = new Set(this.wanted.map((t) => t.id));
    for (const [id, group] of this.loaded) {
      if (!wanted.has(id) && this.loaded.size > 40) {
        this.scene.remove(group);
        this.fading.delete(group);
        group.traverse((o) => {
          if (o instanceof THREE.Mesh || o instanceof THREE.LineSegments) {
            o.geometry.dispose();
            (o.material as THREE.Material).dispose();
          }
        });
        this.loaded.delete(id);
      }
    }
    // Keep the shadow frustum centred on the area being explored.
    this.sun.position.set(target.x - 4000, 6000, target.z + 2500);
    this.sun.target.position.set(target.x, 0, target.z);
    this.sun.target.updateMatrixWorld();
    this.renderer.shadowMap.enabled = this.camera.zoom >= 0.45;
    this.renderer.shadowMap.needsUpdate = true;
    this.pumpTiles();
    this.wake();
  }
  private pumpTiles() {
    if (!this.running) return;
    for (const tile of this.wanted) {
      if (this.pending.size >= 2) break;
      if (
        this.loaded.has(tile.id) ||
        this.pending.has(tile.id) ||
        (this.failed.get(tile.id) ?? 0) > Date.now()
      )
        continue;
      this.pending.add(tile.id);
      void this.loadTile(tile);
    }
    const missing = this.wanted.filter((t) => !this.loaded.has(t.id));
    const failed = missing.some(
      (t) => (this.failed.get(t.id) ?? 0) > Date.now(),
    );
    this.host.dispatchEvent(
      new CustomEvent("atlas-detail", {
        detail: failed
          ? "Some detail is unavailable · move the map to retry"
          : missing.length
            ? `Adding building detail · ${this.wanted.length - missing.length}/${this.wanted.length}`
            : "",
      }),
    );
  }
  private async loadTile(tile: Tile) {
    try {
      const decoded = await this.decode(tile);
      if (!this.running || !this.wanted.some((t) => t.id === tile.id)) return;
      const group = new THREE.Group();
      group.position.set(tile.offset[0], 0, tile.offset[1]);
      this.mesh(
        group,
        decoded,
        { start: 0, count: tile.surfaceFloats },
        this.materials.building,
      );
      group.add(
        new THREE.LineSegments(
          this.geometry(decoded, {
            start: tile.surfaceFloats,
            count: tile.edgeFloats,
          }),
          this.materials.edge,
        ),
      );
      group.traverse(o => {
        if (o instanceof THREE.Mesh || o instanceof THREE.LineSegments) {
          const material = (o.material as THREE.Material).clone();
          material.userData.targetOpacity = material.opacity;
          material.userData.originalTransparent = material.transparent;
          material.transparent = true;
          material.opacity = this.reduced ? material.userData.targetOpacity : 0;
          o.material = material;
        }
      });
      if (!this.reduced) this.fading.set(group, performance.now());
      this.scene.add(group);
      this.loaded.set(tile.id, group);
      this.renderer.shadowMap.needsUpdate = true;
      this.wake();
    } catch (error) {
      if (this.running) this.failed.set(tile.id, Date.now() + 15000);
    } finally {
      this.pending.delete(tile.id);
      this.pumpTiles();
    }
  }
  private fitZoomLimit() {
    this.controls.minZoom = Math.min(
      0.045,
      ((this.camera.right - this.camera.left) /
        (this.mapBounds[2] - this.mapBounds[0])) *
        0.7,
      ((this.camera.top - this.camera.bottom) /
        (this.mapBounds[3] - this.mapBounds[1])) *
        0.7,
    );
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
    this.fitZoomLimit();
    this.scheduleTiles();
    this.wake();
  }
  private placePins() {
    const r = this.host.getBoundingClientRect();
    const occupied: { x: number; y: number }[] = [];
    for (const p of this.pins) {
      const [x, z] = cityPoint(Number(p.dataset.lon), Number(p.dataset.lat));
      const v = new THREE.Vector3(x, 55, z).project(this.camera);
      const visible =
        this.labels.projects &&
        v.z >= -1 &&
        v.z <= 1 &&
        Math.abs(v.x) < 1.1 &&
        Math.abs(v.y) < 1.1;
      if (visible)
        occupied.push({
          x: (v.x * 0.5 + 0.5) * r.width + (v.x > 0.3 ? -80 : 80),
          y: (-v.y * 0.5 + 0.5) * r.height,
        });
      p.classList.toggle("label-left", v.x > 0.3);
      p.style.visibility = visible ? "visible" : "hidden";
      p.style.transform = `translate(${(v.x * 0.5 + 0.5) * r.width - 14}px,${(-v.y * 0.5 + 0.5) * r.height - 14}px)`;
    }
    for (const label of this.contextLabels) {
      const [x, z] = cityPoint(
        Number(label.dataset.lon),
        Number(label.dataset.lat),
      );
      const v = new THREE.Vector3(x, 8, z).project(this.camera);
      const px = (v.x * 0.5 + 0.5) * r.width,
        py = (-v.y * 0.5 + 0.5) * r.height;
      const kind = label.dataset.kind as "water" | "parks";
      const visible =
        this.labels[kind] &&
        this.camera.zoom >= Number(label.dataset.minZoom ?? 0.55) &&
        v.z >= -1 &&
        v.z <= 1 &&
        px > 85 &&
        px < r.width - 85 &&
        py > 65 &&
        py < r.height - 100 &&
        !occupied.some(
          (p) => Math.abs(p.x - px) < 155 && Math.abs(p.y - py) < 32,
        );
      label.hidden = !visible;
      if (visible) {
        label.style.transform = `translate(${px}px,${py}px) translate(-50%,-50%)`;
        occupied.push({ x: px, y: py });
      }
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
      if (progress === 1) {
        this.fly = null;
        if (this.orbitAfterArrival) this.setOrbit(true);
      }
      this.dirty = true;
    }
    for (const [group, start] of this.fading) {
      const amount = Math.min(1, (now - start) / 650);
      group.traverse(o => {
        if (o instanceof THREE.Mesh || o instanceof THREE.LineSegments) {
          const material = o.material as THREE.Material;
          material.opacity = material.userData.targetOpacity * amount;
          if (amount === 1) {
            material.transparent = material.userData.originalTransparent;
            material.needsUpdate = true;
          }
        }
      });
      if (amount === 1) this.fading.delete(group);
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
    const x = THREE.MathUtils.clamp(t.x, this.mapBounds[0], this.mapBounds[2]),
      z = THREE.MathUtils.clamp(t.z, this.mapBounds[1], this.mapBounds[3]);
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
  introduce() {
    // Frame approved project positions only; withheld sites never supply geometry.
    const points = this.pins.map((pin) => {
      const [x, z] = cityPoint(Number(pin.dataset.lon), Number(pin.dataset.lat));
      return new THREE.Vector3(x, 0, z);
    });
    if (!points.length) return;
    const bounds = new THREE.Box3().setFromPoints(points);
    const center = bounds.getCenter(new THREE.Vector3());
    const radius = Math.max(1200, bounds.getSize(new THREE.Vector3()).length() / 2);
    // Leave room for labels and the project card throughout the gentle orbit.
    const span = Math.min(this.camera.right - this.camera.left,
      this.camera.top - this.camera.bottom);
    const zoom = Math.min(1.15, span / (radius * 2.9));
    this.controls.target.copy(center);
    this.camera.position.copy(center).add(new THREE.Vector3(1800, 4200, 3000));
    this.camera.zoom = zoom * (this.reduced ? 1 : 0.82);
    this.camera.updateProjectionMatrix();
    this.controls.update();
    this.move(center, zoom, new THREE.Vector3(1400, 2600, 2800));
    this.orbitAfterArrival = !this.reduced;
  }
  captureView(): MapView {
    if (this.fly) return { target: this.fly.toTarget.toArray(),
      offset: this.fly.toOffset.toArray(), zoom: this.fly.toZoom };
    return { target: this.controls.target.toArray(),
      offset: this.camera.position.clone().sub(this.controls.target).toArray(),
      zoom: this.camera.zoom };
  }
  restoreView(view: MapView) {
    this.move(new THREE.Vector3().fromArray(view.target), view.zoom,
      new THREE.Vector3().fromArray(view.offset));
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
    const [minX, minZ, maxX, maxZ] = this.mapBounds;
    const width = maxX - minX,
      height = maxZ - minZ;
    const zoom =
      Math.min(
        (this.camera.right - this.camera.left) / width,
        (this.camera.top - this.camera.bottom) / height,
      ) * 0.82;
    this.move(
      new THREE.Vector3((minX + maxX) / 2, 0, (minZ + maxZ) / 2),
      zoom,
      new THREE.Vector3(0, 28000, 0.01),
    );
  }
  explore(lon: number, lat: number) {
    const [x, z] = cityPoint(lon, lat);
    this.move(
      new THREE.Vector3(x, 0, z),
      1.15,
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
    this.orbitAfterArrival = false;
    this.controls.autoRotate = value && !this.reduced;
    this.controls.autoRotateSpeed = 0.38;
    this.host.dispatchEvent(
      new CustomEvent("atlas-orbit", { detail: this.controls.autoRotate }),
    );
    this.wake();
  }
  setLabelKind(kind: "projects" | "water" | "parks", value: boolean) {
    this.labels[kind] = value;
    this.placePins();
    this.wake();
  }
  dispose() {
    this.running = false;
    this.abort.abort();
    clearTimeout(this.tileTimer);
    cancelAnimationFrame(this.raf);
    this.observer.disconnect();
    this.controls.dispose();
    this.scene.traverse((o) => {
      if (o instanceof THREE.Mesh || o instanceof THREE.LineSegments)
        o.geometry.dispose();
    });
    this.loaded.forEach(group => group.traverse(o => {
      if (o instanceof THREE.Mesh || o instanceof THREE.LineSegments)
        (o.material as THREE.Material).dispose();
    }));
    this.fading.clear();
    Object.values(this.materials).forEach((m) => m.dispose());
    (this.ground.material as THREE.Material).dispose();
    (this.activeHalo.material as THREE.Material).dispose();
    this.renderer.dispose();
    this.renderer.domElement.remove();
  }
}
