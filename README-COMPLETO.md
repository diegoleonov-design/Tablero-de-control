# 📊 Dashboard Completo - Jira + Clockify

Dashboard interactivo que combina datos de **Jira** (tareas) y **Clockify** (horas trabajadas) para un análisis completo de proyectos y equipos.

## 🎯 Características

### KPIs principales
- 📋 Total de tareas
- 📁 Total de proyectos
- 👥 Total de personas
- ⏱️ Total de horas trabajadas

### Visualizaciones
1. **Tareas por Proyecto** - Gráfico de barras (Top 10)
2. **Horas por Proyecto** - Gráfico de barras (Top 10)
3. **Tareas por Estado** - Gráfico de torta
4. **Horas por Persona** - Gráfico horizontal (Top 15)
5. **Tareas por Persona** - Gráfico horizontal (Top 15)

## 🚀 Uso

### 1. Preparar archivos

#### Archivo Jira (CSV)
1. En Jira, ve a **Filtros** > **Ver todos los filtros**
2. Selecciona el filtro con tus tareas
3. Click en **Exportar** > **Exportar a CSV (Todos los campos)**
4. Guarda el archivo

#### Archivo Clockify (Excel o CSV)
1. En Clockify, ve a **Reports** > **Detailed**
2. Selecciona el rango de fechas
3. Click en **Export** > **Excel** o **CSV**
4. Guarda el archivo

### 2. Generar Dashboard

1. **Abre** [dashboard-completo.html](dashboard-completo.html) en tu navegador
2. **Arrastra** o selecciona el archivo CSV de Jira en la primera zona
3. **Arrastra** o selecciona el archivo Excel/CSV de Clockify en la segunda zona
4. **Click** en "🚀 Generar Dashboard"
5. ¡Listo! El dashboard se generará automáticamente

## 📋 Formatos soportados

### Jira
- ✅ CSV con todos los campos
- Columnas requeridas:
  - `Nombre del proyecto`
  - `Persona asignada`
  - `Estado`

### Clockify
- ✅ Excel (.xlsx, .xls)
- ✅ CSV

- Columnas reconocidas automáticamente:
  - **Proyecto**: `Project`, `Proyecto`, `Cliente`, `Client`
  - **Usuario**: `User`, `Usuario`, `Name`, `Nombre`
  - **Duración**: `Duration`, `Duración`, `Time`, `Tiempo`, `Duration (h)`

## 🔧 Solución de problemas

### No se reconocen las horas de Clockify

El dashboard intenta detectar automáticamente las columnas, pero si tu archivo tiene nombres diferentes:

1. Abre el archivo Excel/CSV
2. Asegúrate de que tenga columnas con nombres como:
   - Proyecto o Project
   - Usuario o User
   - Duración o Duration
3. Si los nombres son diferentes, renómbralos

### Formatos de tiempo soportados

El dashboard reconoce estos formatos de Clockify:
- `1:30:00` (1 hora 30 minutos)
- `01:30:00`
- `5h 30m` (5 horas 30 minutos)
- `2d 3h` (2 días 3 horas)

## 🌐 Subir a un sitio web

El dashboard es un **archivo único** que funciona completamente en el navegador.

### Opción 1: Netlify (Recomendado)
1. Ve a [netlify.com](https://netlify.com)
2. Arrastra `dashboard-completo.html` a "Netlify Drop"
3. ¡Listo! Tendrás una URL pública

### Opción 2: GitHub Pages
1. Crea un repositorio en GitHub
2. Sube `dashboard-completo.html`
3. Renómbralo a `index.html`
4. Activa GitHub Pages en Settings > Pages

### Opción 3: Vercel
```bash
npm i -g vercel
vercel --prod
```

### Opción 4: Servidor propio
Sube el archivo a tu servidor web vía FTP o panel de control.

## 🔄 Actualizar datos

Cada vez que quieras ver datos actualizados:

1. Exporta nuevos archivos desde Jira y Clockify
2. Abre el dashboard
3. Carga los nuevos archivos
4. Genera el dashboard nuevamente

**No necesitas recargar la página** - puedes cargar archivos nuevos directamente.

## 🎨 Personalización

### Cambiar colores del gradiente

Edita el CSS en la sección `<style>`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Cambia los colores hexadecimales a tus preferidos.

### Modificar cantidad de items en gráficos

En el código JavaScript, busca `.slice(0, 10)` o `.slice(0, 15)` y cambia el número.

Ejemplo para mostrar Top 20 proyectos:
```javascript
.slice(0, 20)  // Cambiar de 10 a 20
```

## 📊 Datos procesados

El dashboard procesa y combina:

### De Jira:
- Cantidad de tareas por proyecto
- Cantidad de tareas por persona
- Distribución de tareas por estado
- Totales de proyectos y personas

### De Clockify:
- Horas trabajadas por proyecto
- Horas trabajadas por persona
- Total de horas del período

### Combinados:
- Vista completa de productividad
- Análisis de carga de trabajo
- Distribución de esfuerzo por proyecto

## 💡 Tips

1. **Filtros en Jira**: Crea filtros específicos para exportar solo las tareas relevantes
2. **Período en Clockify**: Exporta el mismo período que tus tareas de Jira para datos coherentes
3. **Nombres coincidentes**: Asegúrate de que los nombres de proyectos y personas coincidan entre Jira y Clockify
4. **Archivos grandes**: El dashboard puede procesar archivos grandes, pero puede tomar unos segundos

## 🔒 Privacidad

- ✅ **Todo el procesamiento ocurre en tu navegador**
- ✅ **No se envían datos a ningún servidor**
- ✅ **Tus archivos no se guardan en ningún lado**
- ✅ **100% privado y seguro**

## 📝 Notas técnicas

- Usa **Chart.js** para gráficos interactivos
- Usa **PapaParse** para leer archivos CSV
- Usa **SheetJS (xlsx)** para leer archivos Excel
- Compatible con todos los navegadores modernos
- No requiere instalación ni configuración

## ❓ Preguntas frecuentes

**¿Puedo usar solo uno de los archivos?**
No, el dashboard requiere ambos archivos para funcionar correctamente.

**¿Funciona con otros sistemas además de Jira/Clockify?**
Sí, siempre que los archivos tengan columnas similares (proyecto, persona, duración, etc.)

**¿Puedo guardar el dashboard generado?**
El dashboard se regenera cada vez. Para conservar una versión, toma capturas de pantalla o exporta los gráficos.

**¿Hay límite de tamaño de archivo?**
No hay límite estricto, pero archivos muy grandes (>50MB) pueden tardar más en procesarse.

---

🚀 **Creado para análisis profesional de proyectos**

¿Necesitas ayuda? Abre un issue o consulta la documentación.
