# MUNDO TECH (EMP010, instalación SISOFTMUNDOTECH) - ventas de noviembre 2026 con el REP (actualizado 11-nov-2026 11:25)

Complementa claude/REGLAS_MUNDO_TECH.md. Cambio de alcance (Daniel, 11-nov 11:02): "contabilicemos noviembre con el REP DIAN". Siguen fuera planillas y nómina.
NUNCA pedir la plantilla 745 (instrucción permanente de Daniel): los .cab/.cue/.Ter/.FPT se arman con la estructura de CAB_DOC, CUE_DOC y mae_ter del propio CO.SIA (byte 28 del encabezado = 0 en .cab/.cue y 2 en .Ter; sin enlace al DBC).

## Regla de ventas (tipo 04, serie CCM; arriendo mensual)
- 415505 CRE base (COD_CIU 01) | 24080505 CRE IVA con BAS = base | 13551520 DEB retefuente 3,5% de la base (solo clientes que la practican) | 13551805 DEB ReteICA 0,966% de la base (idem) | 13050505 DEB total menos retenciones, SALDO igual y DOC_REF = número de factura.
- DES_MOV "ARRIENDO <local>" (LC01, LCB.., BDG..): el local sale de la factura de octubre del mismo cliente y valor.
- Base = total - IVA; IVA al peso. Las facturas se emiten los primeros días del mes (todas del 3-nov).
- El REP no trae retenciones (vienen en 0): se aprenden del mes anterior por cliente.
- Medición retroactiva octubre (solo SIASoft): estructura igual a la más frecuente del cliente 50/54 (92,6 %); igual al mes anterior ~96 %.

## Cómo se importa en esta instalación (lecciones del 11-nov)
- Acceso: la ventana es `sia.exe` de ...\mundotech\sisoftmundotech (resolver "sia.exe" en computer_resolve_access). El acceso "SIASOFT NARU" es de OTRA empresa: no usarlo. Verificar en la barra "Empresa:010 - CENTRO COMERCIAL MUNDO TECH SAS".
- Menú Procesos: tecla alt+p (el clic no lo despliega en las capturas). Lista de procesos: la fila 110 sale resaltada por defecto, nunca continuar sin elegir antes la fila.
- 746: fechas 01/11/2026 a 30/11/2026; "Archivo Contab" se elige con el botón "..." (el campo no admite escritura) y se escribe la ruta completa del .cab en el cuadro Nombre de archivo.
- La ruta NO puede tener espacios: con "MUNDO TECH NOV2026\IMPORTAR" dio error 36 (línea 147/83, programa 0000FQXL0014). Con C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\MTNOV2026\MTVTANOV26.cab cargó sin error; pregunta "¿guardar cambios?" y se responde Sí.
- 150: Año 2026, marcar solo el mes; el año inicial salta a 2027 al terminar.

## Resultado (11-nov-2026 11:19 a 11:25) - IMPORTADO Y VERIFICADO
- Lote REP del 6-nov, folios 1474 a 1523 (todas del 3-nov): base 132.363.344; IVA 25.149.034; total 157.512.378 (REP 157.512.379,36); retefuente 635.959 (6 docs); ReteICA 138.699 (4 docs); 13050505 por 156.737.720.
- 746: 50/50 documentos y 160/160 líneas, D = C 157.512.378, folios consecutivos sin duplicados, 0 terceros huérfanos.
- 150 solo noviembre: 0 desfases en RES_CTA (41 cuentas) y en RES_TER (144 pares cuenta+tercero). Mes de noviembre D = C 159.750.378 (incluye 2 documentos de compras ya existentes).
- 5 alertas de clientes con varios locales del mismo valor (local y retenciones por orden): en REPORTE_DUDAS_VENTAS_NOV2026.csv.
- Archivos: PAQUETE_ORIGINAL\MTNOV2026\MTVTANOV26.* (usados) y PAQUETE_ORIGINAL\MUNDO TECH NOV2026\ (detalle y dudas). Respaldo CO.SIA previo: PAQUETE_ORIGINAL\RESPALDO_MUNDOTECH_EMP010_CO.SIA_11NOV_1115.zip.
- Noviembre NO se bloquea: el mes sigue abierto (compras y el REP completo llegan el 1-dic).

## Otros hallazgos del 11-nov
- CP-000460 (fecha 1-dic, período 12) parece duplicado de CP-000459 (período 11).
- Cierre de octubre en SIASoft (IN-000058) 6.427.000 contra borrador del F.350 6.632.000: honorarios +430.300, servicios -126.500, autorretención -509.000. El F.350 de octubre vence el 12-nov.
