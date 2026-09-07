document.documentElement.classList.add("has-js");
import type { CityRenderer } from "./renderer";
const $ = <T extends HTMLElement = HTMLElement>(id: string) =>
  document.getElementById(id) as T;
const shell = $("atlas");
const stage = $("map-stage");
const panel = $("record-panel");
const selects = [
  ...document.querySelectorAll<HTMLButtonElement>(".project-select"),
];
const pins = [...document.querySelectorAll<HTMLButtonElement>(".project-pin")];
let city: CityRenderer | undefined;
let selection: string | null = null;
let returnFocus: HTMLElement | null = null;
let plan = false,
  orbit = false;
const pressed = (id: string, value: boolean) =>
  $(id).setAttribute("aria-pressed", String(value));
function choose(id: string, updateHash = true) {
  const button = selects.find((b) => b.dataset.project === id);
  const record = $(`record-${id}`);
  if (!button || !record) return;
  returnFocus = document.activeElement as HTMLElement;
  selection = id;
  panel.hidden = false;
  panel.scrollTop = 0;
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
  shell.classList.remove("has-selection");
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
  .concat(pins)
  .forEach((b) =>
    b.addEventListener("click", () => choose(b.dataset.project!)),
  );
$("close-record").addEventListener("click", close);
document.addEventListener("keydown", (e) => {
  if (
    e.key === "Escape" &&
    !$<HTMLDialogElement>("model-dialog").open &&
    selection &&
    $("label-panel").hidden
  )
    close();
});
document
  .querySelectorAll<HTMLButtonElement>("[data-record-tab]")
  .forEach((button) =>
    button.addEventListener("click", () => {
      const record = button.closest(".project-record")!;
      record
        .querySelectorAll<HTMLButtonElement>("[data-record-tab]")
        .forEach((b) => {
          b.classList.toggle("active", b === button);
          b.setAttribute("aria-pressed", String(b === button));
        });
      record
        .querySelectorAll<HTMLElement>("[data-record-section]")
        .forEach(
          (s) =>
            (s.hidden = s.dataset.recordSection !== button.dataset.recordTab),
        );
      panel.scrollTop = 0;
    }),
  );
function theme(ink: boolean) {
  document.body.dataset.theme = ink ? "ink" : "paper";
  pressed("paper-mode", !ink);
  pressed("night-mode", ink);
  $("paper-mode").classList.toggle("active", !ink);
  $("night-mode").classList.toggle("active", ink);
  city?.theme(ink);
}
$("paper-mode").addEventListener("click", () => theme(false));
$("night-mode").addEventListener("click", () => theme(true));
$("home-view").addEventListener("click", () => {
  close();
  city?.overview();
  $("view-label").textContent = "BERLIN · CITY OVERVIEW";
  ($("explore-area") as HTMLSelectElement).value = "";
  plan = true;
  pressed("plan-view", true);
});
stage.addEventListener("atlas-detail", (event: Event) => {
  $("detail-status").textContent = (event as CustomEvent<string>).detail;
});
$("explore-area").addEventListener("change", (event) => {
  const select = event.target as HTMLSelectElement;
  if (!select.value) return;
  const [lon, lat] = select.value.split(",").map(Number);
  close();
  city?.explore(lon, lat);
  plan = false;
  pressed("plan-view", false);
  $("view-label").textContent = select.selectedOptions[0].textContent;
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
        input.dataset.labelKind as "projects" | "water" | "parks",
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
  $("map-loading").hidden = true;
  $("map-failure").hidden = false;
  $("failure-message").textContent = message;
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
    $("model-coverage").textContent =
      `${manifest.buildings.toLocaleString("en-GB")} building and building-part shapes across Berlin. Detail loads by area; the overview shows simplified footprints of shapes at least 500 m². Building shapes smaller than 50 m² are omitted; coordinates are rounded to 0.5 m. Source heights are used without vertical exaggeration; unknown heights are omitted. Roofs are simplified. The 2022 geometry is not a current survey.`;
    document
      .querySelectorAll<HTMLInputElement>("[data-label-kind]")
      .forEach((input) =>
        city?.setLabelKind(
          input.dataset.labelKind as "projects" | "water" | "parks",
          input.checked,
        ),
      );
    $("map-loading").hidden = true;
    theme(document.body.dataset.theme === "ink");
    if (location.hash) choose(location.hash.slice(1), false);
    else if (selection) choose(selection, false);
  } catch (error) {
    city?.dispose();
    fail(
      error instanceof Error ? error.message : "Unable to load the city model.",
    );
  }
}
void start();
window.addEventListener("pagehide", (event) => {
  if (!event.persisted) city?.dispose();
});
