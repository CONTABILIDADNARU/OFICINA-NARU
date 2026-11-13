# Borrador 350 (retefuente) RUMASA SAS - octubre 2026 (rehecho 5-nov-2026 sobre el libro de septiembre)

Archivo vigente: C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\BORRADORES RETEFUENTE OCTUBRE\RUMASA SAS\BORRADOR_RTE_FTE_RUMASA_OCTUBRE_V2.xlsx (el sin "V2" estaba abierto en Excel y no se pudo reemplazar: el V2 es el bueno).
Base: libro de septiembre de Daniel (mismas formulas y estructura, regla 16). Vence vie 13 nov 2026 (NIT termina en 3); revision interna mie 11 nov.

## Cifras (recalculadas con LibreOffice)
| Casilla | Base | Retencion |
|---|---|---|
| Rentas de trabajo (236505, 2 empleados) | 18.705.000 | 2.200.000 |
| Arrendamientos PJ (CP-001655) | 1.378.000 | 48.000 |
| Compras PJ 2,5 % (CP-001657, agregada) | 2.087.000 | 52.000 |
| Autorretencion 1,1 % (ingresos netos 188.271.533) | 188.272.000 | 2.071.000 |
| **Total a pagar** | | **4.371.000** |
Septiembre fue 2.662.000.

## Criterios
- 236505 SI es retencion por salarios: 2 empleados con base 9.352.500 y retencion 1.100.000 cada uno. La nomina de octubre trae BAS_MOV en 0; base calculada: (17.500.000 - 680.000 - 680.000 - 170.000 - 3.500.000) x 75 % = 9.352.500 (igual a septiembre).
- FTM-00175 (administracion del edificio): SIN retencion (Daniel, 5-nov 16:36); igual la FTM172. FTM-00176 (asistencia contable, persona natural): solo ICA, fuera del 350 (igual que la FTM-173 de septiembre).
- CP-001657 (aseo y cafeteria, 2.086.765): SI lleva retefuente 2,5 % compras (52.169) y reteICA (Daniel, 5-nov 16:48). La contabilidad importada no la trae: agregada al borrador (fila 4 de AUX RTE FTE, columna W).
- Autorretencion: base = todos los ingresos 4xxx del mes; 1,1 %, CIIU 6201, DV 9, seccional 32 (RUT de junio).
- Hoja REP DIAN: 32 columnas y totales por Grupo (emitido 209.009.330; recibido 5.937.516; general 214.946.846).

## Pendientes
1. Corregir CP-001657 a mano en SIASoft (retefuente 23654015 52.169, reteICA y credito 220505) y volver a correr el 150 de octubre. La reteICA va a ReteICA sep-oct (vence 20 nov), no al 350. Tarifa por confirmar (Bogota: compras 4,14 por mil = 8.639; servicios 9,66 por mil = 20.158).
2. El libro de septiembre trae una fila manual de la FTM172 con 3,5 % (38.134) que subio los arrendamientos a 96.000 (CP-001639 aportaba 57.000): si ya se presento, pudo quedar 39.000 por encima.
3. Octubre sin bancos, egresos ni recibos: los rendimientos suben la base de la autorretencion.
4. La hoja DIAN (imagen) sigue siendo la de septiembre.
5. El 236590 de octubre debe coincidir con 4.371.000 cuando se cause.
