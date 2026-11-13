# NARU CONSULTORES (EMP010) - bitacora de la importacion de octubre 2026

## Cambios y resultado de la importacion (3-nov-2026)
- TRYP (NIT 901885919, FE485-489): lleva retefuente 4% + reteICA 0,966% (indicado por Daniel; no habia historial). Ej. base 875.500: retefuente 35.020, reteICA 8.457, Clientes 998.368. Ventas finales: 99 lineas, D=C 40.031.600, retenciones 1.527.371, debito Clientes 38.504.229.
- Error 1707 "No se encuentra el archivo .CDX estructural" en el 746: los .cue generados tenian la marca de CDX (byte 28 = 1) sin el .CDX. Solucion que funciono: poner byte 28 = 0 en el .cue (carpeta SIN_CDX). Generar siempre los .cue asi.
- El 766 creo 28 terceros duplicados en MAE_TER (mismo NIT, copia exacta). SIASoft no deja borrarlos ("Clave con movimiento" en cue_doc). Se dejan; efecto: filas repetidas en RES_TER (el 150 crea una fila por registro duplicado, suma correcta). Antes de un 766 comparar los NIT contra MAE_TER para no cargar terceros existentes. Archivo de recuperacion: TER_RECUPERACION_28.DBF.
- Respaldo parcial (24 tablas) en PAQUETE_ORIGINAL\\RESPALDO_EMP010_03NOV_1155, tomado despues del 766 y antes del 746.
- Resultado: 746 ventas 21/21 docs y 99/99 lineas; 746 compras 27/27 y 80/80 (identicas a lo generado); 150 octubre: 0 desfases en RES_CTA y RES_TER, D=C octubre 68.630.462 (54 docs, 198 lineas), 0 terceros huerfanos.
- Pendientes preexistentes (no son de octubre): CP-800 de mayo descuadrado 18.000; jul-sep con cuentas 13659504, 520542, 510542 sin acumular (ausentes de MAE_CTA).
- Al copiar archivos del servidor la ruta puede quedar en minuscula (empresas/emp010/co.sia): verificar.py debe apuntar a la copia recien traida (una vez leyo una copia vieja).
