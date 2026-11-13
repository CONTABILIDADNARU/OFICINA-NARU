# CENTRO COMERCIAL MUNDO TECH S.A.S ("MUNDO TECH") - reglas y bitácora (creado 5-nov-2026 11:35; actualizado 12:05)

No confundir con F&M MOTOS (otra empresa, otro chat). Sin nombres de terceros en los reportes (regla 7).

## Alcance (decisión de Daniel, 5-nov-2026)
- Se revisan impuestos y borradores en Excel y se mantienen fechas claras de impuestos. Sin archivos de importación (no hay 766, 746, 150, 745).
- Planillas (PILA): se IGNORAN por ahora (dicho por Daniel).
- Carpetas: impuestos `Z:\ARCHIVO_EMPRESAS\MUNDOTECH\IMPUESTOS` (consolidados 2025 y 2026; subcarpetas DIAN, ICA, IVA 2025-2026, RENTA, RTE FTE 2026 hasta septiembre, RTE ICA 2026 hasta bimestre 5) y SIASoft `Z:\SIASOFT_GENERAL\MUNDOTECH\SISOFTMUNDOTECH\SISOFTMUNDOTECH` (empresa EMP010, única de esa instalación).
- 5-nov 11:41: Daniel autorizó leer SIASoft en solo lectura para cruzar los cierres contra los consolidados. Se leyeron copias de RES_CTA y MAE_CTA de EMP010 y los dos consolidados; no se escribió nada. SIASoft seguía en uso (octubre en contabilización), así que las cifras son una foto de las 11:45.
- Formato de los borradores: REGLA_FORMATO_BORRADORES.md.

## Datos de la empresa (RUT adjuntado el 5-nov-2026; PDF generado 30-jun-2026)
- NIT 901817662, DV 1 (coincide con la fila 51 de EMPRESAS_NIT.md). Persona jurídica. Domicilio Bogotá D.C., seccional Impuestos de Bogotá (32). CIIU 6810 (inicio 1-abr-2024).
- Responsabilidades: 05 (renta, régimen ordinario), 07 (retención), 14 (exógena), 48 (IVA), 52 (facturador electrónico), 55 (beneficiarios finales). NO aparecen 09, 15 ni 47 (SIMPLE).
- Último dígito 2. IVA CUATRIMESTRAL y ReteICA BIMESTRAL (dicho por Daniel el 5-nov). UVT 2026: 52.374.
- ICA propio: SIASoft SÍ lo registra (2025: gasto 14.375.000 en 521505, 13.638.000 por pagar en 2412 tras 737.256 de retenciones a favor, pagado en 2026). Periodicidad (anual o bimestral) y fecha por confirmar con Daniel. En 2026 aún no se ha causado.

## Calendario tributario (NIT terminado en 2; fuente: CALENDARIO_DIAN_2026.md; revisión interna 2 días hábiles antes)
| Obligación | Período | Vence | Revisión interna |
|---|---|---|---|
| Retención en la fuente (F.350) | Octubre 2026 | Jue 12 nov 2026 | Mar 10 nov |
| ReteICA Bogotá | Sep-oct 2026 (bim. 5) | Vie 20 nov 2026 | Mié 18 nov |
| Retención en la fuente | Noviembre 2026 | Vie 11 dic 2026 | Mié 9 dic |
| IVA cuatrimestral (F.300) | Sep-dic 2026 | Jue 14 ene 2027 | Mar 12 ene |
| Retención en la fuente | Diciembre 2026 | Jue 14 ene 2027 | Mar 12 ene |
| ReteICA Bogotá | Nov-dic 2026 (bim. 6) | Vie 15 ene 2027 | Mié 13 ene |
- En noviembre NO hay IVA por presentar. Renta, exógena y beneficiarios finales: sin fecha hasta el calendario 2027. ICA propio: por confirmar.
- Festivos contados: 2 y 16 nov, 8 y 25 dic de 2026; 1 y 11 ene de 2027.

## Margen para el REP (regla 14; dígito 2, colchón de 1 día hábil)
| Retención de | REP del mes | Contabilidad al día | Revisión | Vence |
|---|---|---|---|---|
| Octubre | Mar 3 nov | Lun 9 nov | Mar 10 nov | Jue 12 nov |
| Noviembre | Mar 1 dic | Lun 7 dic | Mié 9 dic | Vie 11 dic |
| Diciembre | Lun 4 ene 2027 | Vie 8 ene | Mar 12 ene | Jue 14 ene |

## Cruce de cierres SIASoft vs consolidados (5-nov-2026, solo lectura)
Cuadra: 2025 ene-nov exacto (retefuente total por mes, autorretención, ReteICA de los 6 bimestres, IVA cuatrimestres 1 y 2). 2026: retefuente total ene-jun y sep; ReteICA bimestres 1, 3 y 4; IVA cuatrimestre 1 (27.301.000, pagado en mayo).
No cuadra o falta (SIASoft contra consolidado 2026):
1. Retefuente total (cuenta 236590, créditos): jul +4.976.000 (igual al valor de junio; parece junio cerrado otra vez) y ago +163.000 (145.000 de autorretención + 18.000 de servicios PJ). Total ene-sep: SIASoft 66.410.000 vs declarado 61.271.000 (+5.139.000).
2. Autorretención (13551905): SIASoft 42.079.000 vs declarado 41.934.000. Todo en agosto: SIASoft 4.685.000 (3,5% sobre 133,86 millones) vs declarado 4.540.000 (base 129.716.000). La celda SIASOFT del consolidado (32.709.000) solo suma ene-jul; por eso muestra 9.225.000 de diferencia (ago + sep). La base declarada difiere de SIASoft por mes (feb +5.168.299; mar +3.807.315; may y jun +2.85 millones; jul -10.457.817; ago -4.147.334) pero en el año queda en 262.
3. Pagos de retefuente sin registrar: saldo de 236590 al 30-sep 37.594.000 vs 7.416.000 esperado (solo sep): 30.178.000 = declaraciones de ene (6.982.000), jun (4.976.000), jul (11.617.000 cerrado) y ago (6.603.000) sin su pago en esa cuenta.
4. Compras PJ julio: base declarada 30.255.000 y retención 756.000 sin crédito en 23654015 en julio. La diferencia de base que marca el consolidado (27.536.992 x 2,5% = 688.425) es eso.
5. Servicios PJ: declarado 408.000 vs 125.300 retenidos (4% de 3.133.000); la cuenta 23652535 queda con saldo débito de 282.960 (cierre de julio por 390.060).
6. Honorarios 10% (23651505): 435.180 retenidos jul-sep (610.280 con octubre) sin declarar ni cerrar. En 2025 también (564.850).
7. ReteICA: el bimestre 2 (mar-abr, vence 22-may) no tiene declaración en el consolidado; SIASoft retuvo 76.334 en esos meses y lo cerró en agosto junto con jul-ago (253.248 cerrado vs 270.000 declarado, +16.752). Acumulado sep-oct en SIASoft a hoy: 85.124.
8. IVA cuatrimestre 2: declarado 68.645.000 vs cierre en SIASoft 68.787.000 (+142.000; el cierre de IVA descontable de servicios, 24081010, quedó 142.831 por debajo del movimiento). Pago del 10-sep sin registrar en 240815 (saldo 68.787.000). En el consolidado, el total de IVA a pagar (95.879.000) no es la suma de los dos cuatrimestres (95.946.000): faltan 67.000 de la casilla 66.
9. Faltan en ambos consolidados: retefuente dic-2025 (7.800.000), autorretención dic-2025 (3.890.000) e IVA sep-dic 2025 (25.983.000, registrado como pagado en marzo de 2026).
10. Hoja ICA del consolidado 2026 dice "AÑO 2025 ANUAL" pero trae ingresos ene-ago 2026 (1.068.782.000) y un impuesto de 9.217.782; SIASoft muestra 13.638.000 por pagar de 2025. La hoja ICA del consolidado 2025 está en cero.
11. El consolidado 2025 trae una hoja RENTA de régimen SIMPLE (anticipos bimestrales, saldo 1.831.000); el RUT no tiene la responsabilidad 47. Parece plantilla u otra empresa: confirmar.

## Pendientes
- Decisión de Daniel sobre los hallazgos 1 a 11 (nada se modificó).
- Confirmar si el ICA propio es anual, y si la hoja SIMPLE es de otra empresa.
- Ver en CUE_DOC (solo lectura) las líneas de julio de compras PJ y servicios PJ, y las de honorarios, si Daniel lo aprueba.
- Retefuente de octubre: falta el REP de octubre y el borrador; revisión el mar 10 nov.
- Al cerrar: actualizar fila 51 de EMPRESAS_NIT.md (ciudad Bogotá, IVA cuatrimestral) y crear su ficha en FICHAS_OFICINA.md (regla 12), solo con fechas de impuestos.
