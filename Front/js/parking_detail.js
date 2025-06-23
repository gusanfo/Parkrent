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
                </div>
                <div id="calendarContainer" style="min-width:340px; margin-left:2rem;">
                    <div id="calendarBox">
                        <input type="text" id="calendarInline" style="display:none;">
                        <div id="calendarFallback" style="display:none;">
                            <label>Fecha inicio: <input type="date" id="fallbackStart"></label>
                            <label>Fecha fin: <input type="date" id="fallbackEnd"></label>
                        </div>
                    </div>
                    <div id="reservationBox" style="margin-top:1.2rem; text-align:center;">
                        <button id="makeReservationBtn" style="padding:0.7em 1.5em; background:#007bff; color:#fff; border:none; border-radius:5px; font-weight:bold; font-size:1rem; cursor:pointer;">
                            Reservar
                        </button>
                        <div id="reservationMsg" style="margin-top:1rem; min-height:1.5em;"></div>
                    </div>
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
        let selectedDates = [];

        try {
            const picker = new Litepicker({
                element: calendarInput,
                inlineMode: true,
                singleMode: false,
                numberOfMonths: 1,
                numberOfColumns: 1,
                minDate: new Date(new Date().setDate(new Date().getDate() - 1)),
                lockDays: reservedDates,
                disallowLockDaysInRange: true,
                setup: (picker) => {
                    picker.on('selected', (start, end) => {
                        selectedDates = [start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD')];
                    });
                }
            });
        } catch (err) {
            // Si Litepicker falla, muestra los inputs de fallback
            document.getElementById('calendarInline').style.display = 'none';
            document.getElementById('calendarFallback').style.display = 'block';
            // Usar los valores de los inputs de fecha como selectedDates
            document.getElementById('makeReservationBtn').onclick = async function() {
                const msg = document.getElementById('reservationMsg');
                msg.textContent = '';
                const start = document.getElementById('fallbackStart').value;
                const end = document.getElementById('fallbackEnd').value;
                if (!start || !end) {
                    msg.style.color = '#d32f2f';
                    msg.textContent = 'Selecciona un rango de fechas válido.';
                    return;
                }
                selectedDates = [start, end];
                // Obtener datos necesarios
                const id_cliente = localStorage.getItem('userId');
                const id_parqueadero = id; // Usa el id del parqueadero actual
                const fecha_inicio = selectedDates[0];
                const fecha_fin = selectedDates[1];

                // Enviar reserva al backend
                try {
                    const formData = new FormData();
                    formData.append('id_cliente', id_cliente);
                    formData.append('id_parqueadero', id_parqueadero);
                    formData.append('fecha_inicio', fecha_inicio);
                    formData.append('fecha_fin', fecha_fin);

                    const res = await fetch(API_ROUTES.CREATE_RESERVATION, {
                        method: 'POST',
                        body: formData
                    });
                    const data = await res.json();
                    if (res.ok && data.status === "success") {
                        // 1. Obtener el número de celular del propietario
                        try {
                            // Suponiendo que el backend tiene un endpoint para obtener info del parqueadero
                            const parkingRes = await fetch(API_ROUTES.GET_OWNER_INFO_BY_PARKING(id_parqueadero));
                            const parkingData = await parkingRes.json();
                            const ownerName = parkingData.dueño || 'No disponible';
                            const cellphone = parkingData.telefono || 'No disponible';
                            const address = parkingData.direccion || 'No disponible';
                            // 2. Mostrar popup de confirmación
                            showReservationPopup(ownerName, cellphone, address);
                        } catch (err) {
                            showReservationPopup('No disponible');
                        }
                    } else {
                        msg.style.color = '#d32f2f';
                        msg.textContent = data.detail || 'No se pudo realizar la reserva.';
                    }
                } catch (err) {
                    msg.style.color = '#d32f2f';
                    msg.textContent = 'Error de conexión al reservar.';
                }
            };
        }
        // Botón volver
        document.getElementById('backToCustomer').onclick = () => {
            window.location.href = 'customer.html';
        };
        
        document.getElementById('makeReservationBtn').onclick = async function() {
            const msg = document.getElementById('reservationMsg');
            msg.textContent = '';
            // Validar fechas seleccionadas
            if (!selectedDates[0] || !selectedDates[1]) {
                msg.style.color = '#d32f2f';
                msg.textContent = 'Selecciona un rango de fechas válido.';
                return;
            }
            // Obtener datos necesarios
            const id_cliente = localStorage.getItem('userId');
            const id_parqueadero = id; // Usa el id del parqueadero actual
            const fecha_inicio = selectedDates[0];
            const fecha_fin = selectedDates[1];

            // Enviar reserva al backend
            try {
                const formData = new FormData();
                formData.append('id_cliente', id_cliente);
                formData.append('id_parqueadero', id_parqueadero);
                formData.append('fecha_inicio', fecha_inicio);
                formData.append('fecha_fin', fecha_fin);

                const res = await fetch(API_ROUTES.CREATE_RESERVATION, {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                if (res.ok && data.status === "success") {
                    // 1. Obtener el número de celular del propietario
                    try {
                        // Suponiendo que el backend tiene un endpoint para obtener info del parqueadero
                        const parkingRes = await fetch(API_ROUTES.GET_OWNER_INFO_BY_PARKING(id_parqueadero));
                        const parkingData = await parkingRes.json();
                        const ownerName = parkingData.dueño || 'No disponible';
                        const cellphone = parkingData.telefono || 'No disponible';
                        const address = parkingData.direccion || 'No disponible';
                        // 2. Mostrar popup de confirmación
                        showReservationPopup(ownerName, cellphone, address);
                    } catch (err) {
                        showReservationPopup('No disponible');
                    }
                } else {
                    msg.style.color = '#d32f2f';
                    msg.textContent = data.detail || 'No se pudo realizar la reserva.';
                }
            } catch (err) {
                msg.style.color = '#d32f2f';
                msg.textContent = 'Error de conexión al reservar.';
            }
        };
    } catch (err) {
        console.error('Error al cargar el parqueadero:', err);
        container.innerHTML = 'Error al cargar la información del parqueadero.';
    }
}

function showReservationPopup(ownerName, cellphone, address) {
    const popup = document.createElement('div');
    popup.style.position = 'fixed';
    popup.style.top = '0';
    popup.style.left = '0';
    popup.style.width = '100vw';
    popup.style.height = '100vh';
    popup.style.background = 'rgba(0,0,0,0.5)';
    popup.style.display = 'flex';
    popup.style.alignItems = 'center';
    popup.style.justifyContent = 'center';
    popup.style.zIndex = '9999';

    popup.innerHTML = `
        <div style="background:#fff; padding:2em 2.5em; border-radius:10px; text-align:center; max-width:90vw;">
            <h2 style="color:#28a745;">¡Reserva realizada con éxito!</h2>
            <p>
                <strong>Dueño:</strong> ${ownerName}<br>
                <strong>Teléfono:</strong> <span style="color:#007bff;">${cellphone}</span><br>
                <strong>Dirección:</strong> ${address}
            </p>
            <button id="closeReservationPopup" style="margin-top:1.5em; padding:0.7em 2em; background:#007bff; color:#fff; border:none; border-radius:5px; font-weight:bold; font-size:1rem; cursor:pointer;">
                Cerrar
            </button>
        </div>
    `;
    document.body.appendChild(popup);
    document.getElementById('closeReservationPopup').onclick = () => {
        popup.remove();
        // Redirige a la página de reservas del cliente
        window.location.href = "../pages/customer_reservations.html";
    };
}

window.addEventListener('DOMContentLoaded', loadParkingDetail);