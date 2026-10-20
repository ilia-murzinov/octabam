# `glitch-quartet` — TAPE + SC + SHATTER + STUTTR

Probe remix for the retracted sequencer-stall claim
(`docs/contributing/FAILURE_MODES.md`). PLATE+SPRING harvested; DARK kept.

```bash
make bus REMIX=glitch-quartet
ot_emu --image out/mainos_bus.bin --card <card.img> \
  --set OCTABAM --project RIG --load-ms 90000 \
  --sequencer --internal-clock --frames 200 --dsp
```

20 Oct 2026 on this tip: `frames run : 200 … run ended REACHED`.
