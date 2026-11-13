# Checklist para aplicar en el SIASoft ORIGINAL — OCTOPUX PUBLICIDAD SAS (EMP010), octubre 2026

Preparado el 2 de noviembre de 2026 a partir de las pruebas hechas en la copia (carpeta SIASOFT_V23_OCTOPUX_1).

## Reglas que no se rompen
- NUNCA ejecutar ni sugerir los procesos 799 (blanquear tablas), 800 (borrar documentos), 660 (blanqueo de periodo) ni 110 (cierre de ejercicio).
- Nunca escribir directo en las tablas DBF. Toda carga entra por los procesos del programa (766, 746, 150). Leer los DBF es seguro.
- No abrir archivos con datos reales sin decir cuál y para qué, y esperar la aprobación de Daniel.
- Ante la duda entre dos caminos, preguntar.

## Lo que se aprendió en la copia (los 5 procesos)
| Proceso | Qué hace | Cuidado |
|---|---|---|
| 745 | Exporta documentos (.cab/.cue/.Ter/.FPT) y un ZIP | BORRA la carpeta EXPORT. Copiar su contenido antes, o exportar a una carpeta vacía |
| 746 | Importa documentos (el .CAB elige el juego) | No crea terceros. Rechaza llaves existentes (año-periodo-tipo-número). Si las fechas están mal o el período está bloqueado, importa 0 sin error. No actualiza RES_*. Crea un .CDX junto al origen |
| 765 | Exporta terceros (DBF de 55 campos) | Filtra por FEC_ING |
| 766 | Importa terceros | Solo inserta; no actualiza los existentes |
| 150 | "Actualizar acumulados (recalculo)": reconstruye RES_CTA/RES_TER | También modificó acumulados de otros períodos (mayo y septiembre) y ACU_BAN en la copia |

Regla: no editar un documento importado en el programa antes de correr el 150 (deja RES_TER mal).
Si aparece "Alias name is already in use": Anular, cerrar SIASoft por completo, abrirlo de nuevo y repetir el proceso una sola vez.
Si SIASoft no abre desde una ruta con espacios: usar una ruta sin espacios.

## Orden de trabajo (siempre este)
1. Terceros (766) → 2. Documentos (746) → 3. Recálculo (150) → 4. Verificación (solo lectura).

## Antes de empezar (obligatorio)
1. Hacer una copia de seguridad de la carpeta CO.SIA de la empresa EMP010 (EMPRESAS\EMP010\CO.SIA) y guardarla fuera de la carpeta del programa. No continuar sin esa copia.
2. Confirmar con Daniel cuántos documentos hay hoy en octubre 2026 en la original: compras (05 y 18), documento soporte (05A) y ventas (04). En la copia, antes de las pruebas, había 102 DSOC, 5 documentos 05, 5 documentos 18 y ningún documento 04 de octubre.
3. Confirmar que no se importó antes ninguno de estos juegos: si ya existe la llave, el 746 la rechaza.
4. Desbloquear octubre (el 746 no importa con el período bloqueado). Volver a bloquearlo al final.
5. La carpeta donde está el juego de importación debe tener permisos de escritura (el 746 escribe un .CDX allí).
6. Pedir a Claude que regenere los juegos contra la original si la original tiene documentos distintos a los esperados. El juego fue armado con una plantilla de exportación de la copia.

## Archivos del paquete (carpeta PAQUETE_ORIGINAL)
| Archivo | Para qué | Proceso |
|---|---|---|
| TERVTAORI.DBF (+ .FPT) | 112 terceros nuevos (clientes de las ventas de octubre). Dudas de nombres en TERVTAORI_dudas.csv | 766 |
| AGTVTAORI.cab (+ .cue, .Ter, .FPT) | 4.993 ventas de octubre (documentos tipo 04), una por una con su consecutivo | 746, fechas 01/10/2026 a 22/10/2026 |
| AGTCOMP1.cab (+ .cue, .Ter, .FPT) | 2 compras faltantes: FC-000671 (Panamericana) y FC-000672 (Sumiprint) | 746, fechas 28/10 a 29/10/2026 |
| scripts\verificar.py | Verificación de solo lectura | Después del 150 |

Nota sobre AGTCOMP1: hay que importar el .cab con ese nombre desde su propia carpeta; el 746 deja un .CDX al lado.

## Resultados esperados (si la original quedó igual que la copia antes de las pruebas)
- 766: debe cargar 112 terceros.
- 746 ventas: debe decir 4.993 importados. Si dice otra cifra, parar y avisar a Claude.
- Ventas de octubre: 14.979 líneas, débitos = créditos = 3.569.981.223. Base 2.999.983.932 (igual a la DIAN). IVA 569.997.291 (diferencia de +344 contra la DIAN, es redondeo de centavos).
- Por serie: FBB 60, FBC 372, FBD 122, FBF 775, FBG 622, FBH 716, FBI 677, FBJ 807, FCO 842.
- 746 compras: 2 importados.
- Después del 150: cero cuentas y cero pares cuenta-tercero desfasados en la verificación.

## Procedimiento
1. 766: cargar TERVTAORI.DBF. Verificar que el maestro sube en 112.
2. 746: elegir AGTVTAORI.cab, fechas 01/10/2026 a 22/10/2026, pulsar UNA sola vez. Tarda (casi 15.000 líneas).
3. 746: elegir AGTCOMP1.cab, fechas 28/10/2026 a 29/10/2026, pulsar una sola vez.
4. 150: marcar SOLO octubre, mismas opciones que en la copia.
5. Verificar con scripts\verificar.py:
   python3 verificar.py "<ruta a EMPRESAS\EMP010\CO.SIA>" 2026 10
6. Bloquear octubre.

## Decisiones y pendientes de Daniel
- 13 ventas con forma de pago "2" quedaron en caja (11050505). Si algunas van a clientes (13050505), cambia la cuenta del débito, no el total.
- Los 112 terceros nuevos: 22 dudas de nombres (la mayoría nombres de 3 palabras; se asumió 1 nombre y 2 apellidos). Se corrigen a mano en el programa sin afectar las ventas. Tampoco tienen dirección ni teléfono.
- 4 NIT mal digitados en documento soporte: DSOC 5 (1031162659 debía ser 1031162956), DSOC 47 (10725219187 → 1075219187), DSOC 68 (100352363 → 1000352363), DSOC 88 (1014176550 → 1014179550). Daniel decidió dejarlos como están. En la copia ya existen los terceros correctos.
- DSOC 38: falta el reteICA en tu registro. Pendiente de confirmar si fue omisión.
- Nota de ajuste NAOC1: se identifica con el DSOC 44 (sin retención). Pendiente confirmar con Daniel.
- Proveedores en el generador de compras: Transportes El Palmar (NIT 800139755): 523550 con retención 1% en 23652510. Credibanco (860032909) es autorretenedor: gasto 523515 con IVA, base igual al gasto. Bold (901281572): cuenta según los últimos 6 meses (IVA cero: 520518; con IVA: 523515). Panamericana (830037946): 143505, mercancía.
- Diferencia de $344 en IVA contra la DIAN por redondeo: Daniel no ha dicho si la acepta o prefiere cargar centavos.
- Datos de prueba que quedan SOLO en la copia y no van a la original: FC-AGT001, FC-AGT002, el tercero ficticio 900555123, y los documentos FBF-734 a FBF-743 y FBG-627 importados como prueba (en el paquete ya van incluidos en AGTVTAORI).

## Resultados medidos en la copia (para la meta de 95%)
- Compras: 91,7% estricto, 95,4% ajustado (0 errores del generador; las diferencias fueron errores de digitación y criterio en el registro).
- Documento soporte: 94 de 102 exactos (92,2%); las diferencias son 4 NIT mal digitados, 1 reteICA omitido, 1 de texto y 1 de fecha.
- Ventas: cuadran con la DIAN; no hay ventas de octubre registradas a mano contra las que medir.

## Borrador del formulario 350 de octubre (OCTOPUX, 901013514)
- Retención por servicios: 4.325.000 (101 DSOC a personas naturales, 6%, base 72.080.000) + 7.000 (flete 1%, base 700.000).
- Autorretención especial: base de ingresos 2.999.983.932 × 0,55% = 16.500.000.
- ReteIVA: 0. Total a pagar: 20.832.000.
- Falta pasar los valores al libro de Daniel (hojas FORMULARIO, AUX RTE FTE, AUX INGRESOS) y anotar el CIIU. Se necesita su archivo del 350 de otro mes.
- Archivo de apoyo: BORRADOR_350_OCTOPUX_OCT2026.xlsx.
