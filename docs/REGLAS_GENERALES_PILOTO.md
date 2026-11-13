# REGLAS GENERALES DEL PILOTO (vigentes desde 3-nov-2026)

Estas reglas aplican a todas las sesiones y clientes. Donde choquen con las instrucciones iniciales del proyecto (regla 3: "solo sobre una copia" y regla 4: "avisar antes de abrir cualquier archivo"), mandan estas, por decisión expresa de Daniel.

## 1. Respaldo y lugar de trabajo
- En cada sesión nueva: copia de seguridad de CO.SIA de la empresa en `C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL` (aprobación general de Daniel).
- Después se trabaja sobre la empresa original en el servidor; la copia queda solo como respaldo.
- Siempre se informa a Daniel qué respaldo se hizo y dónde.
- Sigue vigente: avisar antes de cualquier proceso que modifique datos (766, 746, 150) y verificar después de cada importación. Nunca 799, 800, 660 ni 110. Nunca escribir directo en DBF.

## 2. Nombre de empresa
- Siempre "NOMBRE (número SIASoft)". Ejemplos: NARU CONSULTORES (EMP010), RUMASA (EMP010), PARAMO CONNECT (EMP061), LEXPERTISE (EMP041).
- El nombre es la llave; los números se pueden repetir entre instalaciones, los nombres no.
- Escribir la ruta completa y verificar el nombre de la empresa dentro de CO.SIA antes de importar.

## 3. Medición de coincidencia (compuerta por sesión)
- Una sesión = un cliente + un mes.
- Prueba retroactiva de solo lectura: las reglas se aprenden con meses anteriores al mes de referencia y se comparan, documento por documento, contra lo realmente contabilizado.
- Piso: coincidencia >= 95% por documento completo (cuenta, tercero, IVA y retenciones). La meta real es acercarse a 100%.
- Con menos de 95%: no se genera nada; se muestran las reglas que fallaron y Daniel decide.
- Se reporta además un segundo número ponderado por valor.

## 4. Parada por desfase (2% por documento)
- Cada documento (factura, nota, documento soporte) es su propio 100%.
- Si total, base, IVA o retenciones se desvían 2% o más frente al REP: parar y revisar qué error se encontró.
- El redondeo no cuenta (centavos o $1; compras con IVA hacia abajo).
- Entre 1% y 2% (no redondeo): no para, pero se marca como alerta en el reporte.

## 5. Paradas sin excepción
- Débitos distintos de créditos en lo generado.
- IVA que no cuadra con el REP más allá del redondeo.
- Documentos duplicados.
- Período bloqueado o conteo importado distinto del esperado (el 746 puede importar 0 sin error).

## 6. Cuenta dudosa
- Una cuenta contable dudosa o proveedor sin regla aprendida va al reporte de dudas, junto con terceros nuevos. Cuenta contra el 95% pero no frena la sesión por sí sola.

## 7. Lectura de archivos (agregada 3-nov-2026 16:04)
- Permiso general de Daniel: leer los archivos necesarios para agilizar los proyectos, siempre en modo solo lectura (CO.SIA/DBF, REP, plantillas, scripts del proyecto), sin pedir aprobación archivo por archivo.
- Sigue valiendo: nada de escritura sobre datos reales fuera de los procesos del programa (766, 746, 150); no imprimir ni repetir nombres de terceros salvo que Daniel lo pida; no abrir archivos ajenos al cliente en curso (por ejemplo, otras empresas en la misma carpeta SIASoft).

## 8. PDF de la DIAN (modificación 3-nov-2026 16:07)
- Claude NO lee los PDF. Solo los descarga (CUFE + NIT desde catalogo-vpfe.dian.gov.co), les quita la contraseña (el NIT) y los guarda sin contraseña en una carpeta propia por cliente y mes, para que Daniel los revise.
- Se descargan solo los documentos que quedan en el reporte de dudas (terceros sin historial, notas crédito, descripciones nuevas), no todos.
- Nombre de archivo sin nombres de terceros: `<prefijo>-<folio>_<NIT>.pdf`. Un script por lote, que devuelve solo un resumen (descargados, descifrados, fallidos).
- Si la descarga falla, la duda queda en el reporte y Daniel decide la cuenta.

## 9. Bitácora por cliente y mes
Columnas: empresa (número), mes, alcance, mes de referencia, % de coincidencia (documento y valor), dudas abiertas, conteo esperado vs importado, débitos = créditos, estado, PDF descargados, pendientes de Daniel.

| Empresa | Mes | Estado |
|---|---|---|
| Octopux Publicidad SAS | oct-2026 | Aplicado en original; pendientes los corrige a mano la persona encargada |
| NARU CONSULTORES (EMP010) | oct-2026 | Importado y verificado (3-nov): ventas 21/21 docs y 99/99 líneas, compras 27/27 y 80/80, 150 con 0 desfases, D=C 68.630.462, 0 terceros huérfanos. Pendientes anteriores a octubre en claude/RESULTADO_NARU_OCT2026.md. Borrador del 350 de octubre (4-nov): autorretención 370.000 (ver regla 16) |
| PARAMO CONNECT (EMP061) | oct-2026 | Importado (confirmado por Daniel el 3-nov 22:47; marcado "Aplicado" en la oficina virtual). Falta registrar la verificación de solo lectura (conteos, D=C, huérfanos, acumulados) y confirmar bloqueo del período (ver claude/REGLAS_PARAMO_CONNECT.md) |
| RUMASA (EMP010, instalación MOUNTAIN) | oct-2026 | Importado por Daniel y verificado en solo lectura el 5-nov: 21 docs nuevos (ventas 3, compras 15, DS 2, NC 1) y 61/61 líneas, 197.791.750 igual al REP, D=C (mes 251.832.669), 2 terceros nuevos sin duplicados, 0 huérfanos, 150 con 0 desfases (ver claude/REGLAS_RUMASA.md). Falta confirmar el bloqueo de octubre. Borrador del 350 de octubre (5-nov, sobre el libro de septiembre): total 4.371.000 (ver claude/BORRADOR_350_RUMASA_OCT2026.md); falta corregir CP-001657 en SIASoft. Medición retroactiva con sep-2026 aplazada |
| LEXPERTISE (EMP041) | oct-2026 | Compras y ventas (referencia 2026). Sin ventas. 4 compras CP-123 a CP-126 + 1 tercero: importado y verificado en solo lectura el 3-nov (4/4 docs, 12/12 líneas, D=C, 0 desfases); falta confirmar que octubre quedó bloqueado (ver claude/REGLAS_LEXPERTISE.md) |

## 10. Calendario tributario de cada empresa (agregada 3-nov-2026 22:19)
- Toda empresa nueva del piloto: antes de su primera sesión se verifica su calendario tributario con su RUT y se deja en una sección "Calendario tributario" de su `claude/REGLAS_<EMPRESA>.md`. No se suponen fechas ni responsabilidades.
- Del RUT se toma: NIT sin dígito de verificación (último dígito = retención en la fuente e IVA; últimos dos dígitos = planilla PILA); responsabilidades (retención en la fuente, IVA y si es bimestral o cuatrimestral, autorretenedor, agente de retención de ICA); si tiene empleados (planilla); ciudad del domicilio (ReteICA e ICA distritales).
- Fuentes: DIAN para retención e IVA (tablas ya cargadas en `claude/CALENDARIO_DIAN_2026.md`); Secretaría Distrital de Hacienda para ReteICA e ICA de Bogotá; planilla por día hábil según los dos últimos dígitos, contando festivos. Las tablas de portales secundarios se contrastan con la fuente oficial antes de fijar fechas.
- Revisión interna: 2 días hábiles antes de cada vencimiento (decisión de Daniel, 3-nov-2026; no 5).
- En la sección de cada empresa se anota: NIT usado, fuente y fecha de consulta, y qué datos faltan por confirmar con el RUT.
- Si cambia el calendario (decreto, festivo nuevo), se actualizan todas las empresas.
- Las fechas de estas secciones alimentan las tareas programadas y el monitor de la oficina virtual.

## 11. División de chats (agregada 3-nov-2026 23:05)
- Un chat por empresa dentro del proyecto: ahí van sus reglas, el REP, los archivos, la importación y la verificación. Lo aprendido se guarda en su `claude/REGLAS_<EMPRESA>.md`.
- Un chat solo para la oficina virtual: ahí se modifica la página (agregar o quitar empresas, fechas, diseño). No se hace trabajo contable de una empresa en ese chat.
- Los documentos del proyecto son el puente entre chats. Los estados de la oficina salen de ellos, no de la memoria de otro chat.
- La página no se entera sola: cuando una empresa avance, se pide en el chat de la oficina "actualiza <empresa>" y se lee su documento.
- El botón "Ya quedó aplicado y está bien" de la página es un atajo guardado solo en el navegador; el estado oficial es el que queda en el documento de la empresa.

## 12. Alta en la oficina virtual al cerrar una empresa (ajustada 3-nov-2026 23:20)
- Escala: unas 65 empresas. La oficina debe crecer sin volverse ilegible (lista con búsqueda y filtro por estado, pisos por departamento, y una empresa a la vez en el escritorio, no 65 fichas a la vez).
- Las fichas viven en UN solo documento: `claude/FICHAS_OFICINA.md`. No se repiten al final de cada `REGLAS_<EMPRESA>.md`.
- Cada vez que se cierra el proceso de una empresa (importada y verificada, o dejada lista a la espera de aprobación), su chat hace dos cosas en el mismo paso y nada más: (1) anota el resultado en su `REGLAS_<EMPRESA>.md`; (2) actualiza SU ficha en `FICHAS_OFICINA.md`, sin tocar las fichas de otras empresas (se lee el documento completo antes y se reescribe conservando las demás).
- La ficha lleva: nombre y número SIASoft (regla 2); NIT sin DV y ciudad; estado de un renglón (Aplicado / Espera tu decisión / Espera tu aprobación / Por confirmar); Listo, Falta y Siguiente paso en lenguaje sencillo y sin nombres de terceros; fechas de impuestos y fechas de planillas, separadas (regla 13).
- Con esa ficha, el chat de la oficina crea su espacio en la página. Si la ficha no existe, la empresa no entra a la oficina.
- Si el documento de fichas se vuelve largo, pasa a una tabla compacta con una fila por empresa.
- Cuando el volumen lo pida, los datos de las empresas pasan de estar escritos dentro de la página a un archivo de datos aparte, para no tener que reescribir la página por cada empresa.

## 13. Puesto "Planillas" separado de "Impuestos" (agregada 3-nov-2026 23:20; ajustada 4-nov-2026 08:40)
- La oficina tiene un puesto "Planillas" que muestra SOLO fechas de planillas (PILA). Así se separan las fechas de impuestos de las de recursos humanos. Nómina y liquidaciones siguen fuera por ahora.
- Fecha de planilla: día hábil según los dos últimos dígitos del NIT (ej. 14 = 3.er día hábil, 15 = 4.º, 65 = 11.º), contando festivos. Revisión interna: 2 días hábiles antes (regla 10).
- Las fechas de planilla por empresa van en su ficha (línea "Planillas") y en la sección de calendario de su `REGLAS_<EMPRESA>.md`.
- Tiene empleados (indicación de Daniel, 4-nov): el REP DIAN trae las nóminas electrónicas (NOPC, NOLX...). Si el REP del mes trae nómina electrónica, la empresa entra a Planillas. Un mes sin nómina no prueba que no haya empleados: se miran los últimos 2 o 3 REP antes de descartar, y si no es claro queda "por confirmar" (con nómina o RUT). No se supone.
- Semáforo de fechas en la oficina (impuestos y planillas): rojo 2 días o menos para la revisión, amarillo 3 a 5 días, verde más de 5. La etiqueta de texto (Atrasada, Hoy, Urgente, Próxima, Con tiempo) acompaña siempre al color.

## 14. Margen para pedir el REP (aprobada por Daniel el 3-nov-2026 23:21; excepción 1-2-3 decidida el 4-nov-2026 09:00; vale para todas las empresas hasta nuevo cambio)
- Se cuenta hacia atrás desde el vencimiento de la retención en la fuente, en días hábiles (contando festivos):
  - Vencimiento menos 2: revisión interna (regla 10).
  - Revisión menos 3: contabilidad al día (746 y 150 verificados), para liquidar el borrador.
  - Contabilidad al día menos 4: Daniel entrega el REP del mes (generar archivos, reporte de dudas, aprobación, importar y verificar).
  - En total: el REP debe estar 9 días hábiles antes del vencimiento de la retención.
- El REP de un mes se pide el primer día hábil del mes siguiente (el REP debe traer todas las facturas del mes).
- EXCEPCIÓN (opción B de Daniel, 4-nov) para los dígitos 1, 2 y 3: el margen de 9 días caería antes del cierre del mes. Se pide el REP el primer día hábil del mes siguiente, se mantienen los 4 días hábiles de procesamiento y se acorta el colchón de liquidación a los días que queden (0, 1 y 2 días hábiles para los dígitos 1, 2 y 3; con 0 la liquidación del borrador es el mismo día en que queda al día la contabilidad). La revisión interna no cambia (2 días hábiles antes de vencer).
- Empresas de la misma fecha de vencimiento (mismo último dígito del NIT) se piden el mismo día; cada empresa nueva calcula su fecha con su NIT.
- ReteICA (vence el mismo día para todas): se usa la fecha más temprana de las empresas para tener el bimestre completo al día.
- Las planillas no dependen del REP sino de la nómina; se tratan aparte.
- Calendario de REP de todos los dígitos (octubre, noviembre y diciembre, ya con la excepción): `claude/CALENDARIO_REP.md`. Piloto: REP de noviembre mar 1 dic (terminan en 4) y mié 2 dic (terminan en 5); REP de diciembre lun 4 ene 2027 (4) y mar 5 ene 2027 (5). Octubre del piloto ya quedó cubierto.
- Aviso programado (solo recordatorio, no ejecuta nada): 1 dic 7:30 a. m. Octopux y Paramo; 2 dic 7:30 a. m. Naru y Lexpertise. Quedan por programar los avisos de enero y los de las demás empresas.

## 15. Registro de empresas y NIT (agregada 4-nov-2026 08:40; ajustada 08:55)
- `claude/EMPRESAS_NIT.md` guarda el nombre y el NIT de todas las empresas de Daniel (55 cargadas el 4-nov; faltan unas 10 para llegar a ~65), con su último dígito y su día hábil de planilla.
- Estar en el registro NO significa trabajar la empresa ni que entre a la oficina (regla 12). Es solo para que cada chat nuevo ya tenga sus datos.
- Cada chat de empresa, al abrir, lee su fila, la completa (número SIASoft, ciudad, IVA, empleados) con el RUT y el REP, y actualiza solo su fila. Sin nombres de terceros.
- Tabla de retención en la fuente, IVA cuatrimestral, ICA y ReteICA Bogotá: cargada y validada el 4-nov en `claude/CALENDARIO_DIAN_2026.md` (retención e IVA para todos los dígitos en los meses del piloto). Sigue pendiente validar la tabla PILA (planillas): solo las franjas 08-14, 15-21 y 64-69 están verificadas.

## 16. Borradores del formulario 350 (retefuente) (agregada 4-nov-2026 09:10)
- Cada vez que Daniel pida crear el borrador de retención en la fuente, se guarda en `C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\BORRADORES RETEFUENTE <MES>` (ej. `BORRADORES RETEFUENTE OCTUBRE`, el mes del período declarado).
- Dentro, una carpeta por empresa con el nombre de la empresa (ej. `NARU CONSULTORES`) y en ella el borrador en Excel (`BORRADOR_RTE_FTE_<EMPRESA>_<MES>.xlsx`).
- Se arma sobre el libro del mes anterior de esa empresa (hojas FORMULARIO, AUX INGRESOS, AUX AUT, AUX RTE FTE, REP DIAN), editando el archivo sin perder logos ni vínculos; se verifica recalculando.
- Autorretención especial (casilla 59 = base: todos los ingresos del mes sin IVA, casilla 68 = base x tarifa de la casilla 28, redondeada a miles). Los rendimientos financieros que aún no estén contabilizados entran en el mes en que se registren (ej. los de agosto entraron en septiembre).
- NARU CONSULTORES (NIT 901669465, DV 1, CIIU 7010, tarifa 1,1%): autorretenedora especial; en octubre no hay retención por compras (los proveedores grandes son autorretenedores), ni por nómina, ni reteIVA. Borrador octubre: base 33.640.000, autorretención y total a pagar 370.000.
- RUMASA SAS (NIT 901053453, DV 9, CIIU 6201): autorretención especial al 1,1 % (base: todos los ingresos 4xxx del mes); retención por salarios en 236505 (OJO: es retención, no nómina por pagar). Borrador octubre (5-nov, sobre el libro de septiembre): salarios 2.200.000 + arrendamiento 48.000 + autorretención 2.071.000 + compra CP-001657 52.000 = 4.371.000 en total. Las FTM de administración de edificio no llevan retención.
