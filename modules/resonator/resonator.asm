; ---------------------------------------------------------------------------
; RESONATOR -- Rings-inspired 4-mode modal bank (FX1 station).
;
; Frames in place at x:(r0)/x:(r0+n0), knobs from r6, state in r7.
; Law (resonator_ref.py; Spectrum VOWL / JOS two-zero):
;   y = 2*b0*(dx/2) + 2*m1*y1 - a2*y2
;   R = exp(-pi*bw/fs), m1 = R*cos(w0), a2 = R^2, b0 = (1-a2)/2
;
; P table (build rewrites the one table-base literal below), 111 words:
;   +0 FREQ_U 33  +33 COS 33  +66 R 33  +99 RATIOS 12 (ratio/16)
;
; r7: $00..$09 L (x1 x2 + 4*(y1 y2)), $0a..$13 R same,
;     $20 dry, $21 MIX, $30..$43 4*(b0 m1 a2 gL gR),
;     $44 STRU $45 R-idx $46 BRIT $47 POS $48 BODY*4
;     $49 u0 $4a R0 $4b i  $4d u  $4e cos  $51 a2 $52 m1 $54..$55 gains
;     $57 0=L / 1=R for gain pick
; ---------------------------------------------------------------------------

init:
        move    x:>$213,r4
        move    #>$ffffff,m4
        move    x:(r4),x0
        move    x0,a
        move    #>$4000,x0
        sub     x0,a
        clr     b
        move    #>$1,x0
        tst     a
        tpl     x0,b
        move    b,x:(r7+$20)
        clr     a
        move    r7,r4
        move    #>$ffffff,m4
        do      #<$14,>rs_iz
        move    a,x:(r4)+
rs_iz:
        rts

proc:
        move    x:(r7+$20),a
        tst     a
        bne     rs_end
        move    #>$fab1e0,r5            ; the P table -- rewritten by build_bus.py
        move    r5,x:(r7+$5a)
        move    x:(r6+$5),a
        and     #>$7f0000,a
        move    #>$7f0000,x0
        cmp     x0,a
        move    #>$7fffff,x0
        teq     x0,a
        move    a,x:(r7+$21)
        move    x:(r6+$1),a
        and     #>$7f0000,a
        move    a,x:(r7+$44)
        move    x:(r6+$2),a
        and     #>$7f0000,a
        move    a,x1                    ; DECY
        move    #>$7f0000,a
        sub     x1,a                    ; ~ (127-DECY)/128 in top bits
        and     #>$7f0000,a
        move    a,x:(r7+$45)
        move    x:(r6+$3),a
        and     #>$7f0000,a
        move    a,x:(r7+$46)
        move    x:(r6+$4),a
        and     #>$7f0000,a
        move    a,x0
        move    #>$733333,y1
        mpy     x0,y1,a
        add     #>$066666,a
        move    a,x:(r7+$47)
        move    x:(r6+$6),a
        and     #>$7f0000,a
        asr     #$10,a,a
        move    a1,x0
        move    x0,a
        asl     #$2,a,a
        move    a,x:(r7+$48)
; u0
        move    x:(r7+$5a),r5
        move    #>$ffffff,m5
        move    x:(r6+$0),a
        and     #>$7fffff,a
        move    a1,x1
        asr     #$12,a,a
        move    a1,n5
        move    x1,a
        and     #>$3ffff,a
        asl     #$5,a,a
        move    (r5)+n5
        move    a,x0
        move    p:(r5)+,y0
        move    p:(r5),b
        move    y0,a
        sub     a,b
        move    b,y1
        mpy     x0,y1,a
        add     y0,a
        move    a,x:(r7+$49)
; R0
        move    x:(r7+$5a),r5
        move    #$42,n5
        move    (r5)+n5
        move    x:(r7+$45),a
        and     #>$7fffff,a
        move    a1,x1
        asr     #$12,a,a
        move    a1,n5
        move    x1,a
        and     #>$3ffff,a
        asl     #$5,a,a
        move    (r5)+n5
        move    a,x0
        move    p:(r5)+,y0
        move    p:(r5),b
        move    y0,a
        sub     a,b
        move    b,y1
        mpy     x0,y1,a
        add     y0,a
        move    a,x:(r7+$4a)
; coeffs
        move    r7,r1
        move    #$30,n1
        move    (r1)+n1
        clr     a
        move    a,x:(r7+$4b)
        do      #4,>rs_bld
        bsr     rs_build
        move    x:(r7+$4b),a
        add     #>$1,a
        move    a,x:(r7+$4b)
rs_bld:
; samples
        move    #>$1,n0
        do      n7,>rs_sz
        clr     a
        move    a,x:(r7+$57)
        move    x:(r0),x1
        move    r7,r4
        move    r7,r3
        move    #$30,n3
        move    (r3)+n3
        bsr     rs_chan
        move    a,y0
        move    x:(r0),a
        move    y0,b
        sub     a,b
        move    b,y1
        move    x:(r7+$21),x0
        mpy     x0,y1,b
        add     b,a
        move    a,x:(r0)+
        move    #>$1,x0
        move    x0,x:(r7+$57)
        move    x:(r0),x1
        move    r7,r4
        move    #$0a,n4
        move    (r4)+n4
        move    r7,r3
        move    #$30,n3
        move    (r3)+n3
        bsr     rs_chan
        move    a,y0
        move    x:(r0),a
        move    y0,b
        sub     a,b
        move    b,y1
        move    x:(r7+$21),x0
        mpy     x0,y1,b
        add     b,a
        move    a,x:(r0)+
rs_sz:
rs_end:
        rts

; r4 -> x1, r3 -> coeffs, x1 = input, $57 = channel. wet in a.
; Acc parks in $58. Four modes fully unrolled (no do/bsr: cycle_count).
rs_chan:
        move    x:(r4),y0
        move    x1,x:(r4)+
        move    x:(r4),x0
        move    y0,x:(r4)+
        move    x1,a
        sub     x0,a
        asr     #$1,a,a
        move    a,x1
        clr     a
        move    a,x:(r7+$58)
; ---- mode 0 ----
        move    x1,x0
        move    x:(r3)+,y1
        mpy     x0,y1,a
        asl     #$1,a,a
        move    a,y0
        move    x:(r4),x0
        move    x:(r3)+,y1
        mpy     x0,y1,a
        asl     #$1,a,a
        add     y0,a
        move    x0,y0
        move    x:(r4+$1),x0
        move    y0,x:(r4+$1)
        move    x:(r3)+,y1
        mpy     x0,y1,b
        sub     b,a
        move    a,x:(r4)+
        move    (r4)+
        move    a,x0
        move    x:(r3)+,a
        move    x:(r3)+,y1
        move    x:(r7+$57),b
        tst     b
        tne     y1,a
        move    a,y1
        mpy     x0,y1,a
        move    x:(r7+$58),b
        add     a,b
        move    b,x:(r7+$58)
; ---- mode 1 ----
        move    x1,x0
        move    x:(r3)+,y1
        mpy     x0,y1,a
        asl     #$1,a,a
        move    a,y0
        move    x:(r4),x0
        move    x:(r3)+,y1
        mpy     x0,y1,a
        asl     #$1,a,a
        add     y0,a
        move    x0,y0
        move    x:(r4+$1),x0
        move    y0,x:(r4+$1)
        move    x:(r3)+,y1
        mpy     x0,y1,b
        sub     b,a
        move    a,x:(r4)+
        move    (r4)+
        move    a,x0
        move    x:(r3)+,a
        move    x:(r3)+,y1
        move    x:(r7+$57),b
        tst     b
        tne     y1,a
        move    a,y1
        mpy     x0,y1,a
        move    x:(r7+$58),b
        add     a,b
        move    b,x:(r7+$58)
; ---- mode 2 ----
        move    x1,x0
        move    x:(r3)+,y1
        mpy     x0,y1,a
        asl     #$1,a,a
        move    a,y0
        move    x:(r4),x0
        move    x:(r3)+,y1
        mpy     x0,y1,a
        asl     #$1,a,a
        add     y0,a
        move    x0,y0
        move    x:(r4+$1),x0
        move    y0,x:(r4+$1)
        move    x:(r3)+,y1
        mpy     x0,y1,b
        sub     b,a
        move    a,x:(r4)+
        move    (r4)+
        move    a,x0
        move    x:(r3)+,a
        move    x:(r3)+,y1
        move    x:(r7+$57),b
        tst     b
        tne     y1,a
        move    a,y1
        mpy     x0,y1,a
        move    x:(r7+$58),b
        add     a,b
        move    b,x:(r7+$58)
; ---- mode 3 ----
        move    x1,x0
        move    x:(r3)+,y1
        mpy     x0,y1,a
        asl     #$1,a,a
        move    a,y0
        move    x:(r4),x0
        move    x:(r3)+,y1
        mpy     x0,y1,a
        asl     #$1,a,a
        add     y0,a
        move    x0,y0
        move    x:(r4+$1),x0
        move    y0,x:(r4+$1)
        move    x:(r3)+,y1
        mpy     x0,y1,b
        sub     b,a
        move    a,x:(r4)+
        move    (r4)+
        move    a,x0
        move    x:(r3)+,a
        move    x:(r3)+,y1
        move    x:(r7+$57),b
        tst     b
        tne     y1,a
        move    a,y1
        mpy     x0,y1,a
        move    x:(r7+$58),b
        add     a,b
        move    b,a
        rts

rs_build:
        move    x:(r7+$5a),r5
        move    #>$ffffff,m5
        move    #$63,n5
        move    (r5)+n5
        move    x:(r7+$48),a
        move    x:(r7+$4b),x0
        add     x0,a
        move    a1,n5
        move    (r5)+n5
        move    p:(r5),a
        asl     #$4,a,a
        move    a,y0
        move    x:(r7+$4b),a
        move    a1,n0
        move    #>$1,b
        move    n0,y1
        add     y1,b
        move    b,x0
        move    n0,a
        asl     #$15,a,a
        move    a,y1
        mpy     x0,y1,a
        add     x0,a
        move    a,b
        sub     y0,b
        move    b,y1
        move    x:(r7+$44),x0
        mpy     x0,y1,a
        add     y0,a
        move    a,y1
        move    x:(r7+$49),x0
        mpy     x0,y1,a
        move    #>$79999a,x0
        cmp     x0,a
        tgt     x0,a
        move    a,x:(r7+$4d)
        move    x:(r7+$5a),r5
        move    #$21,n5
        move    (r5)+n5
        move    x:(r7+$4d),a
        and     #>$7fffff,a
        move    a1,x1
        asr     #$12,a,a
        move    a1,n5
        move    x1,a
        and     #>$3ffff,a
        asl     #$5,a,a
        move    (r5)+n5
        move    a,x0
        move    p:(r5)+,y0
        move    p:(r5),b
        move    y0,a
        sub     a,b
        move    b,y1
        mpy     x0,y1,a
        add     y0,a
        move    a,x:(r7+$4e)
        move    x:(r7+$46),a            ; BRIT
        move    a,y0
        move    #>$7fffff,a
        sub     y0,a                    ; 1 - BRIT
        move    a,y1
        move    x:(r7+$4b),a
        asl     #$15,a,a
        move    a,x0
        mpy     x0,y1,a
        move    a,x0
        move    #>$466666,y1
        mpy     x0,y1,a
        move    a,y0
        move    #>$7fffff,a
        sub     y0,a                    ; 1 - widen
        move    a,y1
        move    x:(r7+$4a),x0
        mpy     x0,y1,a
        move    #>$400000,x0
        cmp     x0,a
        tmi     x0,a
        move    a,x0
        move    x:(r7+$4e),y1
        mpy     x0,y1,b
        move    b,x:(r7+$52)
        move    a,y1
        mpy     x0,y1,b
        move    b,x:(r7+$51)
        asr     #$1,b,b
        neg     b
        add     #>$400000,b
        move    b,x:(r1)+
        move    x:(r7+$52),x0
        move    x0,x:(r1)+
        move    x:(r7+$51),x0
        move    x0,x:(r1)+
        move    x:(r7+$4b),a
        add     #>$1,a
        move    a,x0
        move    x:(r7+$47),y1
        mpy     x0,y1,a
        and     #>$7fffff,a
        asl     #$1,a,a
        abs     a
        move    a,y0
        move    #>$7fffff,a
        sub     y0,a
        abs     a
        move    a,x0
        move    #>$600000,y1
        mpy     x0,y1,a
        add     #>$200000,a
        move    a,x0
        move    #>$2ccccd,y1
        mpy     x0,y1,a
        move    a,x:(r7+$54)
        move    x:(r7+$47),a
        move    #>$400000,x0
        sub     x0,a                    ; pos - 0.5
        move    a,x0
        move    #>$2ccccd,y1
        mpy     x0,y1,a
        move    a,x:(r7+$55)
        move    x:(r7+$54),x0
        move    #>$7fffff,b
        move    x:(r7+$55),a
        sub     a,b
        move    b,y1
        mpy     x0,y1,a
        move    a,x:(r1)+
        move    x:(r7+$54),x0
        move    #>$7fffff,b
        move    x:(r7+$55),a
        add     a,b
        move    b,y1
        mpy     x0,y1,a
        move    a,x:(r1)+
        rts
