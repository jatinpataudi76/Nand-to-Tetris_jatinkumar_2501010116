// Box.asm  -  K = 16
// Box: starts at row 16, 20 rows tall, 16 pixels wide (1 word).
// Start address = SCREEN + 32*16 = SCREEN + 512 = 16896
// Key pressed -> black box (-1). Key released -> box cleared (0).

(LOOP)
    @KBD
    D=M
    @PRESSED
    D;JNE           // any key down?

    @color
    M=0             // no key: colour = white
    @DRAW
    0;JMP

(PRESSED)
    @color
    M=-1            // key: colour = black

(DRAW)
    @SCREEN
    D=A
    @512            // 32 * 16 = start row offset
    D=D+A
    @addr
    M=D             // addr = first word of the box

    @20
    D=A
    @cnt
    M=D             // cnt = 20 rows

(ROW)
    @color
    D=M
    @addr
    A=M
    M=D             // RAM[addr] = colour

    @32
    D=A
    @addr
    M=D+M           // next row = +32 words

    @cnt
    M=M-1
    D=M
    @ROW
    D;JGT           // repeat while cnt > 0

    @LOOP
    0;JMP
