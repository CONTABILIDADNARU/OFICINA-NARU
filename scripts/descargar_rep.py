"""
descargar_rep.py (v3) - Descarga el REP ("Descargar listados") de la DIAN para una o varias empresas.

Flujo real (grabado por Daniel, 6-nov-2026):
  1) Ingreso > Empresa > Representante legal: cedula + NIT  -> la DIAN manda un correo "Token Acceso DIAN"
     al correo de la empresa con un boton "Ingrese aqui" (el token ES ese enlace, vive ~30 min).
  2) Se usa el correo MAS RECIENTE (cada solicitud genera un token nuevo).
  3) Portal > Descargar listados (/Document/Export): rango de fechas + Grupos "Todos" > Exportar Excel.
  4) Esperar a que el estado pase del circulo al chulo verde > icono de descarga > llega un .zip con el .xlsx.

Este programa hace 1 y 3 y guarda/descomprime/renombra el resultado como REP_<EMPRESA>_<MES>.xlsx.
Tu haces: completar Cloudflare si aparece y hacer clic en "Ingrese aqui" del correo mas reciente.
Cedula y NIT se leen de config.json (local). Claude nunca los ve.

Uso:
  python descargar_rep.py --config config.json --mes OCT2026 --empresa "NOMBRE" [--explorar] [--conectar]
  python descargar_rep.py ... --desde 2026-05-01 --hasta 2026-08-31   (cuatrimestre para IVA)
--conectar: usar un Chrome normal abierto con --remote-debugging-port=9222 --user-data-dir=C:\\chrome_dian
"""
import argparse, calendar, json, re, sys, time, zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright

LOGIN_URL = "https://catalogo-vpfe.dian.gov.co/User/CompanyLogin"
EXPORT_URL = "https://catalogo-vpfe.dian.gov.co/Document/Export"
PERFIL = Path.home() / ".dian_rep_perfil"
DEST_DEFECTO = r"C:\Users\USUARIO\Desktop\PAQUETE_ORIGINAL\REP"
MESES = {"ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AGO": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DIC": 12}
FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def slug(s):
    return re.sub(r"[^A-Z0-9]+", "_", s.upper()).strip("_")


def rango_mes(mes):
    m, y = MESES[mes[:3].upper()], int(mes[3:])
    return f"{y}-{m:02d}-01", f"{y}-{m:02d}-{calendar.monthrange(y, m)[1]:02d}"


def cargar(ruta):
    cfg = json.loads(Path(ruta).read_text(encoding="utf-8"))
    for e in cfg["empresas"]:
        for k in ("nombre", "nit", "cedula"):
            if not str(e.get(k, "")).strip():
                sys.exit(f"config.json: falta '{k}' en una empresa ({e.get('nombre', '?')}). Llenalo tu en tu equipo.")
    return cfg


def pagina_de_trabajo(ctx):
    """Reutiliza una pestana existente del Chrome conectado (mas estable que abrir una nueva)."""
    for _ in range(4):
        try:
            pg = ctx.pages[0] if ctx.pages else ctx.new_page()
            pg.bring_to_front()
            return pg
        except Exception:
            time.sleep(1.5)
    return ctx.new_page()


def pedir_ingreso(page, emp, espera=6):
    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    page.get_by_text("Representante", exact=False).first.click()
    page.wait_for_timeout(1500)
    try:
        page.locator("select").first.select_option(label=emp.get("tipo_doc", "Cédula de ciudadanía"))
    except Exception:
        pass
    page.get_by_placeholder(re.compile("representante", re.I)).fill(str(emp["cedula"]))
    page.get_by_placeholder(re.compile("NIT de la empresa|NIT", re.I)).first.fill(str(emp["nit"]))
    print(f"  Esperando {espera} s para que Cloudflare termine su verificacion (si pide un clic, hazlo tu)...")
    page.wait_for_timeout(int(espera * 1000))
    page.get_by_role("button", name=re.compile("Entrar", re.I)).click()
    print("  -> Ingreso solicitado. Abre el correo de la empresa, usa el 'Token Acceso DIAN' MAS RECIENTE")
    print("     y haz clic en 'Ingrese aqui'. El programa detecta cuando el portal abre (espera hasta 30 min).")


def esperar_portal(ctx, minutos=30):
    fin = time.time() + minutos * 60
    while time.time() < fin:
        for pg in ctx.pages:
            u = pg.url
            if "catalogo-vpfe.dian.gov.co" in u and "/User/" not in u:
                pg.wait_for_load_state("domcontentloaded")
                return pg
        time.sleep(2)
    raise TimeoutError("No se detecto el portal abierto (token vencido o no se hizo clic).")


def fijar_rango(page, d, h):
    """Intenta escribir el rango en el selector de fechas; devuelve True si quedo bien."""
    try:
        campo = page.get_by_text("Rango de fechas").locator("xpath=following::input[1]")
        campo.click()
        page.wait_for_timeout(600)
        cajas = [c for c in page.locator("input:visible").all() if FECHA.match(c.input_value() or "")]
        if len(cajas) >= 2:
            cajas[0].fill(d)
            cajas[1].fill(h)
            cajas[1].press("Enter")
            page.wait_for_timeout(600)
        v = campo.input_value()
        return d in v and h in v
    except Exception as ex:
        print("   (no pude escribir el rango automaticamente:", type(ex).__name__, ")")
        return False


def guardar_descarga(d, destino, base, guardados):
    tmp = destino / ("_tmp_" + d.suggested_filename)
    d.save_as(str(tmp))
    salida = []
    if zipfile.is_zipfile(tmp):
        with zipfile.ZipFile(tmp) as z:
            for nm in z.namelist():
                if nm.lower().endswith((".xlsx", ".xls", ".csv")):
                    ext = Path(nm).suffix
                    ruta = destino / (base + ext)
                    n = 1
                    while ruta.exists():
                        n += 1
                        ruta = destino / f"{base}_{n}{ext}"
                    ruta.write_bytes(z.read(nm))
                    salida.append(ruta)
        tmp.unlink()
    else:
        ruta = destino / (base + (Path(d.suggested_filename).suffix or ".xlsx"))
        tmp.replace(ruta)
        salida.append(ruta)
    for r in salida:
        print(f"  Guardado: {r}")
    guardados.extend(salida)


def exportar(page, emp, d, h, destino, base, explorar, carpeta_exp):
    guardados = []
    page.on("download", lambda dl: guardar_descarga(dl, destino, base, guardados))
    page.goto(EXPORT_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    if not fijar_rango(page, d, h):
        input(f"  Escoge TU el rango {d} a {h} en el selector de fechas y presiona ENTER aqui... ")
    page.get_by_role("button", name=re.compile("Exportar Excel", re.I)).click()
    print(f"  Exportacion solicitada ({d} a {h}). Cuando el estado cambie del circulo al CHULO VERDE,")
    print("  pulsa el icono de descarga de la fila. (No pulses la X: cancela la tarea.)")
    if explorar:
        carpeta_exp.mkdir(parents=True, exist_ok=True)
        page.wait_for_timeout(4000)
        (carpeta_exp / f"{slug(emp['nombre'])}_tabla.html").write_text(page.locator("body").inner_html(), encoding="utf-8")
        page.screenshot(path=str(carpeta_exp / f"{slug(emp['nombre'])}_export.png"), full_page=True)
    input("  Cuando el archivo se haya descargado, presiona ENTER aqui... ")
    return guardados


def procesar_descarga(empresa, mes, destino):
    desc = Path.home() / "Downloads"
    zips = sorted(desc.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    zips = [z for z in zips if time.time() - z.stat().st_mtime < 3600]
    if not zips:
        sys.exit("No hay .zip reciente (ultima hora) en Descargas.")
    base = f"REP_{slug(empresa)}_{mes}"
    salida = []
    with zipfile.ZipFile(zips[0]) as z:
        for nm in z.namelist():
            if nm.lower().endswith((".xlsx", ".xls", ".csv")):
                ext = Path(nm).suffix
                ruta = destino / (base + ext)
                n = 1
                while ruta.exists():
                    n += 1
                    ruta = destino / f"{base}_{n}{ext}"
                ruta.write_bytes(z.read(nm))
                salida.append(ruta)
    for r in salida:
        print(f"Guardado: {r}  (desde {zips[0].name})")
    if not salida:
        print("El zip no trae xlsx/csv.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--mes", required=True, help="ej. OCT2026")
    ap.add_argument("--desde")
    ap.add_argument("--hasta")
    ap.add_argument("--empresa")
    ap.add_argument("--todas", action="store_true")
    ap.add_argument("--explorar", action="store_true")
    ap.add_argument("--conectar", action="store_true")
    ap.add_argument("--solo-ingreso", action="store_true", help="solo pide el ingreso (cedula/NIT) y termina; el resto lo hace Claude en Chrome")
    ap.add_argument("--procesar-descarga", action="store_true", help="toma el .zip mas reciente de Descargas, lo descomprime y lo renombra REP_<EMPRESA>_<MES>")
    ap.add_argument("--espera", type=float, default=6, help="segundos de espera antes de pulsar Entrar (por defecto 6)")
    a = ap.parse_args()
    cfg = cargar(a.config)
    destino = Path(cfg.get("carpeta_destino", DEST_DEFECTO))
    destino.mkdir(parents=True, exist_ok=True)
    if a.procesar_descarga:
        procesar_descarga(a.empresa or "EMPRESA", a.mes, destino)
        return
    d, h = (a.desde, a.hasta) if (a.desde and a.hasta) else rango_mes(a.mes)
    sel = cfg["empresas"] if a.todas else [e for e in cfg["empresas"] if e["nombre"].upper() == (a.empresa or "").upper()]
    if not sel:
        sys.exit("No encontre la empresa en config.json (use --empresa 'NOMBRE' o --todas).")
    resumen = []
    with sync_playwright() as p:
        if a.conectar:
            ctx = p.chromium.connect_over_cdp("http://localhost:9222").contexts[0]
        else:
            ctx = p.chromium.launch_persistent_context(str(PERFIL), channel="chrome", headless=False, accept_downloads=True)
        for emp in sel:
            print(f"\n== {emp['nombre']} ({a.mes}: {d} a {h}) ==")
            t0 = time.time()
            login = pagina_de_trabajo(ctx)
            try:
                try:
                    pedir_ingreso(login, emp, a.espera)
                except Exception as ex1:
                    if "closed" not in str(ex1).lower():
                        raise
                    print("  La pestana se cerro; reintento una vez con una pestana nueva...")
                    time.sleep(2)
                    login = ctx.new_page()
                    pedir_ingreso(login, emp, a.espera)
                if a.solo_ingreso:
                    print("  Ingreso solicitado. Avisale a Claude en el chat: 'token pedido'.")
                    resumen.append((emp["nombre"], "TOKEN PEDIDO", round(time.time() - t0)))
                    continue
                portal = esperar_portal(ctx)
                f = exportar(portal, emp, d, h, destino, f"REP_{slug(emp['nombre'])}_{a.mes}", a.explorar, destino / "_explorar")
                resumen.append((emp["nombre"], "OK" if f else "SIN DESCARGA", round(time.time() - t0)))
            except Exception as ex:
                resumen.append((emp["nombre"], f"ERROR: {type(ex).__name__}", round(time.time() - t0)))
                print("  Error:", ex)
        if not a.conectar:
            ctx.close()
    print("\nRESUMEN (empresa, resultado, segundos)")
    for n, r, s in resumen:
        print(f"  {n}: {r} ({s} s)")


if __name__ == "__main__":
    main()
