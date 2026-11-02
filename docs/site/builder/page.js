// The web builder page: give it your own OCTATRACK_OS1.40C zip, download the
// card image of the remix the manifest names. Everything runs in this browser tab.
import { build } from "./builder.js";
import { makeEft } from "./eft-run.js";

const root = document.getElementById("octabam-builder");
const el = (tag, attrs = {}, ...kids) => {
  const n = Object.assign(document.createElement(tag), attrs);
  n.append(...kids);
  return n;
};
const here = (p) => new URL(p, import.meta.url);

/** Short column labels so the matrix fits without overlapping headers. */
const FEAT_SHORT = {
  "SCOPE": "SCOPE",
  "COPY PROJECT": "COPY",
  "DARK REV": "DARK",
  "SYNTH": "SYNTH",
  "CX OSC": "CX",
  "VOID": "VOID",
  "RESONATOR": "RESON",
  "SHATTER": "SHTR",
  "STUTTR": "STUT",
};

function featureTable(manifest, rows) {
  const featureRows = manifest.featureRows || [];
  const byRemix = manifest.features || Object.fromEntries(
    rows.map((r) => [r.name, r.features || []]));
  if (!featureRows.length || !rows.length) return null;

  // Remixes as rows, features as columns — names stay readable.
  const table = el("table", { className: "ob-features" });
  const head = el("tr", {}, el("th", { scope: "col", className: "ob-corner" }, "REMIX"));
  for (const feat of featureRows) {
    head.append(el("th", {
      scope: "col",
      title: feat,
      textContent: FEAT_SHORT[feat] || feat,
    }));
  }
  table.append(el("thead", {}, head));

  const body = el("tbody");
  for (const r of rows) {
    const tr = el("tr", { "data-remix": r.name },
      el("th", { scope: "row", title: r.title || r.name }, r.name));
    const has = new Set(byRemix[r.name] || []);
    for (const feat of featureRows) {
      tr.append(el("td", {}, has.has(feat) ? "●" : ""));
    }
    body.append(tr);
  }
  table.append(body);

  const clearHover = () => {
    table.querySelectorAll(".ob-row-hover").forEach((n) => n.classList.remove("ob-row-hover"));
    table.querySelectorAll(".ob-col-hover").forEach((n) => n.classList.remove("ob-col-hover"));
    table.querySelectorAll(".ob-cell-hover").forEach((n) => n.classList.remove("ob-cell-hover"));
  };
  table.addEventListener("mouseleave", clearHover);
  table.addEventListener("mouseover", (e) => {
    const cell = e.target.closest("td, th");
    if (!cell || !table.contains(cell)) return;
    clearHover();
    const col = cell.cellIndex;
    const row = cell.parentElement;
    row.classList.add("ob-row-hover");
    for (const tr of table.rows) {
      const c = tr.cells[col];
      if (c) c.classList.add("ob-col-hover");
    }
    cell.classList.add("ob-cell-hover");
  });

  return el("div", { className: "ob-features-wrap" }, table);
}

async function main() {
  const manifest = await (await fetch(here("manifest.json"))).json();
  const rows = manifest.remixes || [];
  if (!rows.length) throw new Error("manifest has no remixes");

  const pick = el("select", { id: "ob-remix" });
  for (const r of rows) {
    pick.append(el("option", { value: r.name, textContent: `${r.name} (${r.imageName || r.version})` }));
  }
  const metaOf = () => rows.find((r) => r.name === pick.value) || rows[0];

  const file = el("input", { type: "file", id: "ob-file", accept: ".zip,.syx", hidden: true });
  const choose = el("button", { type: "button", id: "ob-choose", textContent: "Choose OS file" });
  const chosen = el("span", { id: "ob-chosen", textContent: " No file chosen." });
  const go = el("button", { id: "ob-go", textContent: "Build", disabled: true });
  const status = el("p", { id: "ob-status", role: "status" });
  const links = el("p", { id: "ob-links" });
  const built = el("p", { className: "ob-meta" },
    `octabam ${manifest.version} · commit ${manifest.commit.slice(0, 8)} · ${manifest.date}` +
    (manifest.dev ? " (dev)" : ""));

  const matrix = featureTable(manifest, rows);
  const kids = [];
  if (matrix) kids.push(matrix);
  kids.push(
    el("p", { className: "ob-controls" }, el("label", {}, "Remix ", pick)),
    el("p", { className: "ob-controls" },
      el("span", { className: "ob-hint" }, "OCTATRACK_OS1.40C_dist.zip or .syx"),
      el("br"),
      choose, chosen, file),
    el("p", { className: "ob-controls" }, go),
    status, links, built);
  root.replaceChildren(...kids);

  const syncPickHighlight = () => {
    root.querySelectorAll(".ob-features tr[data-remix]").forEach((tr) => {
      tr.classList.toggle("ob-selected", tr.dataset.remix === pick.value);
    });
  };
  pick.addEventListener("change", syncPickHighlight);
  syncPickHighlight();

  choose.addEventListener("click", () => file.click());
  file.addEventListener("change", () => {
    go.disabled = !file.files.length;
    chosen.textContent = ` ${file.files.length ? file.files[0].name : "No file chosen."}`;
  });

  go.addEventListener("click", async () => {
    go.disabled = true;
    links.replaceChildren();
    const meta = metaOf();
    try {
      const bytes = new Uint8Array(await file.files[0].arrayBuffer());
      const patch = new Uint8Array(await (await fetch(here(meta.patch))).arrayBuffer());
      const createModule = (await import("./eft.mjs")).default;
      const r = await build({
        file: bytes, patch, meta, eft: makeEft(createModule),
        onStep: (s) => { status.textContent = s + "..."; },
      });
      status.textContent = "Done. Nothing was uploaded; the files below exist only in this tab.";
      const dl = (data, name, label) => el("a", {
        href: URL.createObjectURL(new Blob([data], { type: "application/octet-stream" })),
        download: name, textContent: label,
      });
      links.append(
        dl(r.bin, r.names.bin, `${r.names.bin} (card)`), " · ",
        dl(r.syx, r.names.syx, `${r.names.syx} (MIDI)`), " · ",
        dl(r.rmx, r.names.rmx, `${r.names.rmx} (REMIX SWITCH)`));
    } catch (err) {
      status.textContent = String(err && err.message ? err.message : err);
    } finally {
      go.disabled = !file.files.length;
    }
  });
}

main().catch((err) => {
  root.textContent = String(err && err.message ? err.message : err);
});
