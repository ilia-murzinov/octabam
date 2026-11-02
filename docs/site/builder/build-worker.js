// Runs the stock→patch→container chain off the UI thread so the tab stays
// responsive (no "Page Unresponsive" while eft.wasm is in callMain).
import { build } from "./builder.js";
import { makeEft } from "./eft-run.js";

let eft = null;

async function getEft() {
  if (!eft) {
    const { default: createModule } = await import("./eft.mjs");
    eft = makeEft(createModule);
  }
  return eft;
}

function owned(u8) {
  const copy = u8.slice();
  return { bytes: copy.buffer, byteLength: copy.byteLength };
}

self.onmessage = async (ev) => {
  const { id, file, patch, meta } = ev.data;
  try {
    const result = await build({
      file: new Uint8Array(file),
      patch: new Uint8Array(patch),
      meta,
      eft: await getEft(),
      onStep: (step) => self.postMessage({ id, type: "step", step }),
    });
    const bin = owned(result.bin);
    const syx = owned(result.syx);
    const rmx = owned(result.rmx);
    self.postMessage(
      {
        id,
        type: "done",
        names: result.names,
        bin: bin.bytes,
        syx: syx.bytes,
        rmx: rmx.bytes,
      },
      [bin.bytes, syx.bytes, rmx.bytes],
    );
  } catch (err) {
    self.postMessage({
      id,
      type: "error",
      message: String(err && err.message ? err.message : err),
    });
  }
};
