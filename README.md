# 📊 Dashboard de Proyectos Jira

Dashboard interactivo para visualizar métricas de proyectos, tareas y equipos desde datos exportados de Jira.

## 🎯 Características

- **KPIs principales**: Total de tareas, proyectos, personas y horas trabajadas
- **Visualizaciones interactivas**:
  - Gráfico de barras: Tareas por proyecto (Top 10)
  - Gráfico de torta: Distribución de tareas por estado
  - Gráfico de barras horizontal: Tareas por persona (Top 15)

## 📋 Requisitos

- Node.js instalado (para procesar datos)
- Navegador web moderno
- Archivo CSV exportado desde Jira

## 🚀 Uso

### 1. Exportar datos desde Jira

1. En Jira, ve a **Filtros** > **Ver todos los filtros**
2. Selecciona el filtro con las tareas que deseas visualizar
3. Click en **Exportar** > **Exportar a CSV (Todos los campos)**
4. Guarda el archivo como `Jira-2.csv` en esta carpeta

### 2. Procesar los datos

```bash
node process_data.js
```

Este comando:
- Lee el archivo `Jira-2.csv`
- Procesa y agrupa los datos
- Genera `dashboard_data.json` con las métricas

### 3. Visualizar el dashboard

Abre el archivo `index.html` en tu navegador:

```bash
open index.html
```

O simplemente haz doble click en `index.html`

## 📁 Estructura de archivos

```
Dashboard/
├── Jira-2.csv              # Datos exportados desde Jira
├── process_data.js         # Script para procesar el CSV
├── dashboard_data.json     # Datos procesados (generado)
├── index.html             # Dashboard web
└── README.md              # Este archivo
```

## 🌐 Subir a un sitio web

### Opción 1: GitHub Pages (Gratis)

1. Sube los archivos a un repositorio de GitHub
2. Ve a **Settings** > **Pages**
3. Selecciona la rama y carpeta
4. Tu dashboard estará en `https://tu-usuario.github.io/nombre-repo/`

### Opción 2: Netlify (Gratis)

1. Crea una cuenta en [Netlify](https://netlify.com)
2. Arrastra la carpeta del dashboard a Netlify Drop
3. ¡Listo! Tu dashboard estará online

### Opción 3: Vercel (Gratis)

1. Instala Vercel CLI: `npm i -g vercel`
2. En la carpeta del dashboard: `vercel`
3. Sigue las instrucciones

### Opción 4: Servidor web tradicional

Sube todos los archivos (index.html, dashboard_data.json) a tu servidor web mediante FTP o panel de control.

## 🔄 Actualizar datos

Para actualizar el dashboard con nuevos datos:

1. Exporta nuevo CSV desde Jira con el mismo nombre `Jira-2.csv`
2. Ejecuta: `node process_data.js`
3. Recarga la página del dashboard

## 📊 Métricas mostradas

### Por Cliente/Proyecto
- Nombre del proyecto
- Cantidad de tareas por proyecto
- (Horas trabajadas si están disponibles en Jira)

### Por Persona
- Nombre de la persona
- Cantidad de tareas asignadas

### Por Estado
- Estado de la tarea
- Cantidad de tareas en cada estado
- Distribución porcentual

## 🎨 Personalización

### Cambiar colores

Edita el archivo `index.html` en la sección `<style>`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Modificar gráficos

Los gráficos usan Chart.js. Puedes personalizar:
- Tipos de gráfico (bar, line, pie, doughnut)
- Colores
- Etiquetas
- Animaciones

Consulta la [documentación de Chart.js](https://www.chartjs.org/docs/latest/)

## ⚡ Automatización

Para automatizar la actualización del dashboard:

### Script bash (macOS/Linux)

Crea un archivo `actualizar.sh`:

```bash
#!/bin/bash
node process_data.js
echo "Dashboard actualizado: $(date)"
```

Hazlo ejecutable: `chmod +x actualizar.sh`

### Tarea programada (cron)

```bash
# Actualizar diariamente a las 9 AM
0 9 * * * cd /ruta/al/dashboard && /usr/local/bin/node process_data.js
```

## 🐛 Solución de problemas

### Error al cargar datos

- Verifica que `dashboard_data.json` existe
- Abre la consola del navegador (F12) para ver errores

### Gráficos no se muestran

- Verifica conexión a internet (Chart.js se carga desde CDN)
- Revisa la consola del navegador

### Datos incorrectos

- Verifica que el CSV exportado tiene el formato correcto
- Asegúrate de exportar "Todos los campos" desde Jira

## 📝 Notas

- El dashboard es completamente estático (HTML/CSS/JS)
- No requiere servidor backend
- Los datos se procesan localmente con Node.js
- Compatible con todos los navegadores modernos

## 🤝 Contribuciones

¿Tienes ideas para mejorar el dashboard? ¡Adelante!

---

Creado con ❤️ para análisis de proyectos
