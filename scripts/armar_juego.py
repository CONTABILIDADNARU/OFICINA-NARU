"""Arma un juego de importación (.cab/.cue/.Ter/.FPT) para el proceso 746 de SIASoft,
usando como plantilla la exportación del propio programa (proceso 745)."""
import struct, os

def parse(d):
    n = struct.unpack('<I', d[4:8])[0]; hl, rl = struct.unpack('<HH', d[8:12])
    fs = {}; off = 32; pos = 1
    while d[off] != 0x0D:
        fs[d[off:off + 11].split(b'\0')[0].decode()] = (pos, d[off + 16], chr(d[off + 11]), d[off + 17]); pos += d[off + 16]; off += 32
    return n, hl, rl, fs

def recs(d):
    n, hl, rl, fs = parse(d)
    return [d[hl + i * rl: hl + (i + 1) * rl] for i in range(n)]

def get(r, fs, k):
    p, l = fs[k][0], fs[k][1]; return r[p:p + l].decode('latin1').strip()

def putc(r, fs, k, v):
    p, l = fs[k][0], fs[k][1]; return r[:p] + v.encode('latin1').ljust(l)[:l] + r[p + l:]

def putn(r, fs, k, v, dec=2):
    p, l = fs[k][0], fs[k][1]; s = f"{v:.{dec}f}"; assert len(s) <= l, (k, s)
    return r[:p] + s.rjust(l).encode('latin1') + r[p + l:]

def build(template_bytes, records):
    n, hl, rl, fs = parse(template_bytes)
    h = bytearray(template_bytes[:hl]); h[4:8] = struct.pack('<I', len(records))
    return bytes(h) + b''.join(records) + b'\x1a'

def juego(plantilla_dir, base, docs, ter_codes_plantilla, out_dir):
    """docs: lista de dict(trn, num, fec, factura, detalle, ter, des, lines=[dict(cta, base, deb, cre)])"""
    P = plantilla_dir + 'COOct312026'
    cab = open(P + '.cab', 'rb').read(); cue = open(P + '.cue', 'rb').read(); ter = open(P + '.Ter', 'rb').read(); fpt = open(P + '.FPT', 'rb').read()
    _, _, _, fc = parse(cab); _, _, _, fu = parse(cue); _, _, _, ft = parse(ter)
    tc = [r for r in recs(cab) if get(r, fc, 'NUM_TRN') == 'FC-000666'][0]
    tu = [r for r in recs(cue) if get(r, fu, 'NUM_TRN') == 'FC-000666'][0]
    out_cab, out_cue = [], []
    for d in docs:
        h = tc
        for k, v in (('ANO_DOC', d['fec'][:4]), ('PER_DOC', d['fec'][4:6]), ('COD_TRN', d['trn']), ('NUM_TRN', d['num']), ('FEC_DOC', d['fec']),
                     ('DETALLE', d.get('detalle', '')), ('FACTURA', d['factura']), ('FEC_VEN', d['fec'])):
            h = putc(h, fc, k, v)
        out_cab.append(h)
        for l in d['lines']:
            r = tu
            for k, v in (('ANO_DOC', d['fec'][:4]), ('PER_DOC', d['fec'][4:6]), ('COD_TRN', d['trn']), ('NUM_TRN', d['num']), ('COD_CTA', l['cta']),
                         ('COD_TER', d['ter']), ('DES_MOV', d['des'])):
                r = putc(r, fu, k, v)
            r = putn(r, fu, 'BAS_MOV', l['base']); r = putn(r, fu, 'DEB_MOV', l['deb']); r = putn(r, fu, 'CRE_MOV', l['cre'])
            out_cue.append(r)
    tr = [r for r in recs(ter) if get(r, ft, 'COD_TER') in ter_codes_plantilla]
    files = {base + '.cab': build(cab, out_cab), base + '.cue': build(cue, out_cue), base + '.Ter': build(ter, tr), base + '.FPT': fpt}
    os.makedirs(out_dir, exist_ok=True)
    for nm, data in files.items():
        open(out_dir + nm, 'wb').write(data)
    return files
