document.documentElement.classList.add("has-js");
import type { CityRenderer, MapView } from "./renderer";
const $ = <T extends HTMLElement = HTMLElement>(id: string) =>
  document.getElementById(id) as T;
const shell = $("atlas");
const stage = $("map-stage");
const panel = $("record-panel");
const selects = [
  ...document.querySelectorAll<HTMLButtonElement>(".project-select"),
];
const pins = [...document.querySelectorAll<HTMLButtonElement>(".project-pin")];
const basicPins = pins.filter((pin) => pin.dataset.depth === "basic");
const basicDirectory = [...document.querySelectorAll<HTMLButtonElement>(".basic-directory .project-select")];
const placeFilter = $<HTMLSelectElement>("basic-place-filter");
const placeFilterStatus = $("place-filter-status");
function distanceKm(lon1: number, lat1: number, lon2: number, lat2: number) {
  const radians = Math.PI / 180;
  const dLat = (lat2 - lat1) * radians;
  const dLon = (lon2 - lon1) * radians;
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1 * radians) * Math.cos(lat2 * radians) * Math.sin(dLon / 2) ** 2;
  return 12742 * Math.asin(Math.min(1, Math.sqrt(a)));
}
placeFilter.addEventListener("change", () => {
  const selected = placeFilter.value ? placeFilter.value.split(",").map(Number) : null;
  const visibleIds = new Set<string>();
  for (const pin of basicPins) {
    const nearby = !selected || distanceKm(Number(pin.dataset.lon), Number(pin.dataset.lat), selected[0], selected[1]) <= 3;
    pin.classList.toggle("filtered-out", !nearby);
    if (nearby) visibleIds.add(pin.dataset.project!);
  }
  for (const button of basicDirectory) button.hidden = !visibleIds.has(button.dataset.project!);
  const count = visibleIds.size;
  placeFilterStatus.textContent = selected
    ? `${count} basic listing${count === 1 ? "" : "s"} within 3 km of ${placeFilter.selectedOptions[0].textContent}.`
    : `Showing all ${count} basic listings.`;
  $("selection-status").textContent = placeFilterStatus.textContent;
});
let city: CityRenderer | undefined;
let selection: string | null = null;
const viewHistory: { camera: MapView; label: string; area: string; plan: boolean; project: string | null }[] = [];
function rememberView() {
  if (!city) return;
  viewHistory.push({ camera: city.captureView(), label: $("view-label").textContent ?? "BERLIN",
    area: $("area-name").textContent ?? "Choose an area", plan, project: selection });
  if (viewHistory.length > 20) viewHistory.shift();
}
function previousView() {
  if (shell.classList.contains("record-expanded")) {
    showFullRecord(false);
    return;
  }
  close();
  const previous = viewHistory.pop();
  if (previous) {
    if (previous.project) choose(previous.project, true, false);
    city?.restoreView(previous.camera);
    $("view-label").textContent = previous.label;
    $("area-name").textContent = previous.area;
    plan = previous.plan;
    pressed("plan-view", plan);
  }
  $("back-to-city").hidden = viewHistory.length === 0 && !selection;
}
let returnFocus: HTMLElement | null = null;
let plan = false,
  orbit = false;
const pressed = (id: string, value: boolean) =>
  $(id).setAttribute("aria-pressed", String(value));
function choose(id: string, updateHash = true, remember = true) {
  const button = selects.find((b) => b.dataset.project === id);
  const record = $(`record-${id}`);
  if (!button || !record) return;
  if (basicPins.some((pin) => pin.dataset.project === id && pin.classList.contains("filtered-out"))) {
    placeFilter.value = "";
    placeFilter.dispatchEvent(new Event("change"));
  }
  record.querySelectorAll<HTMLElement>("[data-record-section]").forEach(section => {
    section.hidden = section.dataset.recordSection !== "overview";
  });
  if (remember && selection !== id) rememberView();
  returnFocus = document.activeElement as HTMLElement;
  selection = id;
  $("label-panel").hidden = true;
  $("labels-view").setAttribute("aria-expanded", "false");
  city?.setOrbit(false);
  panel.hidden = false;
  panel.scrollTop = 0;
  shell.classList.remove("record-expanded");
  $<HTMLDetailsElement>("area-picker").open = false;
  $("back-to-city").hidden = false;
  shell.classList.add("has-selection");
  document
    .querySelectorAll<HTMLElement>(".project-record")
    .forEach((r) => (r.hidden = r !== record));
  selects.forEach((b) => b.setAttribute("aria-expanded", String(b === button)));
  pins.forEach((p) => p.classList.toggle("selected", p.dataset.project === id));
  const pin = pins.find((p) => p.dataset.project === id);
  if (pin) {
    plan = false;
    pressed("plan-view", false);
    city?.select(Number(pin.dataset.lon), Number(pin.dataset.lat));
  } else city?.clearSelection();
  $("view-label").textContent = id + " / PROJECT RECORD";
  $("selection-status").textContent =
    `Selected ${button.querySelector("strong")?.textContent}. ${pin ? "" : "Location withheld."}`;
  if (updateHash) history.replaceState(null, "", `#${id}`);
  if (innerWidth <= 700) $<HTMLDetailsElement>("project-picker").open = false;
  panel.focus({ preventScroll: true });
}
function close() {
  panel.hidden = true;
  shell.classList.remove("has-selection", "record-expanded");
  selection = null;
  selects.forEach((b) => b.setAttribute("aria-expanded", "false"));
  pins.forEach((p) => p.classList.remove("selected"));
  city?.clearSelection();
  $("view-label").textContent = "CENTRAL BERLIN";
  history.replaceState(null, "", location.pathname);
  if (returnFocus?.isConnected) {
    const picker = returnFocus.closest("details");
    const target =
      picker && !picker.open ? picker.querySelector("summary") : returnFocus;
    target?.focus({ preventScroll: true });
  }
}
selects
  .concat(pins, [...document.querySelectorAll<HTMLButtonElement>(".legend-project-link")])
  .forEach((b) =>
    b.addEventListener("click", () => choose(b.dataset.project!)),
  );
$("close-record").addEventListener("click", previousView);
$("back-to-city").addEventListener("click", previousView);
document.addEventListener("keydown", (e) => {
  if (
    e.key === "Escape" &&
    !$<HTMLDialogElement>("model-dialog").open &&
    selection &&
    $("label-panel").hidden
  )
    previousView();
});
function showFullRecord(expanded: boolean) {
  if (!selection) return;
  const record = $(`record-${selection}`);
  shell.classList.toggle("record-expanded", expanded);
  record.querySelectorAll<HTMLElement>("[data-record-section]").forEach(section => {
    section.hidden = section.dataset.recordSection !== (expanded ? "history" : "overview");
  });
  panel.scrollTop = 0;
  if (expanded) panel.focus({ preventScroll: true });
  else record.querySelector<HTMLButtonElement>("[data-expand-record]")?.focus({ preventScroll: true });
}
function cityOverview() {
  viewHistory.length = 0;
  close();
  city?.introduce();
  $("view-label").textContent = "BERLIN · CITY OVERVIEW";
  $("area-name").textContent = "City overview";
  $("back-to-city").hidden = true;
  $<HTMLDetailsElement>("area-picker").open = false;
  plan = false;
  pressed("plan-view", false);
}
document.querySelectorAll<HTMLButtonElement>("[data-expand-record]").forEach(button => {
  button.addEventListener("click", () => {
    showFullRecord(true);
  });
});
$("home-view").addEventListener("click", cityOverview);
stage.addEventListener("atlas-detail", (event: Event) => {
  $("detail-status").textContent = (event as CustomEvent<string>).detail;
});
document.querySelectorAll<HTMLButtonElement>("[data-area]").forEach(button => {
  button.addEventListener("click", () => {
    if (button.dataset.area === "overview") { cityOverview(); return; }
    rememberView();
    const [lon, lat] = button.dataset.area!.split(",").map(Number);
    close();
    city?.explore(lon, lat);
    plan = false;
    pressed("plan-view", false);
    $("area-name").textContent = button.textContent;
    $("view-label").textContent = button.textContent;
    $("back-to-city").hidden = false;
    $<HTMLDetailsElement>("area-picker").open = false;
    $("area-picker").querySelector("summary")!.focus();
  });
});
document.addEventListener("click", event => {
  if (!$("area-picker").contains(event.target as Node))
    $<HTMLDetailsElement>("area-picker").open = false;
});
document.addEventListener("keydown", event => {
  if (event.key === "Escape" && $<HTMLDetailsElement>("area-picker").open) {
    $<HTMLDetailsElement>("area-picker").open = false;
    $("area-picker").querySelector("summary")!.focus();
  }
});
$("zoom-in").addEventListener("click", () => city?.zoom(1.5));
$("zoom-out").addEventListener("click", () => city?.zoom(1 / 1.5));
$("north").addEventListener("click", () => {
  plan = false;
  pressed("plan-view", false);
  city?.north();
});
$("plan-view").addEventListener("click", () => {
  plan = !plan;
  pressed("plan-view", plan);
  city?.setPlan(plan);
});
const labelPanel = $("label-panel");
const labelButton = $("labels-view");
function showLabels(open: boolean) {
  labelPanel.hidden = !open;
  labelButton.setAttribute("aria-expanded", String(open));
}
labelButton.addEventListener("click", () =>
  showLabels(Boolean(labelPanel.hidden)),
);
$("close-labels").addEventListener("click", () => {
  showLabels(false);
  labelButton.focus();
});
document
  .querySelectorAll<HTMLInputElement>("[data-label-kind]")
  .forEach((input) =>
    input.addEventListener("change", () =>
      city?.setLabelKind(
        input.dataset.labelKind as "projects" | "basic" | "water" | "parks",
        input.checked,
      ),
    ),
  );
document.addEventListener("click", (event) => {
  const target = event.target as Node;
  if (!labelPanel.contains(target) && !labelButton.contains(target))
    showLabels(false);
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !labelPanel.hidden) {
    showLabels(false);
    labelButton.focus();
  }
});
$("orbit-view").addEventListener("click", () => city?.setOrbit(!orbit));
stage.addEventListener("atlas-orbit", (e: Event) => {
  orbit = (e as CustomEvent<boolean>).detail;
  pressed("orbit-view", orbit);
  $("orbit-view").querySelector("span")!.textContent = orbit
    ? "Pause"
    : "Orbit";
});
if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
  $<HTMLButtonElement>("orbit-view").disabled = true;
  $("orbit-view").title =
    "Automatic motion is disabled by your reduced-motion preference.";
}
$("fullscreen-view").addEventListener("click", async () => {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await shell.requestFullscreen();
  } catch {
    $("selection-status").textContent =
      "Fullscreen is not available in this browser.";
  }
});
document.addEventListener("fullscreenchange", () =>
  $("fullscreen-view").setAttribute(
    "aria-label",
    document.fullscreenElement ? "Exit fullscreen" : "Enter fullscreen",
  ),
);
const dialog = $<HTMLDialogElement>("model-dialog");
$("about-map").addEventListener("click", () => dialog.showModal());
$("close-model").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (e) => {
  if (e.target === dialog) {
    const r = dialog.getBoundingClientRect();
    if (
      e.clientX < r.left ||
      e.clientX > r.right ||
      e.clientY < r.top ||
      e.clientY > r.bottom
    )
      dialog.close();
  }
});
function fail(message: string) {
  if (shell.classList.contains("atlas-failed")) return;
  shell.classList.add("atlas-failed");
  if (dialog.open) dialog.close();
  showLabels(false);
  $("map-loading").hidden = true;
  $("failure-message").textContent = message;
  const failure = $("map-failure");
  failure.hidden = false;
  city?.dispose();
  city = undefined;
  failure.focus({ preventScroll: true });
}
stage.addEventListener("atlas-error", (e: Event) =>
  fail((e as CustomEvent<string>).detail),
);
$("retry-map").addEventListener("click", () => location.reload());
window.addEventListener("hashchange", () => {
  if (location.hash) choose(location.hash.slice(1), false);
  else if (selection) close();
});
async function start() {
  try {
    const { CityRenderer } = await import("./renderer");
    city = new CityRenderer(stage, (zoom, angle) => {
      const width = stage.clientWidth;
      const height = stage.clientHeight;
      const half = width < 700 ? 1350 : 1600;
      const metersPerPixel = (half * 2) / (height * zoom);
      const target = metersPerPixel * 78;
      const unit =
        target >= 5000
          ? 5000
          : target >= 2000
            ? 2000
            : target >= 1000
              ? 1000
              : target >= 500
                ? 500
                : target >= 200
                  ? 200
                  : target >= 100
                    ? 100
                    : 50;
      $("scale-label").textContent =
        unit >= 1000 ? `${unit / 1000} km` : `${unit} m`;
      $("scale-rule").style.width = `${unit / metersPerPixel}px`;
      $("north-arrow").style.transform = `rotate(${-angle}rad)`;
    });
    const manifest = await city.load(
      (message) => ($("loading-message").textContent = message),
    );
    if (shell.classList.contains("atlas-failed")) return;
    $("model-coverage").textContent =
      `${manifest.buildings.toLocaleString("en-GB")} building and building-part shapes across Berlin. Detail loads by area; the overview shows simplified footprints of shapes at least 500 m². Building shapes smaller than 50 m² are omitted; coordinates are rounded to 0.5 m. Source heights are used without vertical exaggeration; unknown heights are omitted. Roofs are simplified. The 2022 geometry is not a current survey.`;
    document
      .querySelectorAll<HTMLInputElement>("[data-label-kind]")
      .forEach((input) =>
        city?.setLabelKind(
          input.dataset.labelKind as "projects" | "basic" | "water" | "parks",
          input.checked,
        ),
      );
    $("map-loading").hidden = true;
    if (location.hash) choose(location.hash.slice(1), false);
    else if (selection) choose(selection, false);
    else city.introduce();
  } catch (error) {
    const message =
      error instanceof Error && /WebGL|graphics context/i.test(error.message)
        ? "Your browser could not start the 3D view. The project records are still available."
        : error instanceof Error
          ? error.message
          : "Unable to load the city model.";
    fail(
      message,
    );
  }
}
void start();
window.addEventListener("pagehide", (event) => {
  if (!event.persisted) city?.dispose();
});
