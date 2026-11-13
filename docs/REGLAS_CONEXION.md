# CONEXION CENTRO DE... (EMP070 en el SIASoft compartido FERRE_GUAYACANES_CONEXION_SEGMETA_PIANOS) - revision sep/oct 2026

Servidor: Z:\SIASOFT_GENERAL\FERRE_GUAYACANES_CONEXION_SEGMETA_PIANOS\SIASOFT_V23\EMPRESAS\EMP070\CO.SIA. En esa instalacion hay 4 empresas (EMP010, 070, 071, 074): solo se trabaja EMP070 (identificada el 9-nov porque septiembre del libro cuadra con el REP: 14 ventas y 45 compras).
NIT 901775243. Regimen simple (decision de Daniel, 9-nov): sin retenciones en compras ni en ventas. Historial a usar: todo 2026 (ene-sep); septiembre es el mes de referencia ya contabilizado.
Respaldo del CO.SIA (9-nov 20:45): C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\RESPALDO_EMP070_CONEXION_09NOV_2045.zip (98 archivos, sin los .bak/.tbk antiguos; verificado).

## Estado antes de la carga (9-nov-2026, solo lectura)
- Ventas sep+oct: 74/74 en el libro (FCE694-FCE767 con total e IVA iguales al REP). Sep a caja 11050505 (14), oct a bancos 11200505 (60). Nada que generar.
- Compras sep: 45/45 en el libro (2 con contrapartida distinta a 220505: una a 22050505 sin tercero y una al banco 11100510).
- Compras oct: en el libro 9 (CP-303 a CP-311). Pendientes 51 del REP, 23.261.697 en total.

## Formato observado
- Ventas (04): FACTURA vacia, COD_VEN 01, DES_MOV "VENTA DE SERVICIOS"; 413505 CRE base | 24080505 BAS=base CRE iva | caja/bancos DEB total.
- Compras (05, CP-n): gasto DEB (= total - IVA) | IVA DEB BAS=base | 220505 CRE total con DOC_REF = numero. IVA 19% en 24081005 (bienes) o 24081010 (servicios), 5% en 24081027. 66 de 280 compras no llevan IVA. Retenciones: 0 en 2026.
- FACTURA = prefijo + espacio + ultimos 4 digitos del folio (SPRM 5889). DES_MOV "FC <FACTURA> <DETALLE>".
- Documento soporte: tipo 80D, serie DSO: gasto 523515 DEB | 220505 CRE con COD_TER, DOC_MOV y DOC_REF = DSOnn; DES_MOV "DSOnn PRES. SERVICIOS ENTRENAMIENTO"; sin IVA ni retencion.

## Medicion retroactiva (cuenta de gasto por proveedor, aprendiendo solo lo anterior)
- Septiembre: 54,5% por documento (con historial: 24 aciertan, 17 fallan). Proveedores con una sola cuenta 77%; con varias cuentas 4 ok / 11 mal. No llega al 95%: la cuenta se pide a Daniel en el reporte de dudas. IVA, total y tercero salen del REP: 100%.

## RESULTADO CARGA OCTUBRE 2026 (9-nov, noche; la hizo Claude en SIASoft con permiso de Daniel)
- 766: 6 terceros nuevos (sin duplicados). 746: 50 docs CP-312 a CP-361, 146 lineas, D=C 21.261.697; IVA 1.631.640; 220505 CRE 21.261.697; 0 terceros huerfanos.
- DSO26 (80D, 17-oct-2026, $2.000.000, persona natural NIT 53073931; CUFE en el REP): gasto 523515 (decision de Daniel). Se uso el folio de la DIAN (26): en el libro el ultimo era DSO24 y el DSO25 no aparece en el REP. Cargado con 746.
- 150 solo octubre (dos veces): octubre D=C 70.037.844; 0 desfases en RES_CTA y en RES_TER (248 pares cuenta+tercero).
- Reglas definitivas: IVA redondeado al peso (no hacia abajo); contrapartida 220505 con DOC_REF=CP-n; tiquetes a 529520; proveedores sin historial aprobados por Daniel (529525, 529530, 529560, 523505).
- Pendiente: Daniel bloquea el periodo de octubre.
- PDF del DSO26 de la DIAN: catalogo-vpfe.dian.gov.co, buscar con CUFE + NIT del emisor; el PDF baja con clave = ese NIT (a Descargas del PC).

## Leccion 746 (error 1707 .CDX)
- Primer intento dio error 1707 y dejo basura en memoria (luego "Ya existe doc CP-312..." sin que hubiera nada cargado). Solucion: .cue byte 28 = 0 y carpeta limpia sin .CDX; salir del 746 (No a imprimir errores, No a guardar), reabrirlo desde la lista de procesos y reintentar una vez; cargo sin error y se responde Si a "guardar cambios". Verificar siempre leyendo cab_doc/cue_doc del servidor.
- Con computer use: open_application "Sia" abre un SIASoft NUEVO con login (no entrar claves; cerrar con Salir). Para volver a la ventana ya abierta usar clic en la barra de tareas (acceso File Explorer, solo clic).
