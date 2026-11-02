// The web builder page: give it your own OCTATRACK_OS1.40C zip, download the
// card image of the remix the manifest names. Everything runs in this browser tab;
// the heavy eft.wasm work is in a worker so the tab stays responsive.
const root = document.getElementById("octabam-builder");

// Keep dropdown chrome with this module — mkdocs/CDN has desynced builder.css
// from page.js before and left the control looking like a plain white button.
if (!document.getElementById("ob-builder-ui-css")) {
  const link = document.createElement("link");
  link.id = "ob-builder-ui-css";
  link.rel = "stylesheet";
  link.href = new URL("./builder-ui.css", import.meta.url).href;
  document.head.appendChild(link);
}

const el = (tag, attrs = {}, ...kids) => {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v == null || v === false) continue;
    if (k === "className") n.className = v;
    else if (k === "textContent") n.textContent = v;
    else if (k === "htmlFor") n.htmlFor = v;
    else if (k.startsWith("data-") || k.startsWith("aria-")) n.setAttribute(k, String(v));
    else if (k === "tabIndex") n.tabIndex = v;
    else if (k in n && typeof n[k] !== "function") n[k] = v;
    else n.setAttribute(k, String(v));
  }
  n.append(...kids);
  return n;
};
const here = (p) => new URL(p, import.meta.url);

let buildWorker = null;
let buildSeq = 0;

function getBuildWorker() {
  if (!buildWorker) {
    buildWorker = new Worker(here("build-worker.js"), { type: "module" });
  }
  return buildWorker;
}

function runBuild({ file, patch, meta, onStep }) {
  const worker = getBuildWorker();
  const id = ++buildSeq;
  return new Promise((resolve, reject) => {
    const onMessage = (ev) => {
      if (ev.data.id !== id) return;
      if (ev.data.type === "step") {
        onStep(ev.data.step);
        return;
      }
      worker.removeEventListener("message", onMessage);
      worker.removeEventListener("error", onError);
      if (ev.data.type === "done") {
        resolve({
          bin: new Uint8Array(ev.data.bin),
          syx: new Uint8Array(ev.data.syx),
          rmx: new Uint8Array(ev.data.rmx),
          names: ev.data.names,
        });
      } else {
        reject(new Error(ev.data.message || "build failed"));
      }
    };
    const onError = (err) => {
      worker.removeEventListener("message", onMessage);
      worker.removeEventListener("error", onError);
      reject(err && err.message ? err : new Error(String(err)));
    };
    worker.addEventListener("message", onMessage);
    worker.addEventListener("error", onError);
    const fileBuf = file.slice().buffer;
    const patchBuf = patch.slice().buffer;
    worker.postMessage({ id, file: fileBuf, patch: patchBuf, meta }, [fileBuf, patchBuf]);
  });
}

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
    const tr = el("tr", {
      "data-remix": r.name,
      tabIndex: 0,
      role: "button",
      title: `Select ${r.name}`,
    }, el("th", { scope: "row" }, r.name));
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

/** Custom dropdown — theme nukes native <select> chrome. */
function remixDropdown(rows, onChange) {
  let value = rows[0]?.name || "";
  const labelOf = (name) => {
    const r = rows.find((x) => x.name === name) || rows[0];
    return r ? `${r.name}  ·  ${r.imageName || r.version}` : name;
  };

  const btn = el("button", {
    type: "button",
    className: "ob-dd-btn",
    id: "ob-remix",
    "aria-haspopup": "listbox",
    "aria-expanded": "false",
  });
  const btnText = el("span", { className: "ob-dd-value" }, labelOf(value));
  const btnChev = el("span", { className: "ob-dd-chevron", "aria-hidden": "true" }, "▾");
  btn.append(btnText, btnChev);

  const menu = el("ul", {
    className: "ob-dd-menu",
    role: "listbox",
    hidden: true,
    tabIndex: -1,
  });
  for (const r of rows) {
    const opt = el("li", {
      role: "option",
      "data-value": r.name,
      "aria-selected": r.name === value ? "true" : "false",
      tabIndex: -1,
      textContent: labelOf(r.name),
    });
    menu.append(opt);
  }

  const wrap = el("div", { className: "ob-dd" },
    el("span", { className: "ob-dd-label" }, "Remix"),
    btn, menu);

  const close = () => {
    menu.hidden = true;
    btn.setAttribute("aria-expanded", "false");
    wrap.classList.remove("ob-dd-open");
  };
  const open = () => {
    menu.hidden = false;
    btn.setAttribute("aria-expanded", "true");
    wrap.classList.add("ob-dd-open");
  };
  const setValue = (name, notify = true) => {
    if (!rows.some((r) => r.name === name)) return;
    value = name;
    btnText.textContent = labelOf(name);
    menu.querySelectorAll("[role=option]").forEach((opt) => {
      opt.setAttribute("aria-selected", opt.dataset.value === name ? "true" : "false");
    });
    if (notify) onChange(name);
  };

  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    if (menu.hidden) open();
    else close();
  });
  menu.addEventListener("click", (e) => {
    const opt = e.target.closest("[role=option]");
    if (!opt) return;
    setValue(opt.dataset.value);
    close();
  });
  document.addEventListener("click", (e) => {
    if (!wrap.contains(e.target)) close();
  });
  btn.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      open();
      menu.querySelector('[aria-selected="true"]')?.focus?.();
    }
  });

  return {
    root: wrap,
    get value() { return value; },
    setValue: (name) => setValue(name, true),
    setValueQuiet: (name) => setValue(name, false),
  };
}

async function main() {
  const manifest = await (await fetch(here("manifest.json"))).json();
  const rows = manifest.remixes || [];
  if (!rows.length) throw new Error("manifest has no remixes");

  let selected = rows[0].name;
  const metaOf = () => rows.find((r) => r.name === selected) || rows[0];

  const file = el("input", { type: "file", id: "ob-file", accept: ".zip,.syx", hidden: true });
  const choose = el("button", { type: "button", id: "ob-choose", textContent: "Choose OS file…" });
  const chosen = el("span", { id: "ob-chosen", textContent: "No file chosen" });
  const go = el("button", { id: "ob-go", textContent: "Build", disabled: true });
  const status = el("p", { id: "ob-status", role: "status" });
  const links = el("p", { id: "ob-links" });
  const built = el("p", { className: "ob-meta" },
    `octabam ${manifest.version} · commit ${manifest.commit.slice(0, 8)} · ${manifest.date}` +
    (manifest.dev ? " (dev)" : ""));

  const syncPickHighlight = () => {
    root.querySelectorAll(".ob-features tr[data-remix]").forEach((tr) => {
      tr.classList.toggle("ob-selected", tr.dataset.remix === selected);
    });
  };

  const dropdown = remixDropdown(rows, (name) => {
    selected = name;
    syncPickHighlight();
  });

  const matrix = featureTable(manifest, rows);
  const form = el("div", { className: "ob-form" },
    dropdown.root,
    el("div", { className: "ob-field" },
      el("span", { className: "ob-hint" }, "OS 1.40C (.zip or .syx)"),
      choose, chosen, file),
    go,
    status, links, built);
  const kids = [];
  if (matrix) kids.push(matrix);
  kids.push(form);
  root.replaceChildren(...kids);

  root.querySelectorAll(".ob-features tr[data-remix]").forEach((tr) => {
    const pick = () => {
      selected = tr.dataset.remix;
      dropdown.setValueQuiet(selected);
      syncPickHighlight();
    };
    tr.addEventListener("click", pick);
    tr.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        pick();
      }
    });
  });
  syncPickHighlight();

  choose.addEventListener("click", () => file.click());
  file.addEventListener("change", () => {
    go.disabled = !file.files.length;
    chosen.textContent = file.files.length ? file.files[0].name : "No file chosen";
  });

  go.addEventListener("click", async () => {
    go.disabled = true;
    links.replaceChildren();
    const meta = metaOf();
    try {
      status.textContent = "starting...";
      const bytes = new Uint8Array(await file.files[0].arrayBuffer());
      const patch = new Uint8Array(await (await fetch(here(meta.patch))).arrayBuffer());
      await new Promise((r) => setTimeout(r, 0));
      const r = await runBuild({
        file: bytes,
        patch,
        meta,
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
