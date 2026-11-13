# YANIMAR GROUP S.A.S (EMP069, instalación SOCIETY_BAGS_SML_YANIMAR) - reglas aprendidas, octubre 2026

NIT 902056762 (último dígito 2). Servidor: Z:\SIASOFT_GENERAL\SOCIETY_BAGS_SML_YANIMAR\SIASOFT_V23\EMPRESAS\EMP069\CO.SIA. Respaldo (5-nov, 103 archivos sin .bak): C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\YANIMAR_OCT2026\CO.SIA. Nombre de la empresa dentro de CO.SIA sin verificar (campo NOM_CFG dice "abrir archivos"); EMP069 confirmado por Daniel. Referencia: todo 2026 (decisión de Daniel).
REP octubre: 505 filas = ventas 341 (FEPB 413-557 x145, FEPL 744-939 x196), compras 142 facturas + 9 NC recibidas + 9 acuses (no se contabilizan), nómina NOYG x4 (flujo aparte).

## Estado de octubre en SIASoft antes de generar (5-nov)
Octubre ya estaba contabilizado en parte: ventas 183 (FEPB 145/145, FEPL 38/196 = 744-781), compras CP-411 a CP-524 (114), DCM-8 a DCM-15. Decisión de Daniel: generar SOLO lo que falta.

## Convenciones (aprendidas del historial 2026)
- Ventas tipo 04: NUM_TRN = prefijo-folio (FEPL-744). FACTURA y DETALLE vacíos, COD_VEN 01. Dos líneas: 413504 CRE y cartera DEB, sin IVA ni retenciones (el REP no trae IVA en ventas). DES_MOV = descripción por cliente (variantes de "VENTAS COMERCIO POR MENOR"; o el producto). Consumidor final = tercero 222222222222 (12 dígitos).
- CAMBIO DE RÉGIMEN: hasta el 9-sep las ventas iban a caja 11050505; desde el 10-sep (y todo octubre) van a cartera 13050505 con DOC_REF = NUM_TRN y SALDO = total. Regla: cuenta = la dominante de las últimas 60 ventas, no la del cliente.
- Compras tipo 05: NUM_TRN CP-n sin ceros. FACTURA = prefijo+folio sin espacio, DETALLE = DES_MOV = producto del proveedor (último documento). Gasto DEB (143506 inventario pescado, 529525/529535/529540...), IVA 24081005 DEB con BAS = base (IVA hacia abajo), retefuente 23654020 y reteICA 236825 CRE con BAS = base, pago CRE: 11050505 (efectivo, sin referencia) o 220505 (con DOC_REF = CP, DOC_MOV = factura, SALDO).
- Notas crédito tipo 16: DCM-n sin ceros. Gasto CRE; 220505 DEB con DOC_REF = DOC_CRUC = CP original, DOC_MOV = factura original, ANO_REF = año+período+"05" (20261005). La NC repite el valor de la factura original (devolución total): el cruce se encuentra por proveedor + mismo valor. En las NC cruzadas, el SALDO del 220505 de la factura original queda en 0 (lo aplica el cruce en el programa; el 746 NO lo cambia: la factura que se importa con SALDO = valor se queda con ese saldo hasta aplicar el cruce).
- Pago de compras (efectivo vs 220505): NO se deduce del REP. Octubre: 84 efectivo / 30 crédito. Decisión de Daniel (5-nov): efectivo 11050505 por defecto; 220505 solo si hay una NC por cruzar; se marca en el reporte.

## Medición retroactiva (5-nov, solo lectura: reglas aprendidas con meses anteriores, comparadas contra lo ya contabilizado de octubre)
- VENTAS: 178/183 = 97,3 % por documento; 98,8 % por valor. PASA el 95 %. Con la regla "cuenta del cliente" daba 56,3 %: el régimen cambió.
- COMPRAS: NO PASA. Regla por proveedor 11,6 %; con historial móvil (como para las 28 faltantes) 63,1 % documento completo (pago 71 %, gasto 91 %, retenciones 95 %, IVA 100 %). "Siempre efectivo" acierta 78,6 % del pago. Daniel aprobó generar igual con el pago por defecto y revisar el reporte (5-nov).
- Retenciones: 23654020 solo aparece con base >= 3.817.920 y 236825 con base >= 1.493.840; 7 de 38 proveedores no son coherentes sobre 27 UVT (1.414.098). Confirmar con RUT, no suponer.
- Errores de digitación del registro humano (no del agente): ventas FEPB-517 (37.400 vs 37.440), FEPB-485 (1.558.820 vs 1.558.520), FEPB-470 (504.000 vs 50.400), FEPB-464 (109.020 vs 116.020), FEPB-493 (registrada al revés); compras CP-497 (factura 1030481170 en vez de 10304811706) y CP-512 (DFV159333 en vez de DFV15933).

## Resultado octubre
- Carpeta: PAQUETE_ORIGINAL\YANIMAR_OCT2026\SALIDA_OCT2026 (YANVTA10, YANCOM10, YANNCO10, TERYAN10 + REVISION_YANIMAR_OCT2026.xlsx). Generadores de la sesión: yan_core.py, gen_yan_ventas.py, gen_yan_compras.py.
- Ventas: FEPL-782 a 939, 158 docs, 316 líneas, D=C 25.061.450 = REP, 0 duplicados.
- Compras: CP-525 a CP-552, 28 docs, 62 líneas, D=C 21.722.825 = REP (IVA 15.675 = REP); 27 en efectivo y 1 a 220505 (la de la NC); 3 con retenciones por historial (confirmar RUT). Las 30 "faltantes" del REP eran 28: 2 ya estaban con la factura mal digitada (CP-497, CP-512).
- Notas crédito: 8 de las 9 del REP ya estaban (DCM-8 a 15, cruce por proveedor + valor). NC2223 (1.140.000, 28-oct) = DCM-16 cruzada con CP-526 (FVPA3403, mismo valor, 27-oct).
- Terceros nuevos: 2 personas naturales (cédulas 1026579254 y 4137377) por el 766 (TERYAN10).

## Importación y verificación (5-nov-2026 ~20:40, lectura solo-lectura del servidor)
- Daniel importó el juego completo en el servidor (766, 746 x3 y 150). Verificado contra el respaldo de la tarde: documentos 1.928 -> 2.115 (+187: ventas 158, compras 28, NC 1), líneas 4.132 -> 4.512 (+380), ninguno perdido, llaves repetidas 0, otros períodos intactos.
- Octubre: 341 ventas, 142 compras, 9 NC; débitos = créditos 362.188.746 (aumento 47.924.275 = ventas 25.061.450 + compras 21.722.825 + NC 1.140.000, igual al REP). Todas las líneas generadas coinciden exactas (316 + 62 + 2). 0 terceros huérfanos (MAE_TER 278 -> 280). Consecutivos sin huecos: FEPB 413-557, FEPL 744-939, CP-411 a 552.
- 150: 0 desfases en RES_CTA y RES_TER (el respaldo traía 3 cuentas y 2 pares desfasados de antes; ya quedaron al día).
- PENDIENTE: CP-526 (FVPA3403) sigue con SALDO 1.140.000 en su línea 220505; las demás facturas cruzadas (CP-412, 419, 451, 448, 481, 511, 516, 521) tienen 0. Falta aplicar el cruce con DCM-16 en el programa. Falta confirmar el bloqueo de octubre, la forma de pago de CP-537 y CP-546 y las retenciones de CP-529, CP-537 y CP-546 con el RUT.
