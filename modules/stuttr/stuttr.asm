; CYCLES_FORWARD_BRANCHES
; ---------------------------------------------------------------------------
; STUTTR -- buffer freeze / slice repeater.
;
; Y ring from the stock allocator. Stereo interleaved. Write always advances.
; Clock retriggers a slice; CHNC gates wet; MODE LOOP/REV/DROP/SCRAM.
;
; r7 $20 base $21 write $22 clear $23 maxlen $24 size $25 rate
;    $26 chnc $27 mix $28 mode $29 clock $2a offset $2b active $2c gain
;    $2d dir $2e scram $2f wetL $30 wetR $31 fdbk $32 decy
;    $33 slice start (absolute); read = start + offset, folded into ring
; Labels st00.. only. mpy x0,y1 / y0,x0 / x0,x0 only. init keeps r1. No rep.
; SIZE words (integer): FX2 (kn+1)*32, FX1 (kn+1)*8. Min 8, even.
; RATE clock step: 0x400+(kn<<10) -> ~372ms .. ~64 samples between re-grabs.
; Wet only after a grab (never loop the cleared base). CHNC is on/off.
; ---------------------------------------------------------------------------

init:
        move    #>$ffffff,m4
        move    r7,r4
        move    #>$20,n4
        move    (r4)+n4
        clr     a
        do      #22,>st00
        move    a,x:(r4)+
st00:
        nop
        move    x:>$213,r4
        move    x:(r4),a
        move    a,x:(r7+$20)
        move    a,x:(r7+$21)
        move    a,x:(r7+$33)
        move    #>$80,a
        move    a,x:(r7+$22)
        move    #>$4000,x0
        move    x:(r7+$20),a
        sub     x0,a
        move    #>$0c00,b               ; FX1 maxlen 3072
        move    #>$4000,x0              ; FX2 maxlen 16384
        tst     a
        tpl     x0,b
        move    b,x:(r7+$23)
        move    #>$7fffff,x0
        move    x0,x:(r7+$2c)
        move    #>$1,x0
        move    x0,x:(r7+$2d)
        ; $2b active stays 0 until first grab (wet must not read cleared Y)
        rts

proc:
        move    x:(r7+$22),a
        tst     a
        beq     st01
        sub     #>$1,a
        move    a,x:(r7+$22)
        asl     #$7,a,a
        move    x:(r7+$20),x0
        add     x0,a
        move    a,r4
        move    #>$ffffff,m4
        clr     a
        do      #128,>st02
        move    a,y:(r4)+
st02:
        nop
        rts
st01:
; SIZE -> slice length in words. Short grains: FX2 (kn+1)*32, FX1 (kn+1)*8.
        move    x:(r6+$0),a
        and     #>$7f0000,a             ; LFO low byte must not leak
        asr     #$10,a,a                ; kn 0..127
        add     #>$1,a                  ; 1..128
        move    a,x0
        move    x:(r7+$23),b            ; maxlen
        move    #>$4000,y0
        cmp     y0,b
        bne     st20                    ; FX1 path
        asl     #$5,a,a                 ; FX2: (kn+1)*32  (32..4096 words)
        bra     st21
st20:
        asl     #$3,a,a                 ; FX1: (kn+1)*8   (8..1024 words)
st21:
        move    #>$8,x0
        cmp     x0,a
        tlt     x0,a
        move    x:(r7+$23),x0           ; clamp to maxlen
        cmp     x0,a
        tgt     x0,a
        and     #>$fffffe,a
        move    a,x:(r7+$24)
; RATE -> clock step. Overflow at 0x800000 ≈ re-grab period.
; step = 0x400 + (kn<<10): kn0 ≈ 372ms, kn127 ≈ 64 samples.
        move    x:(r6+$1),a
        and     #>$7f0000,a
        asr     #$10,a,a                ; kn 0..127
        asl     #$a,a,a                 ; kn*1024
        add     #>$400,a
        move    x:(r6+$7),b             ; SYNC 0=FREE 1=/16 2=/8 3=/4
        and     #>$7f0000,b
        asr     #$10,b,b
        move    #>$1,x0
        cmp     x0,b
        bne     st14
        asr     #$4,a,a
        bra     st17
st14:
        move    #>$2,x0
        cmp     x0,b
        bne     st15
        asr     #$3,a,a
        bra     st17
st15:
        move    #>$3,x0
        cmp     x0,b
        bne     st17
        asr     #$2,a,a
st17:
        move    a,x:(r7+$25)
        move    x:(r6+$2),a             ; CHNC: 0 = dry stage, else wet when active
        and     #>$7f0000,a
        move    a,x:(r7+$26)
        move    x:(r6+$3),a             ; FDBK
        and     #>$7fffff,a
        move    a,x:(r7+$31)
        move    x:(r6+$4),a             ; DECY -> step (0 = hold)
        and     #>$7fffff,a
        asr     #$8,a,a
        move    a,x:(r7+$32)
        move    x:(r6+$5),a             ; MIX
        and     #>$7f0000,a
        move    #>$7f0000,x0
        cmp     x0,a
        move    #>$7fffff,x0
        teq     x0,a
        move    a,x:(r7+$27)
        move    x:(r6+$6),a             ; MODE
        and     #>$7f0000,a
        asr     #$10,a,a
        move    a,x:(r7+$28)
        move    #$1,n0
        do      n7,>st19
; write L/R = dry + FDBK * previous wet
        move    x:(r7+$21),r4
        move    #>$ffffff,m4
        move    x:(r0),b
        move    x:(r7+$2f),x0
        move    x:(r7+$31),y1
        mpy     x0,y1,a
        add     b,a
        move    a,y:(r4)+
        move    x:(r0+n0),b
        move    x:(r7+$30),x0
        mpy     x0,y1,a
        add     b,a
        move    a,y:(r4)+
        move    r4,a
        move    x:(r7+$20),x0
        sub     x0,a
        move    x:(r7+$23),x0
        cmp     x0,a
        blt     st03
        move    x:(r7+$20),r4
st03:
        move    r4,x:(r7+$21)
; clock + retrigger (also first grab once the ring holds a full SIZE)
        move    x:(r7+$29),a
        move    x:(r7+$25),x0
        add     x0,a
        move    a,x:(r7+$29)
        move    a1,b
        tst     b
        bmi     st26                    ; RATE overflow -> grab
        move    x:(r7+$2b),b            ; already active?
        tst     b
        bne     st04
        move    x:(r7+$21),a            ; fill: write-base >= size?
        move    x:(r7+$20),x0
        sub     x0,a
        move    x:(r7+$24),x0
        cmp     x0,a
        blt     st04
st26:
        clr     a
        move    a,x:(r7+$29)
        move    #>$7fffff,x0
        move    x0,x:(r7+$2c)
        move    #>$1,x0
        move    x0,x:(r7+$2b)
        move    x:(r7+$21),a
        move    x:(r7+$24),x0
        sub     x0,a
        move    x:(r7+$20),x0
        cmp     x0,a
        bge     st05
        move    x:(r7+$23),x0
        add     x0,a
st05:
        move    a,x:(r7+$33)            ; slice start (absolute)
        clr     a
        move    a,x:(r7+$2a)            ; offset 0 within slice
        move    #>$1,a                  ; dir +1
        move    #>$1,x0
        move    x:(r7+$28),b
        cmp     x0,b
        move    #>$800000,x0            ; -1 for REV
        teq     x0,a
        move    a,x:(r7+$2d)
        move    x:(r7+$28),b
        move    #>$3,x0
        cmp     x0,b
        bne     st04
        move    x:(r7+$2e),a
        add     #>$2d,a
        move    a,x:(r7+$2e)
st04:
; default wet = dry
        move    x:(r0),a
        move    a,x:(r7+$2f)
        move    x:(r0+n0),a
        move    a,x:(r7+$30)
        move    x:(r7+$26),a            ; CHNC 0 = dry
        tst     a
        beq     st10
        move    x:(r7+$2b),a            ; need a grab first
        tst     a
        beq     st10
        move    x:(r7+$2c),a            ; gain 0 -> dry (not muted hole)
        tst     a
        beq     st10
; addr = start + offset (+ SCRAM), fold into ring, read
        move    x:(r7+$33),a
        move    x:(r7+$2a),x0
        add     x0,a
        move    x:(r7+$28),b
        move    #>$3,x0
        cmp     x0,b
        bne     st07
        move    x:(r7+$2e),b
        and     #>$00ffff,b
        move    x:(r7+$24),x0
        cmp     x0,b
        tgt     x0,b
        and     #>$fffffe,b
        add     b,a
st07:
        move    x:(r7+$20),x0           ; fold into [base, base+maxlen)
        cmp     x0,a
        bge     st24
        move    x:(r7+$23),x0
        add     x0,a
st24:
        move    x:(r7+$20),x0
        move    x:(r7+$23),b
        add     x0,b
        cmp     b,a
        blt     st25
        move    x:(r7+$23),x0
        sub     x0,a
st25:
        move    a,r4
        move    #>$ffffff,m4
        move    y:(r4)+,a
        move    a,x:(r7+$2f)
        move    y:(r4)+,a
        move    a,x:(r7+$30)
; advance offset ±2, wrap in [0, size)
        move    x:(r7+$2a),a
        add     #>$2,a
        move    a,x1
        move    x:(r7+$2a),a
        sub     #>$2,a
        move    x:(r7+$2d),b
        tst     b
        tpl     x1,a
        move    #>$0,x0
        cmp     x0,a
        bge     st12
        move    x:(r7+$24),a
        sub     #>$2,a
st12:
        move    x:(r7+$24),x0
        cmp     x0,a
        blt     st13
        move    #>$0,a
st13:
        move    a,x:(r7+$2a)
; gain * DECY step
        move    x:(r7+$2f),x0
        move    x:(r7+$2c),y1
        mpy     x0,y1,a
        move    a,x:(r7+$2f)
        move    x:(r7+$30),x0
        mpy     x0,y1,a
        move    a,x:(r7+$30)
        move    x:(r7+$2c),a
        move    x:(r7+$32),x0
        sub     x0,a
        move    #>$0,x0
        cmp     x0,a
        tlt     x0,a
        move    a,x:(r7+$2c)
; MODE DROP: force silence after the shared path
        move    x:(r7+$28),b
        move    #>$2,x0
        cmp     x0,b
        bne     st10
        clr     a
        move    a,x:(r7+$2f)
        move    a,x:(r7+$30)
st10:
; MIX
        move    x:(r0),b
        move    x:(r7+$2f),a
        sub     b,a
        move    a,x0
        move    x:(r7+$27),y1
        mpy     x0,y1,a
        add     b,a
        move    a,x:(r0)+n0
        move    x:(r0),b
        move    x:(r7+$30),a
        sub     b,a
        move    a,x0
        mpy     x0,y1,a
        add     b,a
        move    a,x:(r0)+
st19:
        nop
        rts
