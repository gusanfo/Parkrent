async function loadOwnerReservations() {
    const ownerId = localStorage.getItem('userId');
    const container = document.getElementById('ownerReservations');
    container.innerHTML = 'Cargando...';
    try {
        const res = await fetch(API_ROUTES.RESERVATIONS_BY_OWNER(ownerId));
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
            container.innerHTML = '';
            data.forEach(r => {
                const fechaInicio = r.fecha_inicio.split('T')[0];
                const fechaFin = r.fecha_fin.split('T')[0];
                let estadoReserva = '';

                // Obtener fecha actual en formato YYYY-MM-DD
                const hoy = new Date();
                const hoyStr = hoy.toISOString().split('T')[0];

                if (r.estado === "2") {
                    estadoReserva = `<span style="color:#d32f2f;font-weight:bold;">Reserva fue cancelada</span>`;
                } else if (fechaFin < hoyStr) {
                    estadoReserva = `<span style="color:#1976d2;font-weight:bold;">Reserva finalizada</span>`;
                } else if (r.estado === "1") {
                    estadoReserva = `<span style="color:#388e3c;font-weight:bold;">Reserva activa</span>`;
                } 

                container.innerHTML += `
                    <div class="parking-card">
                        <strong>Parqueadero:</strong> ${r.direccion}
                        <span style="font-weight:bold; color:${r.estado_parqueadero === "2" ? "#d32f2f" : "#388e3c"};">
                            ${r.estado_parqueadero === "2" ? " (Parqueadero ya no existe)" : " (Activo)"}
                        </span><br>
                        <strong>Cliente:</strong> ${r.cliente}<br>
                        <strong>Desde:</strong> ${fechaInicio} <strong>Hasta:</strong> ${fechaFin}<br>
                        <strong>Costo:</strong> $${r.costo}<br>
                        ${estadoReserva}
                    </div>
                `;
            });
        } else {
            container.innerHTML = 'No hay reservas registradas.';
        }
    } catch (err) {
        container.innerHTML = 'Error al cargar reservas.';
    }
}

function convertReservationsToCsv(reservas) {
    if (!reservas || !reservas.length) return '';
    const hoy = new Date();
    const hoyStr = hoy.toISOString().split('T')[0];

    const headers = [
        "ID Reserva", "Parqueadero", "Cliente", "Fecha Inicio", "Fecha Fin", "Costo", "Estado Reserva", "Estado Parqueadero", "Fecha Descarga"
    ];
    const rows = reservas.map(r => {
        //const fechaFin = r.fecha_fin.split('T')[0];
        const fechaFin = r.fecha_fin.replace('T', ' ').split('.')[0]; // Formatear fecha fin
        let estadoReserva = "";
        if (r.estado === "2") {
            estadoReserva = "Cancelada";
        } else if (fechaFin < hoyStr) {
            estadoReserva = "Reserva finalizada";
        } else if (r.estado === "1") {
            estadoReserva = "Activa";
        }
        return [
            r.id_reserva,
            r.direccion,
            r.cliente,
            r.fecha_inicio.replace('T', ' ').split('.')[0], // Formatear fecha inicio
            fechaFin,
            r.costo,
            estadoReserva,
            r.estado_parqueadero === "2" ? "Parqueadero no existe" : "Activo",
            hoyStr
        ];
    });
    // Unir todo en formato CSV
    return [headers, ...rows].map(row => row.map(val => `"${val}"`).join(',')).join('\r\n');
}

window.downloadReservationsCsv = async function() {
    const ownerId = localStorage.getItem('userId');
    try {
        const res = await fetch(API_ROUTES.RESERVATIONS_BY_OWNER(ownerId));
        const data = await res.json();
        if (!Array.isArray(data) || !data.length) {
            alert("No hay reservas para descargar.");
            return;
        }
        const csv = convertReservationsToCsv(data);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);

        // Crear un enlace temporal y descargar
        const a = document.createElement('a');
        a.href = url;
        a.download = 'reservas.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (err) {
        alert("Error al descargar reservas.");
    }
};

window.loadOwnerReservations = loadOwnerReservations; // Para poder llamarla desde otros archivos
