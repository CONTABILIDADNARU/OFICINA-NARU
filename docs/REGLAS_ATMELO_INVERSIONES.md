# REGLAS ATMELO INVERSIONES (ATMELO INVERSIONES S.A.S.)

Última actualización: 6-nov-2026. Cliente en prueba para automatizar la descarga del REP DIAN. Aún sin trabajo contable en SIASoft: falta definir CO.SIA, número SIASoft y mes de referencia.

## 1. Datos de la empresa
- Nombre en el portal DIAN: Atmelo Inversiones S.A.S.
- Nombre en config.json y .bat: `ATMELO INVERSIONES` (escrito con R; en una primera instrucción se escribió "INVESIONES", era error de digitación).
- Correo donde llega el token DIAN: contabilidadatmelo@gmail.com (en el Chrome de la oficina es la cuenta `/mail/u/4/`; el número puede cambiar si se agregan o quitan cuentas, se identifica por el título de la pestaña).
- NIT y cédula del representante: NO están en este documento ni los ve Claude. Están solo en `config.json` en el PC de oficina, que llena Daniel.
- Número SIASoft: pendiente.

## 2. Resultado de la primera descarga (6-nov-2026)
- REP sep+oct 2026: 144 documentos (72 de septiembre y 72 de octubre) → `PAQUETE_ORIGINAL\REP\REP_ATMELO_INVERSIONES_SEP-OCT2026.xlsx`
- REP solo octubre 2026: 72 documentos, todos con fecha de emisión de octubre → `PAQUETE_ORIGINAL\REP\REP_ATMELO_INVERSIONES_OCT2026.xlsx`
- Columnas del REP: Tipo de documento, CUFE/CUDE, Folio, Prefijo, Divisa, Forma de Pago, Medio de Pago, Fecha Emisión (formato dd-mm-aaaa), Fecha Recepción, NIT Emisor, Nombre Emisor, NIT Receptor, Nombre Receptor, IVA, ICA, IC, INC, Timbre, INC Bolsas, IN Carbono, IN Combustibles, IC Datos, ICL, INPP, IBUA, ICUI, Rete IVA, Rete Renta, Rete ICA, Total, Estado, Grupo.
- La hoja se llama `Rp_Doc_AAAAMMDD_HHMM` y trae el encabezado en la fila 1.

## 3. Flujo de descarga del REP (funcionó de punta a punta)
1. Daniel (o el programa) pide el token en catalogo-vpfe.dian.gov.co: Empresa > Representante legal, cédula, NIT, Cloudflare, Entrar. Claude NO escribe la cédula ni el NIT ni resuelve Cloudflare.
2. Daniel escribe "token pedido" con empresa y mes.
3. Claude abre el correo de la empresa en el Chrome de Daniel, busca "Token Acceso DIAN", abre el MÁS RECIENTE y pulsa "Ingrese aquí".
4. Si el primer clic lleva a la pantalla de login de "Administrador" (con usuario y contraseña autorrellenados por el navegador), NO se envía ese formulario. Se vuelve al correo y se pulsa "Ingrese aquí" una segunda vez; en este caso la segunda vez entró al portal.
5. Ir a `/Document/Export` (Descargar listados). Rango de fechas: abrir el selector, usar "<" para ir al mes, clic en el día 1 y luego en el último día del mes, clic en un área vacía para cerrar. Verificar que el rango diga 2026-10-01 - 2026-10-31. Grupos: Todos.
6. Exportar Excel → confirmar "Sí". La tarea tarda varios minutos (esta vez cerca de 10): círculo azul = en proceso, círculo rojo con raya = aparente error, visto verde = lista. Refrescar la página cada 30–60 s. NO usar la X (cancela) ni el icono de papelera (borra). Si aparece rojo, esperar y refrescar antes de volver a exportar: en esta prueba las dos tareas terminaron solas con visto verde y quedaron duplicadas.
7. Pulsar el icono de descarga de la fila con visto verde. Llega un .zip con nombre GUID a Descargas.
8. Para ubicar el zip: el listado de Descargas es enorme (más de 230.000 caracteres). No listar a la vista; guardar la salida en archivo y ordenar por fecha de modificación para tomar el más reciente. Traerlo con device_stage_files, descomprimir, renombrar `REP_<EMPRESA>_<MES>.xlsx` y devolverlo con device_commit_files a `PAQUETE_ORIGINAL\REP`.
9. Reportar solo conteos y fechas, sin nombres de terceros. Cerrar las pestañas que Claude abrió.

## 4. Programa de automatización en el PC de oficina (equipo eq-aux2)
Carpeta: `C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\PROGRAMA_REP`
- `descargar_rep.py` (v3.3), `config.json`, `PEDIR_TOKEN_ATMELO.bat` (usar este), `1_pedir_token.bat`, `2_renombrar_descarga.bat`.
- Python instalado versión 3.14.x; `python` no queda en el PATH, se usa `py` o la ruta `C:\Users\USUARIO\AppData\Local\Python\pythoncore-3.15-64\python.exe`. El `.bat` actual detecta cuál usar.
- Playwright instalado con `pip install playwright`. `py -m playwright install chrome` dice que Chrome ya está instalado: está bien, NO usar `--force`.
- `config.json`: las claves `nombre`, `nit`, `cedula`, `tipo_doc` NO se tocan; solo se escriben los valores entre las comillas de la derecha, sin puntos, guiones ni dígito de verificación. Error cometido: escribir los números en lugar del nombre de la clave.
- El `.bat` abre un Chrome aparte (`C:\chrome_dian`, puerto 9222) para pedir el token. Para que Claude lea el correo se usa el Chrome normal donde está la extensión.
- Claude no puede ejecutar los `.bat` ni comandos en el PC (el entorno de comandos de Windows no está disponible).

## 5. Reglas que aplican a esta empresa
- Reglas del proyecto y `REGLAS_GENERALES_PILOTO.md`: backup de CO.SIA en PAQUETE_ORIGINAL, trabajar sobre copia, meta 95% por sesión, parar si un documento se desvía 2% o más, verificar todo importado.
- Nombre de la carpeta de la empresa: `ATMELO INVERSIONES (número SIASoft)`, cuando se defina el número.
- Antes de abrir cualquier archivo con datos reales, avisar cuál y para qué.
- Compras: IVA hacia abajo. Ventas: base = total − IVA. Consumidor final: tercero 2222222.
- Autorretenedores y mínimos de retención: confirmar con el RUT, no suponer.

## 6. Pendiente para empezar el trabajo contable
- Copia del CO.SIA de la empresa y número SIASoft.
- Mes ya contabilizado para medir coincidencia (la meta es 95%).
- Series de facturas y una exportación 745 como plantilla.
- Confirmar con el RUT las retenciones y si es autorretenedor.
- Archivos: decidir si el REP de octubre se compara contra septiembre ya contabilizado (el archivo sep+oct sirve de apoyo).
