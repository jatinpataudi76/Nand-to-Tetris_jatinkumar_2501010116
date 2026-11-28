import sys, re

COMP = {
    '0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100',
    'A': '0110000', '!D': '0001101', '!A': '0110001', '-D': '0001111',
    '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
    'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
    'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111',
    'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101',
}
DEST = {'': '000', 'M': '001', 'D': '010', 'MD': '011',
        'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}
JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

SYMBOLS = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
           'SCREEN': 16384, 'KBD': 24576}
for i in range(16):
    SYMBOLS['R' + str(i)] = i

NAME = re.compile(r'^[A-Za-z_.$:][\w.$:]*$')


def clean(line):
    # drop comment, then drop all whitespace
    return ''.join(line.split('//')[0].split())


def main(path):
    errors = []
    symbols = dict(SYMBOLS)

    # read file, keep original line numbers
    with open(path) as f:
        lines = [(n, clean(t)) for n, t in enumerate(f, 1)]
    lines = [(n, t) for n, t in lines if t]

    # ---- pass 1: find labels ----
    code = []
    rom = 0
    for n, t in lines:
        if t.startswith('(') and t.endswith(')'):
            name = t[1:-1]
            if not NAME.match(name):
                errors.append(f"Line {n}: invalid label '{t}'")
            elif name in symbols:
                errors.append(f"Line {n}: duplicate label '{name}'")
            else:
                symbols[name] = rom
        else:
            code.append((n, t))
            rom += 1

    # ---- pass 2: translate ----
    out = []
    nxt = 16
    for n, t in code:
        if t[0] == '@':
            x = t[1:]
            if x.isdigit() and int(x) <= 32767:
                val = int(x)
            elif NAME.match(x):
                if x not in symbols:
                    symbols[x] = nxt
                    nxt += 1
                val = symbols[x]
            else:
                errors.append(f"Line {n}: invalid instruction '{t}'")
                continue
            out.append(format(val, '016b'))
        else:
            dest, comp, jump = '', t, ''
            if '=' in comp:
                dest, comp = comp.split('=', 1)
            if ';' in comp:
                comp, jump = comp.split(';', 1)
            if comp in COMP and dest in DEST and jump in JUMP:
                out.append('111' + COMP[comp] + DEST[dest] + JUMP[jump])
            else:
                errors.append(f"Line {n}: invalid instruction '{t}'")

    if errors:
        errors.sort(key=lambda e: int(e.split(':')[0].split()[1]))
        print('\n'.join(errors))
        print(f"{len(errors)} error(s), no .hack file written.")
        return

    outpath = path.rsplit('.', 1)[0] + '.hack'
    with open(outpath, 'w') as f:
        f.write('\n'.join(out) + '\n')
    print(f"OK: {len(out)} instructions -> {outpath}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python assembler.py File.asm")
    else:
        main(sys.argv[1])
