# 📊 Dashboard Interactivo - Altromondo

Dashboard con **filtros interactivos** y **análisis de tareas cerradas** por persona.

## 🎯 Nuevas Características

### ✨ Filtros Interactivos
- **Click en cualquier gráfico** para filtrar todos los demás
- **Filtrado cruzado** entre proyectos, personas y estados
- **Botón "Limpiar Filtros"** para volver a la vista completa
- **Barra de filtros activos** que muestra qué filtros están aplicados

### 📈 Nuevo Gráfico: Tareas Cerradas Este Mes
- Muestra **cantidad de tareas finalizadas en el mes actual** por persona
- Identifica automáticamente estados cerrados:
  - Finalizada, Done, Resuelto, Completado, etc.
- Perfecto para ver **productividad mensual**

## 🖱️ Cómo Usar los Filtros Interactivos

### 1. Filtrar por Proyecto
Click en una barra del gráfico **"Tareas por Proyecto"** o **"Horas por Proyecto"**
- Todos los gráficos mostrarán solo datos de ese proyecto
- Verás cuántas horas y tareas tiene cada persona en ese proyecto
- Verás los estados de las tareas de ese proyecto

### 2. Filtrar por Persona
Click en una barra de **"Tareas por Persona"** o **"Horas por Persona"**
- Todos los gráficos mostrarán solo datos de esa persona
- Verás en qué proyectos trabaja
- Verás cuántas tareas cerró este mes

### 3. Filtrar por Estado
Click en una sección del gráfico de **"Tareas por Estado"**
- Verás qué proyectos tienen tareas en ese estado
- Verás quiénes tienen tareas en ese estado

### 4. Combinar Filtros
Puedes hacer click en múltiples gráficos para combinar filtros:
- Ejemplo 1: Click en "TRANSENER TESLA" → luego click en "diego leonov"
  - Verás solo las tareas de diego en TRANSENER TESLA
- Ejemplo 2: Click en "Finalizada" → luego click en un proyecto
  - Verás solo las tareas finalizadas de ese proyecto

### 5. Limpiar Filtros
Click en el botón **"✕ Limpiar Filtros"** en la barra superior naranja

## 📊 Gráficos Disponibles

1. **Tareas por Proyecto** (Top 10)
   - Click para filtrar por proyecto

2. **Horas por Proyecto** (Top 10)
   - Click para filtrar por proyecto

3. **Tareas por Estado**
   - Click para filtrar por estado

4. **Horas por Persona** (Top 15)
   - Click para filtrar por persona

5. **⭐ Tareas Cerradas Este Mes por Persona** (Top 15)
   - Click para filtrar por persona
   - Muestra solo tareas finalizadas en el mes actual

6. **Tareas por Persona** (Top 15)
   - Click para filtrar por persona

## 🎨 Personalización con Colores Altromondo

- **Azul Navy** (#0d1b5e) - Títulos y valores
- **Azul Medio** (#5c6bc0) - Gráficos de tareas
- **Cyan** (#00bcd4) - Gráficos de horas
- **Verde** (#43e97b) - Tareas cerradas
- **Gradiente de marca** - Fondo y botones

## 🚀 Uso

1. Abre **dashboard-interactivo.html**
2. Carga tu archivo CSV de Jira
3. Carga tu archivo Excel/CSV de Clockify
4. Click en **"🚀 Generar Dashboard"**
5. **Explora los datos** haciendo click en los gráficos

## 💡 Casos de Uso

### Analizar un Proyecto Específico
1. Click en el proyecto en "Tareas por Proyecto"
2. Ve inmediatamente:
   - Quién trabajó en ese proyecto
   - Cuántas horas dedicó cada persona
   - Cuántas tareas cerró cada uno
   - Estado de las tareas

### Ver Productividad de una Persona
1. Click en la persona en "Tareas por Persona"
2. Ve inmediatamente:
   - En qué proyectos trabaja
   - Cuántas horas dedicó a cada proyecto
   - Cuántas tareas cerró este mes
   - Estados de sus tareas

### Analizar Tareas por Estado
1. Click en un estado (ej: "En curso")
2. Ve inmediatamente:
   - Qué proyectos tienen tareas en ese estado
   - Quiénes tienen tareas en ese estado
   - Cuántas tareas hay

### Comparar Productividad Mensual
1. Revisa el gráfico "Tareas Cerradas Este Mes"
2. Identifica quién cerró más tareas
3. Click en una persona para ver detalles

## 🔍 Detalles Técnicos

### Estados Reconocidos como "Cerrados"
- Finalizada
- Done / ✅ Done
- Resuelto / ✅ Resuelto / RESUELTO
- Entrega
- Resolved
- Closed
- Completado / Completed

### Cálculo de Tareas Cerradas
- Se usa la columna "Resuelta" del CSV de Jira
- Se filtran solo tareas del mes y año actuales
- Se agrupa por persona asignada

### Rendimiento
- Procesa miles de tareas en segundos
- Los filtros se aplican instantáneamente
- Todo funciona en el navegador sin servidor

## 📝 Diferencias con Versiones Anteriores

| Característica | dashboard.html | dashboard-completo.html | dashboard-interactivo.html |
|---|---|---|---|
| Carga CSV Jira | ✅ | ✅ | ✅ |
| Carga Excel Clockify | ❌ | ✅ | ✅ |
| Gráficos básicos | ✅ | ✅ | ✅ |
| Colores Altromondo | ❌ | ✅ | ✅ |
| Logo empresa | ❌ | ✅ | ✅ |
| Filtros interactivos | ❌ | ❌ | ✅ |
| Tareas cerradas mes | ❌ | ❌ | ✅ |

## 🌐 Subir a un Sitio Web

El dashboard es un archivo único autónomo:

### Netlify (Recomendado)
1. Ve a [netlify.com](https://netlify.com)
2. Arrastra `dashboard-interactivo.html` a Netlify Drop
3. ¡Listo! URL pública generada

### GitHub Pages
```bash
git add dashboard-interactivo.html "Logo Altro (1).jpg"
git commit -m "Add interactive dashboard"
git push
```
Activa GitHub Pages en Settings → Pages

### Otras opciones
- Vercel
- Servidor web propio
- Firebase Hosting
- Surge.sh

## 🛠️ Resolución de Problemas

### Los filtros no funcionan
- Verifica que ambos archivos estén cargados correctamente
- Recarga la página y vuelve a cargar los archivos

### No muestra tareas cerradas
- Verifica que tu CSV de Jira tenga la columna "Resuelta"
- Asegúrate de que las fechas estén en formato válido
- Solo muestra tareas del mes actual

### El gráfico se ve vacío después de filtrar
- Es normal si no hay datos para esa combinación de filtros
- Click en "✕ Limpiar Filtros" para volver a la vista completa

## 💻 Requisitos

- Navegador moderno (Chrome, Firefox, Safari, Edge)
- JavaScript habilitado
- Archivos de Jira (CSV) y Clockify (Excel/CSV)

## 🎓 Tips Avanzados

1. **Análisis Rápido de Proyecto**
   - Click en proyecto → identifica colaboradores clave

2. **Revisión de Desempeño**
   - Click en persona → ve su distribución de tiempo y tareas

3. **Sprint Review**
   - Filtra por estado "Finalizada" → ve qué se completó

4. **Resource Planning**
   - Compara horas vs tareas para identificar eficiencias

5. **Gestión de Carga**
   - Identifica personas con muchas tareas pero pocas horas

---

🚀 **Dashboard Interactivo - Análisis visual de proyectos en tiempo real**

¿Preguntas? Consulta la documentación o abre un issue.
