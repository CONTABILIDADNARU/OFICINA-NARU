import struct
def parse(d):
    n = struct.unpack('<I', d[4:8])[0]; hl, rl = struct.unpack('<HH', d[8:12])
    fs = {}; off = 32; pos = 1
    while d[off] != 0x0D:
        fs[d[off:off+11].split(b'\0')[0].decode()] = (pos, d[off+16], chr(d[off+11]), d[off+17]); pos += d[off+16]; off += 32
    return n, hl, rl, fs
def recs(d):
    n, hl, rl, fs = parse(d); return [d[hl+i*rl: hl+(i+1)*rl] for i in range(n)]
def get(r, fs, k):
    p, l = fs[k][0], fs[k][1]; return r[p:p+l].decode('latin1').strip()
def putc(r, fs, k, v):
    p, l = fs[k][0], fs[k][1]; return r[:p] + v.encode('latin1', 'replace').ljust(l)[:l] + r[p+l:]
def putn(r, fs, k, v, dec=2):
    p, l = fs[k][0], fs[k][1]; s = f"{v:.{dec}f}"; assert len(s) <= l, (k, s)
    return r[:p] + s.rjust(l).encode('latin1') + r[p+l:]
def build(tb, records):
    n, hl, rl, fs = parse(tb); h = bytearray(tb[:hl]); h[4:8] = struct.pack('<I', len(records))
    return bytes(h) + b''.join(records) + b'\x1a'
