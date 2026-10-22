| SYNTH MACHINE -- octabam override of Tim's selection-guard limits.
| Appended after upstream remix.inc so these .set values win.
        .set    ML_FM_MAX, 3             | FM SYNTH tracks in the Part, at most (same as CX OSC)
        .set    ML_SY_MAX, 2             | SY DRUM tracks in the Part, at most
        .set    ML_SY_WITH_FM, 1         | SY DRUM while an FM SYNTH track is in the Part
