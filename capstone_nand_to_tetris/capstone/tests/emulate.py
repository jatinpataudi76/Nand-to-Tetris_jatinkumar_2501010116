"""Tiny Hack emulator used only to self-check Box.hack (not required by the project).
Usage: python tests/emulate.py Box.hack
"""
import sys

SCREEN, KBD = 16384, 24576


def run(rom, ram, steps):
    a = d = pc = 0
    for _ in range(steps):
        if pc >= len(rom):
            break
        ins = rom[pc]
        if ins >> 15 == 0:
            a = ins
            pc += 1
            continue
        y = ram[a] if (ins >> 12) & 1 else a
        c = (ins >> 6) & 0x3F
        zx, nx, zy, ny, f, no = [(c >> i) & 1 for i in (5, 4, 3, 2, 1, 0)]
        x = 0 if zx else d
        yy = 0 if zy else y
        x = (~x) & 0xFFFF if nx else x
        yy = (~yy) & 0xFFFF if ny else yy
        out = (x + yy) & 0xFFFF if f else x & yy
        out = (~out) & 0xFFFF if no else out
        sgn = out - 65536 if out & 0x8000 else out
        dest, jmp = (ins >> 3) & 7, ins & 7
        old_a = a
        if dest & 1:
            ram[old_a] = out
        if dest & 2:
            d = out
        if dest & 4:
            a = out
        take = (jmp & 4 and sgn < 0) or (jmp & 2 and sgn == 0) or (jmp & 1 and sgn > 0)
        pc = a if take else pc + 1


def main(path):
    rom = [int(l, 2) for l in open(path).read().split()]
    K, rows, words = 16, 20, 1
    ok = True

    ram = [0] * 24577
    ram[KBD] = 75  # key pressed
    run(rom, ram, 5000)
    for r in range(36):
        for w in range(32):
            v = ram[SCREEN + 32 * r + w]
            want = 0xFFFF if (K <= r < K + rows and w < words) else 0
            if v != want:
                ok = False
                print(f"PRESSED mismatch row {r} word {w}: {v:#06x} != {want:#06x}")
    print("key pressed : box drawn rows %d-%d, %d word wide ->" % (K, K + rows - 1, words),
          "OK" if ok else "FAIL")

    ram[KBD] = 0  # key released
    run(rom, ram, 5000)
    cleared = all(ram[SCREEN + i] == 0 for i in range(32 * 40))
    print("key released: screen cleared ->", "OK" if cleared else "FAIL")
    ok = ok and cleared
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Box.hack")
