# NARU CONSULTORES (EMP010) - noviembre 2026: contabilización de las facturas emitidas el 10-nov (11-nov-2026)

## Qué se hizo
- Ventas FE490 a FE512 (23 facturas FVEN emitidas el 10/11/2026, cobro mensual de NARU), tipo 04, un solo juego: NARVTA11.cab/.cue/.Ter/.FPT en PAQUETE_ORIGINAL\NARU_NOV2026 (más REVISION_NARU_NOV2026.xlsx). Datos tomados de los PDF de las facturas (base, IVA, total) y retenciones por el patrón de las últimas 3 facturas de cada cliente.
- Respaldo previo (9 tablas de CO.SIA): PAQUETE_ORIGINAL\RESPALDO_EMP010_NARU_11NOV.
- Sin 766: los 23 clientes ya existían en MAE_TER. Plantilla AGTCOMP1 (sin vínculo al DBC) y .cue con byte 28 = 0 (sin CDX).
- Importado por Claude operando SIASoft con computer use, con orden expresa de Daniel: 746 (fechas 10/11/2026 a 10/11/2026, archivo NARVTA11.cab, "guardar cambios" -> Sí) y 150 solo noviembre (opciones por defecto). Noviembre ya estaba desbloqueado.

## Resultado (verificación de solo lectura de las tablas del servidor)
- 23/23 documentos y 107/107 líneas; D = C = 41.218.625 (base 34.637.500 + IVA 6.581.125). Retefuente 1.260.440, reteICA 272.990, reteIVA 0; débito Clientes 39.685.195.
- Noviembre: 24 documentos (23 FE + RC-325 del 4-nov), 110 líneas, D = C = 47.208.831. Llaves repetidas 0, terceros fuera del maestro 0, desfases en RES_CTA 0 y en RES_TER 0.
- Retenciones por cliente: HOSTALES MG, A TRES MANOS, MENTES PREVENTIVAS, SOCIETY BAGS, PINTURAS DUCOR, OUSOR, PIANOS FORERO, TREFIELECTRIC, TRADE MARK y ROBS FOODS con retefuente 4% + reteICA 0,966%; TRIP DEL RIO y GRUPO TMH solo retefuente; CONEXION, SEGMENTA y CHUCK BERRY sin retenciones.

## Pendientes para Daniel
- Confirmar con el RUT las retenciones de FE502 (solo retefuente), FE505 (patrón cambió), FE506 (CONEXION, régimen simple) y FE509 (CHUCK BERRY, 1 sola factura en el historial).
- Bloquear de nuevo noviembre cuando lo decida (no lo hace Claude).
- Los recibos de caja que cancelan estas ventas se registran cuando entren los pagos.

## Lecciones de operación (computer use)
- Los menús desplegables no se ven en las capturas: abrir procesos con el 3.er icono de la barra de herramientas (lista con 110 marcado por defecto: NUNCA Enter; seleccionar con clic y verificar con zoom antes de Continuar).
- En el 746 el campo Archivo Contab no se escribe: se usa el botón "..." y se escribe la ruta completa en "Nombre de archivo" del selector.
- Después del 150 el campo Año inicial puede quedar en 2027 y el período procesado sale en amarillo: es normal, no repetir.
