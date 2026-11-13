import sys, re, math, os, json, struct
sys.path.insert(0, '.')
from dbf import load
from armar import parse, recs, get, putc, putn, build
import openpyxl
from collections import Counter, defaultdict

BASE = '/mnt/user-data/uploads/SIASOFT_V23/EMPRESAS/EMP010/CO.SIA/'
PK = '/mnt/user-data/uploads/PAQUETE_ORIGINAL/'
REP = '/mnt/user-data/attachments/9b0c6e8d-482d-5403-b893-ab3acf977cf5/27d7e4b8-19370395-3e96-425d-bcc7-de0742c3115a.xlsx'
OUT = '/mnt/user-data/outputs/NARU_OCT2026/'
os.makedirs(OUT, exist_ok=True)
rh = lambda x: int(math.floor(x + 0.5 + 1e-9))
nit = lambda s: str(int(float(s))) if isinstance(s, (int, float)) else str(s).strip().lstrip('0')
idx = lambda a, p: int(a) * 12 + int(p)

_, cab, _ = load(BASE + 'CAB_DOC.DBF'); _, cue, _ = load(BASE + 'CUE_DOC.DBF'); _, ter, _ = load(BASE + 'MAE_TER.DBF')
TER = {t['COD_TER'].lstrip('0'): t for t in ter}
cabk = {(c['ANO_DOC'], c['PER_DOC'], c['COD_TRN'], c['NUM_TRN']): c for c in cab}
lines = defaultdict(list)
for l in cue: lines[(l['ANO_DOC'], l['PER_DOC'], l['COD_TRN'], l['NUM_TRN'])].append(l)

# ---------------- REP
ws = openpyxl.load_workbook(REP, read_only=True, data_only=True).worksheets[0]
rows = list(ws.iter_rows(values_only=True)); H = rows[0]
R = [dict(zip(H, r)) for r in rows[1:] if r[0]]
f = lambda v: float(v or 0)
def fecha(s): d, m, y = s.split('-'); return y + m + d
ven = [r for r in R if r['Grupo'] == 'Emitido' and r['Prefijo'] == 'FVEN']
com = [r for r in R if r['Grupo'] == 'Recibido']
nomina = [r for r in R if r['Grupo'] == 'Emitido' and r['Prefijo'] != 'FVEN']
dudas = []   # (area, referencia, nit, nombre, nivel, detalle)
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
def mk_line(trn, num, fec, cta, ter_, des, base, deb, cre, docref=''):
    r = tu
    for k, v in (('ANO_DOC', fec[:4]), ('PER_DOC', fec[4:6]), ('COD_TRN', trn), ('NUM_TRN', num), ('COD_CTA', cta), ('COD_TER', ter_), ('DES_MOV', des), ('DOC_REF', docref)):
        r = putc(r, fu, k, v)
    r = putn(r, fu, 'BAS_MOV', float(base)); r = putn(r, fu, 'DEB_MOV', float(deb)); r = putn(r, fu, 'CRE_MOV', float(cre))
    return r

# =============== VENTAS: aprender patron de retencion por cliente
RET = {'13551512': ('R', lambda b, i: b * 0.04), '13551805': ('I', lambda b, i: b * 0.00966), '13551715': ('V', lambda b, i: i * 0.15)}
ORD = ['13551512', '13551805', '13551715']
hist = defaultdict(list)    # nit -> [(orden, frozenset ctas)]
for (a, p, t, n), ls in lines.items():
    if t == '04' and a == '2026' and p <= '12':
        c = [l['COD_TER'].lstrip('0') for l in ls if l['COD_CTA'] == '13050505']
        if c:
            m = re.search(r'(\d+)$', n)
            hist[c[0]].append(((int(a), int(p), int(m.group(1)) if m else 0), frozenset(l['COD_CTA'] for l in ls if l['COD_CTA'] in RET)))
for v in hist.values(): v.sort(key=lambda x: x[0])
def patron(h):
    """devuelve (set de cuentas, nivel, nota)"""
    if not h: return None, 'sin historial', 'cliente sin facturas de venta en 2026'
    last3 = [s for _, s in h[-3:]]
    allp = {s for _, s in h}
    if len(set(last3)) > 1: return None, 'duda', 'las ultimas 3 facturas no coinciden: ' + ' / '.join(''.join(RET[c][0] for c in ORD if c in s) or '-' for s in last3)
    cur = last3[0]
    if len(allp) == 1: return cur, 'alta', ''
    return cur, 'media', 'patron cambio en el tiempo; se usa el de las ultimas 3 facturas'
V = []  # ventas generadas
def calc_venta(base, iva, cuentas):
    ret = {c: rh(RET[c][1](base, iva)) for c in ORD if c in cuentas}
    return ret, base + iva - sum(ret.values())
# backtest de ventas: jul-sep con lo aprendido ANTES de cada factura
bt = Counter(); btx = []
for (a, p, t, n), ls in sorted(lines.items(), key=lambda kv: (kv[0][1], int(re.search(r'(\d+)$', kv[0][3]).group(1)) if re.search(r'(\d+)$', kv[0][3]) else 0)):
    if t != '04' or a != '2026' or p not in ('07', '08', '09'): continue
    cl = [l['COD_TER'].lstrip('0') for l in ls if l['COD_CTA'] == '13050505'][0]
    key = (int(a), int(p), int(re.search(r'(\d+)$', n).group(1)))
    h = [x for x in hist[cl] if x[0] < key]
    cuentas, nivel, _ = patron(h)
    b = sum(l['CRE_MOV'] for l in ls if l['COD_CTA'] == '413508'); i = sum(l['CRE_MOV'] for l in ls if l['COD_CTA'] == '24080505')
    real = {l['COD_CTA']: l['DEB_MOV'] for l in ls if l['COD_CTA'] in RET}; deb = [l['DEB_MOV'] for l in ls if l['COD_CTA'] == '13050505'][0]
    if cuentas is None: bt['sin prediccion (' + nivel + ')'] += 1; continue
    pr, dn = calc_venta(b, i, cuentas)
    ok = set(pr) == set(real) and all(abs(pr[c] - real[c]) <= 1 for c in pr) and abs(dn - deb) <= 1
    bt['coincide' if ok else 'difiere'] += 1
    if not ok: btx.append((n, sorted(set(pr) ^ set(real))))
print('BACKTEST VENTAS jul-sep:', dict(bt), btx[:5])

ventas_docs = []
for x in sorted(ven, key=lambda r: (fecha(r['Fecha Emisión']), int(r['Folio']))):
    fol = int(x['Folio']); num = 'FE' + str(fol); fec = fecha(x['Fecha Emisión']); cl = nit(x['NIT Receptor'])
    tot = rh(f(x['Total'])); iva = rh(f(x['IVA'])); base = tot - iva
    if (('2026', fec[4:6], '04', num)) in cabk or any(k[3] == num and k[2] == '04' for k in cabk): duda('Ventas', num, cl, x['Nombre Receptor'], 'ALTA', 'el consecutivo ya existe en CAB_DOC; no se genera'); continue
    if abs(iva - rh(base * 0.19)) > 1: duda('Ventas', num, cl, x['Nombre Receptor'], 'MEDIA', f'IVA {iva:,} no es 19% de la base {base:,}')
    ter_ = '2222222' if cl == '222222222222' else cl
    if ter_ not in TER and ter_ != '2222222': duda('Ventas', num, cl, x['Nombre Receptor'], 'ALTA', 'cliente no existe en MAE_TER (falta 766)')
    cuentas, nivel, nota = patron(hist.get(cl, []))
    if cuentas is None:
        duda('Ventas', num, cl, x['Nombre Receptor'], 'ALTA', 'sin retenciones generadas (' + nota + '); defini retenciones a mano'); cuentas = set(); nivel = 'duda'
    elif nivel == 'media':
        duda('Ventas', num, cl, x['Nombre Receptor'], 'MEDIA', 'retenciones aplicadas: ' + (''.join(RET[c][0] for c in ORD if c in cuentas) or 'ninguna') + ' | ' + nota)
    ret, deb = calc_venta(base, iva, cuentas)
    des = (num + ' GESTION EMPRESARIAL')[:50]
    ls_ = [mk_line('04', num, fec, '413508', ter_, des, 0, 0, base), mk_line('04', num, fec, '24080505', ter_, des, base, 0, iva)]
    for c in ORD:
        if c in ret: ls_.append(mk_line('04', num, fec, c, ter_, des, base, ret[c], 0))
    ls_.append(mk_line('04', num, fec, '13050505', ter_, des, 0, deb, 0, docref=num))
    ventas_docs.append(dict(num=num, fec=fec, cl=cl, nom=x['Nombre Receptor'], base=base, iva=iva, ret=ret, deb=deb, nivel=nivel, h=mk_doc('04', num, fec, vend='01'), ls=ls_))
files = {'NARVTA10.cab': build(cb, [d['h'] for d in ventas_docs]), 'NARVTA10.cue': build(cu, [l for d in ventas_docs for l in d['ls']]), 'NARVTA10.Ter': build(tb, []), 'NARVTA10.FPT': fpt}

# =============== COMPRAS
EXG = re.compile(r'^(2408|2365|2368|1105|1110|1120|22|23)')
ventana = idx(2026, 4)
by = defaultdict(list)     # nit -> [(idx, num, cuenta gasto, detalle, tiene_ret, ret_cta, ret_rate)]
acct_det = defaultdict(Counter)
for (a, p, t, n), ls in lines.items():
    if t not in ('05', '18'): continue
    c = cabk.get((a, p, t, n))
    gas = [l for l in ls if l['DEB_MOV'] > 0 and not EXG.match(l['COD_CTA'])]
    ters = Counter(l['COD_TER'].lstrip('0') for l in ls if l['COD_TER'])
    if not gas or not ters: continue
    rl = [l for l in ls if l['COD_CTA'].startswith('2365')]
    by[ters.most_common(1)[0][0]].append((idx(a, p), n, gas[0]['COD_CTA'], c['DETALLE'] if c else '', bool(rl), rl[0]['COD_CTA'] if rl else None,
                                        round(rl[0]['CRE_MOV'] / rl[0]['BAS_MOV'], 4) if rl and rl[0]['BAS_MOV'] else None))
    if idx(a, p) >= ventana and c and c['DETALLE']: acct_det[gas[0]['COD_CTA']][c['DETALLE']] += 1
nums = [int(m.group(1)) for (a, p, t, n) in cabk if t == '05' for m in [re.match(r'^CP-(\d+)$', n)] if m]
cp = max(nums)
cm_docs = []; held = []
OVR_TOK = {'MINISO': '529520', 'OCTOPUX': '529520', 'EDITORIAL': '529530', 'MECANELECTRO': '529530'}   # indicado por Daniel 3-nov-2026
OVR_USED = {}
OTROS_COLS = ['ICA', 'IC', 'INC', 'Timbre', 'INC Bolsas', 'IN Carbono', 'IN Combustibles', 'IC Datos', 'ICL', 'INPP', 'IBUA', 'ICUI']
print('otros impuestos en compras del REP (no cero):', {k_: sum(1 for x_ in com if f(x_[k_])) for k_ in OTROS_COLS if any(f(x_[k_]) for x_ in com)})
for x in sorted(com, key=lambda r: (fecha(r['Fecha Emisión']), int(r['Folio']))):
    prov = nit(x['NIT Emisor']); fec = fecha(x['Fecha Emisión']); cp += 1; num = f'CP-{cp}'
    ref = f"{x['Prefijo']}-{x['Folio']}"
    tot = rh(f(x['Total'])); iva = rh(f(x['IVA'])); inc = f(x['INC']); ic = f(x['IC']); otros = sum(f(x[k_]) for k_ in OTROS_COLS)
    h = by.get(prov, [])
    ordk = lambda r_: (r_[0], int(re.search(r'(\d+)$', r_[1]).group(1)) if re.search(r'(\d+)$', r_[1]) else 0)
    ult = max(h, key=ordk) if h else None
    rec = [r_ for r_ in h if r_[0] >= ventana]
    if rec:
        accs = Counter(r_[2] for r_ in rec)
        if len(accs) == 1: acc, nivel, nota = next(iter(accs)), 'alta', ''
        else:
            acc = ult[2]; nivel = 'baja'; nota = 'el proveedor uso varias cuentas desde abril (' + ', '.join(f'{k}x{v}' for k, v in accs.most_common()) + '); se uso la de la ultima vez que se relaciono el tercero'
        src = rec
    elif h:
        accs = Counter(r_[2] for r_ in h); acc = ult[2]; nivel = 'media'; nota = 'sin compras desde abril; se uso la cuenta de la ultima vez que se relaciono el tercero (historial: ' + ', '.join(f'{k}x{v}' for k, v in accs.most_common(3)) + ')'; src = h
    else:
        tok = [t_ for t_ in OVR_TOK if t_ in str(x['Nombre Emisor']).upper()]
        if len(tok) == 1:
            acc = OVR_TOK[tok[0]]; nivel = 'definida'; nota = ''; src = []; OVR_USED[prov] = (tok[0], acc)
        else:
            held.append(dict(num=num, ref=ref, fec=fec, prov=prov, nom=x['Nombre Emisor'], total=tot))
            duda('Compras', f'{ref} (reservado {num})', prov, x['Nombre Emisor'], 'ALTA', 'proveedor nuevo sin historial: NO generado; cargarlo con el 766 y definir cuenta de gasto'); continue
    if nota: duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'BAJA' if nivel == 'baja' else 'MEDIA', f'cuenta propuesta {acc}. ' + nota)
    det = Counter(r_[3] for r_ in src if r_[2] == acc and r_[3]).most_common(1)
    if nivel in ('baja', 'media') and ult and ult[2] == acc and ult[3] and (acct_det[acc][ult[3]] >= 2 or not acct_det[acc]): det = [(ult[3], 1)]
    detalle = (det[0][0] if det else (acct_det[acc].most_common(1)[0][0] if acct_det[acc] else ''))[:40]
    taxable = tot - iva - otros; gasto = tot - iva
    if iva == 0: ivacta = None
    else:
        ratio = iva / taxable if taxable else 0
        if abs(ratio - 0.19) < 0.003: ivacta = '24081005'
        elif abs(ratio - 0.05) < 0.003: ivacta = '24081027'
        else: ivacta = '24081005'; duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'ALTA', f'IVA {iva:,} sobre base {taxable:,.0f} = {ratio:.1%}: tarifa mixta o atipica, revisar')
    if otros: duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'INFO', f'impuestos distintos al IVA por {otros:,.2f} (INC {inc:,.0f} / IC {ic:,.0f}); sumados al gasto {acc} segun tu regla; IVA y total cuadran con el REP')
    if str(x['Forma de Pago']) == '2': duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'ALTA', 'forma de pago credito: la dejo a caja 11050505 como indicaste; en el historial 4 de 147 compras fueron a proveedores (220505)')
    dig = re.sub(r'\D', '', str(x['Folio'])); fac = 'FC' + (dig[-6:] if len(dig) > 6 else dig)
    if len(dig) > 6: duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'MEDIA', f'folio de {len(dig)} digitos; FACTURA quedo {fac} (ultimos 6)')
    ret = 0; retcta = None
    if h and sum(1 for r_ in src if r_[4]) / len(src) >= 0.5:
        rr = Counter(r_[6] for r_ in src if r_[6]).most_common(1); rc = Counter(r_[5] for r_ in src if r_[5]).most_common(1)
        if rr and rc: ret = rh(taxable * rr[0][0]); retcta = rc[0][0]; duda('Compras', f'{ref} ({num})', prov, x['Nombre Emisor'], 'MEDIA', f'retefuente {rr[0][0]:.2%} aplicada por historial ({retcta})')
    des = (fac + ' ' + detalle)[:50]
    ls_ = [mk_line('05', num, fec, acc, prov, des, 0, gasto, 0)]
    if ivacta: ls_.append(mk_line('05', num, fec, ivacta, prov, des, taxable, iva, 0))
    if ret: ls_.append(mk_line('05', num, fec, retcta, prov, des, taxable, 0, ret))
    ls_.append(mk_line('05', num, fec, '11050505', prov, des, 0, 0, tot - ret))
    cm_docs.append(dict(num=num, ref=ref, fec=fec, prov=prov, nom=x['Nombre Emisor'], tot=tot, iva=iva, acc=acc, nivel=nivel, fac=fac, detalle=detalle, h=mk_doc('05', num, fec, factura=fac, detalle=detalle), ls=ls_))
for p_, (t_, a_) in OVR_USED.items(): duda('Compras', f'proveedor nuevo {p_} ({t_})', p_, t_, 'INFO', f'cuenta {a_} indicada por Daniel para proveedor nuevo')
print('proveedores nuevos resueltos por indicacion:', {p_: (t_, a_) for p_, (t_, a_) in OVR_USED.items()})
files.update({'NARCOM10.cab': build(cb, [d['h'] for d in cm_docs]), 'NARCOM10.cue': build(cu, [l for d in cm_docs for l in d['ls']]), 'NARCOM10.Ter': build(tb, []), 'NARCOM10.FPT': fpt})

# =============== TERCEROS NUEVOS (766)
T0 = open(PK + 'TERVTAORI.DBF', 'rb').read(); TF = open(PK + 'TERVTAORI.FPT', 'rb').read(); _, thl, _, ft = parse(T0); tmpl = recs(T0)[0]
sup = Counter(); supl = set()
for (a, p, t, n), ls in lines.items():
    if t == '05':
        for l in ls:
            if l['COD_TER']: supl.add(l['COD_TER'].lstrip('0'))
supl &= set(TER)
FLAGS = [k for k in ft if k in ('TIP_PRV','CLASIFIC','IND_RETE','IND_RET','AUT_RET','COD_ACT','COD_CLA','ESTADO','JURID','IND_CRED','IND_COBRO','MAYMIN','CIUDAD','COD_CIU','DPTO','MUN','COD_ACTIV','REGIMEN','RESPON','PAIS','COD_PAIS','CONTA','DEPA','IND_CREE','BLOQUEO','POR_ICA','INT_MORA','DIA_PLAZ','POR_DES')]
modes = {}
for k in FLAGS:
    cnt = Counter(str(TER[n][k]) for n in supl if k in TER[n]);
    if cnt:
        v, c = cnt.most_common(1)[0]
        if c / len(supl) >= 0.6: modes[k] = v
print('proveedores existentes usados como modelo:', len(supl), '| campos por moda:', modes)
def dv(n):
    w = [3,7,13,17,19,23,29,37,41,43,47,53,59,67,71]; s = sum(int(c) * w[i] for i, c in enumerate(reversed(n))); r = s % 11
    return str(r if r < 2 else 11 - r)
EMP = re.compile(r'\b(S\.?A\.?S\.?|LTDA|S\.?A\.?|S\.? ?EN ?C|E\.?U\.?|FUNDACION|CORPORACION|ASOCIACION|COLEGIO|CLUB|GRUPO|COMPA|INVERSIONES|SOLUCIONES|SERVICIOS|PUBLICIDAD|IMPORT|COMERCIALIZ|PRODUCCIONES|AGENCIA|CIA)\b', re.I)
nuevos = {}
for x in com + ven:
    n = nit(x['NIT Emisor']) if x['Grupo'] == 'Recibido' else nit(x['NIT Receptor'])
    nm = x['Nombre Emisor'] if x['Grupo'] == 'Recibido' else x['Nombre Receptor']
    if n not in TER and n != '222222222222': nuevos[n] = re.sub(r'\s+', ' ', str(nm).strip()).upper()
trows = []
for n, nm in sorted(nuevos.items()):
    jur = bool(EMP.search(nm)) or (len(n) == 9 and n[0] in '89'); tdoc = '31' if (len(n) == 9 and n[0] in '89') else '13'
    if jur != (tdoc == '31'): duda('Terceros', n, n, nm, 'MEDIA', f'persona {"juridica" if jur else "natural"} pero documento {tdoc}')
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
        duda('Terceros', n, n, nm, 'BAJA', f'persona natural: separe nombre y apellidos asumiendo {len(t)} palabras ({"1 nombre + 2 apellidos" if len(t)==3 else "revisar"})')
    trows.append(r)
th = bytearray(T0[:thl]); th[4:8] = struct.pack('<I', len(trows))
files['TERNARU10.DBF'] = bytes(th) + b''.join(trows) + b'\x1a'; files['TERNARU10.FPT'] = TF
for nm_ in nomina: pass
duda('REP', 'Nomina electronica', '', '', 'INFO', f'{len(nomina)} documentos NMN (nomina individual) excluidos: no son ventas')

for nm_, data in files.items(): open(OUT + nm_, 'wb').write(data)

# =============== resumen
def lvl(ds): return Counter(d['nivel'] for d in ds)
print('\nVENTAS generadas:', len(ventas_docs), '| base', sum(d['base'] for d in ventas_docs), '| IVA', sum(d['iva'] for d in ventas_docs), '| retenciones', sum(sum(d['ret'].values()) for d in ventas_docs), '| debito Clientes', sum(d['deb'] for d in ventas_docs), '| niveles', dict(lvl(ventas_docs)))
print('COMPRAS generadas:', len(cm_docs), '| total', sum(d['tot'] for d in cm_docs), '| IVA', sum(d['iva'] for d in cm_docs), '| niveles', dict(lvl(cm_docs)), '| retenidas (sin generar):', len(held), 'por', sum(d['total'] for d in held))
print('rango consecutivos compras:', cm_docs[0]['num'] if cm_docs else '-', '->', f'CP-{cp}', '| fechas ventas', min(d['fec'] for d in ventas_docs), max(d['fec'] for d in ventas_docs), '| fechas compras', min(d['fec'] for d in cm_docs), max(d['fec'] for d in cm_docs))
print('TERCEROS nuevos:', len(trows), '| DUDAS:', len(dudas), dict(Counter((d[0], d[4]) for d in dudas)))
json.dump(dict(dudas=dudas, ventas=[{k: v for k, v in d.items() if k not in ('h', 'ls')} for d in ventas_docs], compras=[{k: v for k, v in d.items() if k not in ('h', 'ls')} for d in cm_docs], held=held), open('resultado.json', 'w'), default=list)
