#!/bin/bash

echo "🔄 Actualizando Dashboard de Proyectos..."
echo ""

# Verificar que existe Jira-2.csv
if [ ! -f "Jira-2.csv" ]; then
    echo "❌ Error: No se encontró el archivo Jira-2.csv"
    echo "   Por favor, exporta los datos desde Jira y guárdalos como Jira-2.csv"
    exit 1
fi

# Verificar que Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js no está instalado"
    echo "   Instala Node.js desde https://nodejs.org"
    exit 1
fi

# Procesar datos
echo "📊 Procesando datos del CSV..."
node process_data.js

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Dashboard actualizado correctamente!"
    echo "   Abre index.html en tu navegador para ver los cambios"
    echo ""
    echo "   Última actualización: $(date '+%d/%m/%Y %H:%M:%S')"
else
    echo ""
    echo "❌ Error al procesar los datos"
    exit 1
fi
