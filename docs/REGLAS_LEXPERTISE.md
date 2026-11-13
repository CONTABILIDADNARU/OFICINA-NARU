# LEXPERTISE (EMP041) - sesión octubre 2026 (iniciada 3-nov-2026)

Servidor: Z:\SIASOFT_GENERAL\NARU_R&G_LEXPERTISE\SIASOFT_V23\SIASOFT_V23\EMPRESAS\EMP041\CO.SIA (instalación compartida con NARU EMP010 y otras; solo se trabaja EMP041).
Nombre en el maestro de terceros (NIT propio 901800715): "LEXPERTICE SAS" (el REP dice LEXPERTISE COLOMBIA S.A.S).
Alcance (Daniel): compras y ventas. Mes de referencia: todo 2026 (ene-sep). Sin nómina.

## Respaldo
C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\RESPALDO_EMP041_LEXPERTISE_03NOV_1630.zip (96 archivos de CO.SIA: dbf/cdx/fpt/dbc; sin .bak/.tbk/.htm antiguos). Hecho por el puente porque el shell del equipo no arranca.

## REP octubre (archivo adjunto, 6 documentos)
- 4 facturas de compra, todas del mismo proveedor (NIT 901013514, otro cliente de Daniel): FBH-113 (359.998,80), FBH-179 (460.001,64), FBH-200 (478.001,58), FBI-159 (594.998,81). IVA 19% sobre bases de ~300.000 a ~500.000.
- 0 facturas de venta emitidas: Daniel confirmó que no hubo ventas en octubre. 2 nóminas electrónicas (NOLX 15 y 16): fuera de alcance.

## Estado de la contabilidad antes de importar (solo lectura)
- Octubre 2026 solo tenía el egreso EG-93 (8-oct, crédito a caja 100.000). Sin compras ni ventas.
- 2026: 303 documentos. Compras (05): 26 docs, 10 proveedores, casi todas salen de caja 11050505, consecutivo CP-n (último CP-122, sep). Ventas (04): 32 docs, 28 clientes, consecutivo FELX (último FELX54, sep), cuentas 415550 ingreso, 24080505 IVA, 13050505 clientes, retefuente 13551512 y reteICA 13551805. Documento soporte 05a: 1 (DSN-5).
- FACTURA en compras: "FC" + folio (13 de 26). DETALLE del 529520 en CP-116: GASTOS DE REPRESENTACION.
- Redondeo IVA compras en 2026: 9 exactos, 5 al peso más cercano, 0 hacia abajo, 1 atípico.

## Decisiones de Daniel (3-nov-2026)
1. Proveedor 901013514 (nuevo, sin historial) -> cuenta 529520 (igual que NARU), DETALLE "GASTOS DE REPRESENTACION".
2. Retención: se evalúan como compras; mínimo 27 UVT = 1.414.098 (UVT 2026 = 52.374). Las bases (302.520 a 499.999) no lo alcanzan: sin retefuente ni reteICA.
3. Sin ventas en octubre.

## Juego generado (PAQUETE_ORIGINAL\LEXPERTISE_OCT2026)
- LEXCOM10.cab/.cue/.Ter/.FPT (plantilla AGTCOMP1, .cue con byte 28 = 0 por la lección de NARU) y TERLEX10.DBF/.FPT (1 tercero nuevo para el 766), REVISION_LEXPERTISE_OCT2026.xlsx. Generador: claude/gen_lexpertise.py.
- 4 documentos, 12 líneas: CP-123 (FBH-113, 8-oct, 359.999), CP-124 (FBH-179, 8-oct, 460.002), CP-125 (FBH-200, 8-oct, 478.002), CP-126 (FBI-159, 9-oct, 594.999). Total 1.893.002; IVA 302.245 (24081005); gasto 529520 = total - IVA; crédito caja 11050505. Débitos = créditos 1.893.002.
- REP: total 1.893.000,83 e IVA 302.243,83; diferencia 1,17 pesos de redondeo (IVA al peso más cercano; máximo 0,42 por factura).
- Medición del 95%: no aplica por documento (proveedor sin historial; cuenta definida por Daniel).

## Resultado de la importación (verificado en solo lectura el 3-nov-2026 ~22:55)
- Importado por Daniel (766, 746 y 150). Verificación contra el respaldo de las 16:30 y con verificar.py:
  - Documentos de octubre: 1 tipo 02 (EG-93) + 4 tipo 05 (CP-123 a CP-126); llaves repetidas 0. Documentos 303 -> 307, líneas 1.168 -> 1.180, ninguna perdida ni modificada.
  - Las 12 líneas importadas son idénticas a las generadas (cuentas, tercero, valores, bases, FACTURA y DETALLE).
  - Octubre: 14 líneas, débitos = créditos = 1.993.002 (= 100.000 de EG-93 + 1.893.002).
  - Terceros: MAE_TER 89 -> 90; NIT 901013514 una sola vez (sin duplicados), DV 9, TDOC 31, Bogotá, TIP_PRV 6. Terceros de líneas fuera del maestro: 0.
  - Acumulados: 0 cuentas y 0 pares cuenta-tercero desfasados. Solo cambió octubre: RES_CTA 529520 +1.590.757 (D), 24081005 +302.245 (D), 11050505 +1.893.002 (C); RES_TER pasa de 1.094 a 1.097 filas (3 pares nuevos). Ningún otro período cambió.
- Pendiente (no se puede ver en las tablas leídas): confirmar que octubre 2026 quedó bloqueado de nuevo.

## Calendario tributario (agregado 3-nov-2026 22:19)
- NIT 901800715 (coincide con el del maestro de terceros; sin dígito de verificación, confirmar con el RUT). Último dígito 5 = retención en la fuente e IVA. Últimos dos dígitos 15 = planilla (4.º día hábil).
- Domicilio Bogotá e IVA cuatrimestral (ambos confirmados por Daniel). Revisión interna: 2 días hábiles antes del vencimiento (regla general 10).

| Obligación | Vence | Revisión interna |
|---|---|---|
| Planilla octubre | Vie 6 nov 2026 | Mié 4 nov |
| Retención octubre | Mié 18 nov 2026 | Vie 13 nov |
| ReteICA sep-oct (Bogotá) | Vie 20 nov 2026 | Mié 18 nov |
| Planilla noviembre | Vie 4 dic 2026 | Mié 2 dic |
| Retención noviembre | Mié 16 dic 2026 | Lun 14 dic |
| Planilla diciembre | Jue 7 ene 2027 | Mar 5 ene |
| ReteICA nov-dic (Bogotá) | Vie 15 ene 2027 | Mié 13 ene |
| Retención diciembre | Mar 19 ene 2027 | Vie 15 ene |
| IVA cuatrimestral sep-dic | Mar 19 ene 2027 | Vie 15 ene |

- Fuentes: retención e IVA, tablas de Actualícese y Gerencie; ReteICA Bogotá, Siempre al Día y Alcaldía de Bogotá; planilla, cálculo propio por día hábil con festivos (2 y 16 nov, 8 dic, 1 y 11 ene). Validar contra DIAN y Secretaría de Hacienda antes de fijar.
- Pendiente del RUT: responsabilidades (retención en la fuente, autorretenedor), agente de retención de ICA, ICA propio. El REP de octubre trae 2 nóminas electrónicas: hay planilla (confirmar con nómina).
