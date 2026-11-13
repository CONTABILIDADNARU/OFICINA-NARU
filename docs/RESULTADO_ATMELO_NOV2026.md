# ATMELO INVERSIONES (EMP055) - noviembre 2026: importacion de ventas por Claude (6-nov 12:30)

## Resultado (IMPORTADO por Claude operando SIASoft con computer use, con visto bueno de Daniel)
- Archivo: ATMVTA11.cab/.cue/.Ter/.FPT (PAQUETE_ORIGINAL\ATMELO_NOV2026), REP 1-6 nov: 10 ventas FE-710 a FE-719 (fecha 04/11/2026).
- 746 (fechas 04/11 a 04/11): pregunta "guardar los cambios" -> Si. Periodo noviembre ya estaba desbloqueado por Daniel.
- 150: solo Noviembre 2026, sin marcar opciones destructivas (defecto: revisar cuerpos sin cabeza).
- Verificacion de solo lectura (tablas del servidor): 10 documentos, 30 lineas, D = C = 1.219.293 (417055 CRE 1.024.616 | 24080505 CRE 194.677 | 11050505 DEB 1.219.293). Cero desfases en RES_CTA y RES_TER, cero terceros huerfanos (222222222222 ya existia). No hizo falta 766.
- Pendiente: bloquear de nuevo el periodo (lo hace Daniel). Posible duplicado si el POS/facturacion tambien contabiliza FE-710..719 (el 746 rechaza llaves existentes).

## Leccion tecnica (error 1976 "No es posible resolver el vinculo primario" / error 1 "cod_dbf.dbc no existe")
- Las tablas de EMPxxx\CO.SIA pertenecen a la base cod_dbf.dbc: su encabezado DBF trae al final 263 bytes con el vinculo "cod_dbf.dbc". Si el juego del 746 se arma con encabezados de esas tablas, el 746 busca el DBC y falla.
- Solucion: poner en cero los 263 bytes finales del encabezado (hl-263..hl) de .cab, .cue y .Ter. Las plantillas AGTCOMP1 ya vienen sin vinculo. Copiar cod_dbf.* al lado NO sirve.
- Los menus desplegables de SIASoft no se ven en capturas: navegar con el icono de Procesos de la barra (3er icono, lista con 110 marcado por defecto: NUNCA Enter; seleccionar con clic y Continuar). Ruta a pasar a computer use: \\servidor\empresasnaru\...\SIASOFT_V23\sia.exe completa.
- El 745 no pide carpeta: escribe en SIASOFT_V23\EXPORT del servidor y la borra (esa carpeta tiene ~200 MB de historicos): no usarlo sin respaldar.
