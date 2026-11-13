import sys, re, math, os, json, struct, glob
sys.path.insert(0, '.')
from dbf import load
from armar import parse, recs, get, putc, putn, build
import openpyxl
from collections import Counter, defaultdict

BASE = '/mnt/user-data/uploads/PAQUETE_ORIGINAL/RUMASA_OCT2026/CO.SIA/'
PK = '/mnt/user-data/uploads/PAQUETE_ORIGINAL/'
REP = glob.glob('/mnt/user-data/attachments/*/*DIAN*.xlsx')[0]
OUT = '/mnt/user-data/outputs/RUMASA_OCT2026/'
os.makedirs(OUT, exist_ok=True)
rh = lambda x: int(math.floor(x + 0.5 + 1e-9))
nit = lambda s: str(int(float(s))) if isinstance(s, (int, float)) else re.sub(r'[\s.\-]', '', str(s)).lstrip('0')
idx = lambda a, p: int(a) * 12 + int(p)
numk = lambda n: int(re.search(r'(\d+)$', n).group(1)) if re.search(r'(\d+)$', n) else 0

_, cab, _ = load(BASE + 'CAB_DOC.DBF'); _, cue, _ = load(BASE + 'CUE_DOC.DBF'); _, ter, _ = load(BASE + 'MAE_TER.DBF')
TER = {t['COD_TER'].lstrip('0'): t for t in ter}
cabk = {(c['ANO_DOC'], c['PER_DOC'], c['COD_TRN'], c['NUM_TRN']): c for c in cab}
lines = defaultdict(list)
for l in cue: lines[(l['ANO_DOC'], l['PER_DOC'], l['COD_TRN'], l['NUM_TRN'])].append(l)
exists = lambda trn, num: any(k[2] == trn and k[3] == num for k in cabk)

# ---------------- REP
ws = openpyxl.load_workbook(REP, read_only=True, data_only=True).worksheets[0]
rows = list(ws.iter_rows(values_only=True)); H = rows[0]
R = [dict(zip(H, r)) for r in rows[1:] if r[0]]
f = lambda v: float(v or 0)
def fecha(s): d, m, y = s.split('-'); return y + m + d
tipo = lambda r: str(r['Tipo de documento']).lower()
ven = [r for r in R if r['Grupo'] == 'Emitido' and tipo(r).startswith('factura')]
dso = [r for r in R if r['Grupo'] == 'Emitido' and tipo(r).startswith('documento soporte')]
nomina = [r for r in R if r['Grupo'] == 'Emitido' and tipo(r).startswith('nomina')]
com = [r for r in R if r['Grupo'] == 'Recibido' and tipo(r).startswith('factura')]
nc = [r for r in R if r['Grupo'] == 'Recibido' and tipo(r).startswith('nota')]
dudas = []
def duda(area, ref, n, nm, nivel, det): dudas.append((area, ref, n, nm, nivel, det))

# ---------------- plantilla AGTCOMP1
cb = open(PK + 'AGTCOMP1.cab', 'rb').read(); cu = open(PK + 'AGTCOMP1.cue', 'rb').read(); tb = open(PK + 'AGTCOMP1.Ter', 'rb').read(); fpt = open(PK + 'AGTCOMP1.FPT', 'rb').read()
_, _, _, fc = parse(cb); _, _, _, fu = parse(cu)
tc = recs(cb)[0]; tu = recs(cu)[0]
for k in ('OTRO_TER', 'DETALLE', 'FACTURA', 'FEC_POSF', 'COD_BAN', 'NUM_IMP', 'COD_VEN', 'FIN'): tc = putc(tc, fc, k, '')
for k in ('COD_CIU', 'COD_SUC', 'COD_CCO', 'NUM_CHQ', 'DOC_MOV', 'DOC_CRUC', 'DOC_REF', 'FEC_VENC', 'COD_CON', 'DES_MOV', 'COD_TER'): tu = putc(tu, fu, k, '')
def mk_doc(trn, num, fec, factura='', detalle='', vend=''):
    h = tc
    for k, v in (('ANO_DOC', fec[:4]), ('PER_DOC', fec[4:6]), ('COD_TRN', trn), ('NUM_TRN', num), ('FEC_DOC', fec), ('FEC_VEN', fec), ('FACTURA', factura), ('DETALLE', detalle), ('COD_VEN', vend)):
        h = putc(h, fc, k, v)
    return h
def mk_line(trn, num, fec, cta, ter_, des, base, deb, cre, docref='', docmov='', saldo=0):
    r = tu
    for k, v in (('ANO_DOC', fec[:4]), ('PER_DOC', fec[4:6]), ('COD_TRN', trn), ('NUM_TRN', num), ('COD_CTA', cta), ('COD_TER', ter_), ('DES_MOV', des), ('DOC_REF', docref), ('DOC_MOV', docmov)):
        r = putc(r, fu, k, v)
    r = putn(r, fu, 'BAS_MOV', float(base)); r = putn(r, fu, 'DEB_MOV', float(deb)); r = putn(r, fu, 'CRE_MOV', float(cre))
    if 'SALDO' in fu: r = putn(r, fu, 'SALDO', float(saldo))
    return r
def sin_cdx(b): x = bytearray(b); x[28] = 0; return bytes(x)   # evita error 1707 en el 746

# ======================= VENTAS (tipo 04)
INC = re.compile(r'^(413|414|415|416|417)')
hist = defaultdict(list)    # nit -> [(key, income cta, export?, ret frozenset((cta, rate)), des)]
for (a, p, t, n), ls in lines.items():
    if t != '04' or a != '2026': continue
    cl = [l for l in ls if l['COD_CTA'] in ('13050505', '13050506')]
    if not cl: continue
    inc = [l for l in ls if l['CRE_MOV'] and INC.match(l['COD_CTA'])]
    if not inc: continue
    ret = frozenset((l['COD_CTA'], round(l['DEB_MOV'] / l['BAS_MOV'], 5)) for l in ls if l['COD_CTA'].startswith('1355') and l['BAS_MOV'])
    hist[cl[0]['COD_TER'].lstrip('0')].append(((int(a), int(p), numk(n)), inc[0]['COD_CTA'], cl[0]['COD_CTA'] == '13050506', ret, inc[0]['DES_MOV']))
for v in hist.values(): v.sort(key=lambda x: x[0])
def patron(h):
    if not h: return None, 'sin historial', 'cliente sin facturas de venta en 2026'
    last3 = [x[3] for x in h[-3:]]
    if len(set(last3)) > 1: return None, 'duda', 'las ultimas 3 facturas no coinciden'
    allp = {x[3] for x in h}
    return last3[0], ('alta' if len(allp) == 1 else 'media'), ('' if len(allp) == 1 else 'el patron cambio en el tiempo; se usa el de las ultimas 3 facturas')
def suffix(des):
    m = re.match(r'^\s*[A-Za-z]{0,3}\s*\d+\s*(.*)$', des)
    return (m.group(1) if m else des).strip()
rname = lambda c, rate: f'{c} {rate*100:.3f}%'
OVR_VTA = {'146': dict(des='SERVICIO DE MARQUILLOS', ret=frozenset({('13551522', 0.025)}))}   # Daniel 3-nov: PDF dice SERVICIO DE MARQUILLOS; retefuente 2,5% como ago/sep
ventas_docs = []
for x in sorted(ven, key=lambda r: (fecha(r['Fecha Emisión']), int(r['Folio']))):
    fol = int(x['Folio']); num = str(fol); fec = fecha(x['Fecha Emisión']); cl = nit(x['NIT Receptor']); ref = f"{x['Prefijo']}{fol}"
    exp = 'exporta' in tipo(x)
    tot = rh(f(x['Total'])); iva = rh(f(x['IVA'])); base = tot - iva
    if exists('04', num): duda('Ventas', ref, cl, x['Nombre Receptor'], 'ALTA', 'el consecutivo ya existe en CAB_DOC; no se genera'); continue
    if not exp and abs(iva - rh(base * 0.19)) > 1: duda('Ventas', ref, cl, x['Nombre Receptor'], 'MEDIA', f'IVA {iva:,} no es 19% de la base {base:,}')
    ter_ = '2222222' if cl == '222222222222' else cl
    h = hist.get(cl, [])
    if exp:
        hx = [z for z in h if z[2]]
        inc = hx[-1][1] if hx else '413506'; rec = '13050506'; ret = set(); nivel = 'alta' if hx else 'media'
        if not hx: duda('Ventas', ref, cl, x['Nombre Receptor'], 'MEDIA', 'exportacion de un cliente sin exportaciones previas: 413506 / 13050506 sin IVA ni retenciones (patron de las otras exportaciones)')
        des_suf = suffix(hx[-1][4]) if hx else 'SERVICIOS'
        if not hx: duda('Ventas', ref, cl, x['Nombre Receptor'], 'BAJA', 'descripcion generica SERVICIOS; ajustar')
        if iva: duda('Ventas', ref, cl, x['Nombre Receptor'], 'ALTA', f'exportacion con IVA {iva:,} en el REP: revisar')
    else:
        hn = [z for z in h if not z[2]]
        inc = hn[-1][1] if hn else '413504'; rec = '13050505'
        pat, nivel, nota = patron(hn)
        des_suf = suffix(hn[-1][4]) if hn else 'SERVICIOS'
        if num in OVR_VTA:
            des_suf = OVR_VTA[num]['des']; pat = OVR_VTA[num]['ret']; nivel = 'alta'
            duda('Ventas', ref, cl, x['Nombre Receptor'], 'INFO', 'retefuente 2,5% (13551522) y descripcion SERVICIO DE MARQUILLOS confirmadas por Daniel')
        elif pat is None:
            duda('Ventas', ref, cl, x['Nombre Receptor'], 'ALTA', 'sin retenciones generadas (' + nota + '); definirlas a mano'); pat = frozenset(); nivel = 'duda'
        elif nivel == 'media':
            duda('Ventas', ref, cl, x['Nombre Receptor'], 'MEDIA', 'retenciones: ' + (', '.join(rname(c, r) for c, r in sorted(pat)) or 'ninguna') + ' | ' + nota)
        ret = pat
        if not hn: duda('Ventas', ref, cl, x['Nombre Receptor'], 'BAJA', 'cliente sin ventas previas: descripcion generica SERVICIOS; ajustar')
    retv = [(c, rh(base * r)) for c, r in sorted(ret)] if ret else []
    deb = base + (0 if exp else iva) - sum(v for _, v in retv)
    des = f'FE {num} {des_suf}'.strip()[:50]
    ls_ = [mk_line('04', num, fec, inc, ter_, des, 0, 0, base)]
    if not exp: ls_.append(mk_line('04', num, fec, '24080505', ter_, des, base, 0, iva))
    for c, v in retv: ls_.append(mk_line('04', num, fec, c, ter_, des, base, v, 0))
    ls_.append(mk_line('04', num, fec, rec, ter_, des, 0, deb, 0, docref=num))
    ventas_docs.append(dict(num=num, ref=ref, fec=fec, cl=cl, nom=x['Nombre Receptor'], exp=exp, base=base, iva=0 if exp else iva, ret=sum(v for _, v in retv), deb=deb, nivel=nivel, h=mk_doc('04', num, fec, vend='01'), ls=ls_))
files = {'RUMVTA10.cab': build(cb, [d['h'] for d in ventas_docs]), 'RUMVTA10.cue': sin_cdx(build(cu, [l for d in ventas_docs for l in d['ls']])), 'RUMVTA10.Ter': build(tb, []), 'RUMVTA10.FPT': fpt}

# ======================= helpers de aprendizaje (compras y documento soporte)
EXG = re.compile(r'^(2408|2365|2368|1105|1110|1120|1330|13|22|23|511570|2355)')
RETC = re.compile(r'^(2365|2368)')
def aprender(trn):
    by = defaultdict(list)
    for (a, p, t, n), ls in lines.items():
        if t != trn or a != '2026': continue
        c = cabk.get((a, p, t, n))
        gas = [l for l in ls if l['DEB_MOV'] > 0 and not EXG.match(l['COD_CTA'])]
        ters = Counter(l['COD_TER'].lstrip('0') for l in ls if l['COD_TER'])
        crl = [l for l in ls if l['CRE_MOV'] > 0 and not RETC.match(l['COD_CTA'])]
        if not gas or not ters or not crl: continue
        rl = [(l['COD_CTA'], round(l['CRE_MOV'] / l['BAS_MOV'], 5)) for l in ls if RETC.match(l['COD_CTA']) and l['CRE_MOV'] > 0 and l['BAS_MOV']]
        by[ters.most_common(1)[0][0]].append(dict(k=(idx(a, p), numk(n)), gas=gas[0]['COD_CTA'], cred=crl[-1]['COD_CTA'], ret=tuple(sorted(rl)), det=c['DETALLE'] if c else ''))
    for v in by.values(): v.sort(key=lambda z: z['k'])
    return by
def elegir(h, ventana, clave):
    """devuelve (valor, nivel, nota) para el campo `clave` segun el historial h"""
    rec = [z for z in h if z['k'][0] >= ventana]
    if rec:
        c = Counter(z[clave] for z in rec)
        if len(c) == 1: return next(iter(c)), 'alta', ''
        return h[-1][clave], 'baja', 'varias opciones desde abril (' + ', '.join(f'{k}x{v}' for k, v in c.most_common()) + '); se uso la de la ultima vez'
    c = Counter(z[clave] for z in h)
    return h[-1][clave], 'media', 'sin movimiento desde abril; se uso la de la ultima vez (' + ', '.join(f'{k}x{v}' for k, v in c.most_common(3)) + ')'
def concepto(det, pref):
    m = re.match(r'^\s*' + pref + r'[\s-]*\d+\s*(.*)$', det, re.I)
    return (m.group(1) if m else det).strip()
VENT = idx(2026, 4)

# ======================= DOCUMENTO SOPORTE (tipo 05a)
hs = aprender('05a')
dso_docs = []; dso_held = []
for x in sorted(dso, key=lambda r: (fecha(r['Fecha Emisión']), int(r['Folio']))):
    fol = int(x['Folio']); num = 'FTM-' + str(fol).zfill(5); fec = fecha(x['Fecha Emisión']); t_ = nit(x['NIT Receptor']); ref = f"{x['Prefijo']} {fol}"
    base = rh(f(x['Total']))
    if exists('05a', num): duda('Doc soporte', ref, t_, x['Nombre Receptor'], 'ALTA', 'el consecutivo ya existe en CAB_DOC; no se genera'); continue
    h = hs.get(t_, [])
    if not h:
        dso_held.append(dict(num=num, ref=ref, fec=fec, nit=t_, nom=x['Nombre Receptor'], base=base))
        duda('Doc soporte', f'{ref} (reservado {num})', t_, x['Nombre Receptor'], 'ALTA', 'tercero sin documentos soporte previos: NO generado; definir cuenta de gasto, retenciones y cuenta de pago'); continue
    gas, n1, no1 = elegir(h, VENT, 'gas'); cred, n2, no2 = elegir(h, VENT, 'cred')
    last = h[-1]; ret = last['ret']
    nivel = 'alta' if n1 == n2 == 'alta' else 'baja' if 'baja' in (n1, n2) else 'media'
    if no1: duda('Doc soporte', f'{ref} ({num})', t_, x['Nombre Receptor'], 'BAJA' if n1 == 'baja' else 'MEDIA', f'cuenta de gasto propuesta {gas}. ' + no1)
    if no2: duda('Doc soporte', f'{ref} ({num})', t_, x['Nombre Receptor'], 'BAJA' if n2 == 'baja' else 'MEDIA', f'cuenta de pago propuesta {cred}. ' + no2)
    retv = [(c, rh(base * r)) for c, r in ret]
    if ret: duda('Doc soporte', f'{ref} ({num})', t_, x['Nombre Receptor'], 'MEDIA', 'retenciones copiadas del ultimo DS del tercero: ' + ', '.join(rname(c, r) for c, r in ret))
    else: duda('Doc soporte', f'{ref} ({num})', t_, x['Nombre Receptor'], 'MEDIA', 'sin retenciones (el ultimo DS del tercero no tuvo)')
    conc = concepto(last['det'], 'FTM'); duda('Doc soporte', f'{ref} ({num})', t_, x['Nombre Receptor'], 'BAJA', 'concepto copiado del ultimo DS del tercero; ajustar si cambia: ' + conc[:40])
    fac = f'FTM {fol}'; det = f'{fac} {conc}'.strip(); des = det[:50]; neto = base - sum(v for _, v in retv)
    ls_ = [mk_line('05a', num, fec, gas, t_, des, 0, base, 0)]
    for c, v in retv: ls_.append(mk_line('05a', num, fec, c, t_, des, base, 0, v))
    ls_.append(mk_line('05a', num, fec, cred, t_, des, 0, 0, neto, docref=num, docmov=fac, saldo=neto))
    dso_docs.append(dict(num=num, ref=ref, fec=fec, nit=t_, nom=x['Nombre Receptor'], base=base, ret=sum(v for _, v in retv), neto=neto, gas=gas, cred=cred, nivel=nivel, h=mk_doc('05a', num, fec, factura=fac, detalle=det), ls=ls_))
files.update({'RUMDSO10.cab': build(cb, [d['h'] for d in dso_docs]), 'RUMDSO10.cue': sin_cdx(build(cu, [l for d in dso_docs for l in d['ls']])), 'RUMDSO10.Ter': build(tb, []), 'RUMDSO10.FPT': fpt})

# ======================= COMPRAS (tipo 05)
hc = aprender('05')
# indicado por Daniel 3-nov-2026: NIT sin compras en 2026 -> ultima cuenta historica (2023) 529525 / ASEO Y CAFETERIA; pago 220505
hc['79160978'] = [dict(k=(idx(2026, 10), 0), gas='529520', cred='220505', ret=(), det='FC 0 DECORACION')]   # Daniel 3-nov: 529520
hc['80139187'] = [dict(k=(idx(2026, 10), 0), gas='524510', cred='220505', ret=(), det='FC 0 FERRETERIA')]    # Daniel 3-nov: 524510
hc['860000387'] = [dict(k=(idx(2026, 10), 0), gas='529525', cred='220505', ret=(), det='FC 0 ASEO Y CAFETERIA')]
cp = max(numk(n) for (a, p, t, n) in cabk if t == '05' and re.match(r'^CP-\d+$', n))
cm_docs = []; held = []
for x in sorted(com, key=lambda r: (fecha(r['Fecha Emisión']), r['Prefijo'], int(re.sub(r'\D', '', str(r['Folio'])) or 0))):
    prov = nit(x['NIT Emisor']); fec = fecha(x['Fecha Emisión']); ref = f"{x['Prefijo']}-{x['Folio']}"
    tot = rh(f(x['Total'])); iva = rh(f(x['IVA'])); otros = sum(f(x[k_]) for k_ in ('ICA', 'IC', 'INC', 'Timbre', 'INC Bolsas', 'IN Carbono', 'IN Combustibles', 'IC Datos', 'ICL', 'INPP', 'IBUA', 'ICUI'))
    h = hc.get(prov, [])
    if not h:
        cp += 1; held.append(dict(num=f'CP-{cp:06d}', ref=ref, fec=fec, prov=prov, nom=x['Nombre Emisor'], total=tot))
        duda('Compras', f'{ref} (reservado CP-{cp:06d})', prov, x['Nombre Emisor'], 'ALTA', 'proveedor sin compras en 2026: NO generado; cargarlo (766 si es nuevo) y definir cuenta de gasto y de pago'); continue
    cp += 1; num = f'CP-{cp:06d}'
    if prov in ('79160978', '80139187'): duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'INFO', 'tercero nuevo (766); cuenta de gasto indicada por Daniel segun los items del PDF; pago 220505')
    if prov == '860000387': duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'INFO', 'cuenta 529525 (ultima usada en 2023) y pago 220505 indicados por Daniel; concepto ASEO Y CAFETERIA')
    gas, n1, no1 = elegir(h, VENT, 'gas'); cred, n2, no2 = elegir(h, VENT, 'cred')
    nivel = 'alta' if n1 == n2 == 'alta' else 'baja' if 'baja' in (n1, n2) else 'media'
    if no1: duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'BAJA' if n1 == 'baja' else 'MEDIA', f'cuenta de gasto propuesta {gas}. ' + no1)
    if no2: duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'BAJA' if n2 == 'baja' else 'MEDIA', f'cuenta de pago propuesta {cred}. ' + no2)
    dig = re.sub(r'\D', '', str(x['Folio'])); fac = dig
    conc = concepto(h[-1]['det'], 'FC')
    det = f'FC {fac} {conc}'.strip(); des = det[:50]
    taxable = tot - iva - otros; gasto = tot - iva
    if iva:
        ratio = iva / taxable if taxable else 0
        if not (abs(ratio - 0.19) < 0.003 or abs(ratio - 0.05) < 0.003): duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'ALTA', f'IVA {iva:,} sobre base {taxable:,.0f} = {ratio:.1%}: tarifa mixta o atipica, revisar')
    if otros: duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'INFO', f'impuestos distintos al IVA por {otros:,.2f} sumados al gasto {gas}; IVA y total cuadran con el REP')
    ret = h[-1]['ret'] if sum(1 for z in h if z['ret']) / len(h) >= 0.5 else ()
    retv = [(c, rh(taxable * r)) for c, r in ret]
    if retv: duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'MEDIA', 'retenciones por historial: ' + ', '.join(rname(c, r) for c, r in ret))
    neto = tot - sum(v for _, v in retv)
    ls_ = [mk_line('05', num, fec, gas, prov, des, 0, gasto, 0)]
    if iva: ls_.append(mk_line('05', num, fec, '511570', prov, des, 0, iva, 0))
    for c, v in retv: ls_.append(mk_line('05', num, fec, c, prov, des, taxable, 0, v))
    ls_.append(mk_line('05', num, fec, cred, prov, des, 0, 0, neto, docref=num, docmov=fac, saldo=neto))
    cm_docs.append(dict(num=num, ref=ref, fec=fec, prov=prov, nom=x['Nombre Emisor'], tot=tot, iva=iva, gas=gas, cred=cred, nivel=nivel, fac=fac, detalle=det, h=mk_doc('05', num, fec, factura=fac, detalle=det), ls=ls_))
# ---- notas credito de compra (tipo 16, DCM-n): sin cruce con la factura original (decision de Daniel 3-nov)
nc_docs = []
dcm = max(numk(n) for (a, p, t, n) in cabk if t == '16')
for x in sorted(nc, key=lambda r: (fecha(r['Fecha Emisión']), int(re.sub(r'\D', '', str(r['Folio'])) or 0))):
    prov = nit(x['NIT Emisor']); fec = fecha(x['Fecha Emisión']); fol = re.sub(r'\D', '', str(x['Folio'])); ref = f"NC {x['Prefijo']}-{x['Folio']}"
    tot = rh(f(x['Total'])); iva = rh(f(x['IVA'])); base = tot - iva
    h = hc.get(prov, [])
    if not h: duda('Compras', ref, prov, x['Nombre Emisor'], 'ALTA', 'nota credito de proveedor sin historial: NO generada'); continue
    dcm += 1; num = f'DCM-{dcm:05d}'
    gas, n1, no1 = elegir(h, VENT, 'gas')
    if no1: duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'BAJA' if n1 == 'baja' else 'MEDIA', f'cuenta de gasto propuesta {gas}. ' + no1)
    duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'ALTA', 'NC generada SIN cruce (DOC_CRUC/DOC_REF/ANO_REF vacios, DES_MOV sin factura original): enlazar a mano con la factura original en SIASoft')
    fac = f'ND {fol}'; des = f'{fac} FT 07611032128'   # comprobante original citado en la NC (PDF DIAN); sin cruce
    ls_ = [mk_line('16', num, fec, gas, prov, des, 0, 0, base)]
    if iva: ls_.append(mk_line('16', num, fec, '511570', prov, des, 0 if True else base, 0, iva))
    ls_.append(mk_line('16', num, fec, '220505', prov, des, 0, tot, 0))
    nc_docs.append(dict(num=num, ref=ref, fec=fec, prov=prov, nom=x['Nombre Emisor'], tot=tot, iva=iva, gas=gas, h=mk_doc('16', num, fec, factura=fac), ls=ls_))
files.update({'RUMNCO10.cab': build(cb, [d['h'] for d in nc_docs]), 'RUMNCO10.cue': sin_cdx(build(cu, [l for d in nc_docs for l in d['ls']])), 'RUMNCO10.Ter': build(tb, []), 'RUMNCO10.FPT': fpt})
files.update({'RUMCOM10.cab': build(cb, [d['h'] for d in cm_docs]), 'RUMCOM10.cue': sin_cdx(build(cu, [l for d in cm_docs for l in d['ls']])), 'RUMCOM10.Ter': build(tb, []), 'RUMCOM10.FPT': fpt})

# ======================= TERCEROS NUEVOS (766): solo NIT que NO estan en MAE_TER
T0 = open(PK + 'TERVTAORI.DBF', 'rb').read(); TF = open(PK + 'TERVTAORI.FPT', 'rb').read(); _, thl, _, ft = parse(T0); tmpl = recs(T0)[0]
supl = set()
for (a, p, t, n), ls in lines.items():
    if t == '05':
        for l in ls:
            if l['COD_TER']: supl.add(l['COD_TER'].lstrip('0'))
supl &= set(TER)
FLAGS = [k for k in ft if k in ('TIP_PRV', 'CLASIFIC', 'IND_RETE', 'IND_RET', 'AUT_RET', 'COD_ACT', 'COD_CLA', 'ESTADO', 'JURID', 'IND_CRED', 'IND_COBRO', 'MAYMIN', 'CIUDAD', 'COD_CIU', 'DPTO', 'MUN', 'COD_ACTIV', 'REGIMEN', 'RESPON', 'PAIS', 'COD_PAIS', 'CONTA', 'DEPA', 'IND_CREE', 'BLOQUEO', 'POR_ICA', 'INT_MORA', 'DIA_PLAZ', 'POR_DES')]
modes = {}
for k in FLAGS:
    cnt = Counter(str(TER[n][k]) for n in supl if k in TER[n])
    if cnt:
        v, c = cnt.most_common(1)[0]
        if c / max(len(supl), 1) >= 0.6: modes[k] = v
def dv(n):
    w = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]; s = sum(int(c) * w[i] for i, c in enumerate(reversed(n))); r = s % 11
    return str(r if r < 2 else 11 - r)
EMP = re.compile(r'\b(S\.?A\.?S\.?|LTDA|S\.?A\.?|S\.? ?EN ?C|E\.?U\.?|FUNDACION|CORPORACION|ASOCIACION|COLEGIO|CLUB|GRUPO|COMPA|INVERSIONES|SOLUCIONES|SERVICIOS|PUBLICIDAD|IMPORT|COMERCIALIZ|PRODUCCIONES|AGENCIA|CIA|INC|LLC|CORP|GMBH|LTD)\b', re.I)
nuevos = {}
for x in com + ven + dso:
    if x['Grupo'] == 'Recibido': n, nm = nit(x['NIT Emisor']), x['Nombre Emisor']
    else: n, nm = nit(x['NIT Receptor']), x['Nombre Receptor']
    if n not in TER and n != '222222222222': nuevos[n] = re.sub(r'\s+', ' ', str(nm).strip()).upper()
# solo los que alimentan documentos generados o reservados
uso = {d['cl'] for d in ventas_docs} | {d['nit'] for d in dso_docs} | {d['prov'] for d in cm_docs}
trows = []; tnew = []
for n, nm in sorted(nuevos.items()):
    if n not in uso: continue
    jur = bool(EMP.search(nm)) or (len(n) == 9 and n[0] in '89'); tdoc = '31' if (len(n) == 9 and n[0] in '89') else '13'
    if jur != (tdoc == '31'): duda('Terceros', n, n, nm, 'MEDIA', f'persona {"juridica" if jur else "natural"} pero documento {tdoc}: revisar tipo de documento')
    r = tmpl
    for k, v in modes.items():
        if k in ft and ft[k][2] == 'C': r = putc(r, ft, k, v)
        elif k in ft and ft[k][2] == 'N': r = putn(r, ft, k, float(v), ft[k][3])
    for k in ('NOM_TER', 'RAZ', 'REPRES'): r = putc(r, ft, k, nm)
    for k, v in (('COD_TER', n), ('DV', dv(n)), ('TDOC', tdoc), ('DIR1', ''), ('DIR', ''), ('TEL1', ''), ('EMAIL', ''), ('FEC_ING', '20261103'), ('TIP_PERS', '2' if jur else '1'), ('NOM1', ''), ('NOM2', ''), ('APL1', ''), ('APL2', '')):
        if k in ft: r = putc(r, ft, k, v)
    if not jur:
        t = nm.split()
        n1, n2, a1, a2 = (t[0], '', t[1], '') if len(t) == 2 else (t[0], '', t[1], t[2]) if len(t) == 3 else tuple(t) if len(t) == 4 else (t[0], '', t[-1], '')
        for k, v in (('NOM1', n1), ('NOM2', n2), ('APL1', a1), ('APL2', a2)): r = putc(r, ft, k, v)
        duda('Terceros', n, n, nm, 'BAJA', f'persona natural: nombre y apellidos separados asumiendo {len(t)} palabras; revisar')
    trows.append(r); tnew.append((n, nm, tdoc))
th = bytearray(T0[:thl]); th[4:8] = struct.pack('<I', len(trows))
files['TERRUMASA10.DBF'] = bytes(th) + b''.join(trows) + b'\x1a'; files['TERRUMASA10.FPT'] = TF
duda('REP', 'Nomina electronica', '', '', 'INFO', f'{len(nomina)} documentos de nomina individual excluidos: no se contabilizan por este flujo')

for nm_, data in files.items(): open(OUT + nm_, 'wb').write(data)

# ======================= REVISION xlsx
wb = openpyxl.Workbook(); w = wb.active; w.title = 'Resumen'
def hoja(nombre, cols, data):
    s = wb.create_sheet(nombre); s.append(cols)
    for r in data: s.append(list(r))
    for c in s[1]: c.font = openpyxl.styles.Font(bold=True)
    s.freeze_panes = 'A2'
    for i, col in enumerate(cols): s.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = max(12, min(48, len(col) + 6))
hoja('Ventas', ['Consecutivo', 'REP', 'Fecha', 'NIT', 'Cliente', 'Export', 'Base', 'IVA', 'Retenciones', 'Debito cartera', 'Nivel'], [(d['num'], d['ref'], d['fec'], d['cl'], d['nom'], 'SI' if d['exp'] else '', d['base'], d['iva'], d['ret'], d['deb'], d['nivel']) for d in ventas_docs])
hoja('Doc soporte', ['NUM_TRN', 'REP', 'Fecha', 'NIT', 'Tercero', 'Base', 'Retenciones', 'Neto', 'Gasto', 'Pago', 'Nivel'], [(d['num'], d['ref'], d['fec'], d['nit'], d['nom'], d['base'], d['ret'], d['neto'], d['gas'], d['cred'], d['nivel']) for d in dso_docs] + [(d['num'], d['ref'], d['fec'], d['nit'], d['nom'], d['base'], '', '', '', '', 'RETENIDO') for d in dso_held])
hoja('Compras', ['NUM_TRN', 'REP', 'Fecha', 'NIT', 'Proveedor', 'Total', 'IVA', 'Gasto', 'Pago', 'FACTURA', 'DETALLE', 'Nivel'], [(d['num'], d['ref'], d['fec'], d['prov'], d['nom'], d['tot'], d['iva'], d['gas'], d['cred'], d['fac'], d['detalle'], d['nivel']) for d in cm_docs] + [(d['num'], d['ref'], d['fec'], d['prov'], d['nom'], d['total'], '', '', '', '', '', 'RETENIDO') for d in held])
hoja('Notas credito compra', ['NUM_TRN', 'REP', 'Fecha', 'NIT', 'Proveedor', 'Total', 'IVA', 'Gasto'], [(d['num'], d['ref'], d['fec'], d['prov'], d['nom'], d['tot'], d['iva'], d['gas']) for d in nc_docs])
hoja('Dudas', ['Area', 'Referencia', 'NIT', 'Tercero', 'Nivel', 'Detalle'], dudas)
hoja('Terceros nuevos (766)', ['NIT', 'Nombre', 'TDOC'], tnew)
wb.save(OUT + 'REVISION_RUMASA_OCT2026.xlsx')

# ======================= resumen
def D(ds): return sum(l_[0] for l_ in ds)
print('VENTAS:', len(ventas_docs), '| base', sum(d['base'] for d in ventas_docs), '| IVA', sum(d['iva'] for d in ventas_docs), '| ret', sum(d['ret'] for d in ventas_docs), '| cartera', sum(d['deb'] for d in ventas_docs), '| niveles', dict(Counter(d['nivel'] for d in ventas_docs)), '| fechas', min(d['fec'] for d in ventas_docs), max(d['fec'] for d in ventas_docs))
print('DOC SOPORTE:', len(dso_docs), '| base', sum(d['base'] for d in dso_docs), '| ret', sum(d['ret'] for d in dso_docs), '| neto', sum(d['neto'] for d in dso_docs), '| retenidos', len(dso_held), '| niveles', dict(Counter(d['nivel'] for d in dso_docs)))
print('COMPRAS:', len(cm_docs), '| total', sum(d['tot'] for d in cm_docs), '| IVA', sum(d['iva'] for d in cm_docs), '| niveles', dict(Counter(d['nivel'] for d in cm_docs)), '| retenidas', len(held), 'por', sum(d['total'] for d in held), '| rango', cm_docs[0]['num'] if cm_docs else '-', cm_docs[-1]['num'] if cm_docs else '-')
print('compras fechas', min(d['fec'] for d in cm_docs), max(d['fec'] for d in cm_docs), '| ds fechas', min(d['fec'] for d in dso_docs) if dso_docs else '-', max(d['fec'] for d in dso_docs) if dso_docs else '-')
print('NC compra:', [(d['num'], d['tot'], d['iva'], d['gas']) for d in nc_docs])
print('TERCEROS nuevos:', len(trows), '| DUDAS:', len(dudas), dict(Counter((d[0], d[4]) for d in dudas)))
# cuadre D=C por documento
bad = 0
for d in ventas_docs + dso_docs + cm_docs + nc_docs:
    dd = cc = 0
    for r in d['ls']:
        dd += float(r[fu['DEB_MOV'][0]:fu['DEB_MOV'][0] + fu['DEB_MOV'][1]]); cc += float(r[fu['CRE_MOV'][0]:fu['CRE_MOV'][0] + fu['CRE_MOV'][1]])
    if abs(dd - cc) > 0.5: bad += 1
print('documentos descuadrados:', bad)
print('REP: compras total', sum(rh(f(x['Total'])) for x in com), 'IVA', sum(rh(f(x['IVA'])) for x in com), '| ventas total', sum(rh(f(x['Total'])) for x in ven), '| DS total', sum(rh(f(x['Total'])) for x in dso))
