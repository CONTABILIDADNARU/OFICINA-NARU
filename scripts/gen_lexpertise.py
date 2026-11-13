import sys, re, math, os, json, struct
sys.path.insert(0, 'lib')
from dbf import load
from armar import parse, recs, get, putc, putn, build
import openpyxl
from collections import Counter, defaultdict

BASE = '/mnt/user-data/uploads/SIASOFT_V23/EMPRESAS/EMP041/CO.SIA/'
PK = '/mnt/user-data/uploads/PAQUETE_ORIGINAL/'
REP = '/mnt/user-data/attachments/11e2aa9b-c6b3-57ef-a158-74eb6fbcd043/12c07703-4299a805-cf50-419a-9cdd-653f363388c2.xlsx'
OUT = '/mnt/user-data/outputs/LEXPERTISE_OCT2026/'
os.makedirs(OUT, exist_ok=True)
rh = lambda x: int(math.floor(x + 0.5 + 1e-9))
nit = lambda s: str(int(float(s))) if isinstance(s, (int, float)) else str(s).strip().lstrip('0')
f = lambda v: float(v or 0)
def fecha(s): d, m, y = s.split('-'); return y + m + d

_, cab, _ = load(BASE + 'cab_doc.dbf'); _, cue, _ = load(BASE + 'cue_doc.dbf'); _, ter, _ = load(BASE + 'mae_ter.dbf')
TER = {t['COD_TER'].lstrip('0'): t for t in ter}
cabk = {(c['ANO_DOC'], c['PER_DOC'], c['COD_TRN'], c['NUM_TRN']): c for c in cab}
lines = defaultdict(list)
for l in cue: lines[(l['ANO_DOC'], l['PER_DOC'], l['COD_TRN'], l['NUM_TRN'])].append(l)

ws = openpyxl.load_workbook(REP, read_only=True, data_only=True).worksheets[0]
rows = list(ws.iter_rows(values_only=True)); H = rows[0]
R = [dict(zip(H, r)) for r in rows[1:] if r[0]]
com = [r for r in R if r['Grupo'] == 'Recibido' and r['Tipo de documento'] == 'Factura electrónica']
nomina = [r for r in R if r['Grupo'] == 'Emitido']
ventas = [r for r in R if r['Grupo'] == 'Emitido' and r['Tipo de documento'] == 'Factura electrónica']
print('REP: compras', len(com), '| ventas', len(ventas), '| nominas excluidas', len(nomina))
dudas = []
def duda(area, ref, n, nivel, det): dudas.append((area, ref, n, nivel, det))

cb = open(PK + 'AGTCOMP1.cab', 'rb').read(); cu = bytearray(open(PK + 'AGTCOMP1.cue', 'rb').read()); tb = open(PK + 'AGTCOMP1.Ter', 'rb').read(); fpt = open(PK + 'AGTCOMP1.FPT', 'rb').read()
cu[28] = 0   # leccion NARU: sin marca de CDX estructural
cu = bytes(cu)
_, _, _, fc = parse(cb); _, _, _, fu = parse(cu)
tc = recs(cb)[0]; tu = recs(cu)[0]
for k in ('OTRO_TER', 'DETALLE', 'FACTURA', 'FEC_POSF', 'COD_BAN', 'NUM_IMP', 'COD_VEN', 'FIN'): tc = putc(tc, fc, k, '')
for k in ('COD_CIU', 'COD_SUC', 'COD_CCO', 'NUM_CHQ', 'DOC_MOV', 'DOC_CRUC', 'DOC_REF', 'FEC_VENC', 'COD_CON', 'DES_MOV', 'COD_TER'): tu = putc(tu, fu, k, '')
def mk_doc(trn, num, fec, factura='', detalle=''):
    h = tc
    for k, v in (('ANO_DOC', fec[:4]), ('PER_DOC', fec[4:6]), ('COD_TRN', trn), ('NUM_TRN', num), ('FEC_DOC', fec), ('FEC_VEN', fec), ('FACTURA', factura), ('DETALLE', detalle)):
        h = putc(h, fc, k, v)
    return h
def mk_line(trn, num, fec, cta, ter_, des, base, deb, cre):
    r = tu
    for k, v in (('ANO_DOC', fec[:4]), ('PER_DOC', fec[4:6]), ('COD_TRN', trn), ('NUM_TRN', num), ('COD_CTA', cta), ('COD_TER', ter_), ('DES_MOV', des)):
        r = putc(r, fu, k, v)
    r = putn(r, fu, 'BAS_MOV', float(base)); r = putn(r, fu, 'DEB_MOV', float(deb)); r = putn(r, fu, 'CRE_MOV', float(cre))
    return r

# decisiones de Daniel (3-nov-2026): proveedor nuevo 901013514 -> 529520 'GASTOS DE REPRESENTACION'; caja 11050505; sin retencion (base < 27 UVT = 1.414.098)
CUENTA = {'901013514': ('529520', 'GASTOS DE REPRESENTACION')}
MIN_COMPRAS = 27 * 52374
cp = max(int(m.group(1)) for (a, p, t, n) in cabk if a == '2026' and t == '05' for m in [re.match(r'^CP-(\d+)$', n)] if m)
cm = []
for x in sorted(com, key=lambda r: (fecha(r['Fecha Emisión']), int(r['Folio']))):
    prov = nit(x['NIT Emisor']); fec = fecha(x['Fecha Emisión']); ref = f"{x['Prefijo']}-{x['Folio']}"
    cp += 1; num = f'CP-{cp}'
    if ('2026', fec[4:6], '05', num) in cabk: duda('Compras', ref, prov, 'ALTA', f'{num} ya existe'); continue
    tot_rep = f(x['Total']); iva_rep = f(x['IVA'])
    tot = rh(tot_rep); iva = rh(iva_rep); gasto = tot - iva; base = tot_rep - iva_rep
    if prov not in CUENTA: duda('Compras', ref, prov, 'ALTA', 'proveedor sin cuenta definida'); continue
    acc, detalle = CUENTA[prov]
    ratio = iva_rep / base
    if abs(ratio - 0.19) > 0.003: duda('Compras', ref, prov, 'ALTA', f'IVA {ratio:.1%} sobre la base')
    if abs(iva - iva_rep) > 1 or abs(tot - tot_rep) > 1: duda('Compras', ref, prov, 'ALTA', 'desfase contra REP mayor al redondeo')
    if base >= MIN_COMPRAS: duda('Compras', ref, prov, 'ALTA', f'base {base:,.0f} supera el minimo de retefuente por compras {MIN_COMPRAS:,}')
    fac = 'FC' + str(int(x['Folio']))
    des = (fac + ' ' + detalle)[:50]
    ls_ = [mk_line('05', num, fec, acc, prov, des, 0, gasto, 0),
           mk_line('05', num, fec, '24081005', prov, des, gasto, iva, 0),
           mk_line('05', num, fec, '11050505', prov, des, 0, 0, tot)]
    cm.append(dict(num=num, ref=ref, fec=fec, prov=prov, tot_rep=tot_rep, iva_rep=iva_rep, tot=tot, iva=iva, gasto=gasto, base_rep=round(base, 2), acc=acc, fac=fac, detalle=detalle, h=mk_doc('05', num, fec, fac, detalle), ls=ls_))
files = {'LEXCOM10.cab': build(cb, [d['h'] for d in cm]), 'LEXCOM10.cue': build(cu, [l for d in cm for l in d['ls']]), 'LEXCOM10.Ter': build(tb, []), 'LEXCOM10.FPT': fpt}

# ---- terceros nuevos (766)
T0 = open(PK + 'TERVTAORI.DBF', 'rb').read(); TF = open(PK + 'TERVTAORI.FPT', 'rb').read(); _, thl, _, ft = parse(T0); tmpl = recs(T0)[0]
sup = set()
for (a, p, t, n), ls in lines.items():
    if t == '05':
        for l in ls:
            if l['COD_TER']: sup.add(l['COD_TER'].lstrip('0'))
sup &= set(TER)
FLAGS = [k for k in ft if k in ('TIP_PRV','CLASIFIC','IND_RETE','IND_RET','AUT_RET','COD_ACT','COD_CLA','ESTADO','JURID','IND_CRED','IND_COBRO','MAYMIN','CIUDAD','COD_CIU','DPTO','MUN','COD_ACTIV','REGIMEN','RESPON','PAIS','COD_PAIS','CONTA','DEPA','IND_CREE','BLOQUEO','POR_ICA','INT_MORA','DIA_PLAZ','POR_DES')]
modes = {}
for k in FLAGS:
    cnt = Counter(str(TER[n][k]) for n in sup if k in TER[n])
    if cnt:
        v, c = cnt.most_common(1)[0]
        if c / len(sup) >= 0.6: modes[k] = v
print('proveedores existentes modelo:', len(sup), '| campos por moda:', modes)
def dv(n):
    w = [3,7,13,17,19,23,29,37,41,43,47,53,59,67,71]; s = sum(int(c) * w[i] for i, c in enumerate(reversed(n))); r = s % 11
    return str(r if r < 2 else 11 - r)
nuevos = {}
for x in com:
    n = nit(x['NIT Emisor'])
    if n not in TER: nuevos[n] = re.sub(r'\s+', ' ', str(x['Nombre Emisor']).strip()).upper()
trows = []
for n, nm in sorted(nuevos.items()):
    jur = len(n) == 9 and n[0] in '89'; tdoc = '31' if jur else '13'
    r = tmpl
    for k, v in modes.items():
        if k in ft and ft[k][2] == 'C': r = putc(r, ft, k, v)
        elif k in ft and ft[k][2] == 'N': r = putn(r, ft, k, float(v), ft[k][3])
    for k in ('NOM_TER', 'RAZ', 'REPRES'): r = putc(r, ft, k, nm)
    for k, v in (('COD_TER', n), ('DV', dv(n)), ('TDOC', tdoc), ('DIR1', ''), ('DIR', ''), ('TEL1', ''), ('EMAIL', ''), ('FEC_ING', '20261103'), ('TIP_PERS', '2' if jur else '1'), ('NOM1', ''), ('NOM2', ''), ('APL1', ''), ('APL2', '')):
        if k in ft: r = putc(r, ft, k, v)
    trows.append(r)
    duda('Terceros', n, n, 'INFO', f'tercero nuevo (DV {dv(n)}), sin direccion ni telefono: completar a mano si hace falta')
th = bytearray(T0[:thl]); th[4:8] = struct.pack('<I', len(trows))
files['TERLEX10.DBF'] = bytes(th) + b''.join(trows) + b'\x1a'; files['TERLEX10.FPT'] = TF
duda('REP', 'Nomina electronica', '', 'INFO', f'{len(nomina)} nominas NOLX excluidas (fuera de alcance)')
duda('REP', 'Ventas', '', 'INFO', 'sin ventas en octubre (confirmado por Daniel)')
for nm_, data in files.items(): open(OUT + nm_, 'wb').write(data)

# ---- verificacion de lo generado leyendo los archivos escritos
_, _, _, _ = parse(files['LEXCOM10.cab'])
gc = recs(files['LEXCOM10.cab']); gu = recs(files['LEXCOM10.cue'])
D = sum(float(get(r, fu, 'DEB_MOV')) for r in gu); C = sum(float(get(r, fu, 'CRE_MOV')) for r in gu)
print('docs', len(gc), 'lineas', len(gu), 'D', D, 'C', C, 'D=C', abs(D - C) < 0.005)
for d in cm:
    dd = sum(float(get(r, fu, 'DEB_MOV')) for r in gu if get(r, fu, 'NUM_TRN') == d['num']); cc = sum(float(get(r, fu, 'CRE_MOV')) for r in gu if get(r, fu, 'NUM_TRN') == d['num'])
    print(d['num'], d['ref'], d['fec'], d['fac'], 'total REP', d['tot_rep'], 'total', d['tot'], 'IVA REP', d['iva_rep'], 'IVA', d['iva'], 'gasto', d['gasto'], 'D=C', dd == cc, 'base REP', d['base_rep'], '<', MIN_COMPRAS)
print('suma total', sum(d['tot'] for d in cm), 'suma IVA', sum(d['iva'] for d in cm), 'REP total', round(sum(d['tot_rep'] for d in cm), 2), 'REP IVA', round(sum(d['iva_rep'] for d in cm), 2))
print('terceros nuevos', len(trows), '| byte28 cue', files['LEXCOM10.cue'][28], 'cab', files['LEXCOM10.cab'][28])
print('DUDAS', Counter((d[0], d[3]) for d in dudas))
json.dump(dict(dudas=dudas, compras=[{k: v for k, v in d.items() if k not in ('h', 'ls')} for d in cm]), open('resultado_lex.json', 'w'), default=list)

# ---- revision xlsx
wb = openpyxl.Workbook(); s = wb.active; s.title = 'Compras'
s.append(['Doc', 'REP', 'Fecha', 'Tercero', 'Cuenta', 'Linea', 'Debito', 'Credito', 'Base'])
for d in cm:
    for r in recs(files['LEXCOM10.cue']):
        if get(r, fu, 'NUM_TRN') == d['num']:
            s.append([d['num'], d['ref'], d['fec'], d['prov'], get(r, fu, 'COD_CTA'), get(r, fu, 'DES_MOV'), float(get(r, fu, 'DEB_MOV')), float(get(r, fu, 'CRE_MOV')), float(get(r, fu, 'BAS_MOV'))])
s2 = wb.create_sheet('Dudas'); s2.append(['Area', 'Referencia', 'NIT', 'Nivel', 'Detalle'])
for d in dudas: s2.append(list(d))
wb.save(OUT + 'REVISION_LEXPERTISE_OCT2026.xlsx')
