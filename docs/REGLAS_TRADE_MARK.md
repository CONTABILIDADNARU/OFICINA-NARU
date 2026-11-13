# TRADE MARK (EMP015) - reglas aprendidas y estado (11-nov-2026)

Servidor: Z:\SIASOFT_GENERAL\TRADE_FAIRS_TRADE_MARK_TRYP\SIASOFT_V23\EMPRESAS\EMP015\CO.SIA (instalacion compartida con TRADE FAIRS y TRYP: solo se trabaja EMP015). NIT 901749655. Carpeta documental: Z:\ARCHIVO_EMPRESAS\TRADE MARK (IMPUESTOS, DIAN, etc.). Es una auditoria enero-noviembre 2026: la empresa se fue un tiempo y volvio; puede haber impuestos presentados que faltan por descargar.

## Auditoria compras y ventas (REP ENERO-NOVIEMBRE 2026, 965 filas)
- Ventas ene-sep: REP = SIASoft al peso (151 docs). Octubre: faltan FVE41-FVE50, NC56, NC57, ND1 y FVE40 esta contabilizada con 0 ingreso/IVA (base 24.145.000, IVA 4.587.550; corregir a mano, hoja "FVE40 correccion"). Noviembre: faltan FVE51-65, NC58-60.
- Compras: 611 docs del REP; 103 sin rastro (ni por folio ni por valor) en toda la contabilidad 2026 (64 oct, 20 nov, 19 ene-sep). Otros 214 aparecen solo por valor (revisar por muestra).
- Notas: en SIASoft las NC de venta son NC-n (REP: NC n); facturas de venta FVE+folio; compras 05 = CP-n (ultimo CP-1161), 18 = FC.-n (ultimo FC.-135); 80D = DSn; 16 = NDT-n.

## Formato de contabilizacion aprendido
- Ventas (04): ingreso 413508/415550/414505 segun cliente, IVA 24080505, retefuente 13551512 (4%), reteICA 13551805 (0,966%), reteIVA 13551715 (15% del IVA), cliente 13050505 con DOC_REF = numero. NC (08): 417510, IVA 24080510, retenciones al credito, 13050505 con DOC_CRUC/DOC_REF = factura y ANO_REF = fecha factura, COD_CCO 01. DES_MOV "FVE n CONCEPTO". COD_VEN 01.
- Compras (05 y 18): gasto o 143505 (18), IVA 24081005 (19%) / 24081027 (5%), retenciones 2365xx/2368xx/2367xx, proveedor 220505 (no caja). FACTURA = "FC folio"; DOC_MOV = FACTURA; DOC_REF = consecutivo. DES_MOV = FACTURA + concepto. En 18 el COD_CCO es 01 en gasto e IVA.
- Metodo: se clona el ultimo documento valido del tercero y se reescala (IVA y total siempre iguales al REP).

## Medicion (backtest jul-sep 2026, solo lo anterior a cada documento)
- Ventas 25/30 = 83% (82% por valor); nivel ALTA 23/26 = 88%.
- Compras 62/86 = 72% (52% por valor); nivel ALTA 35/43 = 81%.
- No alcanza el piso de 95%. Fallos: clientes con cuenta de ingreso distinta segun servicio (413508 vs 415550), cambios de retenciones, proveedores con varias cuentas de gasto.

## Archivos generados (AUDITORIA 2026\IMPORTAR_SIASOFT_NOV2026)
TMKVA10/TMKVA11 (ventas alta), TMKVD10/TMKVD11 (ventas con duda), TMKCA10/CA11/CAEA (compras alta; EA = ene-sep), TMKCD10/CD11/CDEA (compras con duda), TERTMK11 (23 terceros para el 766), REVISION_TRADE_MARK_NOV2026.xlsx. Generador: claude/gen_trade_mark.py (+ armar.py, dbf.py). Todos cuadran D=C por documento, sin consecutivos repetidos ni ya existentes. NO importado: espera aprobacion de Daniel. 34 documentos retenidos (27 compras de proveedores sin historial, 4 NC compra, 1 POS, NC56, ND1).

## Pendiente
- Aprobacion de Daniel y orden de importacion: 766 (TERTMK11) > 746 > 150 solo meses afectados; verificar y bloquear periodos.
- Confirmar si octubre/noviembre y ene-sep estan bloqueados (los de ene-sep pueden requerir desbloqueo).
- Cruce de IVA REP vs formularios 300 (cuatrimestres 2025 y 2026) y retefuente: faltan en carpeta may-ago y oct 2026; ReteICA bimestres 3-5 2026.
