import sys, re, math, collections
sys.path.insert(0, '/tmp/claude-0/-home-claude/f9be5458-09d6-56eb-b530-4c15adae9be7/scratchpad')
from dbf import load
import pandas as pd

U = '/mnt/user-data/uploads/SIASOFT_V23_OCTOPUX_1/'
REP = "/mnt/user-data/attachments/f9be5458-09d6-56eb-b530-4c15adae9be7/23dd0896-72d459f1-f027-4d53-afb5-0e331f24c3b6.xlsx"
_, cab, _ = load(U + 'RESPALDO_CO_SIA_20261102/CAB_DOC.DBF')
_, cue, _ = load(U + 'RESPALDO_CO_SIA_20261102/CUE_DOC.DBF')
k = lambda r: (r['ANO_DOC'], r['PER_DOC'], r['COD_TRN'], r['NUM_TRN'])
L = collections.defaultdict(list)
for r in cue: L[k(r)].append(r)
hist = [h for h in cab if (h['ANO_DOC'], h['PER_DOC']) < ('2026', '10') and h['COD_TRN'] in ('05', '18')]
octo = [h for h in cab if (h['ANO_DOC'], h['PER_DOC']) == ('2026', '10') and h['COD_TRN'] in ('05', '18')]
EX = re.compile(r'^(2408|2365|2368|1105|1110|1120|22|23)')

def split(ls):
    gasto = [l for l in ls if l['DEB_MOV'] > 0 and not EX.match(l['COD_CTA'])]
    iva = [l for l in ls if l['COD_CTA'].startswith('2408')]
    ret = [l for l in ls if l['COD_CTA'].startswith('2365')]
    return gasto, iva, ret

# ---- reglas por proveedor, aprendidas SOLO con documentos anteriores a octubre de 2026
rules = {}
by = collections.defaultdict(list)
for h in hist:
    ls = L[k(h)]
    ters = collections.Counter(l['COD_TER'] for l in ls if l['COD_TER'])
    if not ters: continue
    by[ters.most_common(1)[0][0]].append((h, ls))
for nit, docs in by.items():
    trn = collections.Counter(h['COD_TRN'] for h, _ in docs)
    gas = collections.Counter(split(ls)[0][0]['COD_CTA'] for _, ls in docs if split(ls)[0])
    rac = collections.Counter(); rate = collections.Counter()
    for _, ls in docs:
        g, i, r = split(ls)
        for l in r:
            rac[l['COD_CTA']] += 1
            if l['BAS_MOV']: rate[round(l['CRE_MOV'] / l['BAS_MOV'], 4)] += 1
    rules[nit] = dict(n=len(docs), trn=trn.most_common(1)[0][0], gasto=gas.most_common(1)[0][0] if gas else None,
                      gasto_share=(gas.most_common(1)[0][1] / sum(gas.values())) if gas else 0,
                      ret_share=sum(rac.values()) / len(docs), ret_cta=rac.most_common(1)[0][0] if rac else None,
                      ret_rate=rate.most_common(1)[0][0] if rate else None)

rep = pd.read_excel(REP, dtype={'NIT Emisor': str, 'NIT Receptor': str, 'Folio': str, 'Prefijo': str})
r = rep[rep.Grupo == 'Recibido'].copy()
r['fecha'] = pd.to_datetime(r['Fecha Emisión'], format='%d-%m-%Y')
r = r.sort_values(['fecha']).reset_index(drop=True)

print("== REGLAS APRENDIDAS DEL HISTORIAL (antes de oct-2026) para los proveedores del REP ==")
for _, x in r.drop_duplicates('NIT Emisor').iterrows():
    q = rules.get(x['NIT Emisor'])
    print(f"  {x['NIT Emisor']:>10} {x['Nombre Emisor'][:26]:<26}", "SIN HISTORIAL (proveedor nuevo)" if not q else
          f"{q['n']:3d} docs | tipo {q['trn']} | gasto {q['gasto']} ({q['gasto_share']:.0%}) | retefuente en {q['ret_share']:.0%} de docs: {q['ret_cta']} tasa {q['ret_rate']}")

# ---- consecutivos: último número antes de octubre por tipo
last = {}
for t, pat in (('05', r'^CP-(\d+)$'), ('18', r'^FC-(\d+)$')):
    n = [int(re.match(pat, h['NUM_TRN']).group(1)) for h in cab if h['COD_TRN'] == t and re.match(pat, h['NUM_TRN']) and (h['ANO_DOC'], h['PER_DOC']) < ('2026', '10')]
    last[t] = max(n) if n else 0
print("\nÚltimo consecutivo antes de octubre:", last)

# ---- generación
gen = []
cnt = dict(last)
for _, x in r.iterrows():
    q = rules.get(x['NIT Emisor'])
    ivaR = x['IVA']; tot = x['Total']
    if not q:
        cnt['05'] += 1
        gen.append(dict(rep=x, flag='proveedor sin historial: no hay regla de cuenta', num_prov=f"CP-{cnt['05']:06d}")); continue
    t = q['trn']
    cnt[t] += 1
    pref = 'CP-' if t == '05' else 'FC-'
    num = f"{pref}{cnt[t]:06d}"
    iva = math.floor(ivaR + 1e-9); total = round(tot)
    gasto = total - iva
    ret = round(gasto * q['ret_rate']) if (q['ret_share'] >= 0.5 and q['ret_rate']) else 0
    lines = [dict(cta=q['gasto'], base=0.0, deb=float(gasto), cre=0.0)]
    if iva: lines.append(dict(cta='24081005', base=float(gasto), deb=float(iva), cre=0.0))
    if ret: lines.append(dict(cta=q['ret_cta'], base=float(gasto), deb=0.0, cre=float(ret)))
    lines.append(dict(cta='11050505', base=0.0, deb=0.0, cre=float(total - ret)))
    gen.append(dict(rep=x, trn=t, num=num, fec=x['fecha'].strftime('%Y%m%d'), factura='FC' + x['Folio'][-4:], ter=x['NIT Emisor'], lines=lines))
import pickle
pickle.dump(dict(gen=gen), open('/tmp/claude-0/-home-claude/f9be5458-09d6-56eb-b530-4c15adae9be7/scratchpad/gen_compras.pkl', 'wb'))

# ---- comparación contra lo registrado
reg = {(h['COD_TRN'], h['NUM_TRN']): h for h in octo}
regl = {key: L[('2026', '10') + key] for key in reg}
tol = 1.0
print("\n== COMPARACIÓN: generado vs registrado (tolerancia ±1 peso) ==")
ok = 0; tot_cmp = 0; used = set()
for g in gen:
    x = g['rep']
    if 'flag' in g:
        print(f"  {x['Prefijo']} {x['Folio']:>8} {x['Fecha Emisión']}  -> DUDA para el contador ({g['flag']}); consecutivo reservado {g['num_prov']}"); continue
    # buscar el registrado equivalente por tercero y valor
    cand = [key for key, ls in regl.items() if key not in used and any(l['COD_TER'] == g['ter'] for l in ls) and abs(sum(l['DEB_MOV'] for l in ls) - x['Total']) < 2]
    cand.sort(key=lambda kk: reg[kk]['FACTURA'] != g['factura'])
    if cand: used.add(cand[0])
    if not cand:
        print(f"  {x['Prefijo']} {x['Folio']:>8} {x['Fecha Emisión']}  -> generado {g['trn']} {g['num']}, SIN registro equivalente (pendiente de contabilizar)"); continue
    key = cand[0]; h = reg[key]; ls = regl[key]
    tot_cmp += 1
    probs = []
    if key[0] != g['trn']: probs.append(f"tipo {key[0]} vs {g['trn']}")
    if key[1] != g['num']: probs.append(f"número {key[1]} vs {g['num']}")
    if h['FEC_DOC'] != g['fec']: probs.append(f"fecha {h['FEC_DOC']} vs {g['fec']}")
    if h['FACTURA'] != g['factura']: probs.append(f"factura {h['FACTURA']} vs {g['factura']}")
    A = {l['COD_CTA']: (l['DEB_MOV'], l['CRE_MOV'], l['BAS_MOV']) for l in ls}
    B = {l['cta']: (l['deb'], l['cre'], l['base']) for l in g['lines']}
    if set(A) != set(B): probs.append(f"cuentas {sorted(A)} vs {sorted(B)}")
    else:
        for c in A:
            if abs(A[c][0] - B[c][0]) > tol or abs(A[c][1] - B[c][1]) > tol: probs.append(f"valor {c}: reg D{A[c][0]:,.0f}/C{A[c][1]:,.0f} vs gen D{B[c][0]:,.0f}/C{B[c][1]:,.0f}")
            elif abs(A[c][2] - B[c][2]) > tol: probs.append(f"base {c}: {A[c][2]:,.0f} vs {B[c][2]:,.0f}")
    if not probs: ok += 1
    print(f"  {x['Prefijo']} {x['Folio']:>8} -> {key[0]} {key[1]}: " + ("COINCIDE" if not probs else "DIFERENCIAS: " + "; ".join(probs)))
print(f"\nDocumentos comparables: {tot_cmp} | coincidencia total: {ok} ({ok/tot_cmp:.0%})" if tot_cmp else "")
