import sys, re, os, json, struct, math
sys.path.insert(0, '/home/claude/work061')
from dbf import load
from armar import parse, recs, get, putc, putn, build
import openpyxl
from collections import Counter, defaultdict

BASE = '/mnt/user-data/uploads/SIASOFT_V23/EMPRESAS/EMP061/CO.SIA/'
PK = '/mnt/user-data/uploads/PAQUETE_ORIGINAL/'
REP = '/mnt/user-data/attachments/01489600-d0fb-5e65-b75c-01f72e009a1d/afa39342-10.OCTUBRE.xlsx'
OUT = '/mnt/user-data/outputs/PARAMO_OCT2026/'
os.makedirs(OUT, exist_ok=True)
rh = lambda x: int(math.floor(x + 0.5 + 1e-9))
nit = lambda s: str(int(float(s))) if isinstance(s, (int, float)) else str(s).strip().replace(' ','').lstrip('0')
idx = lambda a, p: int(a) * 12 + int(p)
num_of = lambda s: int(re.search(r'(\d+)$', s).group(1)) if re.search(r'(\d+)$', s) else 0
UMBRAL = 1750905
RATE = {'236810': 0.00966, '236830': 0.00866, '236805': 0.01104, '23652525': 0.06, '23651505': 0.10, '23653010': 0.035, '23652535': 0.04}

_, cab, _ = load(BASE + 'cab_doc.dbf'); _, cue, _ = load(BASE + 'cue_doc.dbf'); _, ter, _ = load(BASE + 'mae_ter.dbf')
TER = {t['COD_TER'].lstrip('0'): t for t in ter}
cabk = {(c['ANO_DOC'], c['PER_DOC'], c['COD_TRN'], c['NUM_TRN']): c for c in cab}
lines = defaultdict(list)
for l in cue: lines[(l['ANO_DOC'], l['PER_DOC'], l['COD_TRN'], l['NUM_TRN'])].append(l)
ordk = lambda k: (idx(k[0], k[1]), num_of(k[3]))
dudas = []
def duda(area, ref, n, nivel, det): dudas.append((area, ref, n, nivel, det))

# ---------------- REP (Hoja1)
ws = openpyxl.load_workbook(REP, read_only=True, data_only=True)['Hoja1']
rows = list(ws.iter_rows(values_only=True)); H = rows[0]
R = [dict(zip(H, r)) for r in rows[1:] if r[0]]
f = lambda v: float(v or 0)
def fecha(s): d, m, y = s.split('-'); return y + m + d
ME = '901987014'
rds = [r for r in R if r['Prefijo'] == 'DSPC' and str(r['NIT Emisor']) == ME]
rnd = [r for r in R if r['Tipo de documento'] and 'ajuste' in r['Tipo de documento']]
rvt = [r for r in R if r['Grupo'] == 'Emitido' and r['Prefijo'] in ('FEPC', 'NCPC') and str(r['NIT Emisor']) == ME]
rcm = [r for r in R if r['Grupo'] == 'Recibido']

# ---------------- plantilla AGTCOMP1
cb = open(PK + 'AGTCOMP1.cab', 'rb').read(); cu = open(PK + 'AGTCOMP1.cue', 'rb').read(); tb = open(PK + 'AGTCOMP1.Ter', 'rb').read(); fpt = open(PK + 'AGTCOMP1.FPT', 'rb').read()
_, _, _, fc = parse(cb); _, _, _, fu = parse(cu)
tc = recs(cb)[0]; tu = recs(cu)[0]
for k in ('OTRO_TER', 'DETALLE', 'FACTURA', 'FEC_POSF', 'COD_BAN', 'NUM_IMP', 'COD_VEN', 'FIN'): tc = putc(tc, fc, k, '')
for k in ('COD_CIU', 'COD_SUC', 'COD_CCO', 'NUM_CHQ', 'DOC_MOV', 'DOC_CRUC', 'DOC_REF', 'FEC_VENC', 'COD_CON', 'DES_MOV', 'COD_TER', 'ANO_REF'): tu = putc(tu, fu, k, '')
def mk_doc(trn, num, fec, factura='', detalle=''):
    h = tc
    for k, v in (('ANO_DOC', fec[:4]), ('PER_DOC', fec[4:6]), ('COD_TRN', trn), ('NUM_TRN', num), ('FEC_DOC', fec), ('FEC_VEN', fec), ('FACTURA', factura), ('DETALLE', detalle)):
        h = putc(h, fc, k, v)
    return h
def mk_line(trn, num, fec, cta, ter_, des, base, deb, cre, docref='', cruc='', anoref='', saldoc=0):
    r = tu
    for k, v in (('ANO_DOC', fec[:4]), ('PER_DOC', fec[4:6]), ('COD_TRN', trn), ('NUM_TRN', num), ('COD_CTA', cta), ('COD_TER', ter_), ('DES_MOV', des[:50]), ('DOC_REF', docref), ('DOC_CRUC', cruc), ('ANO_REF', anoref)):
        r = putc(r, fu, k, v)
    r = putn(r, fu, 'BAS_MOV', float(base)); r = putn(r, fu, 'DEB_MOV', float(deb)); r = putn(r, fu, 'CRE_MOV', float(cre))
    if saldoc: r = putn(r, fu, 'SAL_DOC', float(saldoc))
    return r

# ---------------- historial de documento soporte
EXG_RET = ('2365', '2368')
def ds_hist_docs():
    out = []
    for k, ls in lines.items():
        if k[2] != '05A': continue
        p = [l for l in ls if l['COD_CTA'] == '220505']
        gl = [l for l in ls if l['DEB_MOV'] > 0]
        if not p or not gl: continue
        out.append(dict(k=k, i=idx(k[0], k[1]), n=num_of(k[3]), ter=p[0]['COD_TER'].lstrip('0'), base=sum(l['DEB_MOV'] for l in gl), gas=gl[0]['COD_CTA'],
                        ret=frozenset(l['COD_CTA'] for l in ls if l['CRE_MOV'] > 0 and l['COD_CTA'] != '220505'), det=cabk[k]['DETALLE'].strip(), lines=ls))
    return sorted(out, key=lambda d: (d['i'], d['n']))
DSH = ds_hist_docs()
# DS anulados por nota de ajuste (mismo tercero y valor)
nds = []
for k, ls in lines.items():
    if k[2] == '08A': nds.append((ls[0]['COD_TER'].lstrip('0'), sum(l['DEB_MOV'] for l in ls), idx(k[0], k[1]), num_of(k[3])))
ann = set()
for t, a, i, n in sorted(nds, key=lambda x: (x[2], x[3])):
    c = [d for d in DSH if d['ter'] == t and abs(d['base'] - a) < 1 and d['i'] <= i and d['k'] not in ann]
    if c: ann.add(max(c, key=lambda d: (d['i'], d['n']))['k'])
CLEAN = [d for d in DSH if d['k'] not in ann]
STD = ('5135', '5235')
def ds_predict(ter_, base, hist):
    h = [d for d in hist if d['ter'] == ter_]
    last = h[-1] if h else None
    note = ''
    if last and last['gas'][:4] not in STD:
        return last['gas'], set(last['ret']), last, 'replica'
    prefix = last['gas'][:4] if last else '5135'
    if base <= UMBRAL: gas, ret = prefix + '15', {'23652525', '236810'}
    else: gas, ret = prefix + '17', {'236810'}
    return gas, ret, last, 'regla'
# backtest septiembre (aprendiendo solo lo anterior, sin anulados)
bt = Counter()
for d in [x for x in CLEAN if x['i'] == idx(2026, 9)]:
    hist = [x for x in CLEAN if (x['i'], x['n']) < (d['i'], d['n'])]
    gas, ret, last, mode = ds_predict(d['ter'], d['base'], hist)
    ok = gas == d['gas'] and (set(ret) - {'236810'}) == (set(d['ret']) - {'236810', '236830', '236805'})
    bt['exacto' if ok else 'gasto ok, ret dif' if gas == d['gas'] else 'dif'] += 1
print('BACKTEST DS septiembre (limpios):', dict(bt), 'de', sum(bt.values()))

# ---------------- emparejar notas de ajuste con el DS que anulan (regla de Daniel 3-nov: DS y nota anulados van SIN retenciones)
rep_ds = [(nit(x['NIT Receptor']), rh(f(x['Total'])), int(x['Folio']), fecha(x['Fecha Emisión'])) for x in rds]
anul_folio = {}; nd_match = {}
for x in sorted(rnd, key=lambda r: int(re.search(r'(\d+)$', str(r['Folio'])).group(1))):
    refn = str(x['Folio']).strip(); tn = nit(x['NIT Receptor']); an_ = rh(f(x['Total'])); fn = fecha(x['Fecha Emisión'])
    cc = [r for r in rep_ds if r[0] == tn and r[1] == an_ and r[2] not in anul_folio and r[3] <= fn]
    if cc:
        o_ = max(cc, key=lambda r: (r[3], r[2])); anul_folio[o_[2]] = refn; nd_match[refn] = o_[2]
print('ND emparejadas con DS del REP:', len(nd_match), 'de', len(rnd))

# ---------------- DS octubre
ds_docs = []; ds_by_folio = {}
for x in sorted(rds, key=lambda r: int(r['Folio'])):
    fol = int(x['Folio']); num = 'DS' + str(fol)
    fec = fecha(x['Fecha Emisión']); t = nit(x['NIT Receptor']); base = rh(f(x['Total']))
    if ('2026', fec[4:6], '05A', num) in cabk: continue
    hist = CLEAN + [d for d in ds_docs if not d['anul']]
    gas, ret, last, mode = ds_predict(t, base, hist)
    ref = f'DSPC{fol}'
    an = fol in anul_folio
    if an: ret = set(); duda('DS', ref, t, 'INFO', f'anulado por {anul_folio[fol]}: sin ICA ni retencion (regla de Daniel)')
    if an: pass
    elif t not in TER: duda('DS', ref, t, 'ALTA', 'tercero nuevo: cargar con el 766; cuenta ' + gas + ' propuesta por la regla de valor, sin historial')
    elif last is None: duda('DS', ref, t, 'ALTA', f'tercero sin documentos soporte en el historial; cuenta {gas} por la regla de valor')
    elif mode == 'regla' and (last['gas'], set(last['ret'])) != (gas, ret) and not (last['gas'] == gas):
        duda('DS', ref, t, 'MEDIA', f'regla de valor ({base:,}) propone {gas}; el ultimo documento del tercero uso {last["gas"]}')
    elif mode == 'regla' and last['gas'] == gas and ('23652525' in last['ret']) != ('23652525' in ret):
        duda('DS', ref, t, 'MEDIA', f'cuenta {gas} igual al ultimo documento pero la retefuente difiere (ultimo: {"con" if "23652525" in last["ret"] else "sin"})')
    elif mode == 'replica': duda('DS', ref, t, 'MEDIA', f'cuenta especial {gas} del tercero, se replico su ultimo documento')
    if mode == 'regla' and not an and 0.92 * UMBRAL <= base <= 1.08 * UMBRAL: duda('DS', ref, t, 'MEDIA', f'valor {base:,} cerca del salario minimo 2026 ({UMBRAL:,}): la regla propone {gas}; confirmar si lleva retefuente')
    det = (last['det'] if last and last['det'] else 'SERVICIO DE DIGITACION')[:40]
    if last and last['det'] and last['det'] != 'SERVICIO DE DIGITACION' and mode == 'regla': duda('DS', ref, t, 'INFO', f'DETALLE tomado del ultimo documento del tercero: {det}')
    des = (ref + ' ' + det)[:50]
    rl = {c: rh(base * RATE[c]) for c in sorted(ret) if c != '236810'}
    ica = rh(base * RATE['236810']) if '236810' in ret else 0
    neto = base - sum(rl.values()) - ica
    ls_ = [mk_line('05A', num, fec, gas, t, des, 0, base, 0)]
    for c, v in rl.items(): ls_.append(mk_line('05A', num, fec, c, t, des, base, 0, v))
    if ica: ls_.append(mk_line('05A', num, fec, '236810', t, des, base, 0, ica))
    ls_.append(mk_line('05A', num, fec, '220505', t, des, 0, 0, neto, docref=ref))
    d = dict(ref=ref, num=num, fec=fec, ter=t, base=base, gas=gas, det=det, anul=an, ret=frozenset(ret), rl=rl, ica=ica, neto=neto, h=mk_doc('05A', num, fec, factura=ref, detalle=det), ls=ls_,
             k=('2026', fec[4:6], '05A', num), i=idx(fec[:4], fec[4:6]), n=fol, lines_mirror=[(c, 'C' if c == gas else 'D', 0) for c in []], mirror=ls_)
    ds_docs.append(d); ds_by_folio[fol] = d
# ---------------- ND octubre (nota de ajuste del DS)
nd_docs = []
used_orig = set(ann)
def cands(t, amt):
    c = [d for d in DSH if d['ter'] == t and abs(d['base'] - amt) < 1 and d['k'] not in used_orig]
    c += [d for d in ds_docs if d['ter'] == t and abs(d['base'] - amt) < 1 and d['k'] not in used_orig]
    return c
for x in sorted(rnd, key=lambda r: int(re.search(r'(\d+)$', str(r['Folio'])).group(1))):
    fol = int(re.search(r'(\d+)$', str(x['Folio'])).group(1)); num = 'ND' + str(fol); ref = str(x['Folio']).strip()
    fec = fecha(x['Fecha Emisión']); t = nit(x['NIT Receptor']); amt = rh(f(x['Total']))
    if ('2026', fec[4:6], '08A', num) in cabk: continue
    c = [ds_by_folio[nd_match[ref]]] if ref in nd_match and nd_match[ref] in ds_by_folio else cands(t, amt)
    des = (ref + ' ANULACION')[:50]
    if t not in TER: duda('ND', ref, t, 'ALTA', 'tercero nuevo: cargar con el 766')
    if c:
        o = max(c, key=lambda d: (d['i'], d['n'])); used_orig.add(o['k'])
        okey = o['k']; onum = okey[3]; oano = okey[0] + okey[1] + okey[2]
        ols = o['mirror'] if 'mirror' in o else o['lines']
        ls_ = []
        for l in (ols if isinstance(ols[0], dict) else []):
            pass
        # reconstruir lineas del original (sistema: dict; generado: bytes) -> usar datos de cuenta/valores
        if 'mirror' in o:
            spec = [('gas', o['gas'], o['base'])] + [('ret', c_, v) for c_, v in o['rl'].items()] + ([('ret', '236810', o['ica'])] if o['ica'] else []) + [('cx', '220505', o['neto'])]
        else:
            spec = []
            for l in o['lines']:
                if l['COD_CTA'] == '220505': spec.append(('cx', '220505', l['CRE_MOV']))
                elif l['DEB_MOV'] > 0: spec.append(('gas', l['COD_CTA'], l['DEB_MOV']))
                else: spec.append(('ret', l['COD_CTA'], l['CRE_MOV']))
        for kind, cta, v in spec:
            if kind == 'gas': ls_.append(mk_line('08A', num, fec, cta, t, des, 0, 0, v))
            elif kind == 'ret': ls_.append(mk_line('08A', num, fec, cta, t, des, o['base'], v, 0))
            else: ls_.append(mk_line('08A', num, fec, cta, t, des, 0, v, 0, docref=onum, cruc=onum, anoref=oano, saldoc=v))
        tot_d = sum(float(l_[2]) for l_ in []) if False else None
        duda('ND', ref, t, 'INFO', f'anula el {onum} (mismo tercero y valor {amt:,})' + (' [DS que se genera en este lote]' if 'mirror' in o else ''))
        if sum(1 for k_, c_, v in spec if k_ == 'ret') and 'mirror' in o: duda('ND', ref, t, 'MEDIA', f'el {onum} tiene retenciones; la nota las reversa completas (neto {o["neto"]:,}, REP trae {amt:,} = base)')
        gas = o['gas']
    else:
        h = [d for d in CLEAN if d['ter'] == t]; gas = h[-1]['gas'] if h else '513517'
        ls_ = [mk_line('08A', num, fec, gas, t, des, 0, 0, amt), mk_line('08A', num, fec, '220505', t, des, 0, amt, 0)]
        duda('ND', ref, t, 'ALTA', f'no encontre el DS original (mismo tercero y valor {amt:,}); la deje sin cruce, cuenta {gas}')
    nd_docs.append(dict(ref=ref, num=num, fec=fec, ter=t, amt=amt, h=mk_doc('08A', num, fec, factura=ref), ls=ls_))

# ---------------- VENTAS (04) y nota credito
ven_hist = defaultdict(list)
for k in sorted([k for k in lines if k[2] in ('04', '08') and k[0] == '2026'], key=ordk):
    ls = lines[k]; cl = [l for l in ls if l['COD_CTA'].startswith('1305')]
    if cl: ven_hist[cl[0]['COD_TER'].strip().lstrip('0')].append((k, ls))
vt_docs = []
vt_sorted = sorted([x for x in rvt if x['Prefijo'] == 'FEPC'], key=lambda r: int(r['Folio']))
for x in vt_sorted:
    fol = int(x['Folio']); num = 'FEPC' + str(fol); fec = fecha(x['Fecha Emisión']); t = nit(x['NIT Receptor'])
    if ('2026', fec[4:6], '04', num) in cabk: continue
    tot = rh(f(x['Total'])); iva = rh(f(x['IVA']))
    h = [(k, ls) for k, ls in ven_hist.get(t, []) if k[2] == '04']
    if t not in TER: duda('Ventas', num, t, 'ALTA', 'cliente nuevo: cargar con el 766')
    if iva: duda('Ventas', num, t, 'ALTA', f'IVA {iva:,} distinto de cero: estas ventas no han tenido IVA; revisar estructura')
    if h:
        k0, l0 = h[-1]
        ing = [l for l in l0 if l['CRE_MOV'] > 0 and not l['COD_CTA'].startswith('2408')][0]['COD_CTA']
        cart = [l for l in l0 if l['COD_CTA'].startswith('1305')][0]['COD_CTA']
        rets = [(l['COD_CTA'], round(l['DEB_MOV'] / l['BAS_MOV'], 5)) for l in l0 if l['COD_CTA'].startswith('1355') and l['BAS_MOV']]
        suf = (l0[0]['DES_MOV'][len(k0[3]) + 1:] if l0[0]['DES_MOV'].startswith(k0[3]) else '').strip()
        niv = 'alta' if len({tuple(l['COD_CTA'] for l in ls) for k, ls in h[-3:]}) == 1 else 'media'
        if niv == 'media': duda('Ventas', num, t, 'MEDIA', 'la estructura de las ultimas 3 ventas del cliente no coincide; use la ultima')
    else:
        ing, cart, rets, suf = '417005', '13050506', [], ''
        duda('Ventas', num, t, 'ALTA', 'cliente sin ventas en 2026: cuentas 417005/13050506 supuestas (exportacion sin retenciones)')
    base = tot; rv = {c: rh(base * r) for c, r in rets}
    cartv = base - sum(rv.values()); des = (num + ' ' + suf)[:50]
    ls_ = [mk_line('04', num, fec, ing, t, des, 0, 0, base)] + [mk_line('04', num, fec, c, t, des, base, v, 0) for c, v in rv.items()] + [mk_line('04', num, fec, cart, t, des, 0, cartv, 0, docref=num)]
    vt_docs.append(dict(num=num, fec=fec, ter=t, base=base, ing=ing, cart=cart, ret=rv, deb=cartv, h=mk_doc('04', num, fec), ls=ls_))

# ---------------- COMPRAS (05): detectar las ya registradas y generar las faltantes
sis_cp = [(k, ls) for k, ls in lines.items() if k[2] == '05' and k[0] == '2026' and k[1] == '10']
def registrada(x):
    t = nit(x['NIT Emisor']); dig = re.sub(r'\D', '', str(x['Folio'])); tot = f(x['Total'])
    for k, ls in sis_cp:
        if not any(l['COD_TER'].strip().lstrip('0') == t for l in ls): continue
        fac = re.sub(r'\D', '', cabk[k]['FACTURA'])
        if dig.endswith(fac) or fac.endswith(dig) or abs(sum(l['DEB_MOV'] for l in ls) - tot) < 2: return k
    return None
EXG = re.compile(r'^(2408|2365|2368|1105|1110|1120|2205)')
by = defaultdict(list)
for k, ls in lines.items():
    if k[2] != '05': continue
    gas = [l for l in ls if l['DEB_MOV'] > 0 and not EXG.match(l['COD_CTA'])]
    ters = Counter(l['COD_TER'].strip().lstrip('0') for l in ls if l['COD_TER'].strip())
    if not gas or not ters: continue
    by[ters.most_common(1)[0][0]].append((k, ls, gas[0]['COD_CTA']))
for v in by.values(): v.sort(key=lambda x: ordk(x[0]))
cp = max(num_of(k[3]) for k in lines if k[2] == '05' and k[3].startswith('CP-'))
cm_docs = []; ya = []; held = []
MANUAL = {'FVE-739': dict(acc='524540', ctra='11050505', det='SERVICIO AUTOMOTRIZ')}  # decision Daniel 3-nov: caja, cuenta 52, sin retefuente por ahora (pendiente RUT)
for x in sorted(rcm, key=lambda r: (fecha(r['Fecha Emisión']), int(re.sub(r'\D', '', str(r['Folio'])) or 0))):
    k = registrada(x); ref = f"{x['Prefijo']}-{x['Folio']}"
    if k: ya.append((ref, k[3])); continue
    t = nit(x['NIT Emisor']); fec = fecha(x['Fecha Emisión']); tot = rh(f(x['Total'])); iva = rh(f(x['IVA']))
    h = by.get(t, [])
    man = MANUAL.get(ref)
    if not h and not man:
        held.append((ref, t, tot)); duda('Compras', ref, t, 'ALTA', 'proveedor sin compras en el historial: NO generada; definir cuenta de gasto'); continue
    if man: k0, l0, acc = None, [], man['acc']; duda('Compras', ref, t, 'MEDIA', 'sin retefuente por decision de Daniel; confirmar con el RUT (autorretenedor/gran contribuyente)')
    else: k0, l0, acc = h[-1]
    rets = [(l['COD_CTA'], round(l['CRE_MOV'] / l['BAS_MOV'], 5)) for l in l0 if l['COD_CTA'].startswith(EXG_RET) and l['BAS_MOV']]
    ctrap = [l['COD_CTA'] for l in l0 if l['CRE_MOV'] > 0 and l['COD_CTA'] in ('220505', '11050505')]
    ctra = man['ctra'] if man else (ctrap[0] if ctrap else '220505')
    niv = 'alta' if man else 'alta' if len({(a, tuple(sorted(r_))) for _, _, a in h[-3:] for r_ in [()]}) == 1 and len({a for _, _, a in h[-3:]}) == 1 else 'baja'
    if niv == 'baja': duda('Compras', ref, t, 'BAJA', f'el proveedor uso varias cuentas en sus ultimas compras; use la ultima ({acc})')
    cp += 1; num = f'CP-{cp:06d}'
    taxable = tot - iva; gasto = taxable
    ivacta = None
    if iva:
        ratio = iva / taxable if taxable else 0
        ivacta = '24081005' if abs(ratio - 0.19) < 0.003 else '24081005'
        if abs(ratio - 0.19) >= 0.003: duda('Compras', ref, t, 'ALTA', f'IVA {iva:,} sobre base {taxable:,} = {ratio:.1%}: tarifa atipica')
    rv = {c: rh(taxable * r) for c, r in rets}
    if rv: duda('Compras', ref, t, 'MEDIA', 'retenciones por historial del proveedor: ' + ', '.join(f'{c} {r:.3%}' for c, r in rets))
    dig = re.sub(r'\D', '', str(x['Folio'])); fac = 'FC' + dig[-8:]
    det = man['det'] if man else cabk[k0]['DETALLE'].strip()[:40]
    des = (fac + ' ' + det)[:50]
    if f(x['IVA']) != iva: duda('Compras', ref, t, 'INFO', f'IVA REP {f(x["IVA"]):,.2f} redondeado a {iva:,} (peso mas cercano); gasto = total - IVA')
    if ctra == '11050505': duda('Compras', ref, t, 'INFO', 'contrapartida caja 11050505 segun el ultimo documento del proveedor')
    ls_ = [mk_line('05', num, fec, acc, t, des, 0, gasto, 0)]
    if ivacta: ls_.append(mk_line('05', num, fec, ivacta, t, des, taxable, iva, 0))
    for c, v in rv.items(): ls_.append(mk_line('05', num, fec, c, t, des, taxable, 0, v))
    ls_.append(mk_line('05', num, fec, ctra, t, des, 0, 0, tot - sum(rv.values()), docref=fac if ctra == '220505' else ''))
    cm_docs.append(dict(num=num, ref=ref, fec=fec, ter=t, tot=tot, iva=iva, acc=acc, h=mk_doc('05', num, fec, factura=fac, detalle=det), ls=ls_))

# ---------------- TERCEROS NUEVOS (766)
T0 = open(PK + 'TERVTAORI.DBF', 'rb').read(); TF = open(PK + 'TERVTAORI.FPT', 'rb').read(); _, thl, _, ft = parse(T0); tmpl = recs(T0)[0]
dst = {d['ter'] for d in DSH if d['ter'] in TER}
FL = [k for k in ('TIP_PRV', 'CLASIFIC', 'IND_RETE', 'IND_RET', 'AUT_RET', 'ESTADO', 'JURID', 'IND_CRED', 'IND_COBRO', 'MAYMIN', 'CIUDAD', 'COD_CIU', 'DPTO', 'MUN', 'PAIS', 'IND_CREE', 'TDOC', 'TIP_PERS', 'DIA_PLAZ', 'POR_DES', 'POR_ICA', 'INT_MORA') if k in ft]
modes = {}
for k in FL:
    cnt = Counter(str(TER[n][k]) for n in dst if k in TER[n])
    if cnt:
        v, c = cnt.most_common(1)[0]
        if c / len(dst) >= 0.6: modes[k] = v
print('terceros DS existentes (modelo):', len(dst), '| campos por moda:', {k: modes[k] for k in modes})
nat = [t for t in ter if str(t['TIP_PERS']) == '1.0' and t['TDOC'] == '13']
dv_blank = sum(1 for t in nat if not str(t.get('DV', '')).strip()) / max(1, len(nat))
def dvf(n):
    w = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]; s = sum(int(c) * w[i] for i, c in enumerate(reversed(n))); r = s % 11
    return str(r if r < 2 else 11 - r)
nuevos = {}
for x in rds:
    n = nit(x['NIT Receptor']); nuevos[n] = (re.sub(r'\s+', ' ', str(x['Nombre Receptor']).strip()).upper(), 'DS')
for x in rnd + rvt:
    n = nit(x['NIT Receptor']); nuevos.setdefault(n, (re.sub(r'\s+', ' ', str(x['Nombre Receptor']).strip()).upper(), 'VTA/ND'))
for x in rcm:
    n = nit(x['NIT Emisor']); nuevos.setdefault(n, (re.sub(r'\s+', ' ', str(x['Nombre Emisor']).strip()).upper(), 'COMPRA'))
nuevos = {n: v for n, v in nuevos.items() if n not in TER and n != ME}
trows = []
for n, (nm, orig) in sorted(nuevos.items()):
    num_ = n.isdigit() or n.startswith('PPT'); jur = num_ and len(n) == 9 and n[0] in '89'
    r = tmpl
    for k, v in modes.items():
        if ft[k][2] == 'C': r = putc(r, ft, k, v)
        elif ft[k][2] == 'N': r = putn(r, ft, k, float(v), ft[k][3])
    for k in ('NOM_TER', 'RAZ', 'REPRES'): r = putc(r, ft, k, nm)
    tdoc = '31' if jur else '13' if num_ else '42'
    for k, v in (('COD_TER', n), ('TDOC', tdoc), ('DIR1', ''), ('DIR', ''), ('TEL1', ''), ('EMAIL', ''), ('FEC_ING', '20261103'), ('TIP_PERS', '2' if jur else '1'), ('NOM1', ''), ('NOM2', ''), ('APL1', ''), ('APL2', '')):
        if k in ft: r = putc(r, ft, k, v)
    if 'DV' in ft: r = putc(r, ft, 'DV', dvf(n) if (n.isdigit() and (jur or dv_blank < 0.5)) else '')
    if not jur:
        t_ = nm.split()
        if len(t_) == 4: a1, a2, n1, n2 = t_
        elif len(t_) == 3: a1, a2, n1, n2 = t_[0], t_[1], t_[2], ''
        elif len(t_) == 2: a1, a2, n1, n2 = t_[0], '', t_[1], ''
        else: a1, a2, n1, n2 = t_[0], '', ' '.join(t_[1:]), ''
        for k, v in (('NOM1', n1), ('NOM2', n2), ('APL1', a1), ('APL2', a2)):
            if k in ft: r = putc(r, ft, k, v)
        if len(t_) != 4: duda('Terceros', n, n, 'BAJA', f'persona natural de {len(t_)} palabras: separe apellidos y nombres asumiendo APELLIDO1 APELLIDO2 NOMBRE1 (orden del REP y del maestro actual)')
    trows.append(r)
th = bytearray(T0[:thl]); th[4:8] = struct.pack('<I', len(trows))

files = {}
def addset(pref, docs):
    files[pref + '.cab'] = build(cb, [d['h'] for d in docs]); files[pref + '.cue'] = build(cu, [l for d in docs for l in d['ls']])
    files[pref + '.Ter'] = build(tb, []); files[pref + '.FPT'] = fpt
addset('PARDSO10', ds_docs); addset('PARNDO10', nd_docs); addset('PARVTA10', vt_docs); addset('PARCOM10', cm_docs)
files['TERPARAMO10.DBF'] = bytes(th) + b''.join(trows) + b'\x1a'; files['TERPARAMO10.FPT'] = TF
for n_, d_ in files.items(): open(OUT + n_, 'wb').write(d_)

# ---------------- resumen
def tot(docs, key): return sum(d[key] for d in docs)
print('DS generados:', len(ds_docs), '| base', tot(ds_docs, 'base'), '| ICA', tot(ds_docs, 'ica'), '| retefuente', sum(sum(d['rl'].values()) for d in ds_docs), '| neto 220505', tot(ds_docs, 'neto'))
print('   cuentas:', Counter(d['gas'] for d in ds_docs), '| con retefuente:', sum(1 for d in ds_docs if d['rl']))
print('ND generadas:', len(nd_docs), '| total', tot(nd_docs, 'amt'))
print('VENTAS generadas:', len(vt_docs), [(d['num'], d['base'], d['ing'], d['cart'], d['ret']) for d in vt_docs])
print('COMPRAS ya registradas:', ya, '| generadas:', [(d['num'], d['ref'], d['tot'], d['iva'], d['acc']) for d in cm_docs], '| retenidas:', held)
print('TERCEROS nuevos:', len(trows), dict(Counter(v[1] for v in nuevos.values())))
print('DUDAS:', len(dudas), dict(Counter((d[0], d[3]) for d in dudas)))
json.dump(dict(dudas=dudas, nuevos={k: v for k, v in nuevos.items()}), open('/home/claude/work061/resultado_paramo.json', 'w'), default=list)

# ---------------- reporte de revision (sin nombres de terceros)
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
wb = Workbook(); hdr = Font(bold=True, color='FFFFFF'); fill = PatternFill('solid', fgColor='305496')
def sheet(name, head, data, widths=None):
    w = wb.create_sheet(name); w.append(head)
    for c in w[1]: c.font = hdr; c.fill = fill; c.alignment = Alignment(wrap_text=True, vertical='center')
    for r in data: w.append(list(r))
    for i, c in enumerate(head): w.column_dimensions[chr(65 + i)].width = (widths or {}).get(i, max(12, min(60, len(str(c)) + 4)))
    w.freeze_panes = 'A2'; return w
wb.remove(wb.active)
niv = {'ALTA': 0, 'MEDIA': 1, 'BAJA': 2, 'INFO': 3}
res = [('Documento soporte (05A)', f'{ds_docs[0]["num"]} a {ds_docs[-1]["num"]}', len(ds_docs), tot(ds_docs, 'base'), 'Base = total del REP; ICA y retefuente al peso mas cercano'),
       ('Notas de ajuste DS (08A)', f'{nd_docs[0]["num"]} a {nd_docs[-1]["num"]}', len(nd_docs), tot(nd_docs, 'amt'), 'Cruzadas con el DS que anulan'),
       ('Ventas (04)', ', '.join(d['num'] for d in vt_docs), len(vt_docs), tot(vt_docs, 'base'), 'FEPC29, FEPC30 y NCPC-2 ya estaban'),
       ('Compras (05)', ', '.join(d['num'] for d in cm_docs), len(cm_docs), tot(cm_docs, 'tot'), '9 ya registradas; FVE-739 manual (524540, caja, sin retefuente)'),
       ('Terceros nuevos (766)', 'TERPARAMO10.DBF', len(trows), '', 'DS: 1, compra: 1')]
sheet('Resumen', ['Concepto', 'Rango', 'Documentos', 'Valor', 'Nota'], res, {0: 28, 1: 40, 2: 12, 3: 18, 4: 60})
sheet('Dudas', ['Area', 'Referencia', 'NIT', 'Nivel', 'Detalle'], sorted(dudas, key=lambda d: (niv[d[3]], d[0], d[1])), {0: 10, 1: 22, 2: 14, 3: 8, 4: 110})
sheet('DS', ['Documento', 'DSPC', 'NIT', 'Valor', 'Cuenta gasto', 'Retefuente', 'ICA', 'Neto 220505', 'Existia el tercero'], [(d['num'], d['ref'], d['ter'], d['base'], d['gas'], sum(d['rl'].values()), d['ica'], d['neto'], 'si' if d['ter'] in TER else 'NO') for d in ds_docs])
sheet('ND', ['Documento', 'NAPC', 'NIT', 'Valor'], [(d['num'], d['ref'], d['ter'], d['amt']) for d in nd_docs])
sheet('Ventas', ['Documento', 'NIT', 'Ingreso', 'Cartera', 'Base', 'Retenciones', 'Debito cartera'], [(d['num'], d['ter'], d['ing'], d['cart'], d['base'], sum(d['ret'].values()), d['deb']) for d in vt_docs])
sheet('Compras', ['Documento', 'REP', 'NIT', 'Total', 'IVA', 'Cuenta gasto'], [(d['num'], d['ref'], d['ter'], d['tot'], d['iva'], d['acc']) for d in cm_docs] + [('(retenida)', r_, t_, v_, '', '') for r_, t_, v_ in held])
sheet('Compras ya registradas', ['REP', 'Documento en sistema'], ya)
wb.save(OUT + 'REVISION_PARAMO_OCT2026.xlsx')
print('xlsx ok')
