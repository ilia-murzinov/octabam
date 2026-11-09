# hooks-machines-cx (test remix)

ANALOG BD and CX OSC in one image: HOOKS gives the track's machine list seven rows, ANALOG BD on row 5 and CX OSC on row 6, and the list scrolls. See [HOOKS](../../../modules/hooks/README.md) (`machine_rows`).

OCTA303 conflicts with CX OSC (shared LFO SETUP PMTR name site) — that pair is refused.

`tools/verify/verify_hooks.py hooks-machines-cx` checks the bridged sites in this image after
`make bus REMIX=hooks-machines-cx`.
