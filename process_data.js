const fs = require('fs');
const readline = require('readline');

function parseTimeToHours(timeStr) {
    if (!timeStr || timeStr.trim() === '') {
        return 0;
    }

    let hours = 0;
    const daysMatch = timeStr.match(/(\d+)d/);
    const hoursMatch = timeStr.match(/(\d+)h/);
    const minutesMatch = timeStr.match(/(\d+)m/);

    if (daysMatch) {
        hours += parseInt(daysMatch[1]) * 8; // 1 día = 8 horas
    }
    if (hoursMatch) {
        hours += parseInt(hoursMatch[1]);
    }
    if (minutesMatch) {
        hours += parseInt(minutesMatch[1]) / 60;
    }

    return Math.round(hours * 100) / 100;
}

function parseCSVLine(line) {
    const result = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
        const char = line[i];

        if (char === '"') {
            if (inQuotes && line[i + 1] === '"') {
                current += '"';
                i++;
            } else {
                inQuotes = !inQuotes;
            }
        } else if (char === ',' && !inQuotes) {
            result.push(current);
            current = '';
        } else {
            current += char;
        }
    }
    result.push(current);
    return result;
}

async function processJiraCSV(csvFile) {
    const horasPorProyecto = {};
    const tareasPorProyecto = {};
    const tareasPorPersona = {};
    const tareasPorEstado = {};
    const proyectos = new Set();
    const personas = new Set();

    let totalHoras = 0;
    let totalTareas = 0;
    let isFirstLine = true;

    const fileStream = fs.createReadStream(csvFile, { encoding: 'utf-8' });
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    for await (const line of rl) {
        if (isFirstLine) {
            isFirstLine = false;
            continue;
        }

        const row = parseCSVLine(line);
        if (row.length < 54) continue;

        const proyecto = row[6] || 'Sin proyecto';
        const persona = row[13] || 'Sin asignar';
        const estado = row[4] || 'Sin estado';
        const tiempoTrabajado = row[53] || '';

        const horas = parseTimeToHours(tiempoTrabajado);

        if (proyecto && proyecto.trim()) {
            horasPorProyecto[proyecto] = (horasPorProyecto[proyecto] || 0) + horas;
            tareasPorProyecto[proyecto] = (tareasPorProyecto[proyecto] || 0) + 1;
            proyectos.add(proyecto);
        }

        if (persona && persona.trim()) {
            tareasPorPersona[persona] = (tareasPorPersona[persona] || 0) + 1;
            personas.add(persona);
        }

        if (estado && estado.trim()) {
            tareasPorEstado[estado] = (tareasPorEstado[estado] || 0) + 1;
        }

        totalHoras += horas;
        totalTareas += 1;
    }

    // Ordenar datos
    const horasPorProyectoOrdenado = Object.fromEntries(
        Object.entries(horasPorProyecto).sort(([, a], [, b]) => b - a)
    );

    const tareasPorProyectoOrdenado = Object.fromEntries(
        Object.entries(tareasPorProyecto).sort(([, a], [, b]) => b - a)
    );

    const tareasPorPersonaOrdenado = Object.fromEntries(
        Object.entries(tareasPorPersona).sort(([, a], [, b]) => b - a)
    );

    return {
        kpis: {
            total_horas: Math.round(totalHoras * 100) / 100,
            total_tareas: totalTareas,
            total_proyectos: proyectos.size,
            total_personas: personas.size
        },
        horas_por_proyecto: horasPorProyectoOrdenado,
        tareas_por_proyecto: tareasPorProyectoOrdenado,
        tareas_por_persona: tareasPorPersonaOrdenado,
        tareas_por_estado: tareasPorEstado
    };
}

(async () => {
    console.log('Procesando Jira-2.csv...');
    const data = await processJiraCSV('Jira-2.csv');

    fs.writeFileSync('dashboard_data.json', JSON.stringify(data, null, 2), 'utf-8');

    console.log('✅ Datos procesados correctamente!');
    console.log(`Total de horas: ${data.kpis.total_horas}`);
    console.log(`Total de tareas: ${data.kpis.total_tareas}`);
    console.log(`Total de proyectos: ${data.kpis.total_proyectos}`);
    console.log(`Total de personas: ${data.kpis.total_personas}`);
})();
