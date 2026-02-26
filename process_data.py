import csv
import json
from datetime import datetime

MESES_ES = {
    'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'ago': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12
}

ESTADOS_FINALIZADOS = {
    'finalizada', 'cerrado', 'resuelto', 'done', 'closed', 'resolved',
    'completado', 'completada', 'terminado', 'terminada'
}

def parse_jira_date(date_str):
    if not date_str or not date_str.strip():
        return None
    try:
        parts = date_str.strip().split(' ')
        date_part = parts[0]
        day, mon, year = date_part.split('/')
        month = MESES_ES.get(mon.lower().replace('.', ''), 0)
        if not month:
            return None
        full_year = 2000 + int(year) if int(year) < 100 else int(year)
        return datetime(full_year, month, int(day))
    except Exception:
        return None

def format_date(dt):
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%d')

def seconds_to_hours(s):
    if not s or not s.strip():
        return None
    try:
        return round(int(s) / 3600, 2)
    except Exception:
        return None

# ── Mappings ────────────────────────────────────────────────────────────────

CLIENT_JIRA_MAP = {
    "Transener": [
        "TRANSENER TESLA",
        "TRANSENER Costeo Emplazamiento",
        "TRANSENER Mantenimiento",
    ],
    "SACDE": [
        "SACDE - Francos",
        "SACDE - Equipos",
        "SACDE - Partes Diarios",
        "SACDE APP MATERIALES",
        "SACDE Mantenimiento",
        "SACDE PORTAL",
    ],
    "Bayer": ["Bayer"],
    "Pampa Energia": ["PAMPA Almacenes Mejoras"],
}

JIRA_TO_CLIENT = {}
for _client, _projs in CLIENT_JIRA_MAP.items():
    for _p in _projs:
        JIRA_TO_CLIENT[_p] = _client

CLOCKIFY_TO_JIRA = {
    "Tesla": "TRANSENER TESLA",
    "Costeo de Emplazamiento": "TRANSENER Costeo Emplazamiento",
    "Migración S4": "TRANSENER Mantenimiento",
    "Interface de Francos Compensatorios": "TRANSENER Mantenimiento",
    "Trello": "TRANSENER Mantenimiento",
    "Premios": "TRANSENER Mantenimiento",
    "Paquete 4 ''Francos APK''": "SACDE - Francos",
    "Portal de Proveedores FASE 1": "SACDE PORTAL",
    "Portal de Proveedores FASE 2": "SACDE PORTAL",
    "Auditoria Seguridad": "SACDE Mantenimiento",
    "Soporte": "SACDE Mantenimiento",
    "Consultoria FICO": "SACDE Mantenimiento",
    "App Facilites": "Bayer",
    "Mejoras Solped": "Bayer",
    "Mejoras App Almacenes- Fase 2": "PAMPA Almacenes Mejoras",
}

CLIENT_COLORS = {
    "Transener":   "#6366f1",
    "SACDE":       "#f59e0b",
    "Bayer":       "#3b82f6",
    "Pampa Energia": "#10b981",
}

# ── Clockify processing ─────────────────────────────────────────────────────

def process_clockify(csv_file):
    by_jira_project = {}
    by_client = {}

    with open(csv_file, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 16:
                continue
            project = row[0].strip()
            client  = row[1].strip()
            user    = row[5].strip()
            task    = row[3].strip()
            try:
                duration = float(row[15])
            except Exception:
                duration = 0

            jira_proj   = CLOCKIFY_TO_JIRA.get(project)
            jira_client = JIRA_TO_CLIENT.get(jira_proj, client)

            if jira_proj:
                d = by_jira_project.setdefault(jira_proj, {'total': 0, 'users': {}, 'tasks': {}})
                d['total'] += duration
                d['users'][user] = d['users'].get(user, 0) + duration
                if task:
                    d['tasks'][task] = d['tasks'].get(task, 0) + duration

            eff_client = jira_client if jira_proj else client
            if eff_client and eff_client.strip():
                c = by_client.setdefault(eff_client, {'total': 0, 'users': {}})
                c['total'] += duration
                c['users'][user] = c['users'].get(user, 0) + duration

    return by_jira_project, by_client

# ── Jira processing ─────────────────────────────────────────────────────────

def process_jira(csv_file):
    today = datetime.today()
    clients = {}

    with open(csv_file, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 55:
                continue

            resumen   = row[0].strip()
            issue_key = row[1].strip()
            estado    = row[4].strip()
            proyecto  = row[6].strip()
            asignado  = row[13].strip() or 'Sin asignar'

            client = JIRA_TO_CLIENT.get(proyecto)
            if not client:
                continue

            horas_est    = seconds_to_hours(row[51])
            horas_rest   = seconds_to_hours(row[52])
            horas_worked = seconds_to_hours(row[53])

            fecha_fin        = parse_jira_date(row[23])  # due date
            fecha_resolucion = parse_jira_date(row[22])  # resolved date

            es_finalizado = estado.lower() in ESTADOS_FINALIZADOS

            # Deviation (days): positive = late, negative = early
            desvio_dias = None
            if fecha_fin and fecha_resolucion:
                desvio_dias = (fecha_resolucion - fecha_fin).days

            # ── Semáforo fechas ──────────────────────────────────────────
            if fecha_fin:
                if es_finalizado:
                    if desvio_dias is not None:
                        semaforo_fecha = 'verde' if desvio_dias <= 0 else 'rojo'
                    else:
                        semaforo_fecha = 'verde'
                else:
                    dias_restantes = (fecha_fin - today).days
                    if dias_restantes < 0:
                        semaforo_fecha = 'rojo'
                    elif dias_restantes <= 7:
                        semaforo_fecha = 'amarillo'
                    else:
                        semaforo_fecha = 'verde'
            else:
                semaforo_fecha = 'gris'

            # Effective consumed hours (if worked not available, infer from est - rest)
            if horas_worked is None and horas_est is not None and horas_rest is not None:
                horas_consumed_eff = round(horas_est - horas_rest, 2)
            else:
                horas_consumed_eff = horas_worked

            # ── Semáforo horas ───────────────────────────────────────────
            if horas_est is not None and horas_consumed_eff is not None:
                if horas_consumed_eff > horas_est:
                    semaforo_horas = 'rojo'
                elif not es_finalizado and horas_est > 0 and (horas_consumed_eff / horas_est) >= 0.8:
                    semaforo_horas = 'amarillo'
                else:
                    semaforo_horas = 'verde'
            else:
                semaforo_horas = 'gris'

            task = {
                "id":               issue_key,
                "resumen":          resumen,
                "estado":           estado,
                "persona":          asignado,
                "horas_estimadas":  horas_est,
                "horas_consumidas": horas_consumed_eff,
                "horas_pendientes": horas_rest,
                "fecha_fin":        format_date(fecha_fin),
                "fecha_fin_real":   format_date(fecha_resolucion),
                "desvio_dias":      desvio_dias,
                "sobre_estimacion": semaforo_horas == 'rojo',
                "es_finalizado":    es_finalizado,
                "semaforo_fecha":   semaforo_fecha,
                "semaforo_horas":   semaforo_horas,
            }

            clients.setdefault(client, {}).setdefault(proyecto, []).append(task)

    return clients

# ── Build final structure ───────────────────────────────────────────────────

def build_dashboard(jira_by_client, cw_by_project, cw_by_client):
    clientes_list = []

    for client_name in sorted(jira_by_client.keys()):
        projects = jira_by_client[client_name]
        total_est = 0
        total_consumed_jira = 0
        total_pending_jira = 0
        total_tareas = 0
        proyectos_list = []

        for proj_nombre in sorted(projects.keys()):
            tareas = projects[proj_nombre]
            cw = cw_by_project.get(proj_nombre, {})

            proj_est      = sum(t['horas_estimadas']  or 0 for t in tareas)
            proj_consumed = sum(t['horas_consumidas'] or 0 for t in tareas)
            proj_pending  = sum(t['horas_pendientes'] or 0 for t in tareas)

            total_est           += proj_est
            total_consumed_jira += proj_consumed
            total_pending_jira  += proj_pending
            total_tareas        += len(tareas)

            cw_users = [
                {"nombre": u, "horas": round(h, 2)}
                for u, h in sorted(cw.get('users', {}).items(), key=lambda x: -x[1])
            ]

            tareas_sorted = sorted(tareas, key=lambda t: (
                t['horas_estimadas'] is None,
                t['fecha_fin'] is None,
                t['fecha_fin'] or ''
            ))

            proyectos_list.append({
                "nombre":                    proj_nombre,
                "horas_estimadas":           round(proj_est, 2),
                "horas_consumidas_jira":     round(proj_consumed, 2),
                "horas_pendientes_jira":     round(proj_pending, 2),
                "horas_consumidas_clockify": round(cw.get('total', 0), 2),
                "personas_clockify":         cw_users,
                "total_tareas":              len(tareas),
                "tareas":                    tareas_sorted,
            })

        client_cw = cw_by_client.get(client_name, {})

        clientes_list.append({
            "nombre":  client_name,
            "color":   CLIENT_COLORS.get(client_name, "#667eea"),
            "kpis": {
                "horas_estimadas":           round(total_est, 2),
                "horas_consumidas_jira":     round(total_consumed_jira, 2),
                "horas_pendientes_jira":     round(total_pending_jira, 2),
                "horas_consumidas_clockify": round(client_cw.get('total', 0), 2),
                "total_tareas":              total_tareas,
                "total_proyectos":           len(projects),
            },
            "proyectos": proyectos_list,
        })

    return {
        "generado": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "clientes": clientes_list,
    }

# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("Procesando datos...")

    cw_by_project, cw_by_client = process_clockify(
        'Clockify_Time_Report_Detailed_01_01_2026-31_01_2026.csv'
    )
    jira_by_client = process_jira('Jira-2.csv')

    dashboard = build_dashboard(jira_by_client, cw_by_project, cw_by_client)

    # JSON (por compatibilidad)
    with open('dashboard_data.json', 'w', encoding='utf-8') as f:
        json.dump(dashboard, f, ensure_ascii=False, indent=2)

    # JS embebible (para abrir index.html directo sin servidor)
    with open('dashboard_data.js', 'w', encoding='utf-8') as f:
        f.write('window.DASHBOARD_DATA = ')
        json.dump(dashboard, f, ensure_ascii=False, indent=2)
        f.write(';\n')

    print("✅ dashboard_data.json y dashboard_data.js generados!")
    for c in dashboard['clientes']:
        k = c['kpis']
        print(f"  {c['nombre']}: {k['total_tareas']} tareas | "
              f"Est: {k['horas_estimadas']}h | "
              f"Clockify: {k['horas_consumidas_clockify']}h")
