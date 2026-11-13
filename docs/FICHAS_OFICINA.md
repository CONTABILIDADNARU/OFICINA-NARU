# FICHAS DE OFICINA (modelo, actualizado 9-nov-2026 21:45)

Cada ficha es lo que la oficina virtual necesita para crear el espacio de una empresa (regla 12 de REGLAS_GENERALES_PILOTO.md). Es el único lugar donde se guardan las fichas. Sin nombres de terceros. El estado oficial es el de esta ficha; la página es una vista.

Campos: nombre y número SIASoft | NIT sin DV y ciudad | estado de un renglón (Aplicado / Espera tu decisión / Espera tu aprobación / Por confirmar) | Listo | Falta | Siguiente paso | fechas de impuestos | fechas de planillas (separadas, regla 13).

Calendario común de las 4 primeras (Bogotá, IVA cuatrimestral, ReteICA Bogotá bimestral; revisión interna 2 días hábiles antes). F&M MOTOS tiene calendario propio (IVA bimestral, termina en 1). Fechas por validar contra DIAN, Secretaría de Hacienda y UGPP/operador PILA; responsabilidades, autorretenedor, agente de ICA y si la empresa tiene empleados siguen por confirmar con el RUT y con nómina.

## OCTOPUX PUBLICIDAD SAS
- NIT 901013514 (termina en 4; planilla por los dos últimos dígitos, 14 = 3.er día hábil), Bogotá.
- Estado: Aplicado.
- Listo: compras y ventas de octubre en la contabilidad original. Retefuente de octubre (borrador 350) REVISADA por Daniel el 4-nov 12:57: total a pagar 20.832.000 (ver BORRADOR_350_OCTOPUX_OCT2026.md).
- Falta: unos pendientes que la persona encargada corrige a mano; no hay cifras de verificación guardadas. Del 350: pegar el REP de octubre en su hoja y mover o borrar el archivo suelto mal ubicado.
- Siguiente paso: armar sus reglas por proveedor (ver REGLAS_OCTOPUX.md); la retención vence 17 nov.
- Impuestos: retención oct vence 17 nov (revisión 12 nov; borrador ya revisado); ReteICA sep-oct 20 nov (18 nov; octubre 696.293 informativo); retención nov 15 dic (11 dic); ReteICA nov-dic 15 ene (13 ene); retención dic e IVA cuatrimestral 18 ene (14 ene).
- Planillas: oct vence 5 nov (revisión 3 nov); nov vence 3 dic (1 dic); dic vence 6 ene (4 ene).

## NARU CONSULTORES (EMP010)
- NIT 901669465 (termina en 5; planilla 65 = 11.º día hábil), Bogotá.
- Estado: Aplicado.
- Listo: octubre importado y verificado; ventas 21/21 y compras 27/27; D=C 68.630.462; 0 terceros huérfanos; 150 sin desfases.
- Falta (anterior a octubre): compra CP-800 de mayo descuadrada por $18.000; 3 cuentas (13659504, 520542, 510542) sin acumular jul-sep; 28 terceros duplicados que SIASoft no deja borrar.
- Siguiente paso: decidir si se corrige CP-800 y si se crean las 3 cuentas.
- Impuestos: retención oct vence 18 nov (revisión 13 nov); ReteICA sep-oct 20 nov (18 nov); retención nov 16 dic (14 dic); ReteICA nov-dic 15 ene (13 ene); retención dic e IVA cuatrimestral 19 ene (15 ene).
- Planillas: oct vence 18 nov (revisión 13 nov); nov vence 16 dic (14 dic); dic vence 19 ene (15 ene).

## PARAMO CONNECT (EMP061)
- NIT 901987014 (termina en 4; planilla 14 = 3.er día hábil), Bogotá.
- Estado: Aplicado (confirmado por Daniel el 3-nov 22:47).
- Listo: octubre importado (88 DS, 13 notas de ajuste, 3 ventas, 4 compras según el juego generado).
- Falta: registrar la verificación de solo lectura y confirmar bloqueo del período; confirmar cómo se resolvieron FVE-739 (retefuente según RUT), FEPC33 y los 22 DS cercanos a $1.750.905.
- Siguiente paso: correr verificar.py y anotar cifras.
- Impuestos: iguales a Octopux (termina en 4).
- Planillas: iguales a Octopux (14).

## LEXPERTISE (EMP041)
- NIT 901800715 (termina en 5; planilla 15 = 4.º día hábil), Bogotá.
- Estado: Aplicado.
- Listo: 4 compras CP-123 a CP-126 por $1.893.002; verificado en solo lectura el 3-nov (4/4 docs, 12/12 líneas, D=C, 0 desfases); sin ventas.
- Falta: confirmar que octubre quedó bloqueado.
- Siguiente paso: confirmar el bloqueo.
- Impuestos: iguales a Naru (termina en 5).
- Planillas: oct vence 6 nov (revisión 4 nov); nov vence 4 dic (2 dic); dic vence 7 ene (5 ene).

## F&M MOTOS S.A.S (EMP010, instalación SIASOFT_V4_F&MOTOS)
- NIT 902067901 (DV 1 confirmado con el RUT; termina en 1; planilla 01 = 2.º día hábil, por validar), Bogotá D.C., seccional 32, CIIU 4541, empresa nueva (constituida 19-may-2026).
- Estado: Aplicado (borradores de octubre y sep-oct cerrados por Daniel el 4-nov 12:24; pendiente solo la revisión final del lun 9 nov).
- Alcance: solo se compara el REP DIAN contra los borradores de impuestos (IVA bimestral y retención en la fuente). No se lee SIASoft ni se cargan archivos: la contabilidad la lleva una persona aparte en un servidor remoto (ver REGLAS_FM_MOTOS.md).
- Listo: borrador de IVA sep-oct (saldo a pagar 59.804.000; IVA bimestral hasta fin de año; sin saldo a favor de jul-ago, casillas 78/84 en cero correctas) y borrador de retefuente de octubre (total 9.130.000, con autorretención especial 8.555.000), con carátula, NIT, DV 1, período y seccional 32 verificados con el RUT; guardados en PAQUETE_ORIGINAL. Proveedores de octubre revisados contra el listado de autorretenedores y grandes contribuyentes; sin retefuente faltante.
- Falta (menores, sin decisión de Daniel): casilla 54 informativa (unos 244,7 millones frente a 155,7); naturaleza de los 66,7 millones sin IVA en 5 facturas de venta; IF en casillas 89/93 y IFERROR en controles.
- Siguiente paso: revisión final de retención e IVA el lun 9 nov; REP de noviembre el mar 1 dic.
- Impuestos: retención oct e IVA bimestral sep-oct vencen mié 11 nov (revisión lun 9 nov); ReteICA sep-oct 20 nov (18 nov), solo si es agente; retención nov 10 dic (7 dic); retención dic e IVA bimestral nov-dic 13 ene (8 ene). Tabla bimestral validada con la infografía del 4-nov (ver CALENDARIO_DIAN_2026.md).
- Planillas: tiene empleados (nómina individual en el REP de sep y oct). Oct vence mié 4 nov (revisión 30 oct); nov vence 2 dic (30 nov); dic vence 5 ene (31 dic). Franja 00-07 sin validar.

## R&G SST CONSULTORES SAS (EMP040)
- NIT 901802925 (termina en 5; planilla 25 = 5.º día hábil, por validar), Bogotá (por confirmar con el RUT).
- Estado: Espera tu decisión.
- Listo: octubre ya estaba contabilizado a mano y cuadra con el REP: 11 ventas, 7 compras y 4 documentos soporte (22 de 22). Verificación de solo lectura el 4-nov: D=C 11.594.422, 0 terceros huérfanos, 0 desfases. Respaldo de CO.SIA en PAQUETE_ORIGINAL. No hay nada que importar.
- Falta: 2 errores de digitación para corregir a mano (CP-121 con el tercero de la propia empresa en vez del proveedor; CP-124 con $6 de más) y 2 dudas (tarifa de retefuente de DSN-93; cuenta distinta en CP-125 y CP-126). Confirmar que octubre quedó bloqueado, el RUT (ciudad, IVA cuatrimestral, autorretenedor) y si hay planilla.
- Siguiente paso: tu decisión sobre las dudas y, con la contabilidad al día (10 nov), el borrador de retefuente (ver REGLAS_RG_SST_CONSULTORES.md).
- Impuestos: iguales a Naru (termina en 5): retención oct vence 18 nov (revisión 13 nov); ReteICA sep-oct 20 nov (18 nov); retención nov 16 dic (14 dic); ReteICA nov-dic 15 ene (13 ene); retención dic e IVA cuatrimestral 19 ene (15 ene).
- Planillas: oct vence lun 9 nov (revisión jue 5 nov); nov vence lun 7 dic (3 dic); dic vence vie 8 ene (6 ene). Por confirmar si tiene empleados: el REP de octubre no trae nóminas electrónicas.

## RUMASA SAS (EMP010, instalación MOUNTAIN)
- NIT 901053453 (DV 9, seccional 32 y CIIU 6201 confirmados con el RUT de junio; termina en 3; planilla 53 = 9.º día hábil, por validar), Bogotá, CIIU 6201.
- Estado: Espera tu decisión.
- Listo: octubre importado por Daniel y verificado en solo lectura el 5-nov: 21 documentos nuevos (ventas 3, compras 15, documento soporte 2, nota crédito 1), 197.791.750 nuevos igual al REP, D=C, 0 desfases, 0 terceros huérfanos, 2 terceros nuevos. Borrador de retefuente de octubre armado el 5-nov sobre el libro de septiembre (ver BORRADOR_350_RUMASA_OCT2026.md): salarios 2.200.000 + arrendamiento 48.000 + autorretención 1,1 % sobre 188.272.000 = 2.071.000; total 4.371.000 (arrendamiento 48.000 y compra CP-001657 52.000; archivo V2).
- Falta: corregir a mano en SIASoft la CP-001657 (retefuente 52.169 y reteICA) y correr el 150; revisar si la fila manual de la FTM172 en el borrador de septiembre (38.134) debía estar; confirmar que octubre quedó bloqueado; octubre aún no tiene bancos, egresos ni recibos (los rendimientos suben la base de la autorretención); pegar la imagen del estado DIAN de octubre.
- Siguiente paso: tu revisión del borrador antes del mié 11 nov.
- Impuestos: retención oct vence vie 13 nov (revisión mié 11 nov); retención nov lun 14 dic (jue 10 dic); retención dic vie 15 ene (mié 13 ene). IVA bimestral o cuatrimestral y ReteICA por confirmar (el RUT trae responsabilidad 48 de IVA, sin periodicidad).
- Planillas: tiene empleados (nómina contabilizada). Oct vence vie 13 nov (revisión mié 11 nov); nov vence lun 14 dic (jue 10 dic); dic vence vie 15 ene (mié 13 ene). Franja 50-57 sin validar.

## CONEXIÓN CENTRO DE LIDERAZGO Y BIENESTAR SAS (EMP070, instalación FERRE_GUAYACANES_CONEXION_SEGMETA_PIANOS)
- NIT 901775243 (termina en 3; planilla 43 = 8.º día hábil, por validar), ciudad por confirmar con el RUT. Régimen simple (decisión de Daniel, 9-nov): sin retenciones en compras ni en ventas. En esa instalación hay 4 empresas (EMP010, 070, 071, 074): solo se trabaja la EMP070.
- Estado: Aplicado en SIASoft, pendiente que Daniel bloquee octubre (en la oficina figura "Por confirmar" hasta que lo marque).
- Listo: octubre cargado el 9-nov por Claude con permiso de Daniel: 6 terceros nuevos (766); 50 compras CP-312 a CP-361, 146 líneas, D=C 21.261.697, IVA 1.631.640; documento soporte DSO26 por 2.000.000 a la cuenta 523515; 150 de octubre sin desfases (248 pares); octubre completo D=C 70.037.844; 0 terceros huérfanos. Ventas sep-oct (74 de 74) ya estaban en el libro. Respaldo de CO.SIA en PAQUETE_ORIGINAL (RESPALDO_EMP070_CONEXION_09NOV_2045.zip).
- Falta: que Daniel bloquee octubre; en septiembre la regla de cuenta de gasto por proveedor acertó solo 54,5 % por documento (no llega al 95 %): la cuenta de proveedores sin historial la aprueba Daniel (ver REGLAS_CONEXION.md).
- Siguiente paso: bloquear octubre y marcarlo en la oficina; confirmar con el RUT ciudad, qué declara en régimen simple y cada cuánto, y si tiene empleados.
- Impuestos: por confirmar (régimen simple; no se asumen fechas de retención ni de IVA).
- Planillas (tentativas, por validar, y por confirmar si tiene empleados): oct vence jue 12 nov (revisión mar 10 nov); nov vence vie 11 dic (mié 9 dic); dic vence jue 14 ene (mar 12 ene).
