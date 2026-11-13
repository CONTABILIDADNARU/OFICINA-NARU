# RUMASA SAS (EMP010 en SIASOFT_GENERAL\MOUNTAIN) - reglas aprendidas, octubre 2026 (en construccion)

Servidor: Z:\SIASOFT_GENERAL\MOUNTAIN\MOUNTAIN\SIASOFT_V23\EMPRESAS\EMP010\CO.SIA. Copia de trabajo/backup (solo CO.SIA, 101 archivos sin .BAK, 3-nov 15:10): C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\RUMASA_OCT2026\CO.SIA
Decision de Daniel (3-nov): aplicar en el servidor; la copia queda como backup. Yo solo genero archivos; cargas por 766/746/150. No se pide exportacion 745: se usa siempre la plantilla AGTCOMP1 (como NARU y PARAMO).

## Alcance
Ventas (tipo 04), documento soporte FTM (05a) y compras (05). Nomina electronica (NMEM) no se contabiliza por este flujo.
REP octubre: 24 docs = 2 FE + 1 exportacion (FE148), 2 DS (FTM175-176), 3 nomina, 15 facturas de compra, 1 NC recibida (NCSD-455710).
Historial septiembre: 85 docs (04 x2, 05 x28, 05a x3, 02 x24, 06 x22...). Ultimos consecutivos: ventas 145, DS FTM-00174, compras CP-001653.

## Convenciones del sistema (aprendidas del historial 2026)
- Ventas: NUM_TRN = folio (146), FACTURA vacia, COD_VEN 01, DES_MOV = "FE ### " + descripcion del cliente (CONFIGURACION DE LA INFORMACION, SERVICIO DE MARQUILLOS...). Orden: ingreso 413504 CRE | IVA 24080505 CRE (BAS=base) | retenciones 1355xx DEB (BAS=base, tarifa aprendida por cliente) | cartera 13050505 DEB con DOC_REF=folio. Patron por cliente = ultimas 3 facturas; si no coinciden, sin retenciones y duda ALTA.
- Exportacion: 413506 CRE / 13050506 DEB, sin IVA ni retenciones. Cliente del exterior existe en MAE_TER sin guiones (475615425, TDOC 31).
- Compras: NUM_TRN CP-001654 (6 digitos). FACTURA = digitos del folio del REP; DETALLE = DES_MOV = "FC <folio> <concepto>" (concepto del ultimo documento del proveedor). Orden: gasto DEB (total - IVA) | IVA descontable 511570 DEB (BAS 0) | retenciones CRE si >=50% de su historial las tuvo | credito (220505 / banco / caja segun el proveedor) con DOC_MOV=FACTURA, SALDO=credito, DOC_REF=NUM_TRN.
- Documento soporte 05a: NUM_TRN FTM-00175 (5 digitos), FACTURA "FTM 175", DETALLE = DES_MOV = "FTM 175 <concepto>". Gasto DEB (=Total del REP) | retenciones CRE | pago CRE neto con DOC_MOV="FTM 175", SALDO, DOC_REF=NUM_TRN. Cuentas y retenciones = ultima vez del tercero (BAJA/MEDIA).
- Cuenta de gasto y de pago por proveedor/tercero: una sola desde abril = alta; varias = la de la ultima vez (baja); sin movimiento desde abril = ultima vez (media); sin historial 2026 = documento RETENIDO (no se genera).
- Redondeo: IVA y total al peso mas cercano (REP trae centavos); base/gasto = total - IVA. (Pendiente confirmar si RUMASA redondea IVA de compras hacia abajo; diferencia maxima 1 peso.)
- .cue siempre con byte 28 = 0 (evita error 1707 del 746). Antes de un 766 comparar NIT contra MAE_TER (el 766 duplico 28 terceros en NARU).

## Resultado octubre (juego generado, sin importar)
- Carpeta: PAQUETE_ORIGINAL\RUMASA_OCT2026\SALIDA_OCT2026 (RUMVTA10, RUMDSO10, RUMCOM10, TERRUMASA10 + REVISION_RUMASA_OCT2026.xlsx). Generador: gen_rumasa.py.
- Ventas FE146-148: 3 docs, 10 lineas, D=C 188.575.679. FE147 repite exactamente FE145 de septiembre (retefuente 39.600 + reteICA 9.563). FE146 sin retenciones (patron del cliente inestable). FE148 exportacion 186.670.767.
- DS FTM-175/176: 2 docs, 3.278.556, retenciones 21.146 (ICA 0,966% en FTM176).
- Compras: 11 de 15 generadas (CP-001654..001668 con huecos reservados), total 2.534.664, IVA 306.368; retenidas 4 por 3.333.451 (proveedores sin compras en 2026; 2 de ellos no estan en MAE_TER). NC NCSD-455710 (69.400) no generada.
- Cuadre contra REP: compras 2.534.664 + 3.333.451 = 5.868.115; ventas 188.575.679; DS 3.278.556.
- Octubre ya trae 2 docs (tipos 14 y 25) en CAB_DOC.

## Actualizacion 3-nov 15:25 (decision de Daniel)
- NIT 860000387 (TONOS SAS; sin compras en 2026, ultimas en 2023): CP-001657 (2.483.250) y CP-001661 (322.200) a 529525 ASEO Y CAFETERIA (ultima cuenta usada), pago 220505. Historial revisado completo: 51 periodos desde dic-2022.
- Siguen retenidas 2 compras (528.001): CP-001664 (NIT 79160978, 518.001) y CP-001667 (NIT 80139187, 10.000); sin historial en ningun tipo y fuera de MAE_TER (terceros nuevos, 766). Falta cuenta de gasto.
- Compras generadas: 13 de 15, total 5.340.114, IVA 754.297. Cuenta de pago por defecto: 220505 (domina en 2026).

## Notas credito de compra (3-nov 15:30)
- 2023-2025: tipo 07 (ND##, a caja 11050505); 2024: 80N (NDS#). 2026: tipo 16, NUM_TRN DCM-00001..00005 (ultimo DCM-00005, ago-2026). Estructura: gasto CRE | IVA 511570 CRE | 220505 DEB con DOC_CRUC=DOC_REF=CP original, ANO_REF=ano+periodo+"05", DOC_MOV=factura original. FACTURA "ND <folio>"; DES_MOV "ND <folio> FT <factura original>".
- NCSD-455710 (NIT 900319753, 69.400, IVA 7.488, 07-oct): generada como DCM-00006 SIN cruce (decision de Daniel; la factura original no aparece en el historial ni en el REP): 529525 CRE 61.912 | 511570 CRE 7.488 | 220505 DEB 69.400. Archivos RUMNCO10. Enlazar a mano en SIASoft.

## Cierre del juego de octubre (3-nov 15:40, decisiones de Daniel tras leer los PDF de la DIAN)
- PDF DIAN (se descargan desde catalogo-vpfe.dian.gov.co con CUFE + NIT; el PDF viene cifrado con el NIT como clave): NCSD-455710 es "NC sin referencia a facturas" (tipo operacion 22), items mascarpone y queso iberico, reemplaza el comprobante de caja 07611032128 del 07-oct (no hay factura en el REP; octubre no tiene compras registradas). DCM-00006 queda SIN cruce, DES_MOV "ND 455710 FT 07611032128".
- FE146: descripcion SERVICIO DE MARQUILLOS; retefuente 2,5% 13551522 (15.269); cartera 711.543. El cliente alterna retenciones (abr-may 3,5%; jun-jul ninguna; ago-sep 2,5%).
- CP-001664 (NIT 79160978, 518.001; hamaca, cojin, bolsa, relleno): 529520, pago 220505. CP-001667 (NIT 80139187, 10.000; bandolas con mosqueton): 524510, pago 220505. Ambos terceros nuevos van por el 766 (TERRUMASA10).
- Resultado final: ventas 3 (188.575.679, cartera 188.511.247), DS 2 (3.278.556), compras 15 de 15 (5.868.115, IVA 838.600 = REP), NC 1 (69.400), terceros nuevos 2. Todos D=C.
- Fechas para el 746: ventas 01-05/10; compras 06-28/10; DS 30/10; NC 07/10.

## Estado final (3-nov 15:50, decision de Daniel)
- RUMASA queda como CASO DE DOCUMENTACION: el juego de octubre se genero y se reviso, pero NO se importa a SIASoft ni se modifica la empresa EMP010. La sesion sirve para dejar escritas las reglas de RUMASA para uso futuro.
- Si mas adelante se decide aplicar: copia de CO.SIA -> desbloquear octubre (ya tiene tipos 14 y 25) -> 766 TERRUMASA10 (re-verificar NIT contra MAE_TER) -> 746 por conjunto (RUMVTA10, RUMDSO10, RUMCOM10, RUMNCO10) -> 150 solo octubre -> verificar.py -> bloquear.
- Pendientes sin cerrar (solo relevantes si se aplica): confirmar redondeo del IVA de compras (abajo vs peso mas cercano, max 1 peso); confirmar campos de CAB/CUE que la plantilla no trae (RC_PROV, FEC_CONT, REVELA, IND_CRUC, FEC_CON, COD_BANC) en la primera importacion; DS con cuentas/conceptos de confianza baja/media.
- Lecciones reutilizables para otros clientes: (1) sin 745: plantilla AGTCOMP1 fija; (2) aprender por tercero con ventana desde abril, "ultima vez" cuando hay varias cuentas; (3) documento sin historial 2026 = retenido hasta que Daniel decida cuenta; (4) NC tipo 22 sin referencia no lleva cruce; (5) los PDF de la DIAN se bajan por CUFE+NIT y se descifran con el NIT.

## Importacion y verificacion (5-nov-2026 ~16:25, lectura solo-lectura del servidor)
- Daniel importo el juego completo en el servidor (EMP010, instalacion MOUNTAIN): 766 (2 terceros), 746 (4 juegos) y 150 (octubre).
- Verificado contra el respaldo del 3-nov: documentos 3.348 -> 3.369 (+21: ventas 3, compras 15, DS 2, NC 1), lineas 16.061 -> 16.122 (+61 = esperadas), ninguna perdida, llaves repetidas 0.
- 21 documentos nuevos, todos D=C. Total nuevo 197.791.750 (= ventas 188.575.679 + DS 3.278.556 + compras 5.868.115 + NC 69.400, igual al REP).
- Octubre completo: tipos 14:1, 25:1, 04:3, 05:15, 05a:2, 16:1; 134 lineas, debitos = creditos = 251.832.669.
- Terceros: MAE_TER 343 -> 345 (NIT 79160978 y 80139187), sin duplicados; terceros huerfanos 0.
- Acumulados: 0 cuentas desfasadas (65) y 0 pares cuenta-tercero desfasados (112).
- Pendiente: confirmar que octubre quedo bloqueado (no se ve en las tablas); cruce manual de DCM-00006 si aparece el original.

## Borrador 350 y calendario (5-nov-2026)
- Borrador de retefuente de octubre armado sobre el formato general: ver claude/BORRADOR_350_RUMASA_OCT2026.md. Total 2.119.000 (arrendamiento PJ 48.000 + autorretencion 1,1 % sobre 188.272.000 = 2.071.000). RUMASA se comporta como autorretenedora especial (13551920 mensual al 1,1 %); confirmar con el RUT.
- Calendario (NIT 901053453, termina en 3; planilla 53 = 9.o dia habil, por validar; ciudad e IVA por confirmar con el RUT): retencion oct vence vie 13 nov (revision mie 11 nov); nov lun 14 dic (jue 10 dic); dic vie 15 ene (mie 13 ene). Planillas: oct vie 13 nov; nov lun 14 dic; dic vie 15 ene (tiene empleados: nomina 25 contabilizada).
- REP de octubre se pidio el mar 3 nov (digito 3, colchon 2 dias habiles segun CALENDARIO_REP.md).

## Correccion 350 (5-nov-2026 16:40)
- El primer borrador (2.119.000) tenia dos errores mios: tomo 236505 como nomina por pagar (es retencion por salarios: 2.200.000) y se armo sobre la plantilla porque no tenia el libro de septiembre. Rehecho sobre el libro de septiembre de Daniel: total 4.357.000 (ver claude/BORRADOR_350_RUMASA_OCT2026.md). RUT de junio: NIT 901053453 DV 9, seccional 32, Bogota, CIIU 6201; responsabilidades 05, 07, 10, 14, 42, 48, 52 (sin periodicidad de IVA).
- Leccion: en 2365 mirar tambien 236505 y la autorretencion como ingresos 4xxx; antes de armar un borrador pedir el libro del mes anterior.
- 5-nov 16:40: Daniel aclaro que FTM-00175 (y la FTM172) son ADMINISTRACION y no llevan retencion; borrador final 4.319.000. Al guardar archivos en el computador de Daniel con device_commit_files, verificar siempre volviendo a traer el archivo (el primer guardado puede copiar una version anterior; usar una ruta de salida nueva).
- 5-nov 16:50: CP-001657 lleva retefuente 2,5 % y reteICA segun Daniel; borrador V2 = 4.371.000. Si el archivo esta abierto en Excel, device_commit_files lo rechaza: guardar con otro nombre (_V2).
