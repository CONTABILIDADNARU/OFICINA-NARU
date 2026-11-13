# R&G SST CONSULTORES SAS (EMP040) - auditoria y reglas, octubre 2026 (4-nov-2026)

Instalacion: Z:\SIASOFT_GENERAL\NARU_R&G_LEXPERTISE\SIASOFT_V23\SIASOFT_V23\EMPRESAS\EMP040\CO.SIA (misma instalacion que NARU EMP010 y LEXPERTISE EMP041; solo se trabaja EMP040).
Respaldo (96 tablas activas, sin los .bak viejos de 9, 53 y 65 MB): C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\RESPALDO_EMP040_RG_04NOV_1450.zip
Alcance indicado por Daniel: compras, ventas y documentos soporte. Mes de referencia: todo el historial (2024 a 2026). REP de octubre entregado el 4-nov (el dia que toca para el digito 5).

## Hallazgo principal: octubre YA estaba contabilizado a mano
- El REP trae 11 ventas (FERG218-228), 7 compras recibidas y 4 documentos soporte (DSRG92-95), sin nominas electronicas. El sistema ya tiene exactamente esos 22 documentos en octubre: 04 x11, 05 x7, 05a x4. NO se genero ningun juego de importacion (no hay 766, 746 ni 150 por correr).
- El trabajo de la sesion fue auditar lo registrado contra el REP y contra el historial de cada cliente, proveedor y tercero.
- Verificacion de solo lectura (verificar.py sobre las tablas leidas el 4-nov 14:46): 22 documentos, 89 lineas, debitos = creditos = 11.594.422, 0 llaves repetidas, 0 terceros fuera del maestro, 0 cuentas y 0 pares cuenta-tercero desfasados en RES_CTA / RES_TER. (Desde las tablas no se ve si octubre esta bloqueado: confirmarlo en el programa.)

## Cuadre contra el REP (documento por documento)
- Ventas 11/11: base e IVA iguales al REP. Base 3.140.000 + IVA 596.600 = 3.736.600. Tercero correcto en las 11.
- Documento soporte 4/4: valor igual al REP (4.850.000), tercero correcto y existente en el maestro.
- Compras 7/7 existen. IVA al peso mas cercano en las 7 (igual que NARU; Octopux era hacia abajo). Total REP 3.007.816 vs sistema 3.007.822 (la diferencia son los $6 de CP-124).
- Ninguna diferencia llega al 2% por documento (regla 4).

## Errores de digitacion del registro humano (reportar aparte, no son del agente)
1. CP-121 (FBH-182, 426.001): quedo registrada con el tercero igual al NIT de la propia empresa (901802925) en vez del NIT del proveedor (OCTOPUX 901013514). Las otras dos facturas FBH (CP-120, CP-122) si llevan el proveedor. Los valores estan bien; afecta el auxiliar por tercero y los reportes por proveedor.
2. CP-124 (AHQK-111233): total 985.127 contra 985.121 del REP (diferencia $6): gasto 902.204 cuando debia ser 902.198; el IVA 82.923 si cuadra.

## Dudas de criterio (decide Daniel)
- DSN-93 (800.000): la retefuente paso a 4% (23652535) y el tercero venia con 6% (23652525) en sus 3 documentos anteriores, de 450.000. Confirmar la tarifa y la cuenta.
- CP-125 y CP-126 (mismo proveedor, misma fecha): CP-125 (416.730) a 524010 y CP-126 (11.313) a 524510. Confirmar si ambas deben ir a la misma cuenta.
- CP-123: el proveedor usaba 519525 hasta enero de 2025 y desde marzo de 2025 usa 529525 (octubre sigue lo reciente). Solo informativo.

## Reglas aprendidas del historial (sirven para el proximo mes)
### Ventas (tipo 04)
- NUM_TRN = FERG + folio. COD_VEN 01. DES_MOV = "GESTION EMPRESARIAL <MES> 2026". FACTURA vacia.
- Lineas: ingreso 415550 CRE (algunas con 413508 o 413509) | IVA 24080505 CRE (BAS=base) | retefuente 4% 13551512 DEB (BAS=base) | reteICA 0,966% 13551805 DEB (BAS=base) | Clientes 13050505 DEB neto con DOC_REF = numero.
- Retenciones por cliente: los 11 de octubre repiten el patron de las ultimas facturas del cliente (cuentas y valores). Retefuente 4% y reteICA 0,966% al peso mas cercano (ej. base 330.000: 13.200 + 3.188).
- Notas credito: tipo 08, NUM_TRN NCRG + numero, FACTURA = mismo numero, DETALLE "ANULACION FERG<n>", 417510 DEB + 24080510 DEB / 13050505 CRE con DOC_REF = factura anulada. 13 en 2026.
### Documento soporte (tipo 05a, minuscula en CAB_DOC)
- NUM_TRN = DSN-<folio> (DSN-95 = DSRG95). FACTURA = DSRG + folio. DETALLE libre (ej. ARRENDAMIENTO OCTUBRE 2026).
- Lineas: gasto DEB | retefuente CRE (BAS=base) | ICA 236810 CRE 0,966% (BAS=base) | 220505 CRE neto con DOC_REF = NUM_TRN.
- Cuentas de retefuente en uso: 23652525 = 6%, 23652535 = 4%, 23653010 = 3,5% (arrendamientos, gasto 522005). Gasto frecuente 523515; tambien 512005 y 522005. La cuenta y la retencion de cada tercero se repiten casi siempre (3 de 4 en octubre identicos al ultimo documento del tercero).
### Compras (tipo 05, CP-n sin ceros)
- Casi todas a caja 11050505 (algunas a 220505). FACTURA = FC + digitos del folio (a veces recortado). DETALLE = concepto del proveedor.
- Orden: gasto DEB | IVA 24081005 (o 24081027 al 5%) DEB BAS=base | caja CRE total. Gasto = total - IVA; sin retencion en compras en 2026 (ninguna de las 25 de 2026 lleva 2365).
- Compras a OCTOPUX: son compras, sin retencion, gasto 529520 (igual que NARU y LEXPERTISE).
- Siguientes consecutivos: compras CP-127, ventas FERG229, DS DSN-96, notas credito NCRG25.

## Cifras de octubre utiles para el 350
- Retefuente de los 4 DS: 188.750 (152.000 al 4% + 36.750 al 3,5%). ReteICA retenido en los DS: 46.851. Compras sin retencion.
- Las retenciones de las ventas (cuenta 1355) las practican los clientes a la empresa: son anticipo a favor, no se declaran como retencion practicada.
- Autorretenedor especial (casilla 59): NO confirmado; sale del RUT. No se supone.
- Si Daniel pide el borrador del 350, va a PAQUETE_ORIGINAL\BORRADORES RETEFUENTE OCTUBRE\R&G SST CONSULTORES (regla 16); se necesita el libro del mes anterior.

## Calendario tributario (agregado 4-nov-2026)
- NIT 901802925 (dato de EMPRESAS_NIT, sin DV; confirmar con el RUT). Ultimo digito 5 = retencion e IVA. Ultimos dos digitos 25 = planilla (5.o dia habil; tabla PILA por validar).
- Domicilio Bogota e IVA cuatrimestral: SUPUESTOS (como NARU y LEXPERTISE); Daniel debe confirmarlos con el RUT. El REP no los trae.
- Revision interna: 2 dias habiles antes del vencimiento.

| Obligacion | Vence | Revision interna |
|---|---|---|
| Planilla octubre | Lun 9 nov 2026 | Jue 5 nov |
| Retencion octubre | Mie 18 nov 2026 | Vie 13 nov |
| ReteICA sep-oct (Bogota) | Vie 20 nov 2026 | Mie 18 nov |
| Planilla noviembre | Lun 7 dic 2026 | Jue 3 dic |
| Retencion noviembre | Mie 16 dic 2026 | Lun 14 dic |
| Planilla diciembre | Vie 8 ene 2027 | Mie 6 ene |
| ReteICA nov-dic (Bogota) | Vie 15 ene 2027 | Mie 13 ene |
| Retencion diciembre | Mar 19 ene 2027 | Vie 15 ene |
| IVA cuatrimestral sep-dic | Mar 19 ene 2027 | Vie 15 ene |

- REP (digito 5): octubre se pidio mie 4 nov; contabilidad al dia mar 10 nov; REP de noviembre mie 2 dic; de diciembre mar 5 ene 2027 (ver CALENDARIO_REP.md).
- Planilla: el REP de octubre no trae nominas electronicas. Un solo mes no prueba que no haya empleados: mirar los REP de agosto y septiembre antes de descartar la planilla. Queda "por confirmar" (regla 13).
- Fuentes: CALENDARIO_DIAN_2026.md (retencion, IVA y ReteICA); planilla por dia habil con festivos 2 y 16 nov, 8 dic, 1 y 11 ene. Pendiente del RUT: responsabilidades, autorretenedor, agente de ICA.

## Estado
- Octubre: auditado, sin documentos por importar. Pendientes de Daniel: los 2 errores de digitacion, 2 dudas de criterio, confirmar bloqueo de octubre, confirmar con el RUT ciudad e IVA.
