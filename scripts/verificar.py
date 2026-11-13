"""Verificación de SOLO LECTURA de una importación en SIASoft (no escribe nada).
Uso (en el computador donde está SIASoft, con python3):
    python3 verificar.py "<ruta a EMPRESAS/EMP010/CO.SIA>" 2026 10
Revisa: documentos por tipo, débitos = créditos, terceros huérfanos, llaves repetidas y acumulados RES_CTA / RES_TER
contra las líneas de CUE_DOC del período. Solo lee DBF."""
import struct, sys, collections, os
ruta, ano, per = sys.argv[1], sys.argv[2], sys.argv[3]
def load(p, cols):
    d = open(os.path.join(ruta, p), 'rb').read(); n = struct.unpack('<I', d[4:8])[0]; hl, rl = struct.unpack('<HH', d[8:12]); fs = {}; off = 32; pos = 1
    while d[off] != 0x0D:
        nm = d[off:off + 11].split(b'\0')[0].decode(); fs[nm] = (pos, d[off + 16], chr(d[off + 11])); pos += d[off + 16]; off += 32
    out = []
    for i in range(n):
        r = d[hl + i * rl:hl + (i + 1) * rl]
        if r[:1] == b'*': continue
        row = {}
        for c in cols:
            p0, l, t = fs[c]; v = r[p0:p0 + l].decode('latin1').strip(); row[c] = (float(v) if v else 0.0) if t == 'N' else v
        out.append(row)
    return out
cab = load('CAB_DOC.DBF', ['ANO_DOC', 'PER_DOC', 'COD_TRN', 'NUM_TRN']); cue = load('CUE_DOC.DBF', ['ANO_DOC', 'PER_DOC', 'COD_TRN', 'NUM_TRN', 'COD_CTA', 'COD_TER', 'DEB_MOV', 'CRE_MOV'])
rc = load('RES_CTA.DBF', ['ANO_ACU', 'COD_CTA', 'DEB_' + per, 'CRE_' + per]); rt = load('RES_TER.DBF', ['ANO_ACU', 'COD_CTA', 'COD_TER', 'DEB_' + per, 'CRE_' + per])
m = {r['COD_TER'] for r in load('MAE_TER.DBF', ['COD_TER'])}
h = [x for x in cab if (x['ANO_DOC'], x['PER_DOC']) == (ano, per)]
print('Documentos del período por tipo:', dict(collections.Counter(x['COD_TRN'] for x in h)))
print('Llaves repetidas:', len(h) - len({(x['COD_TRN'], x['NUM_TRN']) for x in h}))
l = [x for x in cue if (x['ANO_DOC'], x['PER_DOC']) == (ano, per)]
print('Líneas:', len(l), '| débitos', round(sum(x['DEB_MOV'] for x in l)), '| créditos', round(sum(x['CRE_MOV'] for x in l)))
print('Terceros de líneas fuera del maestro (período):', sorted({x['COD_TER'] for x in l if x['COD_TER']} - m))
A = collections.defaultdict(lambda: [0, 0]); T = collections.defaultdict(lambda: [0, 0])
for x in l:
    A[x['COD_CTA']][0] += x['DEB_MOV']; A[x['COD_CTA']][1] += x['CRE_MOV']
    if x['COD_TER']: T[(x['COD_CTA'], x['COD_TER'])][0] += x['DEB_MOV']; T[(x['COD_CTA'], x['COD_TER'])][1] += x['CRE_MOV']
sa = collections.defaultdict(lambda: [0, 0])
for r in rc:
    if r['ANO_ACU'] == ano: sa[r['COD_CTA']][0] += r['DEB_' + per]; sa[r['COD_CTA']][1] += r['CRE_' + per]
st = collections.defaultdict(lambda: [0, 0])
for r in rt:
    if r['ANO_ACU'] == ano: st[(r['COD_CTA'], r['COD_TER'])][0] += r['DEB_' + per]; st[(r['COD_CTA'], r['COD_TER'])][1] += r['CRE_' + per]
bad = [c for c in A if abs(sa[c][0] - A[c][0]) > 1 or abs(sa[c][1] - A[c][1]) > 1]
badt = [k for k in T if abs(st[k][0] - T[k][0]) > 1 or abs(st[k][1] - T[k][1]) > 1]
print('Cuentas con acumulado desfasado (RES_CTA):', len(bad), bad[:10], '-> si hay desfases, falta correr el proceso 150')
print('Pares cuenta-tercero desfasados (RES_TER):', len(badt), badt[:10])
