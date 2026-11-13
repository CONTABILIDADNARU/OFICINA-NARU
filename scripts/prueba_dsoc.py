import sys, re, math, collections
sys.path.insert(0, '/tmp/claude-0/-home-claude/f9be5458-09d6-56eb-b530-4c15adae9be7/scratchpad')
from dbf import load
import pandas as pd

U = '/mnt/user-data/uploads/SIASOFT_V23_OCTOPUX_1/SIASOFT_V23_OCTOPUX/EXPORT/'
REP = "/mnt/user-data/attachments/f9be5458-09d6-56eb-b530-4c15adae9be7/23dd0896-72d459f1-f027-4d53-afb5-0e331f24c3b6.xlsx"
_, cab, _ = load(U + 'COOct312026.cab'); _, cue, _ = load(U + 'COOct312026.cue')
k = lambda r: (r['COD_TRN'], r['NUM_TRN'])
L = collections.defaultdict(list)
for r in cue: L[k(r)].append(r)
reg = {int(h['NUM_TRN'][4:]): h for h in cab if h['COD_TRN'] == '05A'}

rep = pd.read_excel(REP, dtype={'NIT Emisor': str, 'NIT Receptor': str, 'Folio': str, 'Prefijo': str})
d = rep[rep['Tipo de documento'] == 'Documento soporte con no obligados'].copy()
d['f'] = d.Folio.astype(int); d = d.sort_values('f')
na = rep[rep['Tipo de documento'] == 'Nota de ajuste del documento soporte']

# ---------- 1) aprender reglas SOLO con los folios 1..10
def parts(ls):
    g = [l for l in ls if l['COD_CTA'].startswith('5135')][0]
    rf = [l for l in ls if l['COD_CTA'].startswith('2365')]
    ri = [l for l in ls if l['COD_CTA'].startswith('2368')]
    cj = [l for l in ls if l['COD_CTA'].startswith('1105')]
    return g, rf, ri, cj
learn = [f for f in range(1, 11)]
rf_acc = collections.Counter(); ri_acc = collections.Counter(); rf_rate = collections.Counter(); ri_rate = collections.Counter(); det = collections.Counter(); gac = collections.Counter(); cj_acc = collections.Counter()
for f in learn:
    h = reg[f]; ls = L[k(h)]; g, rf, ri, cj = parts(ls)
    gac[g['COD_CTA']] += 1; det[h['DETALLE']] += 1
    if rf: rf_acc[rf[0]['COD_CTA']] += 1; rf_rate[round(rf[0]['CRE_MOV'] / g['DEB_MOV'], 4)] += 1
    if ri: ri_acc[ri[0]['COD_CTA']] += 1; ri_rate[round(ri[0]['CRE_MOV'] / g['DEB_MOV'] * 1000, 2)] += 1
    cj_acc[cj[0]['COD_CTA']] += 1
R = dict(gasto=gac.most_common(1)[0][0], rf_cta=rf_acc.most_common(1)[0][0], rf=rf_rate.most_common(1)[0][0],
         ri_cta=ri_acc.most_common(1)[0][0], ri=ri_rate.most_common(1)[0][0] / 1000, caja=cj_acc.most_common(1)[0][0], det=det.most_common(1)[0][0])
print("Reglas aprendidas con los folios 1-10:", R)
print("DETALLE en los 102 registrados:", collections.Counter(h['DETALLE'] for h in reg.values()).most_common(3))

# ---------- 2) identificar el DSOC anulado por la nota de ajuste
anul = {}
for _, n in na.iterrows():
    m = d[(d['NIT Receptor'] == n['NIT Receptor']) & (abs(d.Total - n.Total) < 1)]
    print(f"Nota {n['Folio']}: receptor {n['NIT Receptor']} total {n.Total:,.0f} -> DSOC candidatos:", list(m.f))
    if len(m) == 1: anul[int(m.f.iloc[0])] = n

# ---------- 3) generar los 102 + nota y comparar
def gen_dsoc(x):
    f = int(x.f); tot = int(round(x.Total)); fec = pd.to_datetime(x['Fecha Emisión'], format='%d-%m-%Y').strftime('%Y%m%d')
    base = dict(num=f"DSOC{f:05d}", factura=f"DSOC{f}", fec=fec, ter=x['NIT Receptor'], det=R['det'])
    if f in anul:
        base['lines'] = {R['gasto']: (tot, 0), '220505': (0, tot)}
    else:
        rf = round(tot * R['rf']); ri = round(tot * R['ri'])
        base['lines'] = {R['gasto']: (tot, 0), R['rf_cta']: (0, rf), R['ri_cta']: (0, ri), R['caja']: (0, tot - rf - ri)}
    return base

tol = 1
cat = collections.defaultdict(list); exact = 0
for _, x in d.iterrows():
    g = gen_dsoc(x); h = reg[int(x.f)]; ls = L[k(h)]
    A = collections.defaultdict(lambda: [0, 0])
    for l in ls: A[l['COD_CTA']][0] += l['DEB_MOV']; A[l['COD_CTA']][1] += l['CRE_MOV']
    p = []
    if {l['COD_TER'] for l in ls} != {g['ter']}: p.append(('tercero', f"registrado {sorted({l['COD_TER'] for l in ls})} vs DIAN {g['ter']}"))
    if h['FEC_DOC'] != g['fec']: p.append(('fecha', f"registrado {h['FEC_DOC']} vs DIAN {g['fec']}"))
    if h['FACTURA'] != g['factura']: p.append(('factura', f"{h['FACTURA']} vs {g['factura']}"))
    if h['DETALLE'] != g['det']: p.append(('detalle', f"{h['DETALLE']!r} vs {g['det']!r}"))
    if set(A) != set(g['lines']): p.append(('cuentas', f"{sorted(A)} vs {sorted(g['lines'])}"))
    else:
        for c, (dd, cc) in g['lines'].items():
            if abs(A[c][0] - dd) > tol or abs(A[c][1] - cc) > tol: p.append(('valor', f"{c}: reg D{A[c][0]:,.0f}/C{A[c][1]:,.0f} vs gen D{dd:,.0f}/C{cc:,.0f}"))
    if not p: exact += 1
    for t, m in p: cat[t].append((int(x.f), m))
print(f"\n== DOCUMENTOS SOPORTE: generados 102 vs registrados ==")
print(f"Coinciden en todo (±1 peso): {exact} de {len(d)} ({exact/len(d):.1%})")
for t, v in cat.items():
    print(f"\nDiferencias de tipo '{t}': {len(v)} docs")
    for f, m in v[:8]: print(f"   DSOC {f}: {m}")
docs_con_dif = {f for v in cat.values() for f, _ in v}
solo_typo_fecha = {f for f in docs_con_dif if all(t in ('tercero', 'fecha') for t, ff in [(t, f2) for t, vv in cat.items() for f2, _ in vv if f2 == f])}
print(f"\nDocs que difieren SOLO por tercero o fecha (errores de digitación/criterio del registro): {len(solo_typo_fecha)}")
print(f"Docs con otras diferencias (error del generador o excepción real): {len(docs_con_dif - solo_typo_fecha)} -> {sorted(docs_con_dif - solo_typo_fecha)}")

# nota de ajuste
for _, n in na.iterrows():
    h = [h for h in cab if h['COD_TRN'] == '08A'][0]; ls = L[('08A', h['NUM_TRN'])]
    f = [ff for ff in anul if anul[ff].equals(n)]
    print(f"\nNota de ajuste: REP {n['Folio']} ({n.Total:,.0f}) | registrada {h['NUM_TRN']} fec {h['FEC_DOC']} det {h['DETALLE']!r} | anula DSOC {f}")
    print("  generada: D 220505 / C 513515 por", f"{n.Total:,.0f}", "| registrada:", [(l['COD_CTA'], l['DEB_MOV'], l['CRE_MOV']) for l in ls], "| detalle esperado:", f"ANULACION DSOC{f[0]}" if f else "?")
