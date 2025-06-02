// Obtener el id de la URL
function getParkingId() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function loadParkingDetail() {
    const id = getParkingId();
    const container = document.getElementById('parkingDetail');
    if (!id) {
        container.innerHTML = 'Parqueadero no encontrado.';
        return;
    }
    container.innerHTML = 'Cargando información...';
    try {
        const res = await fetch(API_ROUTES.GET_PARKING(id));
        if (!res.ok) throw new Error('No se pudo obtener la información');
        const data = await res.json();
        if (!data || !data.direccion) {
            container.innerHTML = 'No se encontró información del parqueadero.';
            return;
        }
        // Manejar fotos null o vacías
        let fotos = [];
        if (data.fotos) {
            try { fotos = JSON.parse(data.fotos); } catch (e) { fotos = []; }
        }
        let fotosHtml = fotos.length > 0
            ? fotos.map(f => `<img src="../../Back/${f}" alt="Foto" style="width:300px; height:240px; margin:5px; border-radius:6px;" onerror="this.onerror=null;this.src='../assets/images/parking1.jpeg';">`).join('')
            : `<img src="../assets/images/parking1.jpeg" alt="Foto" style="width:300px; height:240px; margin:5px; border-radius:6px;">`;
        // Manejar reservas vacías o inexistentes
        let reservasHtml = '';
        if (Array.isArray(data.reservations) && data.reservations.length > 0) {
            reservasHtml = '<h4>Reservas:</h4><ul>';
            data.reservations.forEach(r => {
                reservasHtml += `<li>Desde: ${r.fecha_inicio.split('T')[0]} - Hasta: ${r.fecha_fin.split('T')[0]}</li>`;
            });
            reservasHtml += '</ul>';
        } else {
            reservasHtml = '<p>No hay reservas registradas.</p>';
        }
        // Renderiza el layout con botón de volver
        container.innerHTML = `
            <button id="backToCustomer" style="margin-bottom:1.5rem; background:#007bff; color:#fff; border:none; border-radius:5px; padding:0.7em 2em; font-weight:bold; cursor:pointer;">
                <span class="material-icons" style="vertical-align:middle;"> <= </span> Volver
            </button>
            <div class="parking-detail-flex">
                <div class="parking-detail-card">
                    <h2>${data.direccion}</h2>
                    <div>${fotosHtml}</div>
                    <p><strong>Ciudad:</strong> ${data.nombre_lugar}</p>
                    <p><strong>Dimensiones:</strong> ${data.largo}m x ${data.ancho}m</p>
                    <p><strong>Precio/día:</strong> $${data.costo_dia}</p>
                    ${reservasHtml}
                </div>
                <div id="calendarContainer" style="min-width:340px; margin-left:2rem;">
                    <input type="text" id="calendarInline" style="display:none;">
                </div>
            </div>
        `;
        // Obtener fechas reservadas
        const currentDate = new Date();
        currentDate.setDate(currentDate.getDate() - 1);
        const todayStr = currentDate.toISOString().split('T')[0];
        console.log('Fecha de hoy:', todayStr);
        const reservedDates = [];
        if (Array.isArray(data.reservations)) {
            data.reservations.forEach(r => {
                const start = new Date(r.fecha_inicio.split('T')[0]);
                const end = new Date(r.fecha_fin.split('T')[0]);
                for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
                    const dateStr = d.toISOString().split('T')[0];
                    if (dateStr >= todayStr) { // Solo fechas desde hoy
                        reservedDates.push(dateStr);
                    }
                }
            });
        }
        console.log('Fechas reservadas:', reservedDates);

        // Inicializar Litepicker en modo inline y bloquear días reservados y días pasados
        const calendarInput = document.getElementById('calendarInline');
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        new Litepicker({
            element: calendarInput,
            inlineMode: true,
            singleMode: false,
            numberOfMonths: 1,
            numberOfColumns: 1,
            minDate: new Date(new Date().setDate(new Date().getDate() - 1)),
            lockDays: reservedDates,
            disallowLockDaysInRange: true
        });
        // Botón volver
        document.getElementById('backToCustomer').onclick = () => {
            window.location.href = 'customer.html';
        };
    } catch (err) {
        console.error('Error al cargar el parqueadero:', err);
        container.innerHTML = 'Error al cargar la información del parqueadero.';
    }
}

window.addEventListener('DOMContentLoaded', loadParkingDetail);