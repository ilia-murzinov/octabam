| SHATTER -- live param icons (DRAM Linked). GNU as, -mcpu=5475.
| Same widget ABI as CX OSC / VOID ui.s: stock value-only, then 17x13 blit.
| Compact (flags bit 1) = stock only. trap-icon-bit31: bit 31 = bottom.
|
| Locked set: FOLD=CX, CLIP=H squareize, CRSH=v4 plateaus (8→2),
| FDBK=CX box+loop, MODE=A brick/blob/shards, TONE=B shelf, RATE=A ticks.
| DRV / MIX / LIM stay stock dials (no widgets here).

        .text
        .global wid_fold, wid_clip, wid_crsh, wid_fdbk
        .global wid_mode, wid_tone, wid_rate
        .global fmt_mode

        .set    STOCK_WIDGET, 0x400479b4
        .set    BLIT, 0x400128a8
        .set    SPRINTF, 0x40013a08

| MODE label formatter: void fmt(char *buf, int value) — same cave shape as
| tools/build/label_fmt.py. HARD / SOFT / CHAOS.
fmt_mode:
        movel   %sp@(8),%d0
        cmpil   #3,%d0
        blo     fmt_mode_ok
        moveq   #0,%d0
fmt_mode_ok:
        lea     fmt_mode_tab(%pc),%a0
        movew   %a0@(0,%d0:l:2),%d1
        andil   #0xffff,%d1
        addal   %d1,%a0
        movel   %a0,%sp@(8)
        jmp     SPRINTF

wid_fold:
        moveq   #0,%d0
        bra     wid
wid_clip:
        moveq   #1,%d0
        bra     wid
wid_crsh:
        moveq   #2,%d0
        bra     wid
wid_fdbk:
        moveq   #3,%d0
        bra     wid
wid_mode:
        moveq   #4,%d0
        bra     wid
wid_tone:
        moveq   #5,%d0
        bra     wid
wid_rate:
        moveq   #6,%d0
        bra     wid

| widget(x, y, slot, value, flags, fmt, window)
wid:
        lea     %sp@(-44),%sp
        moveml  %d2-%d7/%a2-%a6,%sp@
        movel   %d0,%d7
        movel   %sp@(64),%d5
        movel   %d5,%d0
        btst    #1,%d5
        bne     wid_stock
        bset    #1,%d0
        movel   %d0,%sp@(64)
wid_stock:
        movel   %sp@(72),%sp@-
        movel   %sp@(72),%sp@-
        movel   %sp@(72),%sp@-
        movel   %sp@(72),%sp@-
        movel   %sp@(72),%sp@-
        movel   %sp@(72),%sp@-
        movel   %sp@(72),%sp@-
        jsr     STOCK_WIDGET
        lea     %sp@(28),%sp
        movel   %d5,%sp@(64)
        btst    #1,%d5
        bne     wid_out
        movel   %sp@(60),%d6
        tstl    %d7
        beq     ic_fold
        subql   #1,%d7
        beq     ic_clip
        subql   #1,%d7
        beq     ic_crsh
        subql   #1,%d7
        beq     ic_fdbk
        subql   #1,%d7
        beq     ic_mode
        subql   #1,%d7
        beq     ic_tone
        bra     ic_rate


| FOLD: CX wavefolder (Buchla cartoon). drive Q6 = 64 + value*192/127.
ic_fold:
        bsr     ic_clr
        movel   %d6,%d5
        movel   #192,%d0
        mulul   %d0,%d5
        moveq   #127,%d0
        divul   %d0,%d5
        addil   #64,%d5
        moveq   #1,%d7
ic_fold_col:
        lea     fold_sin(%pc),%a0
        mvsb    %a0@(0,%d7:l),%d3
        mulsl   %d5,%d3
        asrl    #6,%d3
ic_fold_f:
        cmpil   #5,%d3
        bgt     ic_fold_hi
        cmpil   #-5,%d3
        blt     ic_fold_lo
        bra     ic_fold_ok
ic_fold_hi:
        moveq   #10,%d0
        subl    %d3,%d0
        movel   %d0,%d3
        bra     ic_fold_f
ic_fold_lo:
        moveq   #-10,%d0
        subl    %d3,%d0
        movel   %d0,%d3
        bra     ic_fold_f
ic_fold_ok:
        moveq   #6,%d1
        subl    %d3,%d1
        bpl     ic_fold_r0
        moveq   #0,%d1
ic_fold_r0:
        cmpil   #12,%d1
        ble     ic_fold_r1
        moveq   #12,%d1
ic_fold_r1:
        moveq   #6,%d2
        cmpl    %d1,%d2
        bge     ic_fold_ord
        movel   %d1,%d0
        movel   %d2,%d1
        movel   %d0,%d2
ic_fold_ord:
        movel   %d7,%d0
        bsr     vline
        addql   #1,%d7
        cmpil   #15,%d7
        ble     ic_fold_col
        bra     blit


| CLIP H: sine → square (flat duty grows with the knob).
| Same lobe convention as FOLD (d1 = 6 − s, fill to midline).
ic_clip:
        bsr     ic_clr
        movel   %d6,%d5
        moveq   #5,%d0
        mulul   %d0,%d5
        moveq   #127,%d0
        divul   %d0,%d5                  | flat 0..5
        moveq   #1,%d7
ic_clip_lp:
        lea     fold_sin(%pc),%a0
        mvsb    %a0@(0,%d7:l),%d3
        cmpil   #3,%d5
        bge     ic_clip_sq
        cmpil   #1,%d5
        blt     ic_clip_sin
        movel   %d3,%d0
        tstl    %d0
        bpl     ic_clip_ab
        negl    %d0
ic_clip_ab:
        cmpil   #4,%d0                   | |s| > ~0.7 of peak
        ble     ic_clip_sin
ic_clip_sq:
        tstl    %d3
        bmi     ic_clip_bot
        moveq   #1,%d1
        moveq   #6,%d2
        bra     ic_clip_draw
ic_clip_bot:
        moveq   #6,%d1
        moveq   #11,%d2
        bra     ic_clip_draw
ic_clip_sin:
        moveq   #6,%d1
        subl    %d3,%d1
        bpl     ic_clip_r0
        moveq   #0,%d1
ic_clip_r0:
        cmpil   #12,%d1
        ble     ic_clip_r1
        moveq   #12,%d1
ic_clip_r1:
        moveq   #6,%d2
        cmpl    %d1,%d2
        bge     ic_clip_draw
        movel   %d1,%d0
        movel   %d2,%d1
        movel   %d0,%d2
ic_clip_draw:
        movel   %d7,%d0
        bsr     vline
        addql   #1,%d7
        cmpil   #15,%d7
        ble     ic_clip_lp
        bra     blit


| CRSH v4: plateau count 8→2; fat 2-px bars + walls.
| Heights stored as Python-y (0=top); drawn as asm row = 12 − y.
ic_crsh:
        bsr     ic_clr
        movel   %d6,%d5
        moveq   #6,%d0
        mulul   %d0,%d5
        moveq   #127,%d0
        divul   %d0,%d5
        moveq   #8,%d4
        subl    %d5,%d4                  | n = 8 − 6v/127
        cmpil   #2,%d4
        bge     ic_crsh_n
        moveq   #2,%d4
ic_crsh_n:
        lea     heights(%pc),%a2
        moveq   #0,%d7                   | i
ic_crsh_hloop:
        cmpil   #3,%d4
        ble     ic_crsh_alt
        cmpil   #5,%d4
        ble     ic_crsh_tab
        | n >= 6: sample sin at plateau center, bucket-quantize
        movel   %d7,%d0
        lsll    #1,%d0
        addql   #1,%d0                   | 2i+1
        moveq   #14,%d1
        mulul   %d1,%d0
        movel   %d4,%d1
        lsll    #1,%d1                   | 2n
        divul   %d1,%d0
        addql   #1,%d0                   | cx
        cmpil   #1,%d0
        bge     ic_crsh_cxlo
        moveq   #1,%d0
ic_crsh_cxlo:
        cmpil   #15,%d0
        ble     ic_crsh_cx
        moveq   #15,%d0
ic_crsh_cx:
        lea     fold_sin(%pc),%a0
        mvsb    %a0@(0,%d0:l),%d3
        addql   #6,%d3                   | t = s+6 → 0..12
        moveq   #4,%d0
        cmpil   #7,%d4
        bge     ic_crsh_bk
        moveq   #3,%d0                   | buckets
ic_crsh_bk:
        movel   %d0,%d1
        subql   #1,%d1                   | buckets-1
        mulul   %d1,%d3
        addql   #6,%d3
        moveq   #12,%d0
        divul   %d0,%d3                  | b = round-ish
        moveq   #8,%d0
        mulul   %d0,%d3
        divul   %d1,%d3                  | b*8/(buckets-1)
        moveq   #10,%d0
        subl    %d3,%d0                  | y
        cmpil   #1,%d0
        bge     ic_crsh_y0
        moveq   #1,%d0
ic_crsh_y0:
        cmpil   #10,%d0
        ble     ic_crsh_yst
        moveq   #10,%d0
        bra     ic_crsh_yst
ic_crsh_alt:
        movel   %d7,%d0
        andil   #1,%d0
        beq     ic_crsh_a2
        moveq   #9,%d0
        bra     ic_crsh_yst
ic_crsh_a2:
        moveq   #2,%d0
        bra     ic_crsh_yst
ic_crsh_tab:
        lea     crsh_tab5(%pc),%a0
        mvzb    %a0@(0,%d7:l),%d0
ic_crsh_yst:
        moveb   %d0,%a2@(0,%d7:l)
        addql   #1,%d7
        cmpl    %d4,%d7
        blt     ic_crsh_hloop

        moveq   #0,%d7
        moveq   #-1,%d5                  | prev y
ic_crsh_draw:
        mvzb    %a2@(0,%d7:l),%d3        | y
        | x0 = 1 + i*14/n
        movel   %d7,%d0
        moveq   #14,%d1
        mulul   %d1,%d0
        divul   %d4,%d0
        addql   #1,%d0
        | x1 = 1 + (i+1)*14/n - 1
        movel   %d7,%d1
        addql   #1,%d1
        moveq   #14,%d2
        mulul   %d2,%d1
        divul   %d4,%d1                  | (i+1)*14/n
        cmpl    %d0,%d1
        bge     ic_crsh_xok
        movel   %d0,%d1
ic_crsh_xok:
        movel   %d0,%a3                  | x0
        movel   %d1,%a4                  | x1
        | hline at y and y+1 → asm rows 12-y and 11-y
        movel   %a3,%d0
        moveq   #12,%d1
        subl    %d3,%d1
        movel   %a4,%d2
        bsr     hline
        movel   %a3,%d0
        moveq   #11,%d1
        subl    %d3,%d1
        movel   %a4,%d2
        bsr     hline
        cmpil   #-1,%d5
        beq     ic_crsh_next
        cmpl    %d5,%d3
        beq     ic_crsh_next
        movel   %a3,%d0
        moveq   #12,%d1
        subl    %d5,%d1
        moveq   #12,%d2
        subl    %d3,%d2
        cmpl    %d1,%d2
        bge     ic_crsh_w0
        movel   %d1,%a5
        movel   %d2,%d1
        movel   %a5,%d2
ic_crsh_w0:
        bsr     vline
        movel   %a3,%d0
        moveq   #11,%d1
        subl    %d5,%d1
        moveq   #11,%d2
        subl    %d3,%d2
        cmpl    %d1,%d2
        bge     ic_crsh_w1
        movel   %d1,%a5
        movel   %d2,%d1
        movel   %a5,%d2
ic_crsh_w1:
        bsr     vline
ic_crsh_next:
        movel   %d3,%d5
        addql   #1,%d7
        cmpl    %d4,%d7
        blt     ic_crsh_draw
        bra     blit


| FDBK: CX modulator box; loop OR'd when value > 0; lsll #1 nudge down.
ic_fdbk:
        lea     img_fdbk(%pc),%a0
        bsr     copy
        tstl    %d6
        beq     ic_fdbk_n
        lea     img_loop(%pc),%a0
        bsr     orimg
ic_fdbk_n:
        lea     data(%pc),%a0
        moveq   #16,%d0
ic_fdbk_lsl:
        movel   %a0@,%d1
        lsll    #1,%d1
        andil   #0xfff80000,%d1
        movel   %d1,%a0@+
        subql   #1,%d0
        bge     ic_fdbk_lsl
        bra     blit


| MODE A: HARD brick / SOFT blob / CHAOS shards (static glyphs).
ic_mode:
        lea     img_mode_hard(%pc),%a0
        tstl    %d6
        beq     ic_mode_go
        lea     img_mode_soft(%pc),%a0
        cmpil   #1,%d6
        beq     ic_mode_go
        lea     img_mode_chaos(%pc),%a0
ic_mode_go:
        bsr     copy
        bra     blit


| TONE B: shelf wedge, low-left ↔ high-right; double-column thick.
| Bars grow from the bottom (asm row 0).
ic_tone:
        bsr     ic_clr
        moveq   #1,%d7
ic_tone_lp:
        | lo_h = 10*(15-x)/14 ; hi_h = 10*(x-1)/14
        moveq   #15,%d0
        subl    %d7,%d0
        moveq   #10,%d1
        mulul   %d1,%d0
        moveq   #14,%d1
        divul   %d1,%d0                  | lo_h
        movel   %d7,%d1
        subql   #1,%d1
        moveq   #10,%d2
        mulul   %d2,%d1
        moveq   #14,%d2
        divul   %d2,%d1                  | hi_h
        movel   %d1,%d2
        subl    %d0,%d2                  | hi-lo
        mulsl   %d6,%d2
        moveq   #127,%d1
        divsl   %d1,%d2
        addl    %d2,%d0                  | h
        tstl    %d0
        bgt     ic_tone_h0
        bra     ic_tone_next
ic_tone_h0:
        cmpil   #12,%d0
        ble     ic_tone_h1
        moveq   #12,%d0
ic_tone_h1:
        movel   %d0,%d5                  | h
        moveq   #0,%d1
        movel   %d5,%d2
        subql   #1,%d2
        movel   %d7,%d0
        bsr     vline
        movel   %d7,%d0
        addql   #1,%d0
        cmpil   #16,%d0
        bgt     ic_tone_next
        moveq   #0,%d1
        movel   %d5,%d2
        subql   #1,%d2
        bsr     vline
ic_tone_next:
        addql   #1,%d7
        cmpil   #15,%d7
        ble     ic_tone_lp
        bra     blit


| RATE A: tick density (VOID/STUTTR family), double-thick.
ic_rate:
        bsr     ic_clr
        movel   %d6,%d5
        moveq   #7,%d0
        mulul   %d0,%d5
        moveq   #127,%d0
        divul   %d0,%d5
        addql   #1,%d5                   | n = 1..8
        cmpil   #1,%d5
        bne     ic_rate_many
        moveq   #7,%d7
ic_rate_fat:
        moveq   #2,%d1
        moveq   #10,%d2
        movel   %d7,%d0
        bsr     vline
        addql   #1,%d7
        cmpil   #9,%d7
        ble     ic_rate_fat
        bra     blit
ic_rate_many:
        moveq   #0,%d7                   | i
ic_rate_lp:
        movel   %d7,%d0
        moveq   #14,%d1
        mulul   %d1,%d0
        movel   %d5,%d1
        subql   #1,%d1                   | n-1
        divul   %d1,%d0
        addql   #1,%d0                   | x
        moveq   #2,%d1
        moveq   #10,%d2
        movel   %d0,%a3
        bsr     vline
        movel   %a3,%d0
        addql   #1,%d0
        cmpil   #16,%d0
        bgt     ic_rate_next
        moveq   #2,%d1
        moveq   #10,%d2
        bsr     vline
ic_rate_next:
        addql   #1,%d7
        cmpl    %d5,%d7
        blt     ic_rate_lp
        bra     blit


blit:
        movel   %sp@(64),%d0
        btst    #0,%d0
        beq     blit1
        lea     data(%pc),%a0
        moveq   #16,%d0
blit_inv:
        movel   %a0@,%d1
        eoril   #0xfff00000,%d1
        movel   %d1,%a0@+
        subql   #1,%d0
        bge     blit_inv
blit1:
        movel   %sp@(52),%d0
        addql   #7,%d0
        movel   %d0,%sp@-
        movel   %sp@(52),%d0
        addql   #1,%d0
        movel   %d0,%sp@-
        movel   %sp@(80),%sp@-
        pea     bmp(%pc)
        jsr     BLIT
        lea     %sp@(16),%sp
wid_out:
        moveml  %sp@,%d2-%d7/%a2-%a6
        lea     %sp@(44),%sp
        rts

ic_clr:
        lea     data(%pc),%a0
        moveq   #16,%d0
ic_clr1:
        clrl    %a0@+
        subql   #1,%d0
        bge     ic_clr1
        rts
copy:
        lea     data(%pc),%a1
        moveq   #16,%d0
copy1:
        movel   %a0@+,%a1@+
        subql   #1,%d0
        bge     copy1
        rts
orimg:
        lea     data(%pc),%a1
        moveq   #16,%d0
orimg1:
        movel   %a0@+,%d1
        orl     %d1,%a1@+
        subql   #1,%d0
        bge     orimg1
        rts
| vline(x=d0, row0=d1, row1=d2) inclusive; clobbers d3,a0
vline:
        lea     data(%pc),%a0
        lea     %a0@(0,%d0:l:4),%a0
        movel   #0x80000000,%d3
        lsrl    %d1,%d3
vline1:
        orl     %d3,%a0@
        lsrl    #1,%d3
        addql   #1,%d1
        cmpl    %d1,%d2
        bge     vline1
        rts
| hline(x0=d0, row=d1, x1=d2); clobbers d3,a0
hline:
        lea     data(%pc),%a0
        movel   #0x80000000,%d3
        lsrl    %d1,%d3
hline1:
        lea     %a0@(0,%d0:l:4),%a1
        orl     %d3,%a1@
        addql   #1,%d0
        cmpl    %d0,%d2
        bge     hline1
        rts

fold_sin:
        .byte   0, 3, 5, 6, 5, 3, 0, -3, -5, -6, -5, -3, 0, 3, 5, 3, 0
crsh_tab5:
        .byte   2, 5, 9, 4, 8
        .align  2

fmt_mode_tab:
        .word   fmt_mode_s0 - fmt_mode_tab
        .word   fmt_mode_s1 - fmt_mode_tab
        .word   fmt_mode_s2 - fmt_mode_tab
fmt_mode_s0:
        .asciz  "HARD"
fmt_mode_s1:
        .asciz  "SOFT"
fmt_mode_s2:
        .asciz  "CHAOS"
        .align  2

bmp:
        .long   17, 13, 1, data, mask
mask:
        .rept   17
        .long   0xfff80000
        .endr
data:
        .fill   17, 4, 0
heights:
        .fill   8, 1, 0
        .align  2

img_fdbk:
        .long   0x00000000, 0x00000000, 0x00000000, 0x00000000
        .long   0x00000000, 0x3f800000, 0x20800000, 0x20800000
        .long   0x20800000, 0x20800000, 0x20800000, 0x3f800000
        .long   0x00000000, 0x00000000, 0x00000000, 0x00000000
        .long   0x00000000
img_loop:
        .long   0x00000000, 0x00000000, 0x07f00000, 0x0e100000
        .long   0x04100000, 0x00100000, 0x00100000, 0x00100000
        .long   0x00100000, 0x00100000, 0x00100000, 0x00100000
        .long   0x04100000, 0x07f00000, 0x00000000, 0x00000000
        .long   0x00000000

img_mode_hard:
        .long   0x00000000, 0x00000000, 0x00000000, 0x1fc00000
        .long   0x1fc00000, 0x1fc00000, 0x1fc00000, 0x1fc00000
        .long   0x1fc00000, 0x1fc00000, 0x1fc00000, 0x1fc00000
        .long   0x1fc00000, 0x1fc00000, 0x00000000, 0x00000000
        .long   0x00000000
img_mode_soft:
        .long   0x00000000, 0x00000000, 0x00000000, 0x00000000
        .long   0x00000000, 0x07000000, 0x0f800000, 0x1fc00000
        .long   0x3fe00000, 0x1fc00000, 0x0f800000, 0x07000000
        .long   0x00000000, 0x00000000, 0x00000000, 0x00000000
        .long   0x00000000
img_mode_chaos:
        .long   0x00000000, 0x00000000, 0x00200000, 0x04600000
        .long   0x24600000, 0x28a00000, 0x48900000, 0x45100000
        .long   0x25200000, 0x32200000, 0x52100000, 0x48900000
        .long   0x18c00000, 0x31400000, 0x21200000, 0x00200000
        .long   0x00000000
