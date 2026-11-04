; Megabyte owns no DSP audio memory. Preserve the stock FX2 signal for
; the post-FX2 ColdFire delay stage; preserve r1 during init.
init:
        rts
proc:
        do n7,>mb_cpu_end
        nop
mb_cpu_end:
        rts
