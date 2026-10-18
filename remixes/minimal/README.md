# minimal

Your flash remix: upstream stock + CORE ColdFire set + Dark Rev + Tape Echo
+ SYNTH + sidechain + SHATTER + STUTTR + USB out TRACKS MAIN CUE + STEM REC.
No USB in. PLATE REV is harvested (its words hold the glitch inserts).

## Layout

| piece | where |
|---|---|
| BRAIN | MAIN MENU fifth root category |
| STEM REC | **UP + REC** own window (not under PROJECT) |
| RND NAME | FUNC + CUE on create / rename |
| EUCLID FILL | TRACK + PAGE |

PROJECT / SYSTEM / CONTROL / MIDI stay stock.

## Build

Worktree: `octabam/.claude/worktrees/ilia` (branch `ilia`).

```bash
git fetch origin main && git rebase origin/main
make image REMIX=minimal BUILD=N
```

- Card flash: `out/OCTATRACK_OCTABAMN.bin` → OS UPGRADE
- BRAIN switch: `out/MINIMAL N.RMX` → `/BRAIN/REMIXES/`

## Refresh from upstream

```bash
git fetch origin main && git fetch fork
git rebase origin/main
# optional: pull newer feature tips
#   git merge fork/stems-under-project
#   git merge fork/euclid-fill
#   git cherry-pick <rnd-name tip>   # or merge fork/pnr-chord
```
