# Viva notes (K = 16)

## The numbers
- Box: row 16, 20 rows, 1 word wide.
- Start address = 16384 + 32*16 = 16896 (code: `@SCREEN`, `D=A`, `@512`, `D=D+A`).
- Black word = -1 = `1111111111111111`. White = 0.

## Box.asm in plain words (analogy: painting a fence)
You stand at the first plank (`addr`), paint it (`M=D`), walk 32 planks to the next painted spot (`+32`), and count down from 20 (`cnt`) until done. Then you look at the keyboard again to decide whether to paint black or white.

| Lines | What they do |
|---|---|
| `@KBD` `D=M` `@PRESSED` `D;JNE` | read key; jump if not 0 |
| `@color` `M=0` / `M=-1` | choose white or black |
| `@SCREEN` `D=A` `@512` `D=D+A` | D = 16896 |
| `@addr` `M=D` | save start address |
| `@20` `D=A` `@cnt` `M=D` | counter = 20 |
| `@addr` `A=M` `M=D` | go to the saved address and write the colour |
| `@32` `D=A` `@addr` `M=D+M` | addr = addr + 32 |
| `@cnt` `M=M-1` `D=M` `@ROW` `D;JGT` | loop while cnt > 0 |

## Likely "change it on the spot" requests
| Request | Change |
|---|---|
| Move box down by 4 rows | `@512` -> `@640` (32 x 20) |
| Start at another row r | `@512` -> `@(32*r)` |
| Taller (e.g. 30 rows) | `@20` -> `@30` |
| Wider (2 words) | write colour to `addr` and `addr+1` in each row (add a second write, or an inner loop); screen position stays the same |
| Different K | recompute row, width, start offset |
| Box stays after key release | remove the white branch (never set colour to 0) |

After any change: `python assembler.py Box.asm`, reload `Box.hack` in the CPU Emulator.

## Assembler questions
- **Why two passes?** A jump can refer to a label that appears later in the file. Pass 1 learns all label addresses; pass 2 uses them.
- **Why do labels not count as instructions?** They are only names for a position.
- **Variables start at?** RAM 16. R0–R15 are taken (16 = first free).
- **C-instruction format?** `111 a c1..c6 d1 d2 d3 j1 j2 j3`.
- **A-instruction format?** `0` + 15-bit value.
- **My extra feature?** K mod 3 = 1: errors with line numbers instead of a crash. Show `tests/bad.asm`.
- **Why are line numbers still correct after removing comments?** Original line numbers are stored together with each cleaned line.

## Hardware questions
- **Memory map:** 0–16383 RAM, 16384–24575 screen, 24576 keyboard.
- **How does the CPU decide A vs C instruction?** Bit 15.
- **When does a jump happen?** Jump bits match the ALU flags (`ng`, `zr`, positive) and it is a C-instruction.
- **Which chips were built-in in your project?** Answer from your own report.

If you cannot explain a line, do not skip it: re-read it with a tiny example (for example `@32 D=A @addr M=D+M` when addr = 16896 gives 16928).
