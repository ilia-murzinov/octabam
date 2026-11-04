| Megabyte in the stock Echo Freeze filter/mix seam.
| Same protocol as Tape Echo (docs/firmware/COLDFIRE_DELAY.md).
        .text
        .balign 4
        .global mb_cpu_hook, mb_cpu_reset, mb_states
mb_cpu_reset:
        lea     -12(%sp),%sp
        movem.l %d0-%d1/%a0,(%sp)
        lea     mb_states,%a0
        move.l  #((8*48)/4)-1,%d1
        moveq   #0,%d0
mb_clear_loop:
        move.l  %d0,(%a0)+
        subq.l  #1,%d1
        bpl.s   mb_clear_loop
        movem.l (%sp),%d0-%d1/%a0
        lea     12(%sp),%sp
        lea     -16(%sp),%sp
        movem.l %d2-%d5,(%sp)
        jmp     0x40002f4c
mb_cpu_hook:
        lea     -20(%sp),%sp
        movem.l %d0-%d1/%a0-%a1,4(%sp)
        lea     20(%sp),%a0
        move.l  %a0,(%sp)
        jsr     mb_cpu_frame
        tst.l   %d0
        beq.s   mb_stock_path
        movem.l 4(%sp),%d0-%d1/%a0-%a1
        lea     20(%sp),%sp
        jmp     0x4000377a
mb_stock_path:
        movem.l 4(%sp),%d0-%d1/%a0-%a1
        lea     20(%sp),%sp
        move.l  92(%sp),%a5
        move.l  0x800000e8,%d0
        jmp     0x40003624
        .balign 4
mb_states:
        .zero   384
