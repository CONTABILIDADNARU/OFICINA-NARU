import sys, re, math, os, json, struct
sys.path.insert(0, '.')
from dbf import load
from armar import parse, recs, get, putc, putn, build
import pandas as pd
from collections import Counter, defaultdict

SIA = '/mnt/user-data/outputs/EMP015_COPIA/CO.SIA/'
PK  = '/mnt/user-data/uploads/PAQUETE_ORIGINAL/'
OUT = '/mnt/user-data/outputs/TRADE_MARK_NOV2026/'
os.makedirs(OUT, exist_ok=True)
REP = '/mnt/user-data/attachments/a56b3c34-76ce-5750-aa94-2f09abf7e43b/982d5404-ENERO_-_NOVIEMBRE_2026.xlsx'
NIT = '901749655'
rh = lambda x: int(math.floor(x + 0.5 + 1e-9))
nt = lambda s: re.sub(r'\D', '', str(s)).lstrip('0')
tail = lambda n: int(re.search(r'(\d+)$', n).group(1)) if re.search(r'(\d+)$', n) else 0

_, cab, _ = load(SIA + 'cab_doc.dbf'); _, cue, _ = load(SIA + 'cue_doc.dbf'); _, ter, _ = load(SIA + 'mae_ter.dbf'); _, cta, _ = load(SIA + 'mae_cta.dbf')
CTA = {c['COD_CTA'] for c in cta}
TER = {nt(t['COD_TER']): t for t in ter}
cabk = {(c['ANO_DOC'], c['PER_DOC'], c['COD_TRN'], c['NUM_TRN']): c for c in cab}
lines = defaultdict(list)
for l in cue: lines[(l['ANO_DOC'], l['PER_DOC'], l['COD_TRN'], l['NUM_TRN'])].append(l)

TAXPFX = ('2408', '2365', '2367', '2368', '2370', '2205', '1105', '1110', '1120', '1355', '1305', '23', '24')
def roles_v(ls):
    ing = [l for l in ls if l['COD_CTA'].startswith('4') and l['CRE_MOV'] > 0]
    iva = [l for l in ls if l['COD_CTA'].startswith('2408') and l['CRE_MOV'] > 0]
    ret = [l for l in ls if l['COD_CTA'].startswith('1355')]
    cxc = [l for l in ls if l['COD_CTA'].startswith('1305') and l['DEB_MOV'] > 0]
    ok = len(ing) == 1 and len(cxc) == 1 and len(iva) <= 1 and len(ing) + len(iva) + len(ret) + len(cxc) == len(ls)
    return ok, ing, iva, ret, cxc
def roles_c(ls):
    exp = [l for l in ls if l['DEB_MOV'] > 0 and not l['COD_CTA'].startswith(TAXPFX)]
    iva = [l for l in ls if l['COD_CTA'].startswith('2408') and l['DEB_MOV'] > 0]
    ret = [l for l in ls if l['COD_CTA'].startswith(('2365', '2367', '2368')) and l['CRE_MOV'] > 0]
    ap = [l for l in ls if l['COD_CTA'].startswith(('2205', '1105')) and l['CRE_MOV'] > 0]
    ok = len(exp) == 1 and len(ap) == 1 and len(iva) <= 1 and len(exp) + len(iva) + len(ret) + len(ap) == len(ls)
    return ok, exp, iva, ret, ap

# ---------- historial por cliente (ventas) y proveedor (compras)
HV = defaultdict(list); HC = defaultdict(list)
for k, ls in lines.items():
    a, p, t, n = k; c = cabk.get(k)
    if not c or a not in ('2024', '2025', '2026'): continue
    key = (c['FEC_DOC'], tail(n))
    if t == '04':
        ok, ing, iva, ret, cxc = roles_v(ls)
        if ok: HV[nt(cxc[0]['COD_TER'])].append((key, k, c, ls))
    elif t in ('05', '18'):
        ok, exp, iva, ret, ap = roles_c(ls)
        if ok and ap[0]['COD_TER']: HC[nt(ap[0]['COD_TER'])].append((key, k, c, ls))
for h in list(HV.values()) + list(HC.values()): h.sort(key=lambda x: x[0])

def snap(r):
    for s in (0.00966, 0.01104, 0.00414, 0.00966):
        if abs(r - s) < 0.00003: return s
    return round(r, 5)

# ---------- predicción
def pred_venta(tpl_hist, base, iva, num, fec):
    """devuelve (lineas[(cta,cco,base,deb,cre,docref)], nivel, nota)"""
    _, k, c, ls = tpl_hist[-1]
    ok, ing, ivl, ret, cxc = roles_v(ls)
    nota = ''; nivel = 'alta'
    last = tpl_hist[-3:]
    sets = [frozenset(l['COD_CTA'] for l in x[3] if l['COD_CTA'].startswith('1355')) for x in last]
    if len(set(sets)) > 1: nivel = 'duda'; nota = 'las ultimas facturas del cliente no tienen las mismas retenciones'
    ingl = ing[0]; ivt = ivl[0] if ivl else None
    out = [(ingl['COD_CTA'], ingl['COD_CCO'], 0, 0, base, '')]
    if iva > 0:
        out.append((ivt['COD_CTA'] if ivt else '24080505', ivt['COD_CCO'] if ivt else '', base, 0, iva, ''))
    elif ivt: nota += ' | factura sin IVA aunque el cliente suele tenerlo'; nivel = 'duda'
    rsum = 0
    for r in ret:
        if r['COD_CTA'].startswith('135517'):
            rate = r['DEB_MOV'] / ivl[0]['CRE_MOV'] if ivl and ivl[0]['CRE_MOV'] else 0.15; amt = rh(iva * round(rate, 4))
        else:
            rate = snap(r['DEB_MOV'] / ingl['CRE_MOV'] if ingl['CRE_MOV'] else 0); amt = rh(base * rate)
        rsum += amt; out.append((r['COD_CTA'], r['COD_CCO'], base, amt, 0, ''))
    out.append((cxc[0]['COD_CTA'], cxc[0]['COD_CCO'], 0, base + iva - rsum, 0, num))
    des = cxc[0]['DES_MOV']
    return out, nivel, nota, des

def pred_compra(tpl_hist, tot, iva, otros, num, fec):
    _, k, c, ls = tpl_hist[-1]
    ok, exp, ivl, ret, ap = roles_c(ls)
    nota = ''; nivel = 'alta'
    sets = [frozenset(l['COD_CTA'] for l in x[3] if l['COD_CTA'].startswith(('2365', '2367', '2368')) and l['CRE_MOV'] > 0) for x in tpl_hist[-3:]]
    if len(set(sets)) > 1: nivel = 'duda'; nota = 'las ultimas compras del proveedor no tienen las mismas retenciones'
    if len({x[3] and roles_c(x[3])[1][0]['COD_CTA'] for x in tpl_hist[-3:]}) > 1: nivel = 'duda'; nota += ' | las ultimas compras usaron cuentas de gasto distintas'
    taxable = tot - iva - otros; gasto = tot - iva
    out = [(exp[0]['COD_CTA'], exp[0]['COD_CCO'], 0, gasto, 0, '', '')]
    if iva > 0:
        ratio = iva / taxable if taxable else 0
        if ivl:
            tr = ivl[0]['DEB_MOV'] / ivl[0]['BAS_MOV'] if ivl[0]['BAS_MOV'] else 0.19
            ic = ivl[0]['COD_CTA'] if abs(ratio - tr) < 0.003 else None
        else: ic = None
        if ic is None:
            if abs(ratio - 0.19) < 0.003: ic = '24081005'
            elif abs(ratio - 0.05) < 0.003: ic = '24081027'
            else: ic = ivl[0]['COD_CTA'] if ivl else '24081005'; nivel = 'duda'; nota += f' | IVA {ratio:.1%} sobre la base: tarifa atipica'
        out.append((ic, ivl[0]['COD_CCO'] if ivl else exp[0]['COD_CCO'], taxable, iva, 0, '', ''))
    elif ivl: nota += ' | sin IVA aunque el proveedor suele tenerlo'
    rsum = 0
    for r in ret:
        rate = snap(r['CRE_MOV'] / r['BAS_MOV']) if r['BAS_MOV'] else 0; amt = rh(taxable * rate); rsum += amt
        out.append((r['COD_CTA'], r['COD_CCO'], taxable, 0, amt, '', ''))
    out.append((ap[0]['COD_CTA'], ap[0]['COD_CCO'], 0, 0, tot - rsum, num, 'FAC'))
    return out, nivel, nota, exp[0]['DES_MOV']

# ---------- BACKTEST jul-sep (aprende solo lo anterior a cada documento)
def before(h, key): return [x for x in h if x[0] < key]
bt = {'ventas': Counter(), 'compras': Counter()}; bn = {'ventas': Counter(), 'compras': Counter()}; btv = {'ventas': [0, 0], 'compras': [0, 0]}; btfail = []
def norm(lst):
    d = defaultdict(lambda: [0, 0])
    for x in lst: d[x[0]][0] += x[3]; d[x[0]][1] += x[4]
    return d
for h_by, kind in ((HV, 'ventas'), (HC, 'compras')):
    for ter_, h in h_by.items():
        for i, (key, k, c, ls) in enumerate(h):
            if k[0] != '2026' or k[1] not in ('07', '08', '09'): continue
            hist = h[:i]
            if not hist: bt[kind]['sin historial'] += 1; continue
            if kind == 'ventas':
                ok, ing, ivl, ret, cxc = roles_v(ls); base = ing[0]['CRE_MOV']; iva = ivl[0]['CRE_MOV'] if ivl else 0
                pr, nivel, _, _ = pred_venta(hist, base, iva, k[3], c['FEC_DOC']); tot = base + iva
            else:
                ok, exp, ivl, ret, ap = roles_c(ls); iva = ivl[0]['DEB_MOV'] if ivl else 0; tot = exp[0]['DEB_MOV'] + iva
                pr, nivel, _, _ = pred_compra(hist, tot, iva, 0, k[3], c['FEC_DOC'])
            real = norm([(l['COD_CTA'], 0, 0, l['DEB_MOV'], l['CRE_MOV']) for l in ls]); prd = norm(pr)
            good = set(real) == set(prd) and all(abs(real[a][0] - prd[a][0]) <= 1 and abs(real[a][1] - prd[a][1]) <= 1 for a in real)
            bt[kind]['coincide' if good else 'difiere'] += 1; bn[kind][(nivel, good)] += 1
            btv[kind][0] += tot if good else 0; btv[kind][1] += tot
            if not good: btfail.append((kind, k[3], sorted(set(real) ^ set(prd))))
print('BACKTEST', {k: dict(v) for k, v in bt.items()}, '| ponderado por valor', {k: round(v[0] / v[1], 3) if v[1] else None for k, v in btv.items()})
print('POR NIVEL', {k: dict(v) for k, v in bn.items()}); print('fallos ejemplo', btfail[:6])

# ---------- REP
r = pd.read_excel(REP, dtype=str)
for kcol in ['IVA', 'INC', 'IC', 'ICA', 'Total', 'Rete Renta', 'Rete ICA', 'Rete IVA']: r[kcol] = pd.to_numeric(r[kcol], errors='coerce').fillna(0)
OTR = ['ICA', 'IC', 'INC']
t = r['Tipo de documento']
V = r[(r['NIT Emisor'] == NIT) & t.isin(['Factura electrónica', 'Nota de crédito electrónica', 'Nota de débito electrónica'])].copy()
V['num'] = V.apply(lambda x: ('NC-' + str(int(x.Folio)) if x['Tipo de documento'].startswith('Nota de cr') else (x.Prefijo + str(int(x.Folio)))), axis=1)
V['fec'] = pd.to_datetime(V['Fecha Emisión'], format='%d-%m-%Y').dt.strftime('%Y%m%d')
siav = {k[3] for k in cabk if k[2] in ('04', '08', '07')}
Vm = V[~V.num.isin(siav)].sort_values(['fec', 'num'])
print('ventas del REP sin contabilizar:', len(Vm))
C = pd.read_pickle('../clasif.pkl'); X = C[C.grp == 'C'].copy().sort_values(['fecha', 'doc'])
print('compras sin rastro:', len(X))

# ---------- consecutivos de compras
cps = [tail(k[3]) for k in cabk if k[2] == '05' and re.match(r'^CP-\d+$', k[3])]; cp = max(cps)
fcs = [tail(k[3]) for k in cabk if k[2] == '18' and re.match(r'^FC\.-\d+$', k[3])]; fc = max(fcs)
print('ultimo CP', cp, 'ultimo FC.-', fc)

# ---------- plantilla de importación
cb = open(PK + 'AGTCOMP1.cab', 'rb').read(); cu = open(PK + 'AGTCOMP1.cue', 'rb').read(); tb = open(PK + 'AGTCOMP1.Ter', 'rb').read(); fpt = open(PK + 'AGTCOMP1.FPT', 'rb').read()
_, _, _, fcab = parse(cb); _, _, _, fcue = parse(cu)
tc = recs(cb)[0]; tu = recs(cu)[0]
for k in ('OTRO_TER', 'DETALLE', 'FACTURA', 'FEC_POSF', 'COD_BAN', 'NUM_IMP', 'COD_VEN', 'FIN'): tc = putc(tc, fcab, k, '')
for k in ('COD_CIU', 'COD_SUC', 'COD_CCO', 'NUM_CHQ', 'DOC_MOV', 'DOC_CRUC', 'DOC_REF', 'ANO_REF', 'FEC_VENC', 'COD_CON', 'DES_MOV', 'COD_TER', 'INI'): tu = putc(tu, fcue, k, '')
for k in ('BAS_MOV', 'DEB_MOV', 'CRE_MOV', 'SALDO', 'SAL_DOC', 'VR_ABONO', 'VAL_ME'): tu = putn(tu, fcue, k, 0.0)
def mk_doc(trn, num, fec, factura='', vend=''):
    h = tc
    for k, v in (('ANO_DOC', fec[:4]), ('PER_DOC', fec[4:6]), ('COD_TRN', trn), ('NUM_TRN', num), ('FEC_DOC', fec), ('FEC_VEN', fec), ('FACTURA', factura), ('COD_VEN', vend)): h = putc(h, fcab, k, v)
    return h
def mk_line(trn, num, fec, cta_, cco, ter_, des, base, deb, cre, docref='', docmov='', doccruc='', anoref=''):
    x = tu
    for k, v in (('ANO_DOC', fec[:4]), ('PER_DOC', fec[4:6]), ('COD_TRN', trn), ('NUM_TRN', num), ('COD_CTA', cta_), ('COD_CCO', cco), ('COD_TER', ter_), ('DES_MOV', des), ('DOC_REF', docref), ('DOC_MOV', docmov), ('DOC_CRUC', doccruc), ('ANO_REF', anoref)): x = putc(x, fcue, k, v)
    x = putn(x, fcue, 'BAS_MOV', float(base)); x = putn(x, fcue, 'DEB_MOV', float(deb)); x = putn(x, fcue, 'CRE_MOV', float(cre))
    return x

dudas = []; ventas_docs = []; compras_docs = []; held = []
def duda(area, ref, nit_, nivel, det): dudas.append((area, ref, nit_, nivel, det))

# ---------- VENTAS
for x in Vm.itertuples():
    num = x.num; cl = nt(x._asdict()['_6'] if False else getattr(x, '_6', '')) if False else nt(r.loc[x.Index, 'NIT Receptor'])
    tipo = x._asdict()['_1'] if False else r.loc[x.Index, 'Tipo de documento']
    fec = x.fec; tot = rh(x.Total); iva = rh(x.IVA); base = tot - iva
    if tipo.startswith('Nota de d'):
        held.append(dict(area='Ventas', ref=num, nit=cl, fec=fec, total=tot, motivo='nota debito: no hay regla ni cuentas en el historial (la transaccion 07 no se usa en 2026)')); continue
    if tipo.startswith('Nota de cr'):
        held.append(dict(area='Ventas', ref=num, nit=cl, fec=fec, total=tot, motivo='nota credito de venta: el REP no indica la factura que afecta; definir factura origen')); continue
    if num == 'FVE43':
        held.append(dict(area='Ventas', ref=num, nit=cl, fec=fec, total=tot, motivo='Daniel (11-nov): revisar despues si lleva reteIVA 15% (previas: FE167 con reteIVA, FVE16 sin)')); continue
    if cl not in TER: duda('Ventas', num, cl, 'ALTA', 'cliente no existe en MAE_TER (falta 766)')
    h = HV.get(cl)
    if not h: held.append(dict(area='Ventas', ref=num, nit=cl, fec=fec, total=tot, motivo='cliente sin facturas de venta en el historial: definir cuentas y retenciones')); continue
    if iva and abs(iva - rh(base * 0.19)) > 1: duda('Ventas', num, cl, 'MEDIA', f'IVA {iva:,} no es 19% de la base {base:,}')
    ls_, nivel, nota, des0 = pred_venta(h, base, iva, num, fec)
    if nota: duda('Ventas', num, cl, 'MEDIA' if nivel != 'duda' else 'ALTA', nota)
    fac_t = h[-1][2]['FACTURA']
    m = re.match(r'^(\S+)\s+(\d+)\s*(.*)$', des0); concept = m.group(3) if m else ''
    des = (('FVE ' + str(int(num[3:]))) + (' ' + concept if concept else ''))[:50]
    lns = [mk_line('04', num, fec, a, cco, cl, des, b, d, c_, docref=dr) for (a, cco, b, d, c_, dr) in ls_]
    assert abs(sum(l_[3] for l_ in ls_) - sum(l_[4] for l_ in ls_)) < 1, num
    ventas_docs.append(dict(num=num, fec=fec, cl=cl, base=base, iva=iva, deb=ls_[-1][3], nivel=nivel, ctas=[l_[0] for l_ in ls_], h=mk_doc('04', num, fec, vend=h[-1][2]['COD_VEN']), ls=lns, raw=ls_))

# ---------- COMPRAS
for x in X.itertuples():
    row = r.loc[(r['CUFE/CUDE'] == C.loc[x.Index, 'CUFE/CUDE'])].iloc[0]
    tipo = row['Tipo de documento']; prov = x.tt; fec = x.fecha.strftime('%Y%m%d'); tot = rh(row.Total); iva = rh(row.IVA); otros = sum(row[k_] for k_ in OTR)
    ref = f"{row.Prefijo}-{row.Folio}" if isinstance(row.Prefijo, str) else str(row.Folio)
    if tipo != 'Factura electrónica':
        held.append(dict(area='Compras', ref=ref, nit=prov, fec=fec, total=tot, motivo=('nota credito de compra: el REP no indica la factura origen; escoger documento afectado' if 'crédito' in tipo else 'documento equivalente POS')))
        continue
    h = HC.get(prov)
    if prov not in TER: pass
    if not h:
        held.append(dict(area='Compras', ref=ref, nit=prov, fec=fec, total=tot, motivo='proveedor sin compras previas en el historial: definir cuenta de gasto' + ('' if prov in TER else ' y crear tercero (766)'))); continue
    trn = h[-1][1][2]
    if trn == '05': cp += 1; num = f'CP-{cp}'
    else: fc += 1; num = f'FC.-{fc}'
    ls_, nivel, nota, des0 = pred_compra(h, tot, iva, otros, num, fec)
    fol = re.sub(r'\D', '', str(row.Folio)); fac = ('FC ' + (fol[-7:] if len(fol) > 7 else fol))
    if len(fol) > 7: duda('Compras', f'{ref} ({num})', prov, 'MEDIA', f'folio de {len(fol)} digitos; FACTURA quedo {fac}')
    if nota: duda('Compras', f'{ref} ({num})', prov, 'ALTA' if nivel == 'duda' else 'MEDIA', nota)
    if otros: duda('Compras', f'{ref} ({num})', prov, 'INFO', f'impuestos distintos al IVA por {otros:,.0f}; sumados al gasto (regla de Daniel)')
    if row['Forma de Pago'] == '1' and h[-1][3] and h[-1][3][-1]['COD_CTA'].startswith('2205') is False: pass
    if iva == 0 and any(l_[0].startswith('2408') for l_ in ls_): pass
    # concepto del proveedor
    ft = h[-1][2]['FACTURA']; d0 = des0
    concept = d0[len(ft):].strip() if ft and d0.upper().startswith(ft.upper()) else re.sub(r'^\S+\s+\S+\s*', '', d0)
    des = (fac + (' ' + concept if concept else ''))[:50]
    lns = []
    for (a, cco, b, d, c_, dr, kind) in ls_:
        lns.append(mk_line(trn, num, fec, a, cco, prov, des, b, d, c_, docref=(num if kind == 'FAC' else ''), docmov=(fac if kind == 'FAC' else '')))
    assert abs(sum(l_[3] for l_ in ls_) - sum(l_[4] for l_ in ls_)) < 1, num
    for l_ in ls_:
        if l_[0] not in CTA: duda('Compras', f'{ref} ({num})', prov, 'ALTA', f'cuenta {l_[0]} no existe en MAE_CTA')
    compras_docs.append(dict(num=num, trn=trn, ref=ref, fec=fec, prov=prov, tot=tot, iva=iva, acc=ls_[0][0], nivel=nivel, fac=fac, h=mk_doc(trn, num, fec, factura=fac), ls=lns, raw=ls_))
for d in ventas_docs:
    for a in d['ctas']:
        if a not in CTA: duda('Ventas', d['num'], d['cl'], 'ALTA', f'cuenta {a} no existe en MAE_CTA')


# ---------- NOTAS CREDITO de venta: espejo de la factura que anulan (mismo cliente y mismo total)
byN = {d['num']: d for d in ventas_docs}
still = []; nc_docs = []
for hd in held:
    if hd['area'] == 'Ventas' and hd['ref'].startswith('NC-'):
        row = V[V.num == hd['ref']].iloc[0]; cl = hd['nit']
        cand = V[(V['NIT Receptor'].map(nt) == cl) & (V['Tipo de documento'] == 'Factura electrónica') & (V.Total.round(0) == round(row.Total)) & (V.fec <= row.fec)].sort_values('fec')
        part = None
        for pn in cand.num[::-1]:
            if pn in byN: part = byN[pn]; break
        if part is None: still.append(hd); continue
        n = hd['ref']; fec = hd['fec']; nn = int(n[3:]); pn_ = int(part['num'][3:])
        des = f'NCCL {nn} DV FVE {pn_}'[:50]
        ing = part['raw'][0]; iv = [x for x in part['raw'] if x[0].startswith('2408')]; rets = [x for x in part['raw'][1:-1] if x[0].startswith('1355')]; cx = part['raw'][-1]
        tot = part['base'] + part['iva']
        ls_ = [('417510', ing[1], 0, part['base'], 0, '', '', '')]
        if iv: ls_.append(('24080510', iv[0][1], part['base'], part['iva'], 0, '', '', ''))
        for rr in rets: ls_.append((rr[0], rr[1], part['base'], 0, rr[3], '', '', ''))
        ls_.append((cx[0], '01', 0, 0, cx[3], part['num'], part['num'], part['fec']))
        assert abs(sum(x[3] for x in ls_) - sum(x[4] for x in ls_)) < 1, n
        lns = [mk_line('08', n, fec, a, cco, cl, des, b, d, c_, docref=dr, doccruc=dc, anoref=ar) for (a, cco, b, d, c_, dr, dc, ar) in ls_]
        nc_docs.append(dict(num=n, fec=fec, cl=cl, base=part['base'], iva=part['iva'], deb=0, nivel='alta', ctas=[x[0] for x in ls_], h=putc(mk_doc('08', n, fec, factura=f'NCCL {nn}'), fcab, 'COD_VEN', ''), ls=lns, raw=ls_, partner=part['num'], neg=True))
        duda('Ventas', n, cl, 'MEDIA', f'nota credito generada como espejo total de {part["num"]} (mismo cliente y mismo total); confirmar que es la factura que anula')
    else: still.append(hd)
held = still
for hd in [h_ for h_ in held if h_['area'] == 'Ventas' and h_['ref'] in ('NC-56', 'ND1')]:
    held.remove(hd); n = hd['ref']; fec = hd['fec']; cl = hd['nit']; tot = hd['total']
    if n == 'NC-56':
        ls_ = [('417510', '', 0, tot, 0, '', '', ''), ('13050505', '01', 0, 0, tot, '', '', '')]
        des = 'NCCL 56 SIN IVA'; trn = 'NC' ; hdr = putc(mk_doc('08', n, fec, factura='NCCL 56'), fcab, 'COD_VEN', ''); trn = '08'
    else:
        ls_ = [('417510', '', 0, 0, tot, '', '', ''), ('13050505', '', 0, tot, 0, n, '', '')]
        des = 'ND 1 SIN IVA'; hdr = mk_doc('04', n, fec, vend='01'); trn = '04'
    lns = [mk_line(trn, n, fec, a_, cco, cl, des, b_, d_, c_, docref=dr, doccruc=dc, anoref=ar) for (a_, cco, b_, d_, c_, dr, dc, ar) in ls_]
    nc_docs.append(dict(num=n, fec=fec, cl=cl, base=tot, iva=0, deb=0, nivel='duda', ctas=[x[0] for x in ls_], h=hdr, ls=lns, raw=ls_, partner='', neg=(n == 'NC-56')))
    duda('Ventas', n, cl, 'ALTA', 'por decision de Daniel se contabiliza; estructura minima sin IVA ni retenciones (NC56 DEB 417510 / CRE clientes; ND1 DEB clientes / CRE 417510, como transaccion 04). NC56 sin factura cruzada. Revisar retenciones y cruce con FVE49')
ventas_all = ventas_docs + nc_docs
print('NC de venta generadas:', len(nc_docs))

# ---------- archivos: ALTA y DUDA separados
files = {}
def put(prefix, docs):
    if not docs: return
    files[prefix + '.cab'] = build(cb, [d['h'] for d in docs]); files[prefix + '.cue'] = build(cu, [l for d in docs for l in d['ls']]); files[prefix + '.Ter'] = build(tb, []); files[prefix + '.FPT'] = fpt
FILEMAP = {}
def assign(docs, kind):
    for d in docs:
        mm = d['fec'][4:6]
        suf = 'EA' if (kind == 'COM' and mm < '10') else mm
        pref = ('TMKVT' if kind == 'VTA' else 'TMKCO') + ('A' if d['nivel'] == 'alta' else 'D') + suf if False else None
        base = {'VTA': 'TMKV', 'COM': 'TMKC'}[kind] + ('A' if d['nivel'] == 'alta' else 'D') + suf
        d['archivo'] = base; FILEMAP.setdefault(base, []).append(d)
assign(sorted(ventas_all, key=lambda d: (d['fec'], d['num'])), 'VTA'); assign(compras_docs, 'COM')
for k_, docs in FILEMAP.items(): put(k_, docs)
print({k_: len(v) for k_, v in FILEMAP.items()})

# ---------- terceros nuevos para todos los que aparecen (generados o retenidos)
need = {}
for d in ventas_all:
    if d['cl'] not in TER: need[d['cl']] = r.loc[r['NIT Receptor'].map(nt) == d['cl'], 'Nombre Receptor'].iloc[0]
for d in compras_docs:
    if d['prov'] not in TER: need[d['prov']] = r.loc[r['NIT Emisor'].map(nt) == d['prov'], 'Nombre Emisor'].iloc[0]
for hd in held:
    if hd['nit'] not in TER and hd['nit'] != NIT:
        col = ('NIT Receptor', 'Nombre Receptor') if hd['area'] == 'Ventas' else ('NIT Emisor', 'Nombre Emisor')
        m_ = r.loc[r[col[0]].map(nt) == hd['nit'], col[1]]
        if len(m_): need[hd['nit']] = m_.iloc[0]
T0 = open(PK + 'TERVTAORI.DBF', 'rb').read(); TF = open(PK + 'TERVTAORI.FPT', 'rb').read(); _, thl, _, ft = parse(T0); tmpl = recs(T0)[0]
supl = set()
for (a, p, t_, n), ls in lines.items():
    if t_ in ('05', '18'):
        for l in ls:
            if l['COD_TER']: supl.add(nt(l['COD_TER']))
supl &= set(TER)
FLAGS = [k_ for k_ in ft if k_ in ('TIP_PRV','CLASIFIC','IND_RETE','IND_RET','AUT_RET','COD_ACT','COD_CLA','ESTADO','JURID','IND_CRED','IND_COBRO','MAYMIN','CIUDAD','COD_CIU','DPTO','MUN','COD_ACTIV','PAIS','COD_PAIS','CONTA','DEPA','IND_CREE','BLOQUEO','POR_ICA','INT_MORA','DIA_PLAZ','POR_DES')]
modes = {}
recent = sorted(ter, key=lambda x: x['FEC_ING'])[-30:]
for k_ in FLAGS:
    cnt = Counter(str(int(x[k_])) if isinstance(x.get(k_), float) else str(x.get(k_)) for x in recent if k_ in x and not isinstance(x.get(k_), bytes))
    if cnt and cnt.most_common(1)[0][0] != '': modes[k_] = cnt.most_common(1)[0][0]
print('modelo = 30 terceros mas recientes | campos por moda:', modes)
def dv(n_):
    w = [3,7,13,17,19,23,29,37,41,43,47,53,59,67,71]; s_ = sum(int(c_) * w[i_] for i_, c_ in enumerate(reversed(n_))); r_ = s_ % 11
    return str(r_ if r_ < 2 else 11 - r_)
EMP = re.compile(r'\b(S\.?A\.?S\.?|LTDA|S\.?A\.?|S\.? ?EN ?C|E\.?U\.?|FUNDACION|CORPORACION|ASOCIACION|COLEGIO|CLUB|GRUPO|COMPA|INVERSIONES|SOLUCIONES|SERVICIOS|PUBLICIDAD|IMPORT|COMERCIALIZ|PRODUCCIONES|AGENCIA|CIA)\b', re.I)
trows = []; tinfo = []
for n_, nm in sorted(need.items()):
    nm = re.sub(r'\s+', ' ', str(nm).strip()).upper()
    jur = bool(EMP.search(nm)) or (len(n_) == 9 and n_[0] in '89'); tdoc = '31' if (len(n_) == 9 and n_[0] in '89') else '13'
    rr = tmpl
    for k_, v_ in modes.items():
        if k_ in ft and ft[k_][2] == 'C': rr = putc(rr, ft, k_, v_)
        elif k_ in ft and ft[k_][2] == 'N': rr = putn(rr, ft, k_, float(v_), ft[k_][3])
    for k_ in ('NOM_TER', 'RAZ', 'REPRES'): rr = putc(rr, ft, k_, nm)
    for k_, v_ in (('COD_TER', n_), ('DV', dv(n_)), ('TDOC', tdoc), ('DIR1', ''), ('DIR', ''), ('TEL1', ''), ('EMAIL', ''), ('FEC_ING', '20261111'), ('TIP_PERS', '2' if jur else '1'), ('NOM1', ''), ('NOM2', ''), ('APL1', ''), ('APL2', '')):
        if k_ in ft: rr = putc(rr, ft, k_, v_)
    nota = ''
    if not jur:
        t2 = nm.split()
        a_ = (t2[0], '', t2[1], '') if len(t2) == 2 else (t2[0], '', t2[1], t2[2]) if len(t2) == 3 else tuple(t2) if len(t2) == 4 else (t2[0], '', t2[-1], '')
        for k_, v_ in zip(('NOM1', 'NOM2', 'APL1', 'APL2'), a_): rr = putc(rr, ft, k_, v_)
        nota = f'persona natural: nombre separado asumiendo {len(t2)} palabras'
    trows.append(rr); tinfo.append((n_, dv(n_), tdoc, 'juridica' if jur else 'natural', nota))
th = bytearray(T0[:thl]); th[4:8] = struct.pack('<I', len(trows))
files['TERTMK11.DBF'] = bytes(th) + b''.join(trows) + b'\x1a'; files['TERTMK11.FPT'] = TF
for nm_, data in files.items(): open(OUT + nm_, 'wb').write(data)
import pickle
pickle.dump(dict(ventas=ventas_all, compras=compras_docs, need=tinfo, held=held, dudas=dudas, bt=(bt, bn, btv, btfail), filemap={k_: [d['num'] for d in v] for k_, v in FILEMAP.items()}), open('res.pkl', 'wb'))
print('terceros nuevos (766):', len(trows))
print('VENTAS', len(ventas_all), 'FVE base', sum(d['base'] for d in ventas_docs), 'iva', sum(d['iva'] for d in ventas_docs))
print('COMPRAS', len(compras_docs), 'total', sum(d['tot'] for d in compras_docs), 'iva', sum(d['iva'] for d in compras_docs), Counter(d['nivel'] for d in compras_docs))
print('RETENIDAS', len(held), Counter((h_['area'], h_['motivo'][:40]) for h_ in held)); print('DUDAS', Counter((d_[0], d_[3]) for d_ in dudas))
