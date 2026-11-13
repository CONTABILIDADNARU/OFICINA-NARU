# PARAMO CONNECT (EMP061) - hallazgos y reglas, octubre 2026 (IMPORTADO, confirmado por Daniel el 3-nov 22:47)

Instalacion: Z:\SIASOFT_GENERAL\INNOVA_DIGITAL_PARAMO_SIASOFT_TREFIELECTRIC\SIASOFT_SAS\SIASOFT_V23\EMPRESAS\EMP061\CO.SIA
Respaldo (copia de las 94 tablas activas, 3-nov 12:18): C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\COPIA_EMP061_OCT2026
Decision de Daniel (3-nov): trabajar leyendo la original del servidor; la copia queda solo como backup. Nunca escribir DBF; cargas por 766/746/150.

## Estado (actualizado 3-nov-2026 22:55)
- Daniel confirmo que Paramo quedo importada y que la empresa esta bien. En la oficina virtual esta marcada como "Aplicado".
- NO hay todavia verificacion de solo lectura registrada en este documento (conteos importados, D=C, terceros huerfanos, acumulados). Pendiente: correr verificar.py contra el respaldo de las 12:18 y anotar las cifras aqui, y confirmar que octubre quedo bloqueado de nuevo.
- Pendientes de criterio que quedaron abiertos antes de importar (confirmar que decision se tomo): retefuente de FVE-739 (confirmar RUT del proveedor), retenciones de FEPC33, 22 DS marcados MEDIA cerca del minimo 1.750.905, error de digitacion de CP-000088 (se reporta aparte, no es del agente).

## Problema del 745
El 745 da error 1113 "El archivo no esta abierto" (programa EXPORTAR). Deja COOct312026.cab de 0 bytes y sin .Ter. Daniel probo y sale igual -> se arma el juego con la plantilla fija AGTCOMP1 (PAQUETE_ORIGINAL), como en NARU. Las tablas 061 tienen 4 campos extra en CAB (RC_PROV, FEC_CONT) y 4 en CUE (REVELA, IND_CRUC, FEC_CON, COD_BANC) que la plantilla no trae: confirmar en la primera importacion de prueba.

## REP octubre (Hoja1, 137 filas; la otra hoja es parcial del 13/10)
- Documento soporte DSPC: 89 (folios 569-657, sin huecos). Solo el 569 ya esta registrado (DS569).
- Notas de ajuste del DS: 13 (NAPC35-NAPC47), total 37.892.312. En el sistema el ultimo es ND34 (= NAPC34): numerar ND35..ND47.
- Ventas emitidas: FEPC29-33 (29 y 30 ya estan; faltan FEPC31 290.070.084, FEPC32 214.901.546, FEPC33 27.924.548) + NC NCPC-2 (ya esta).
- Compras recibidas: 13. Ya registradas 9 (CP-000085 a CP-000093). Faltan 4: TV43-11302988 (12.100), FVE-739 (6.447.000, IVA 844.143), F9Z1-1022228 (100.000, IVA 15.966), SI66-115060 (51.100, IVA 8.159). Siguiente consecutivo: CP-000094.
- Nomina electronica NOPC (13.100.000): no va. 4 filas sin tipo en Hoja1 parecen totales: se ignoran.

## Errores de digitacion del registro humano (reportar aparte, no del agente)
- CP-000088 (FE-3, REP 1.178.100 con IVA 188.100): quedo gasto 990.000 sin IVA descontable.

## Documento soporte (tipo 05A)
- NUM_TRN = DS + folio (DS569). FACTURA = DSPC + folio. DES_MOV = FACTURA + DETALLE. DETALLE dominante: SERVICIO DE DIGITACION.
- Lineas: gasto DEB | retefuente CRE (BAS=base) | ICA CRE (BAS=base) | 220505 CRE neto con DOC_REF=FACTURA.
- Redondeo al peso mas cercano. Retefuente servicios 6% (23652525); honorarios 10% (23651505); 3,5% (23653010). ICA 0,966% (236810), 0,866% (236830, con 23651505).
- ICA en 453 de 473 DS de 2026.
- Gasto: 513517 (242 docs), 513515 (153), 523515 (58), resto menores. El mismo tercero alterna entre 513515 (casi siempre con retefuente 6%) y 513517 (solo ICA).
- Prediccion de la cuenta en septiembre (85 DS): "ultima vez del tercero" 56/85; umbral por valor del documento (menor a ~2.000.000 -> 513515, mayor -> 513517) 77/85 (90,6%), pero en julio 65/91 y en agosto 71/94. Criterio real confirmado despues por Daniel (ver reglas confirmadas).
- Retefuente en 513515: 53 terceros siempre, 16 nunca, 8 mixtos (decidir por historial del tercero).
- Terceros sin historial en septiembre: 7 de 85.

## Ventas (tipo 04)
- NUM_TRN = FEPC + folio (FEPC29). Exportaciones: 417005 CRE / 13050506 DEB (clientes del exterior), sin IVA ni retenciones. NC: tipo 08, NUM_TRN NCPC-n, 417510 DEB / 13050506 CRE, FACTURA NCPC2.
- Variantes 2026: 415505 (12 docs), 417005 con 13551505 y 13551805 (8 docs).

## Compras (tipo 05)
- NUM_TRN CP-000093 (6 digitos). FACTURA = FC + digitos del folio (criterio humano irregular: ultimos 4 o 6 digitos). Credito a 220505 (proveedores) en la mayoria; a veces 11050505.
- Retefuente compras 23652535 4%; ICA retenido 236810 / 236805. IVA descontable 24081005.

## Reglas confirmadas por Daniel y aprendidas (actualizado 3-nov 12:55)
- Daniel: 513515 lleva retefuente + ICA; 513517 lleva solo ICA. Que el maestro de terceros decida cual NO se confirmo (IND_RETE, IND_RET, AUT_RET, TIP_PRV no lo explican).
- TOPE CONFIRMADO POR DANIEL (3-nov 12:55): el salario minimo 2026 sin auxilio de transporte = 1.750.905 (Decreto 1469/2025). Hasta ese valor (inclusive) -> 513515 con retefuente; pasando del minimo ya pagan planilla y no se retiene -> 513517. Contra el historial el tope 1.750.905 acierta 73,5% (286/389) y 69/83 en septiembre; con 2.000.000 acertaba 82,8%: Daniel mantiene 1.750.905.
- (Version anterior del borrador) valor del documento menor a 2.000.000 -> 513515 (retefuente 6% 23652525 + ICA 0,966% 236810); mayor o igual -> 513517 (solo ICA). El prefijo 5135/5235 sale del ultimo documento del tercero; si su cuenta es otra (511035, 522005, 524525...) se replica su ultima estructura.
- Backtest septiembre (aprendiendo solo lo anterior y sin DS anulados por nota de ajuste): 75 de 83 exactos (90,4%). Antes de limpiar los anulados: 77/85 con solo el valor, 56/85 con "ultima vez del tercero".
- Los DS anulados por una nota de ajuste ensucian el historial (24 de 34 notas detectadas): excluirlos al aprender.
- Nota de ajuste (08A): NUM_TRN ND + folio NAPC; FACTURA NAPC##; DES_MOV "NAPC## ANULACION"; gasto CRE | (retenciones DEB) | 220505 DEB con DOC_REF = DOC_CRUC = DS original, ANO_REF = ano+periodo+tipo del original (ej. 20261005A) y SAL_DOC = valor. Se enlaza con el DS por mismo tercero y mismo valor.
- Ventas FEPC33 (cliente nacional): sigue el patron de su cliente (417005, retefuente 3,5% 13551505, reteICA 0,966% 13551805, cartera 13050505).
- Los 3 documentos de compra faltantes se generan con la ultima cuenta del proveedor; IVA al peso mas cercano; FACTURA = FC + folio.
- Un tercero con permiso PPT existe como PPT + digitos sin espacio, TDOC 13.

## Juego generado para octubre (ya importado segun Daniel)
- Carpeta: PAQUETE_ORIGINAL\PARAMO_OCT2026 (PARDSO10, PARNDO10, PARVTA10, PARCOM10, TERPARAMO10 + REVISION_PARAMO_OCT2026.xlsx). Generador: claude/gen_paramo.py.
- DS570-657: 88 docs, base 350.352.303 (igual al REP menos el DS569), ICA 3.384.410, retefuente 1.744.478, 220505 neto 345.223.415. Cuentas: 513517 x67, 513515 x19, 522005 x1, 523515 x1. (Primera version, antes de ajustar el tope y las anulaciones; ver version regenerada abajo.)
- ND35-47: 13 docs, 37.892.312. Ventas FEPC31-33: 532.896.178. Compras CP-000094 a 96: 3 docs (FVE-739 retenida: proveedor sin historial, NIT nuevo). Terceros nuevos: 1.
- 746 por conjunto: DS fechas 31/10/2026; ND 31/10/2026; ventas 19/10 a 29/10/2026; compras 20/10 a 28/10/2026.

- Regenerado con tope 1.750.905: DS 513517 x74, 513515 x11, retefuente 871.032 (antes 1.744.478), 220505 neto 346.096.861; 22 DS marcados MEDIA (cerca del minimo).

## Regla de Daniel 3-nov: DS anulado por nota de ajuste (sin retenciones)
- Si una nota de ajuste anula completo un DS (mismo tercero y mismo valor), NI el DS NI la nota llevan ICA ni retefuente: el DS queda gasto D / 220505 C y la nota lo reversa con DOC_REF = DOC_CRUC = DS original.
- Se aplico a 13 de 13 notas (NAPC35-47). Los DS anulados tampoco entran al historial para aprender.
- Resultado regenerado: DS570-657 88 docs, base 350.352.303, ICA 3.018.369, retefuente 871.032, 220505 neto 346.462.902. Cuentas 513517 x74, 513515 x11, 523515/522005/523517 x1. ND35-47 13 docs, 37.892.312.
- Cuadre verificado (antes de importar): DS 350.352.303 = 350.352.303; ND 37.892.312 = 37.892.312; ventas 532.896.178 = 532.896.178; compras 163.200 = 163.200.
- Pendiente al momento de generar: cuenta de gasto de FVE-739 (proveedor nuevo, retenida); confirmar retenciones de FEPC33.

## FVE-739 (decision Daniel 3-nov 13:18)
- Servicio automotriz, cerrado a caja: gasto 524540 (area ventas) 5.602.857 D | IVA 24081005 844.143 D | 11050505 caja 6.447.000 C. SIN retefuente por ahora; confirmar con el RUT del proveedor (autorretenedor/gran contribuyente). Si se retiene 4% (23652535): 224.114 y caja 6.222.886.
- Gran contribuyente: no aparece en Res. 248/2025 (retiros/nuevas); lista base Res. 200/2024 no se pudo leer (PDF externo). Autorretenedor: solo lo confirma el RUT.
- IVA 844.143 = 15,07% de la base: parte del servicio es excluida/no gravada (gravado ~4.442.857).
- Consecutivos de compras octubre: CP-000094 (TV43), CP-000095 (FVE-739), CP-000096 (SI66), CP-000097 (F9Z1); total compras 6.610.200 cuadrado. Terceros nuevos: 1 (proveedor FVE-739).

## Calendario tributario (agregado 3-nov-2026 22:19)
- NIT 901987014 (dato de Daniel, sin digito de verificacion; confirmar con el RUT). Ultimo digito 4 = retencion en la fuente e IVA. Ultimos dos digitos 14 = planilla (3.er dia habil).
- Domicilio Bogota e IVA cuatrimestral (ambos confirmados por Daniel). Revision interna: 2 dias habiles antes del vencimiento (regla general 10).

| Obligacion | Vence | Revision interna |
|---|---|---|
| Planilla octubre | Jue 5 nov 2026 | Mar 3 nov |
| Retencion octubre | Mar 17 nov 2026 | Jue 12 nov |
| ReteICA sep-oct (Bogota) | Vie 20 nov 2026 | Mie 18 nov |
| Planilla noviembre | Jue 3 dic 2026 | Mar 1 dic |
| Retencion noviembre | Mar 15 dic 2026 | Vie 11 dic |
| Planilla diciembre | Mie 6 ene 2027 | Lun 4 ene |
| ReteICA nov-dic (Bogota) | Vie 15 ene 2027 | Mie 13 ene |
| Retencion diciembre | Lun 18 ene 2027 | Jue 14 ene |
| IVA cuatrimestral sep-dic | Lun 18 ene 2027 | Jue 14 ene |

- Fuentes: retencion e IVA, tablas de Actualicese y Gerencie; ReteICA Bogota, Siempre al Dia y Alcaldia de Bogota; planilla, calculo propio por dia habil con festivos (2 y 16 nov, 8 dic, 1 y 11 ene). Validar contra DIAN y Secretaria de Hacienda antes de fijar.
- Pendiente del RUT: responsabilidades (retencion en la fuente, autorretenedor), agente de retencion de ICA, ICA propio. El REP de octubre trae nomina electronica (NOPC): hay planilla (confirmar con nomina).
