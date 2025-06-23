async function loadOwnerReservations() {
    const container = document.getElementById('ownerReservations');
    container.innerHTML = 'Cargando reservas...';
    try {
        const ownerId = localStorage.getItem('userId');
        const res = await fetch(API_ROUTES.RESERVATIONS_BY_OWNER(ownerId));
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
            container.innerHTML = '';
            data.forEach(r => {
                const fechaInicio = r.fecha_inicio.split('T')[0];
                const fechaFin = r.fecha_fin.split('T')[0];
                const hoyStr = new Date().toISOString().split('T')[0];
                let estadoReserva = '';
                if (r.estado === "2") {
                    estadoReserva = `<span style="color:#d32f2f;font-weight:bold;">Reserva cancelada</span>`;
                } else if (fechaFin < hoyStr) {
                    estadoReserva = `<span style="color:#1976d2;font-weight:bold;">Reserva finalizada</span>`;
                } else if (r.estado === "1") {
                    estadoReserva = `<span style="color:#388e3c;font-weight:bold;">Reserva activa</span>`;
                }

                // Mostrar teléfono del cliente solo si la reserva está activa
                const mostrarTelefonoCliente = (r.estado === "1" && fechaFin >= hoyStr);

                container.innerHTML += `
                    <div class="parking-card">
                        <strong>Parqueadero:</strong> ${r.direccion}<br>
                        <strong>Desde:</strong> ${fechaInicio} <strong>Hasta:</strong> ${fechaFin}<br>
                        <strong>Cliente:</strong> ${r.cliente || 'No disponible'}<br>
                        ${mostrarTelefonoCliente ? `<strong>Teléfono cliente:</strong> <span style="color:#007bff;">${r.telefono_cliente || 'No disponible'}</span><br>` : ""}
                        <strong>Costo:</strong> $${r.costo}<br>
                        ${estadoReserva}
                    </div>
                `;
            });
        } else {
            container.innerHTML = 'No tienes reservas registradas.';
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

async function loadCustomerReservations() {
    const userId = localStorage.getItem('userId');
    const container = document.getElementById('customerReservations');
    container.innerHTML = 'Cargando reservas...';
    try {
        const res = await fetch(API_ROUTES.RESERVATIONS_BY_CUSTOMER(userId));
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
            container.innerHTML = `
                <div style="background:#fff3cd; color:#856404; border-radius:6px; padding:0.8em 1em; margin-bottom:1em; border:1px solid #ffeeba; font-size:0.98em;">
                    <strong>Nota:</strong> Solo puedes cancelar reservas si faltan 2 días o más para la fecha de inicio.
                </div>
            `;
            data.forEach(r => {
                const fechaInicio = r.fecha_inicio.split('T')[0];
                const fechaFin = r.fecha_fin.split('T')[0];
                let estadoReserva = '';
                const hoy = new Date();
                const hoyStr = hoy.toISOString().split('T')[0];

                // Calcular diferencia de días entre hoy y fechaInicio
                const fechaInicioDate = new Date(fechaInicio);
                const diffTime = fechaInicioDate.getTime() - hoy.getTime();
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

                if (r.estado === "2") {
                    estadoReserva = `<span style="color:#d32f2f;font-weight:bold;">Reserva cancelada</span>`;
                } else if (fechaFin < hoyStr) {
                    estadoReserva = `<span style="color:#1976d2;font-weight:bold;">Reserva finalizada</span>`;
                } else if (r.estado === "1") {
                    estadoReserva = `<span style="color:#388e3c;font-weight:bold;">Reserva activa</span>`;
                }

                // Botón eliminar solo si faltan al menos 2 días para la fecha de inicio
                let deleteBtn = '';
                if (r.estado === "1" && diffDays >= 1) {
                    deleteBtn = `<button class="delete-reservation-btn" data-id="${r.id_reserva}" style="margin-top:0.7em; background:#d32f2f; color:#fff; border:none; border-radius:5px; padding:0.5em 1.2em; font-weight:bold; cursor:pointer;">Eliminar</button>`;
                }

                const mostrarTelefono = (r.estado === "1" && fechaFin >= hoyStr);
                container.innerHTML += `
                    <div class="reservation-card">
                        <div class="reservation-content">
                            <div>
                                <strong>Parqueadero:</strong> ${r.direccion}<br>
                                <strong>Desde:</strong> ${fechaInicio} <strong>Hasta:</strong> ${fechaFin}<br>
                                <strong>Costo:</strong> $${r.costo}<br>
                                <strong>Dueño:</strong> ${r["dueño"] || r.duenio || r.owner || 'No disponible'}<br>
                                ${mostrarTelefono ? `<strong>Teléfono:</strong> <span style="color:#007bff;">${r.telefono || 'No disponible'}</span><br>` : ""}
                                ${estadoReserva}
                            </div>
                            ${deleteBtn}
                        </div>
                    </div>
                `;
            });
        } else {
            container.innerHTML = 'No tienes reservas activas.';
        }
    } catch (err) {
        container.innerHTML = 'Error al cargar reservas.';
    }
};

window.loadCustomerReservations = loadCustomerReservations;

const container = document.getElementById('customerReservations');
container.addEventListener('click', async function(e) {
    if (e.target.classList.contains('delete-reservation-btn')) {
        const reservationId = e.target.getAttribute('data-id')
        if (confirm('¿Seguro que deseas cancelar esta reserva?')) {
            try {
                const res = await fetch(API_ROUTES.DELETE_RESERVATION(reservationId), {
                    method: 'DELETE'
                });
                const data = await res.json();
                if (res.ok && (data.status === "success" || data.mensaje?.toLowerCase().includes("cancelada"))) {
                    alert('Reserva cancelada correctamente.');
                    loadCustomerReservations();
                } else {
                    alert(data.detail || data.mensaje || 'No se pudo cancelar la reserva.');
                }
            } catch (err) {
                alert('Error de conexión al cancelar la reserva.');
            }
        }
    }
});
