# REGLA GENERAL: formato de los borradores de impuestos (Daniel, 5-nov-2026 10:21)

El libro `BORRADOR_RTE_FTE_NARU_AGOSTO.xlsx` dice NARU, pero es el **formato general para TODOS los impuestos y todas las empresas**: mismas hojas, mismos borradores, misma estructura. Cada vez que Daniel pida montar un impuesto (retefuente 350, IVA 300, ReteICA, etc.) se arma sobre ese formato. No se inventa otro diseno.

Copia de la plantilla: `C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\PLANTILLA_BORRADORES\BORRADOR_FORMATO_GENERAL_RETEFUENTE.xlsx` (solo lectura: se trabaja sobre una copia, no sobre la plantilla).

## Hojas del formato (retefuente)
FORMULARIO | AUX INGRESOS | AUX AUT | AUX RTE FTE | REP DIAN | ESTADO REPORTE DIAN (solo imagen) | BORRADOR RETENCION (oculta, no se toca).

## Como se llena (probado con PARAMO CONNECT y RUMASA octubre 2026)
- FORMULARIO: periodo (casillas Z4/AA4: 10 = octubre), NIT en D11, DV en Q11 (algoritmo DIAN), razon social D13, CIIU AQ14, tarifa autorretencion BD14. Los valores del libro de otra empresa se borran siempre. DV, CIIU y seccional se confirman con el RUT.
- AUX RTE FTE: lineas de credito de las cuentas 2365 del mes tomadas de CUE_DOC (columnas ANO_DOC...NIV_CTA), con columna W CONCEPTO ("Servicios PN", "Compras PJ"...) y un bloque resumen CONCEPTO/BASE/RETENCION con SUMIFS. PJ = NIT 31 que empieza por 8 o 9; el resto PN.
- Casillas del formulario: PJ base en T, retencion en AB; PN base en AG, retencion en AV; todo ROUND(-3). Servicios fila 21, arrendamientos fila 23, compras fila 26, honorarios fila 19.
- AUX INGRESOS: todas las lineas 4xxx del mes; total neto = creditos - debitos (las notas credito restan) en P15; T35 = ROUND(P15,-3); retencion de la autorretencion AB35 = ROUND(T35 x BD14, -3).
- REP DIAN: se pega la hoja completa del REP del mes de esa empresa, **las 32 columnas (A a AF, hasta Total, Estado y Grupo), no solo las 18 primeras**, y debajo un bloque de TOTALES por Grupo (Emitido, Recibido, General) con SUMIFS. Error de RUMASA 5-nov: se pegaron solo 18 columnas y el REP quedo sin la columna Total ni totales (Daniel lo noto). Revisar los borradores anteriores de otras empresas por si tienen el mismo defecto.
- Se edita el libro conservando logos y vinculos (se verifica que sigan las imagenes y los externalLinks) y se recalcula para comprobar el total contra la contabilidad (cierre NI de retenciones, cuenta 236590).
- Guardado: `BORRADORES RETEFUENTE <MES>\<EMPRESA>\BORRADOR_RTE_FTE_<EMPRESA>_<MES>.xlsx` (regla 16 de REGLAS_GENERALES_PILOTO.md).
- Script de apoyo: `claude/build350.py` (PARAMO octubre, parametrizable; la version de RUMASA pega 32 columnas y agrega totales).

## Pendientes de este formato
- Cuando no exista el libro del mes anterior de la empresa, se arma sobre esta plantilla (caso PARAMO y RUMASA octubre).
