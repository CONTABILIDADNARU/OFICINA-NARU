# NARU CONSULTORES (EMP010 en el SIASoft compartido con LEXPERTISE y R&G) - reglas aprendidas, octubre 2026

Servidor: Z:\SIASOFT_GENERAL\NARU_R&G_LEXPERTISE\SIASOFT_V23\SIASOFT_V23\EMPRESAS\EMP010\CO.SIA. En esa instalacion hay 7 empresas (EMP010, 020, 040, 041, 097, 098, 099): solo se trabaja EMP010. No usar la carpeta EXPORT del servidor (tiene archivos de otros trabajos y el 745 la borra).

## Datos de partida
- REP octubre: 21 facturas de venta (FVEN 469-489), 27 facturas de compra, 7 nominas electronicas (NMN, se excluyen).
- Octubre ya registrado a mano: 5 recibos de caja (RC-318 a RC-322) y 1 depreciacion. Sin ventas ni compras.
- Ultimos consecutivos antes de octubre: ventas FE468, compras CP-820.

## Ventas (tipo 04)
- NUM_TRN = FE + folio (FE469). FACTURA vacia. COD_VEN 01. FEC_VEN = FEC_DOC. DES_MOV = "FE### GESTION EMPRESARIAL" en todas las lineas. COD_TER en todas las lineas. Sin centro de costo ni ciudad.
- Las ventas van a CLIENTES 13050505 (decision de Daniel, confirmada con el historial: 85/85 abr-sep). Los recibos de caja (tipo 01) las cancelan despues contra el banco 11200505.
- Orden de lineas: 413508 CRE base | 24080505 BAS=base CRE iva | 13551512 retefuente 4% DEB BAS=base | 13551805 reteICA 0,966% DEB BAS=base | 13551715 reteIVA 15% del IVA DEB BAS=base | 13050505 DEB neto con DOC_REF = numero.
- Redondeo: IVA = 19% de la base, al peso mas cercano (121/121 en el historial). Cada retencion se redondea al peso mas cercano (half-up). Debito Clientes = base + IVA - retenciones (121/121).
- Retenciones por cliente (no vienen en el REP): patron de las ULTIMAS 3 facturas del cliente. Si coinciden se aplica (alta si todo el historial coincide, media si el patron cambio). Si no coinciden: duda. Clientes que cambiaron: uno dejo reteICA desde abril, otro dejo reteIVA desde julio, y en dos hay una factura de la mitad del valor habitual sin retencion.
- Backtest jul-sep (aprendiendo solo lo anterior a cada factura): 25 coinciden, 2 difieren, 9 sin prediccion (cambios de patron).

## Compras (tipo 05, CP-n sin ceros)
- Todas salen de CAJA 11050505 (142 de 147 lineas de credito en abr-sep; 4 a proveedores 220505; 1 retefuente en 6 meses). Decision de Daniel: compras a caja.
- Orden: gasto DEB | IVA descontable DEB BAS=base | caja CRE total. IVA 19% -> 24081005; 5% -> 24081027. Tarifa atipica: se deja 24081005 con el IVA del REP y se marca.
- REGLA DE DANIEL (3-nov-2026): IVA y total de cada factura SIEMPRE cuadran con el REP (gasto = total - IVA); cualquier impuesto distinto al IVA (INC, IC, etc.) se suma a la cuenta principal de gasto. Verificado: diferencia maxima 0,50 pesos por factura (redondeo de centavos).
- NARU redondea el IVA al peso mas cercano (184/188), a diferencia de OCTOPUX que lo hacia hacia abajo.
- FACTURA = "FC" + folio (FC47559). DETALLE = concepto del proveedor/cuenta (PARQUEADERO, ELEMENTOS CAFETERIA, COMBUSTIBLE...). DES_MOV = FACTURA + " " + DETALLE (182/221).
- Cuenta de gasto por proveedor: una sola cuenta desde abril = alta. Varias cuentas, o sin compras desde abril = la cuenta de la ULTIMA VEZ que se relaciono el tercero (regla de Daniel, provisional hasta que confirme a mano); queda marcada baja/media. El DETALLE se toma de ese ultimo documento salvo que sea un error de digitacion no repetido (ej. PARUQEADERO).
- Proveedores nuevos de octubre (decision de Daniel, 3-nov-2026): Miniso y OCTOPUX -> 529520 (Gastos de representacion y relaciones publicas, DETALLE "GASTOS DE REPRESENTACION"); Editorial y Mecanelectro -> 529530 (Utiles, papeleria y fotocopias, DETALLE "PAPELERIA"). Se usan las cuentas del grupo 52 (en compras pasadas nunca el grupo 51). OCTOPUX (NIT 901013514) es otro cliente de Daniel: 5 facturas, operacion entre sus dos empresas.
- Medicion (backtest mayo-sep, aprendiendo meses anteriores): proveedores con una sola cuenta aciertan 85,9%; ~45% de las lineas quedan en dudas (proveedor nuevo o ambiguo). Con 12 o 20 meses de historial da igual. En proveedores con varias cuentas, "ultima vez" acierta 24/38 y "mas frecuente" 26/38 (similar, ~2/3). El 95% no se alcanza solo con regla proveedor-cuenta: las compras de caja menor se clasifican por factura.
- Octubre generado: 27 de 27 compras, CP-821 a CP-847, total 12.875.601, IVA 1.724.117 (REP: 12.875.599,16 y 1.724.115,05; diferencia de redondeo por documento), 80 lineas.

## Formato de importacion
- El juego .cab/.cue/.Ter/.FPT usa la plantilla AGTCOMP1 (formato fijo del 745 de SIASoft v23: sin RC_PROV, FEC_CONT, USUARIO, REVELA, IND_CRUC, FEC_CON, COD_BANC). El .Ter va vacio; los terceros nuevos entran por el 766 con TERNARU10.DBF (plantilla TERVTAORI.DBF).
- Archivos: NARU_OCT2026\ (NARVTA10, NARCOM10, TERNARU10, REVISION_NARU_OCT2026.xlsx). Generador: gen_naru.py + armar.py.

## Problemas conocidos en el servidor
- 745 dio error 3 "El archivo ya esta en uso" (programa EXPORTAR) aun con los demas cerrados. Probable bloqueo de CAB_DOC/CUE_DOC por otra sesion o proceso. El 746 y el 150 pueden dar lo mismo: resolver antes de importar (Archivos abiertos / Administrador de tareas del servidor).
- El shell del equipo (device_bash) no arranca (virtualizacion apagada): se leen los DBF copiandolos al espacio de trabajo.

## Calendario tributario (agregado 3-nov-2026 22:19)
- NIT 901669465 (dato de Daniel, sin digito de verificacion; confirmar con el RUT). Ultimo digito 5 = retencion en la fuente e IVA. Ultimos dos digitos 65 = planilla (11.o dia habil).
- Domicilio Bogota e IVA cuatrimestral (ambos confirmados por Daniel). Revision interna: 2 dias habiles antes del vencimiento (regla general 10).

| Obligacion | Vence | Revision interna |
|---|---|---|
| Planilla octubre | Mie 18 nov 2026 | Vie 13 nov |
| Retencion octubre | Mie 18 nov 2026 | Vie 13 nov |
| ReteICA sep-oct (Bogota) | Vie 20 nov 2026 | Mie 18 nov |
| Planilla noviembre | Mie 16 dic 2026 | Lun 14 dic |
| Retencion noviembre | Mie 16 dic 2026 | Lun 14 dic |
| Planilla diciembre | Mar 19 ene 2027 | Vie 15 ene |
| ReteICA nov-dic (Bogota) | Vie 15 ene 2027 | Mie 13 ene |
| Retencion diciembre | Mar 19 ene 2027 | Vie 15 ene |
| IVA cuatrimestral sep-dic | Mar 19 ene 2027 | Vie 15 ene |

- Fuentes: retencion e IVA, tablas de Actualicese y Gerencie; ReteICA Bogota, Siempre al Dia y Alcaldia de Bogota; planilla, calculo propio por dia habil con festivos (2 y 16 nov, 8 dic, 1 y 11 ene). Validar contra DIAN y Secretaria de Hacienda antes de fijar.
- Pendiente del RUT: responsabilidades (retencion en la fuente, autorretenedor), agente de retencion de ICA, ICA propio. El REP de octubre trae 7 nominas electronicas: hay planilla (confirmar con nomina).
