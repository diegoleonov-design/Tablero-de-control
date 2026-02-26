#!/usr/bin/env python3
"""
servidor.py – Proxy local para Dashboard de Proyectos
======================================================
Ejecutá:  python servidor.py
Abrí:     http://localhost:8765

Requiere:  pip install requests
"""

import base64
import json
import os
import re
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("❌  Falta el paquete 'requests'. Instalalo con:\n    pip install requests")
    sys.exit(1)

PORT        = 8765
CONFIG_FILE = "config.json"

# ── MAPPINGS (deben coincidir con index.html) ────────────────────
CLIENT_JIRA_MAP = {
    "Transener":     ["TRANSENER TESLA", "TRANSENER Costeo Emplazamiento", "TRANSENER Mantenimiento"],
    "SACDE":         ["SACDE - Francos", "SACDE - Equipos", "SACDE - Partes Diarios",
                      "SACDE APP MATERIALES", "SACDE Mantenimiento", "SACDE PORTAL"],
    "Bayer":         ["Bayer"],
    "Pampa Energia": ["PAMPA Almacenes Mejoras"],
}
JIRA_TO_CLIENT = {p: cl for cl, ps in CLIENT_JIRA_MAP.items() for p in ps}

CW_TO_JIRA = {
    "Tesla":                               "TRANSENER TESLA",
    "Costeo de Emplazamiento":             "TRANSENER Costeo Emplazamiento",
    "Migración S4":                        "TRANSENER Mantenimiento",
    "Interface de Francos Compensatorios": "TRANSENER Mantenimiento",
    "Trello":                              "TRANSENER Mantenimiento",
    "Premios":                             "TRANSENER Mantenimiento",
    "Paquete 4 ''Francos APK''":           "SACDE - Francos",
    "Portal de Proveedores FASE 1":        "SACDE PORTAL",
    "Portal de Proveedores FASE 2":        "SACDE PORTAL",
    "Auditoria Seguridad":                 "SACDE Mantenimiento",
    "Soporte":                             "SACDE Mantenimiento",
    "Consultoria FICO":                    "SACDE Mantenimiento",
    "App Facilites":                       "Bayer",
    "Mejoras Solped":                      "Bayer",
    "Mejoras App Almacenes- Fase 2":       "PAMPA Almacenes Mejoras",
}

CLIENT_COLORS = {
    "Transener":    "#6366f1",
    "SACDE":        "#f59e0b",
    "Bayer":        "#3b82f6",
    "Pampa Energia":"#10b981",
}

ESTADOS_DONE = {
    "finalizada", "cerrado", "resuelto", "done", "closed", "resolved",
    "completado", "completada", "terminado", "terminada", "entrega",
}

# ── CONFIG ────────────────────────────────────────────────────────
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

# ── UTILS ────────────────────────────────────────────────────────
def secs_to_hours(s):
    return round(s / 3600, 2) if s else None

def parse_iso_duration(s):
    """PT1H30M15S → float horas"""
    if not s or not s.startswith("PT"):
        return 0.0
    h   = int(re.search(r"(\d+)H", s).group(1)) if "H" in s else 0
    m   = int(re.search(r"(\d+)M", s).group(1)) if "M" in s else 0
    sec = int(re.search(r"(\d+)S", s).group(1)) if "S" in s else 0
    return h + m / 60 + sec / 3600

def build_default_jql():
    projs = '","'.join(p for ps in CLIENT_JIRA_MAP.values() for p in ps)
    return f'project in ("{projs}") ORDER BY created DESC'

# ── JIRA API ─────────────────────────────────────────────────────
def fetch_jira(cfg):
    domain = cfg["jira_domain"].strip().rstrip("/")
    token  = base64.b64encode(f"{cfg['jira_email']}:{cfg['jira_token']}".encode()).decode()
    hdrs   = {"Authorization": f"Basic {token}", "Accept": "application/json"}
    jql    = cfg.get("jira_jql") or build_default_jql()
    url    = f"https://{domain}/rest/api/3/search"
    fields = ("summary,status,assignee,duedate,resolutiondate,"
              "timeoriginalestimate,timeestimate,timespent,project")

    issues, start = [], 0
    while True:
        r = requests.get(url, headers=hdrs, params={
            "jql": jql, "fields": fields, "maxResults": 100, "startAt": start
        }, timeout=30)
        r.raise_for_status()
        d = r.json()
        batch = d.get("issues", [])
        issues += batch
        start  += len(batch)
        if start >= d.get("total", 0) or not batch:
            break

    print(f"  Jira: {len(issues)} issues obtenidas")
    return issues

def process_jira(issues):
    by_client = {}
    today     = datetime.utcnow().date()

    for issue in issues:
        f   = issue["fields"]
        prj = f["project"]["name"]
        cl  = JIRA_TO_CLIENT.get(prj)
        if not cl:
            continue

        est  = secs_to_hours(f.get("timeoriginalestimate") or 0) or None
        pend = secs_to_hours(f.get("timeestimate")          or 0) or None
        cons = secs_to_hours(f.get("timespent")             or 0) or None
        if cons is None and est is not None and pend is not None:
            cons = round(est - pend, 2)

        ffin   = (f.get("duedate")         or "")[:10] or None
        ffreal = (f.get("resolutiondate")  or "")[:10] or None

        estado  = (f["status"]["name"] or "").lower()
        is_done = estado in ESTADOS_DONE

        # Semáforo fecha
        if not ffin:
            sf = "gris"
        elif is_done:
            if not ffreal:
                sf = "verde"
            else:
                diff = (datetime.fromisoformat(ffreal) - datetime.fromisoformat(ffin)).days
                sf   = "verde" if diff <= 0 else "rojo"
        else:
            rest = (datetime.fromisoformat(ffin).date() - today).days
            sf   = "rojo" if rest < 0 else ("amarillo" if rest <= 7 else "verde")

        # Semáforo horas
        if est is None or cons is None:
            sh = "gris"
        elif cons > est:
            sh = "rojo"
        elif not is_done and est > 0 and cons / est >= 0.8:
            sh = "amarillo"
        else:
            sh = "verde"

        desvio = None
        if ffin and ffreal:
            desvio = (datetime.fromisoformat(ffreal) - datetime.fromisoformat(ffin)).days

        assignee = f.get("assignee")
        task = {
            "id":               issue["key"],
            "resumen":          f.get("summary", ""),
            "estado":           f["status"]["name"],
            "persona":          assignee["displayName"] if assignee else "Sin asignar",
            "horas_estimadas":  est,
            "horas_consumidas": cons,
            "horas_pendientes": pend,
            "fecha_fin":        ffin,      # YYYY-MM-DD string (frontend convertirá a Date)
            "fecha_fin_real":   ffreal,
            "desvio_dias":      desvio,
            "sem_fecha":        sf,
            "sem_horas":        sh,
        }
        by_client.setdefault(cl, {}).setdefault(prj, []).append(task)

    return by_client

# ── CLOCKIFY API ─────────────────────────────────────────────────
def fetch_clockify(cfg):
    key       = cfg["clockify_key"]
    hdrs_base = {"X-Api-Key": key}
    hdrs_json = {**hdrs_base, "Content-Type": "application/json"}

    # Obtener workspace
    wid = cfg.get("clockify_workspace")
    if not wid:
        r = requests.get("https://api.clockify.me/api/v1/workspaces", headers=hdrs_base, timeout=15)
        r.raise_for_status()
        ws = r.json()
        if not ws:
            raise ValueError("No se encontraron workspaces en Clockify")
        wid = ws[0]["id"]
        cfg["clockify_workspace"] = wid
        save_config(cfg)
        print(f"  Clockify workspace: {ws[0].get('name','?')} ({wid})")

    date_from = cfg.get("clockify_date_from", f"{datetime.now().year}-01-01T00:00:00.000Z")
    date_to   = datetime.utcnow().strftime("%Y-%m-%dT23:59:59.999Z")

    by_proj   = {}
    by_client = {}
    total_entries = 0
    page      = 1

    while True:
        body = {
            "dateRangeStart": date_from,
            "dateRangeEnd":   date_to,
            "detailedFilter": {"page": page, "pageSize": 1000, "sortColumn": "DATE"},
        }
        r = requests.post(
            f"https://reports.api.clockify.me/v1/workspaces/{wid}/reports/detailed",
            headers=hdrs_json,
            json=body,
            timeout=30,
        )
        r.raise_for_status()
        d = r.json()

        for e in d.get("timeentries", []):
            cw_proj   = e.get("projectName", "")
            user      = e.get("userName", "")
            dur_h     = parse_iso_duration(e.get("timeInterval", {}).get("duration", "PT0S"))
            jira_proj = CW_TO_JIRA.get(cw_proj)
            jira_cl   = JIRA_TO_CLIENT.get(jira_proj) if jira_proj else None

            if jira_proj:
                d2 = by_proj.setdefault(jira_proj, {"total": 0, "users": {}})
                d2["total"]      += dur_h
                d2["users"][user] = d2["users"].get(user, 0) + dur_h

            if jira_cl:
                by_client.setdefault(jira_cl, {"total": 0})["total"] += dur_h

            total_entries += 1

        total_count = (d.get("totals") or [{}])[0].get("entriesCount", 0)
        if page * 1000 >= total_count or not d.get("timeentries"):
            break
        page += 1

    print(f"  Clockify: {total_entries} entradas procesadas")
    return by_proj, by_client

# ── BUILD DASHBOARD DATA ─────────────────────────────────────────
def build_data(jira_by_client, cw_by_proj, cw_by_client):
    all_cl = sorted(set(list(jira_by_client) + list(cw_by_client)))
    clients = []

    for cl_name in all_cl:
        projects = jira_by_client.get(cl_name, {})
        color    = CLIENT_COLORS.get(cl_name, "#667eea")
        proj_list = []
        total_est = total_cons = total_pend = total_tasks = 0

        for proj_name in sorted(projects):
            tareas = projects[proj_name]
            cw     = cw_by_proj.get(proj_name, {"total": 0, "users": {}})

            p_est  = sum(t["horas_estimadas"]  or 0 for t in tareas)
            p_cons = sum(t["horas_consumidas"] or 0 for t in tareas)
            p_pend = sum(t["horas_pendientes"] or 0 for t in tareas)

            total_est  += p_est;  total_cons += p_cons
            total_pend += p_pend; total_tasks += len(tareas)

            cw_users = sorted(
                [{"nombre": n, "horas": round(h, 1)} for n, h in cw["users"].items()],
                key=lambda x: -x["horas"]
            )

            def sort_key(t):
                return (t["horas_estimadas"] is None, t["fecha_fin"] is None, t["fecha_fin"] or "9999")

            proj_list.append({
                "nombre":                proj_name,
                "horas_estimadas":       round(p_est,  1),
                "horas_consumidas_jira": round(p_cons, 1),
                "horas_pendientes_jira": round(p_pend, 1),
                "horas_clockify":        round(cw["total"], 1),
                "cw_users":              cw_users,
                "tareas":                sorted(tareas, key=sort_key),
            })

        clients.append({
            "nombre":    cl_name,
            "color":     color,
            "kpis": {
                "horas_estimadas":  round(total_est,  1),
                "horas_consumidas": round(total_cons, 1),
                "horas_pendientes": round(total_pend, 1),
                "horas_clockify":   round(cw_by_client.get(cl_name, {}).get("total", 0), 1),
                "total_tareas":     total_tasks,
                "total_proyectos":  len(projects),
            },
            "proyectos": proj_list,
        })

    return clients

def fetch_all(cfg):
    jira_by_cl = {}
    if cfg.get("jira_domain") and cfg.get("jira_token"):
        print("Conectando con Jira...")
        issues     = fetch_jira(cfg)
        jira_by_cl = process_jira(issues)

    cw_by_proj, cw_by_cl = {}, {}
    if cfg.get("clockify_key"):
        print("Conectando con Clockify...")
        cw_by_proj, cw_by_cl = fetch_clockify(cfg)

    print("Armando datos del dashboard...")
    return build_data(jira_by_cl, cw_by_proj, cw_by_cl)

# ── HTTP SERVER ──────────────────────────────────────────────────
MIME = {
    "html": "text/html; charset=utf-8",
    "js":   "text/javascript",
    "css":  "text/css",
    "jpg":  "image/jpeg",
    "jpeg": "image/jpeg",
    "png":  "image/png",
    "ico":  "image/x-icon",
}

class Handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._serve_file("index.html", MIME["html"])
        elif path == "/api/data":
            self._handle_data()
        elif path == "/api/config":
            cfg  = load_config()
            safe = {
                "jira_domain":        cfg.get("jira_domain", ""),
                "jira_email":         cfg.get("jira_email",  ""),
                "jira_jql":           cfg.get("jira_jql",    ""),
                "has_jira":           bool(cfg.get("jira_token")),
                "has_clockify":       bool(cfg.get("clockify_key")),
                "clockify_date_from": cfg.get("clockify_date_from",
                                              f"{datetime.now().year}-01-01T00:00:00.000Z"),
            }
            self._json(safe)
        else:
            # Static files
            fname = path.lstrip("/")
            ext   = fname.rsplit(".", 1)[-1].lower() if "." in fname else ""
            ct    = MIME.get(ext, "application/octet-stream")
            self._serve_file(fname, ct)

    def do_POST(self):
        path   = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length)) if length else {}

        if path == "/api/config":
            cfg = load_config()
            cfg.update({k: v for k, v in body.items() if v != ""})
            save_config(cfg)
            self._json({"ok": True})
        else:
            self.send_error(404)

    def _handle_data(self):
        cfg = load_config()
        if not cfg.get("jira_token") and not cfg.get("clockify_key"):
            self._json({"error": "No hay credenciales configuradas"}, 400)
            return
        try:
            data = fetch_all(cfg)
            self._json({"clients": data, "ts": datetime.now().isoformat()})
        except Exception as e:
            import traceback; traceback.print_exc()
            self._json({"error": str(e)}, 500)

    def _serve_file(self, path, ct):
        try:
            with open(path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", ct)
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_error(404)

    def _json(self, obj, status=200):
        data = json.dumps(obj, default=str, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}]", fmt % args)


if __name__ == "__main__":
    print(f"\n✅  Dashboard corriendo en http://localhost:{PORT}")
    print(f"    Credenciales en:       {CONFIG_FILE}")
    print("    Ctrl+C para detener\n")
    try:
        HTTPServer(("", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n👋  Servidor detenido")
