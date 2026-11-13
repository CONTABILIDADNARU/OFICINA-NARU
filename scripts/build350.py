import sys; sys.path.insert(0,'/home/claude/work061')
import openpyxl, dbf, glob, datetime, collections
from openpyxl.utils import get_column_letter
T='/mnt/user-data/attachments/01489600-d0fb-5e65-b75c-01f72e009a1d/6b6ec14d-BORRADOR_RTE_FTE_NARU_AGOSTO.xlsx'
REP=glob.glob('/mnt/user-data/attachments/*/*10.OCTUBRE.xlsx')[0]
B='/mnt/user-data/uploads/SIASOFT_V23/EMPRESAS/EMP061/CO.SIA/'
cue=dbf.load(B+'CUE_DOC.DBF')[1]; ter={r['COD_TER'].strip().lstrip('0'):r for r in dbf.load(B+'MAE_TER.DBF')[1]}
cta={r['COD_CTA']:r['NOM_CTA'] for r in dbf.load(B+'MAE_CTA.DBF')[1]}
cab={(r['ANO_DOC'],r['PER_DOC'],r['COD_TRN'],r['NUM_TRN']):r for r in dbf.load(B+'CAB_DOC.DBF')[1]}
def fd(r): return fe(cab[(r['ANO_DOC'],r['PER_DOC'],r['COD_TRN'],r['NUM_TRN'])]['FEC_DOC'])
def pj(t):
    t=t.strip().lstrip('0'); x=ter.get(t); td=str(x['TDOC']).strip() if x else ''
    return 'PJ' if (td=='31' and t[:1] in '89') else 'PN'
CON={'23652525':'Servicios','23652530':'Servicios','23652535':'Servicios','23653010':'Arrendamientos','23654015':'Compras','23651505':'Honorarios'}
def fe(s): return datetime.datetime.strptime(s,'%Y%m%d')
wb=openpyxl.load_workbook(T)
# ---------- AUX RTE FTE
ws=wb['AUX RTE FTE']
for row in ws.iter_rows(min_row=2):
    for c in row: c.value=None
cols=['ANO_DOC','PER_DOC','COD_TRN','NUM_TRN','FEC_DOC','COD_CTA','COD_CIU','COD_SUC','COD_CCO','COD_TER','DES_MOV','NUM_CHQ','DOC_MOV','BAS_MOV','DEB_MOV','CRE_MOV','NOM_CTA','TIP_CTA','NAT_CTA','NIV_CTA']
L=[r for r in cue if r['ANO_DOC']=='2026' and r['PER_DOC']=='10' and r['COD_CTA'] in CON and r['CRE_MOV']>0]
L.sort(key=lambda r:(r['COD_CTA'],r['NUM_TRN']))
ws['W1']='CONCEPTO'
for i,r in enumerate(L,start=2):
    for j,k in enumerate(cols,start=1):
        v=r.get(k,'') if k not in('FEC_DOC',) else fd(r)
        if k=='NOM_CTA': v=cta.get(r['COD_CTA'],'').strip()
        if k in('TIP_CTA','NAT_CTA','NIV_CTA'): v=None
        if isinstance(v,str): v=v.strip()
        ws.cell(i,j).value=v
    ws.cell(i,23).value=f"{CON[r['COD_CTA']]} {pj(r['COD_TER'])}"
last=len(L)+1; s0=last+3
ws.cell(s0,8).value='CONCEPTO'; ws.cell(s0,14).value='BASE'; ws.cell(s0,16).value='RETENCION'
conc=['Servicios PJ','Servicios PN','Arrendamientos PJ','Arrendamientos PN','Compras PJ','Compras PN','Honorarios PJ','Honorarios PN']
for k,c in enumerate(conc,start=1):
    rr=s0+k; ws.cell(rr,8).value=c
    ws.cell(rr,14).value=f'=SUMIFS($N$2:$N${last},$W$2:$W${last},H{rr})'
    ws.cell(rr,16).value=f'=SUMIFS($P$2:$P${last},$W$2:$W${last},H{rr})'
rowof={c:s0+k for k,c in enumerate(conc,start=1)}
# ---------- AUX INGRESOS
wi=wb['AUX INGRESOS']
for row in wi.iter_rows(min_row=2):
    for c in row: c.value=None
I=[r for r in cue if r['ANO_DOC']=='2026' and r['PER_DOC']=='10' and r['COD_CTA'].startswith('4')]
I.sort(key=lambda r:(fd(r),r['NUM_TRN']))
for i,r in enumerate(I,start=2):
    for j,k in enumerate(cols,start=1):
        v=r.get(k,'') if k!='FEC_DOC' else fd(r)
        if k=='NOM_CTA': v=cta.get(r['COD_CTA'],'').strip()
        if k in('TIP_CTA','NAT_CTA','NIV_CTA'): v=None
        if isinstance(v,str): v=v.strip()
        wi.cell(i,j).value=v
assert len(I)<=13
wi['P15']='=SUM(P2:P14)-SUM(O2:O14)'
wi['O15']='=SUM(O2:O14)'; wi['N15']='INGRESOS NETOS (credito - debito)'
# ---------- REP DIAN
wr=wb['REP DIAN']
for row in wr.iter_rows():
    for c in row: c.value=None
src=openpyxl.load_workbook(REP,data_only=True)['Hoja1']
n=0
for i,row in enumerate(src.iter_rows(values_only=True),start=1):
    if all(v is None for v in row): continue
    for j,v in enumerate(row[:18],start=1): wr.cell(i,j).value=v
    n=i
# ---------- FORMULARIO
f=wb['FORMULARIO']
f['Z4']=1; f['AA4']=0
f['D11']=901987014; f['Q11']=7; f['D13']='PARAMO CONNECT S.A.S'
f['AQ14']=None; f['BD14']=0.011
rng=lambda col:f"'AUX RTE FTE'!${col}${rowof['Servicios PJ']}"
def put(cell,conc,col):
    f[cell]=f"=ROUND('AUX RTE FTE'!{col}{rowof[conc]},-3)"
for cell in ('T21','AB21','T26','AB26'): f[cell]=None
put('T21','Servicios PJ','N'); put('AB21','Servicios PJ','P'); put('AG21','Servicios PN','N'); put('AV21','Servicios PN','P')
put('T23','Arrendamientos PJ','N'); put('AB23','Arrendamientos PJ','P'); put('AG23','Arrendamientos PN','N'); put('AV23','Arrendamientos PN','P')
put('T26','Compras PJ','N'); put('AB26','Compras PJ','P'); put('AG26','Compras PN','N'); put('AV26','Compras PN','P')
put('T19','Honorarios PJ','N'); put('AB19','Honorarios PJ','P'); put('AG19','Honorarios PN','N'); put('AV19','Honorarios PN','P')
f['T35']="=ROUND('AUX INGRESOS'!P15,-3)"
wb.save('/mnt/user-data/outputs/BORR350/BORRADOR_RTE_FTE_PARAMO_OCTUBRE.xlsx')
print('lineas retencion',len(L),'ingresos',len(I),'REP filas',n)
