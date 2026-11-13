# F&M MOTOS S.A.S (EMP010, instalación SIASOFT_V4_F&MOTOS) - reglas y bitácora (creado 4-nov-2026 12:05; actualizado 13:05)

No confundir con las otras EMP010 del piloto (NARU CONSULTORES, RUMASA). El nombre es la llave (regla 2).

## Alcance de esta empresa (decisión de Daniel, 4-nov-2026)
- SOLO se compara el REP DIAN contra los borradores de impuestos y se preparan esos borradores (IVA bimestral y retención en la fuente).
- NO se lee SIASoft, NO se generan archivos de importación (no hay 766, 746, 150, 745): la contabilidad la lleva una persona aparte, en un servidor remoto. Lo primordial es que lo declarado sea correcto frente al REP.
- Los auxiliares que traen los borradores (AUX INGRESOS, AUX 2408, AUX RTE FTE...) los arma esa persona/Daniel desde el sistema; Claude solo los lee dentro del libro.
- Antes de este cambio de plan se leyó una vez, en solo lectura, el respaldo RESPALDO_EMP010_03NOV_1155 (PAQUETE_ORIGINAL) y el REP de septiembre y octubre. Ese respaldo era anterior a la carga de las ventas de sep-oct y ya no se usa.
- Sin nombres de terceros en los reportes (regla 7), salvo que Daniel los pida (los pidió el 4-nov para revisar proveedores). Mostrar folios, NIT y valores.

## Datos de la empresa (RUT adjuntado por Daniel el 4-nov-2026; actualización, PDF generado 29-jul-2026)
- NIT 902067901, DV 1 (confirmado en el RUT). Razón social: F&M MOTOS S.A.S. Persona jurídica. Domicilio: Bogotá D.C. Dirección seccional: Impuestos de Bogotá, código 32.
- Actividad principal CIIU 4541 (inicio 19-may-2026). Constitución 19-may-2026 y registro 20-may-2026: es una empresa nueva (primer año de operación).
- Responsabilidades del RUT: 05 (renta, régimen ordinario), 07 (retención en la fuente a título de renta), 14 (informante de exógena), 48 (IVA), 55 (beneficiarios finales). NO aparecen: 09 (retención del IVA), 15 (autorretenedor de renta), 59 (autorretención especial, según Gerencie; validar) ni 52 (facturador electrónico, aunque emite FEFM). Sin reteIVA que practicar, coherente con el REP. A pesar de que el RUT no lo muestra, Daniel decidió (4-nov 12:21) que F&M SÍ aplica autorretención con la tarifa correspondiente.
- Último dígito 1; PILA 01 = 2.º día hábil (franja 00-07 sin validar).
- IVA BIMESTRAL hasta fin de año (confirmado por Daniel el 4-nov 12:23): períodos sep-oct (05) y nov-dic (06) de 2026. Para 2027 la periodicidad se define según los ingresos de 2026 (umbral 92.000 UVT); no suponerla.
- Tiene empleados: el REP trae nómina individual (prefijo NOFM): 14 en septiembre y 30 en octubre. La nómina NO entra al IVA ni al cruce de ventas.
- Series de venta: FEFM (facturas), NCFM (notas crédito). Ventas gravadas al 5% (motos). Facturas "mixtas": parte con IVA 5% y parte sin IVA.
- POR CONFIRMAR: si es agente/contribuyente de ICA.
- Cuidado: el libro de retefuente que se recibió era de otra empresa del registro (IGOMA COLOMBIA MR SAS, NIT 901252830). Se corrigieron carátula, NIT, DV, período y seccional (32; la plantilla traía "3.2"). No copiar datos entre empresas.

## Dónde se guardan los borradores (regla 16 de NARU, aplicada tal cual; el de IVA es por analogía, confirmar con Daniel)
- Retefuente: `C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\BORRADORES RETEFUENTE <MES>\F&M MOTOS\BORRADOR_RTE_FTE_FM_MOTOS_<MES>.xlsx` (octubre ya guardado).
- IVA: `C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\BORRADORES IVA <PERIODO>\F&M MOTOS\BORRADOR_IVA_FM_MOTOS_<PERIODO>.xlsx` (septiembre-octubre ya guardado: BORRADORES IVA SEPTIEMBRE-OCTUBRE).
- Libro IVA: hojas Formulario, AUX INGRESOS, AUX 2408, REP DIAN, AUX RTE IVA, AUX NO GRAV (ventas, casilla 40) y AUX NO GRAV COMPRAS (casilla 54), estas dos creadas el 4-nov. Libro retefuente: FORMULARIO, AUX INGRESOS, AUX AUT, AUX RTE FTE, REP DIAN y BORRADOR RETENCION (oculta, con #REF!, residuo de plantilla).
- Se edita el archivo sin perder logos ni vínculos y se verifica recalculando.

## Criterios decididos por Daniel (4-nov-2026)
- F&M vende; no importa. El IVA de las facturas de agencias de aduana, navieras y logística ("IVA importación 19%") se trata como SERVICIOS gravados al 19% (base en casilla 53, IVA en casilla 75), no como importaciones (casillas 45/69/70).
- La parte NO gravada de las facturas de venta mixtas (5 facturas FEFM245, 246, 247, 248 y 260, por $66.740.000) sale de ventas gravadas y va a ventas no gravadas (casilla 40). La hoja AUX NO GRAV lo calcula con fórmulas vivas: ingreso en 41350610 menos base con IVA en 2408, más ventas no gravadas de 41350606. CERRADO 4-nov 12:28: Daniel dijo que esos $66,74 millones van en no gravados y no se les da más vueltas (no se investiga si son matrícula o pagos por cuenta de terceros).
- Casilla 54 (APLICADO 4-nov 12:27): compras no gravadas = facturas sin IVA del REP (155.691.240) + parte sin IVA de las 4 facturas de compra mixtas (1 de la portuaria y 3 de GS Logística: 89.053.510) = 244.744.751, hoja AUX NO GRAV COMPRAS. La base gravada de esas 4 ya estaba en casillas 53/75. Total compras brutas (57) 263.764.000; compras netas (59) 259.599.000. Las "cinco facturas" que mencionó Daniel son las de venta (casilla 40); las de compra son 4.
- Casillas 89 y 93 con IF a cero; controles AV25, AV26 y AV48 con IFERROR (aplicado 4-nov 12:27). Casillas 78 y 84 en cero: confirmado por Daniel que jul-ago no dejó saldo a favor.
- Nómina individual: excluida del IVA. Notas crédito emitidas: base en casilla 42 e IVA en casilla 79 (verificar siempre, es lo que más mueve el impuesto).
- Rete IVA: el REP de sep y oct no trae rete IVA en ningún documento; casilla 85 en cero respaldada.
- Retención a proveedores (4-nov, 12:11): no se retiene a los autorretenedores de renta ni a los 3 proveedores restantes (ver "Retefuente: proveedores").
- Autorretención especial (CERRADO 4-nov 12:21): F&M aplica autorretención con la tarifa correspondiente y el valor del primer borrador es correcto ($8.555.000 = 712.891.000 x 1,2%); total retefuente octubre 9.130.000. La base son TODOS los ingresos del mes sin IVA (gravados y no gravados) menos notas crédito; es el total de ventas del REP (octubre 775.828.671). No se excluyen las ventas no gravadas (aclarado por Daniel 4-nov 12:14, coherente con la regla 16 de NARU). Aunque el RUT no trae la responsabilidad, no volver a cuestionarlo salvo que Daniel lo pida.

## Resultado del borrador de IVA sep-oct (4-nov-2026) - CERRADO
- REP sep+oct: 178 facturas de venta FEFM (IVA 66.822.047,70) y 6 NCFM (IVA 3.403.809,20); 104 facturas recibidas (IVA 3.592.933,44) y 8 notas crédito recibidas (IVA 0).
- Borrador: IVA generado 66.822.000; casilla 79 = 3.404.000; IVA descontable 3.614.000 (incluye $20.628 de IVA de comisiones bancarias que no está en el REP); saldo a pagar 59.804.000 (antes 59.805.000; $1.000 de redondeo al sumar importaciones y servicios). Ingresos brutos 1.427.076.000 = REP; devoluciones 85.176.000.
- Casilla 79 / base de devoluciones = 3,99% (no 5%): normal, la nota NCFM-13 anula la FEFM245 completa, incluida su parte sin IVA ($17,1 millones).
- Carátula completa (año 2026, período 05, NIT, DV 1, razón social, X bimestral, seccional 32), verificada con el RUT.

## Pendientes (IVA)
Ninguno. Daniel cerró el borrador de sep-oct el 4-nov 12:28. Solo queda la revisión final del lun 9 nov antes del vencimiento (mié 11 nov). Menor y sin decisión: hoja oculta con #REF! en el libro de retefuente.

## Resultado del borrador de retefuente octubre (4-nov-2026) - CAPÍTULO CERRADO
- Autorretención especial: base 712.891.000 (ventas de octubre del REP 775.828.671, gravadas y no gravadas, menos notas crédito 62.938.089; coincide con el REP) x 1,2% = 8.555.000. Retenciones practicadas: base 31.377.000, retención 575.000 (servicios 4% y fletes 1%). Total 9.130.000. Daniel confirmó el 4-nov 12:21 que el valor es correcto y cerró el tema; no se modifica el borrador.
- Composición de lo no gravado de octubre, solo informativa: $22.000.000 en 4 facturas de ventas no gravadas (FEFM249, 251, 258, 259) más la parte sin IVA de las 5 facturas mixtas ($66.740.000). Todo ya está dentro de los 775.828.671; no es un valor adicional.
- Pendiente menor: hoja oculta con #REF! (residuo de plantilla).

## Retefuente: proveedores (revisado el 4-nov-2026)
- Fuentes que Daniel adjuntó: "Listado de autorretenedores del impuesto sobre la renta, autorizados por resolución, corte 25 de febrero de 2026" (DIAN) y Resolución 000200 del 27-dic-2024 (grandes contribuyentes, vigencia 2025-2026). Al corte de febrero; un autorretenedor autorizado después no aparecería (RUT: responsabilidad 15).
- Octubre: 10 proveedores recibidos sin retención con alguna factura sobre 4 UVT (UVT 2026 usada: 52.374, validar). 7 son autorretenedores del listado (NIT 835000149, 860532426, 800215775, 860001560, 800249687, 901187760, 900146342; cuatro de ellos también grandes contribuyentes) y NO se les retiene.
- Los otros 3 (NIT 901295223, 901216768, 900499068): Daniel confirmó que no se les aplica retención (dos son entidades financieras o similares y el otro es gran contribuyente). Ojo: el de gran contribuyente no figura en la Res. 000200 de 2024; Daniel lo afirma (puede venir de otra resolución posterior). Sin retefuente faltante en octubre.
- Los 4 proveedores retenidos (NIT 830035851, 800045556, 900243606, 900503710) no aparecen en ninguna de las dos listas: su retención es consistente.
- GS Logística (900503710): se retuvo sobre $1.951.261 de una factura de $25.018.481. Daniel confirmó (4-nov 12:14) que solo la parte de servicio es sujeta a retefuente y que está correcto.
- Regla para los meses siguientes: antes de reportar posible retefuente faltante, cruzar el NIT contra el listado de autorretenedores y la resolución de grandes contribuyentes vigentes; lo que no aparezca va a Daniel con el RUT.

## Cómo se trabaja cada mes
1. Pedir el REP del mes en la fecha del dígito 1 (CALENDARIO_REP.md): octubre ya entregado el 3-nov; noviembre mar 1 dic; diciembre lun 4 ene 2027.
2. Partir del libro del mes anterior de F&M (nunca de otra empresa): actualizar REP DIAN, auxiliares, carátula (año, período, NIT 902067901, DV 1, razón social, seccional 32).
3. Cruzar contra el REP: ingresos, IVA generado, notas crédito (casilla 79), IVA descontable, casilla 54/57, retención de IVA, retefuente por proveedor y autorretención (1,2% sobre ventas netas del REP).
4. Colorear: verde lo verificado, rojo lo pendiente. Guardar en la carpeta del mes (arriba) e informar a Daniel.
5. Si el REP trae rete IVA, rete renta o rete ICA, revisar casillas 85 y las retenciones; en sep-oct venían en cero.

## Calendario tributario (NIT 902067901, último dígito 1; fuente: CALENDARIO_DIAN_2026.md, consultado 4-nov-2026; revisión interna 2 días hábiles antes)
| Obligación | Vence | Revisión interna |
|---|---|---|
| Retención octubre | Mié 11 nov 2026 | Lun 9 nov |
| IVA bimestral sep-oct | Mié 11 nov 2026 (tabla bimestral DIAN, dígito 1; validado con la infografía del 4-nov 12:20) | Lun 9 nov |
| ReteICA sep-oct (Bogotá) | Vie 20 nov 2026, solo si es agente (no consta en el RUT; confirmar) | Mié 18 nov |
| Retención noviembre | Jue 10 dic 2026 | Lun 7 dic |
| Retención diciembre | Mié 13 ene 2027 | Vie 8 ene |
| IVA bimestral nov-dic | Mié 13 ene 2027 (misma tabla) | Vie 8 ene |

## Planillas (separadas de impuestos, regla 13)
- Tiene empleados (nómina individual NOFM en el REP). NIT termina en 01: 2.º día hábil, franja 00-07 SIN VALIDAR contra la tabla oficial.
- Planilla octubre vence mié 4 nov 2026 (revisión mar 30 oct); noviembre mié 2 dic (lun 30 nov); diciembre mar 5 ene 2027 (jue 31 dic). Festivos contados: 2 y 16 nov, 8 y 25 dic, 1 y 11 ene.
- La planilla no depende del REP sino de la nómina.

## Margen para el REP (regla 14, dígito 1)
- Octubre: REP el mar 3 nov (1.er día hábil), contabilidad al día lun 9 nov, revisión lun 9 nov, vence mié 11 nov, colchón 0. En F&M no hay importación ni 746: "contabilidad al día" significa que la persona encargada dejó contabilizado el mes y el borrador se liquida el mismo día.
