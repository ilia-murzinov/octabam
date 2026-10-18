# rms

Ilia's flash remix with **every open fix** + FM SYNTH **LFO 1 / 2 → VOIC / CHRD**.

## In

- CORE (BRAIN, KITS, MUTE_MODES, SCALE QUANTIZER, TUNER, DIRECT_JUMP_KYOTI, …)
- STEM REC — takes under `AUDIO/STEMS/<project>/YYMMDD-HHMM/`
- EUCLID FILL + RND NAME (date on SAVE AS / COPY PROJECT)
- COPY PROJECT + RECBUF PERSIST
- RELOAD_FROM_PROJECT — CUE+TRACK gated (panel PTN)
- SYNTH MACHINE (`fc24064`) — LFO SETUP PMTR offers `VOIC` / `CHRD`
- Tape Echo + sidechain + SHATTER + STUTTR
- USB out TRACKS MAIN CUE (no USB in)
- REMIX SWITCH

## Build

```bash
make image REMIX=rms BUILD=SC
```

- Card flash: `out/OCTATRACK_OCTABAMSC.bin` → OS UPGRADE
- BRAIN switch: `out/RMS SC.RMX` → `/BRAIN/REMIXES/`
