# Capstone Project: Make the Computer Draw a Box

**Course:** Nand to Tetris – I (ETCCNT301), School of Engineering & Technology, K.R. Mangalam University
**Name:** Jatin Kumar
**Roll no:** 2501010116
**K:** 16
**Box size:** starts at row 16, 20 rows tall, 16 pixels wide (1 word)
**GitHub:** <https://github.com/jatinpataudi76/Nand-to-Tetris_jatinkumar_2501010116>

---

## 1. Overview
The goal is to make the Hack computer show a black box while any key is pressed and remove it when the key is released. The work has three parts: the computer (Part A), an assembler written in Python (Part B) and the box program (Part C).

My personal number is K = 16 (last two digits of 2501010116). It gives:
- Box start row = 16.
- Box height = 20 rows, so rows 16 to 35.
- Box width = 16 x ((16 mod 4) + 1) = 16 x 1 = 16 pixels = one 16-bit word.
- Assembler feature: 16 mod 3 = 1, so the assembler prints clear error messages with line numbers.

## 2. Part A – Building the computer
I joined my chips into `CPU.hdl`, `Memory.hdl` and `Computer.hdl`.

- **CPU:** the A register takes either the instruction (A-instruction) or the ALU output (C-instruction with d1). The ALU's second input is A or M, chosen by the a-bit (instruction[12]). D loads when d2 is set, `writeM` is d3. The jump logic uses the ALU flags `zr` and `ng` with the jump bits j1, j2, j3. The PC loads A when a jump is taken, otherwise it increments.
- **Memory:** address bit 14 separates RAM (0–16383) from the screen/keyboard area. Bit 13 then separates the screen (16384–24575) from the keyboard (24576). A `Mux4Way16` selects the read value.
- **Computer:** `ROM32K` feeds instructions to the CPU, and the CPU talks to `Memory`.

Built-in chips used: <list the built-in chips you used, e.g. ALU, ARegister, DRegister, PC, RAM16K, Screen, Keyboard, ROM32K – and say whether your own versions were used or not>.

### Test results
| Test file | Result | Screenshot |
|---|---|---|
| CPU.tst | <pass/fail> | <insert> |
| Memory.tst | <pass/fail> | <insert> |
| ComputerAdd.tst | <pass/fail> | <insert> |
| ComputerMax.tst | <pass/fail> | <insert> |
| ComputerRect.tst | <pass/fail> | <insert> |

## 3. Part B – Assembler (`assembler.py`)
The assembler reads a `.asm` file and writes a `.hack` file with one 16-bit instruction per line.

**First reading.** Comments and blank lines are removed. Each label such as `(LOOP)` is stored with the number of the next real instruction. Labels do not produce code.

**Second reading.** Every line becomes 16 bits.
- A-instruction `@x`: a number is written in binary. A symbol is looked up in the table. A new variable gets the next free RAM address, starting at 16.
- C-instruction `dest=comp;jump`: the three parts are looked up in tables and joined as `111` + comp (7 bits) + dest (3 bits) + jump (3 bits).

Predefined symbols: R0–R15, SP, LCL, ARG, THIS, THAT, SCREEN (16384), KBD (24576).

**Extra feature (K mod 3 = 1).** Wrong lines do not crash the program. Each error is stored with its original line number and printed at the end, in line order. If there is any error, no `.hack` file is written. Example from `tests/bad.asm`:
```
Line 5: invalid instruction 'D=D+Q'
Line 9: duplicate label 'END'
Line 11: invalid instruction '0;JMPP'
3 error(s), no .hack file written.
```

### Comparison with the official assembler
| Program | Output matches official assembler? |
|---|---|
| Add.asm | <yes/no> |
| Max.asm | <yes/no> |
| Rect.asm | <yes/no> |
| Pong.asm | <yes/no> |

(Compare with: `fc` on Windows or `diff` on Linux/Mac.)

## 4. Part C – Box program (`Box.asm`)
- First word of the box: SCREEN + 32 x 16 = 16384 + 512 = 16896.
- One row is 32 words, so the next row of the box is 32 words later.
- Width is one word, so each row needs one write. Height is 20, so the loop runs 20 times.

**Algorithm.**
1. Read the keyboard (`@KBD`). If it is not 0, colour = -1 (all 16 bits black). Otherwise colour = 0.
2. Set `addr` = 16896 and `cnt` = 20.
3. Repeat 20 times: write colour to RAM[addr], add 32 to `addr`, subtract 1 from `cnt`.
4. Go back to step 1.

`Box.hack` was made with my own `assembler.py` (36 instructions).

**Screenshot of the box:** <insert screenshot from the CPU Emulator>

## 5. One mistake I fixed
<Write one paragraph about a real mistake you ran into and how you fixed it. Say what you saw, why it happened and what you changed. Use your own experience – the viva may ask about it.>

## 6. Conclusion
<2–3 lines: what you built and what you learned.>
