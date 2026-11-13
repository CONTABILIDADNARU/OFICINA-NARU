import struct

def load(path):
    """Lee un DBF de VFP. Devuelve (campos, filas[dict], eliminados)."""
    d = open(path, 'rb').read()
    n = struct.unpack('<I', d[4:8])[0]
    hl, rl = struct.unpack('<HH', d[8:12])
    fs = []
    off, pos = 32, 1
    while d[off] != 0x0D:
        nm = d[off:off + 11].split(b'\0')[0].decode('latin1')
        t = chr(d[off + 11]); l = d[off + 16]; dec = d[off + 17]
        fs.append((nm, t, l, dec, pos))
        pos += l; off += 32
    rows, deleted = [], 0
    for i in range(n):
        r = d[hl + i * rl: hl + (i + 1) * rl]
        if r[0:1] == b'*':
            deleted += 1
            continue
        row = {}
        for nm, t, l, dec, p in fs:
            raw = r[p:p + l]
            if t in 'CNDL':
                v = raw.decode('latin1').strip()
                if t == 'N':
                    try: v = float(v) if v else 0.0
                    except ValueError: v = 0.0
            else:
                v = raw
            row[nm] = v
        rows.append(row)
    return fs, rows, deleted
