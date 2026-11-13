# FLUJO DEL REP DIAN (grabado por Daniel, 6-nov-2026, empresa de prueba INVERSIONES BP)

## Ingreso
- Portal: catalogo-vpfe.dian.gov.co > Empresa > Representante legal: tipo de documento (cédula), cédula del representante y NIT de la empresa. Cloudflare puede marcar "inválido" la primera vez y dejar pasar en el reintento.
- La DIAN envía al correo de la empresa un mensaje "Token Acceso DIAN" (remitente facturacionelectronica@dian.gov.co) con un botón "Ingrese aquí". El token ES ese enlace; vive ~30 min. Cada solicitud genera un token nuevo: usar siempre el MÁS RECIENTE.
- Antes de entrar se puede confirmar a qué correo llegó (para saber que pertenece a la empresa). Al entrar, arriba a la derecha aparecen la empresa y el representante legal.
- El enlace del correo lleva en la URL la cédula y el NIT: no compartir capturas de esa URL.

## Reporte
- Menú lateral > Descargar listados (https://catalogo-vpfe.dian.gov.co/Document/Export). Campos: NIT receptor (opcional), Rango de fechas (calendario de dos meses; se puede abarcar el año), Grupos (Todos = enviados y recibidos).
- Normalmente se necesita el mes anterior; para IVA, el cuatrimestre.
- Botón Exportar Excel crea una tarea (máx. 150.000 documentos). La tabla muestra Fecha, Usuario, Rango, Grupo, Tipo, Total, Estado (círculo = procesando; chulo verde = listo) y Acciones (icono de descarga; la X cancela la tarea). Si se queda procesando mucho, actualizar la página.
- La descarga llega como .zip con un .xlsx adentro (nombre tipo GUID). Hay que descomprimir y renombrar: REP_<EMPRESA>_<MES>.xlsx.

## Automatización (claude/descargar_rep.py v3)
- Hace: pedir ingreso con cédula/NIT leídos de config.json local, detectar cuando abre el portal, ir a Descargar listados, fijar el rango, Exportar Excel, descomprimir y renombrar.
- Sigue siendo manual: Cloudflare si pide acción, el clic en "Ingrese aquí" del correo más reciente, y (por ahora) el clic del icono de descarga cuando sale el chulo.
- Pendiente: automatizar el clic de descarga (con --explorar se guarda el HTML de la tabla) y leer el correo del token de forma automática.
