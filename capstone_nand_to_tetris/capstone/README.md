# Capstone: Make the Computer Draw a Box

Nand to Tetris – I (ETCCNT301), K.R. Mangalam University
Name: Jatin Kumar | Roll no: 2501010116 | **K = 16**

| Item | Value |
|---|---|
| Box start row | 16 |
| Box height | 20 rows (rows 16–35) |
| Box width | 16 x ((16 mod 4) + 1) = 16 px = 1 word |
| First word address | SCREEN + 32*16 = 16384 + 512 = 16896 |
| Assembler extra feature | K mod 3 = 1 -> clear `Line N: ...` error messages |

## Files
- `CPU.hdl`, `Memory.hdl`, `Computer.hdl` – Part A
- `assembler.py` – Part B (two-pass Hack assembler)
- `Box.asm`, `Box.hack` – Part C (`Box.hack` made by `assembler.py`)
- `tests/` – small helper files (`Add.asm`, `Max.asm`, `bad.asm`, `emulate.py`)
- `REPORT.md` – text for the ZOSIMA report
- `VIVA.md` – notes for the viva

## Run
```
python assembler.py Box.asm          # writes Box.hack
python assembler.py tests/bad.asm    # shows the error messages
python tests/emulate.py Box.hack     # optional self-check, no GUI needed
```
Load `Box.hack` in the CPU Emulator (File > Load Program), tick Keyboard, press a key.

## Submit
Copy this folder into your lab repository as `capstone/`, then:
```
git add capstone
git commit -m "Add capstone"
git push
```
