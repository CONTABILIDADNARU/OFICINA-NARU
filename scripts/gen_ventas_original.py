import sys, math, os, struct, re, collections, csv
S='/tmp/claude-0/-home-claude/f9be5458-09d6-56eb-b530-4c15adae9be7/scratchpad'
sys.path.insert(0,S)
from armar_juego import *
from dbf import load
import pandas as pd
REP="/mnt/user-data/attachments/f9be5458-09d6-56eb-b530-4c15adae9be7/23dd0896-72d459f1-f027-4d53-afb5-0e331f24c3b6.xlsx"
P='/mnt/user-data/uploads/SIASOFT_V23_OCTOPUX_1/SIASOFT_V23_OCTOPUX/EXPORT/COOct312026'
T='/mnt/user-data/uploads/SIASOFT_V23_OCTOPUX_1/PRUEBAS_AGENTE/TERAGT2'
OUT='/mnt/user-data/outputs/PAQUETE_ORIGINAL/'
rep=pd.read_excel(REP,dtype={'NIT Emisor':str,'NIT Receptor':str,'Folio':str,'Prefijo':str})
e=rep[(rep.Grupo=='Emitido')&(rep['Tipo de documento']=='Factura electrónica')].copy()
e['fe']=pd.to_datetime(e['Fecha Emisión'],format='%d-%m-%Y')
print('rango fechas:',e.fe.min().date(),e.fe.max().date())
e['num']=e.Prefijo+'-'+e.Folio.astype(int).astype(str)
ya=set()
tot_dian=dict(n=len(e),total=e.Total.sum(),iva=e.IVA.sum(),base=(e.Total-e.IVA).sum())
d=e[~e.num.isin(ya)].sort_values(['fe','Prefijo','Folio']).reset_index(drop=True)
_,ter0,_=load('/mnt/user-data/uploads/SIASOFT_V23_OCTOPUX_1/RESPALDO_CO_SIA_20261102/MAE_TER.DBF'); codes={t['COD_TER'] for t in ter0}
# ---------- documentos
cab=open(P+'.cab','rb').read(); cue=open(P+'.cue','rb').read(); ter=open(P+'.Ter','rb').read(); fpt=open(P+'.FPT','rb').read()
_,_,_,fc=parse(cab); _,_,_,fu=parse(cue)
tc=[r for r in recs(cab) if get(r,fc,'NUM_TRN')=='FC-000666'][0]; tu=[r for r in recs(cue) if get(r,fu,'NUM_TRN')=='FC-000666'][0]
for k in ('OTRO_TER','DETALLE','FACTURA','DIA_PLAZ','FEC_POSF','COD_BAN','NUM_IMP','TRM','DES_COND'): tc=putc(tc,fc,k,'')
for k in ('COD_CIU','COD_SUC','COD_CCO','NUM_CHQ','DOC_MOV','DOC_CRUC','DOC_REF','FEC_VENC','COD_CON'): tu=putc(tu,fu,k,'')
oc,ou=[],[]; sb=si=st=0
for _,x in d.iterrows():
    base=int(round(x['Total']-x['IVA'])); iva=int(round(x['IVA'])); tot=base+iva
    sb+=base; si+=iva; st+=tot
    fec=x.fe.strftime('%Y%m%d'); cod=x['NIT Receptor'] if x['NIT Receptor']!='222222222222' else '2222222'
    h=tc
    for k,v in (('ANO_DOC','2026'),('PER_DOC','10'),('COD_TRN','04'),('NUM_TRN',x.num),('FEC_DOC',fec),('FEC_VEN',fec),('COD_VEN','01')): h=putc(h,fc,k,v)
    oc.append(h)
    for cta,ciu,bas,deb,cre in (('413556','01',0,0,base),('24080505','',base,0,iva),('11050505','',0,tot,0)):
        r=tu
        for k,v in (('ANO_DOC','2026'),('PER_DOC','10'),('COD_TRN','04'),('NUM_TRN',x.num),('COD_CTA',cta),('COD_CIU',ciu),('COD_TER',cod),('DES_MOV','VENTA DE MERCH')): r=putc(r,fu,k,v)
        r=putn(r,fu,'BAS_MOV',float(bas)); r=putn(r,fu,'DEB_MOV',float(deb)); r=putn(r,fu,'CRE_MOV',float(cre)); ou.append(r)
files={'AGTVTAORI.cab':build(cab,oc),'AGTVTAORI.cue':build(cue,ou),'AGTVTAORI.Ter':build(ter,[]),'AGTVTAORI.FPT':fpt}
for n,b in files.items(): open(OUT+n,'wb').write(b)
print(f"docs generados {len(d)} (+{len(ya)} ya importados = {len(d)+len(ya)} vs DIAN {tot_dian['n']})")
print(f"Suma generada: base {sb:,} IVA {si:,} total {st:,}")
print(f"DIAN (4993 fact. completas): base {tot_dian['base']:,.2f} IVA {tot_dian['iva']:,.2f} total {tot_dian['total']:,.2f}")
d11=e[e.num.isin(ya)]; b11=int(round((d11.Total-d11.IVA).sum()))
print(f"(las 11 ya importadas suman base {sum(int(round(a-b)) for a,b in zip(d11.Total,d11.IVA)):,} IVA {sum(int(math.floor(v+1e-9)) for v in d11.IVA):,})")
print('conteo por serie:',d.groupby('Prefijo').size().to_dict())
# ---------- terceros nuevos
def dv(n):
    w=[3,7,13,17,19,23,29,37,41,43,47,53,59,67,71]; s=sum(int(c)*w[i] for i,c in enumerate(reversed(n))); r=s%11
    return str(r if r<2 else 11-r)
nuevos=d[(d['NIT Receptor']!='222222222222')&(~d['NIT Receptor'].isin(codes))].drop_duplicates('NIT Receptor')
nuevos=pd.concat([nuevos]).sort_values('NIT Receptor')
EMP=re.compile(r'\b(S\.?A\.?S\.?|LTDA|S\.?A\.?|S\.? ?EN ?C|E\.?U\.?|FUNDACION|CORPORACION|ASOCIACION|COLEGIO|CLUB|GRUPO|COMPA|INVERSIONES|SOLUCIONES|SERVICIOS|PUBLICIDAD|IMPORT|COMERCIALIZ|PRODUCCIONES|AGENCIA|CIA)\b',re.I)
t0=open(T+'.DBF','rb').read(); tfpt=open(T+'.FPT','rb').read(); _,_,_,ft=parse(t0); tmpl=recs(t0)[0]
rows=[]; dud=[]
for _,x in nuevos.iterrows():
    nit=x['NIT Receptor']; nom=re.sub(r'\s+',' ',str(x['Nombre Receptor']).strip()).upper()
    juridica = bool(EMP.search(nom)) or (len(nit)==9 and nit[0] in '89')
    tdoc='31' if (len(nit)==9 and nit[0] in '89') else '13'
    if len(nit)>10 or len(nit)<6: dud.append((nit,nom,'largo de documento atípico'))
    if juridica != (tdoc=='31'): dud.append((nit,nom,f'persona {"jurídica" if juridica else "natural"} pero doc {tdoc}'))
    r=tmpl
    for k in ('NOM_TER','RAZ','REPRES'): r=putc(r,ft,k,nom)
    r=putc(r,ft,'COD_TER',nit); r=putc(r,ft,'DV',dv(nit)); r=putc(r,ft,'TDOC',tdoc)
    r=putc(r,ft,'DIR1',''); r=putc(r,ft,'DIR',''); r=putc(r,ft,'FEC_ING','20261102')
    r=putc(r,ft,'TIP_PERS','2' if juridica else '1')
    for k in ('NOM1','NOM2','APL1','APL2'): r=putc(r,ft,k,'')
    if not juridica:
        t=nom.split()
        if len(t)==2: n1,n2,a1,a2=t[0],'',t[1],''
        elif len(t)==3: n1,n2,a1,a2=t[0],'',t[1],t[2]
        elif len(t)==4: n1,n2,a1,a2=t
        else: n1,n2,a1,a2=t[0],'',t[-1],''; dud.append((nit,nom,'nombre natural con partes ≠2-4, revisar separación'))
        for k,v in (('NOM1',n1),('NOM2',n2),('APL1',a1),('APL2',a2)): r=putc(r,ft,k,v)
        if len(t)==3: dud.append((nit,nom,'3 palabras: asumí 1 nombre + 2 apellidos'))
    rows.append(r)
h=bytearray(t0[:parse(t0)[1]]); h[4:8]=struct.pack('<I',len(rows))
open(OUT+'TERVTAORI.DBF','wb').write(bytes(h)+b''.join(rows)+b'\x1a'); open(OUT+'TERVTAORI.FPT','wb').write(tfpt)
print('terceros nuevos:',len(rows),'| jurídicos',sum(1 for r in rows if get(r,ft,'TIP_PERS')=='2'),'| naturales',sum(1 for r in rows if get(r,ft,'TIP_PERS')=='1'))
with open(OUT+'TERVTAORI_dudas.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['NIT','Nombre','Duda']); w.writerows(dud)
print('dudas de terceros:',len(dud),collections.Counter(x[2][:20] for x in dud).most_common(5))
cr=d[d['Forma de Pago']==2]; print('facturas forma de pago 2 (crédito) tratadas como caja:',len(cr))
