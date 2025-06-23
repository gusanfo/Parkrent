// Tabs
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
        this.classList.add('active');
        if(this.dataset.tab === 'parkings') document.getElementById('parkingsTab').style.display = 'block';
        if(this.dataset.tab === 'add') document.getElementById('addTab').style.display = 'block';
        if(this.dataset.tab === 'reservations') document.getElementById('reservationsTab').style.display = 'block';
    });
});

// Mostrar nombre del owner
const ownerName = localStorage.getItem('userName') + ' ' + localStorage.getItem('userLastName');
document.getElementById('ownerName').textContent = "Bienvenido, " + ownerName;

// Cargar parqueaderos del owner
async function loadOwnerParkings() {
    const ownerId = localStorage.getItem('userId');
    const container = document.getElementById('ownerParkings');
    container.innerHTML = 'Cargando...';
    try {
        const res = await fetch(API_ROUTES.PARKINGS_BY_OWNER(ownerId));
        const data = await res.json();
        currentParkings = data.parqueaderos || [];
        if (currentParkings.length > 0) {
            container.innerHTML = '';
            currentParkings.forEach((p, idx) => {
                // Parsear el string de fotos a array
                let fotos = [];
                try {
                    fotos = JSON.parse(p.fotos);
                } catch (e) {
                    fotos = [];
                }
                // Tomar la primera foto si existe, si no usar una imagen por defecto
                const primeraFoto = fotos.length > 0
                    ? `../../Back/${fotos[0]}`
                    : '../assets/images/parking1.jpeg';

                container.innerHTML += `
                    <div class="parking-card" data-idx="${idx}">
                        <div class="parking-card-content">
                            <img src="${primeraFoto}" alt="Foto parqueadero">
                            <div>
                                <strong>Dirección:</strong> ${p.direccion}<br>
                                <strong>Descripción:</strong> ${p.descripcion ? p.descripcion : 'Sin descripción'}<br>
                                <strong>Dimensiones:</strong> ${p.largo}m x ${p.ancho}m<br>
                                <strong>Precio/día:</strong> $${p.costo_dia}<br>
                                <button class="edit-parking-btn" data-id="${p.id_parqueadero}" data-idx="${idx}">
                                    <span class="material-icons" style="vertical-align:middle;">edit</span> Editar
                                </button>
                                <button class="delete-parking-btn" data-id="${p.id_parqueadero}" data-idx="${idx}">
                                    <span class="material-icons" style="vertical-align:middle;">delete</span> Eliminar
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            });
        } else {
            container.innerHTML = 'No tienes parqueaderos registrados.';
        }
    } catch (err) {
        container.innerHTML = 'Error al cargar parqueaderos.';
    }
}
loadOwnerParkings();

// Manejar click en botón Editar
document.getElementById('ownerParkings').addEventListener('click', function(e) {
    if (e.target.classList.contains('edit-parking-btn')) {
        const idx = e.target.getAttribute('data-idx');
        openEditModal(idx);
    }
});

let currentParkings = []; // Guarda los parqueaderos cargados

// Abrir modal y llenar datos
function openEditModal(idx) {
    document.getElementById('editParkingMsg').textContent = '';
    document.getElementById('editParkingForm').reset();
    const p = currentParkings[idx];
    document.getElementById('editParkingId').value = p.id_parqueadero;
    document.getElementById('editAddress').value = p.direccion;
    document.getElementById('editDescription').value = p.descripcion || '';
    document.getElementById('editLong').value = p.largo;
    document.getElementById('editWidth').value = p.ancho;
    document.getElementById('editPrice').value = p.costo_dia;

    // Mostrar fotos actuales con checkbox para eliminar
    let fotos = [];
    try { fotos = JSON.parse(p.fotos); } catch (e) { fotos = []; }
    const container = document.getElementById('editPhotosContainer');
    container.innerHTML = '<strong>Fotos a eliminar:</strong><br>';
    fotos.forEach((foto, i) => {
        container.innerHTML += `
            <label>
                <input type="checkbox" class="edit-photo-checkbox" value="${foto}">
                <img src="../../Back/${foto}" alt="foto">
            </label>
        `;
    });

    document.getElementById('editParkingModal').style.display = 'flex';

    // Para cargar países en el modal de edición
    if (window.loadCountries) loadCountries();
}


// Cerrar modal
document.getElementById('closeEditModal').onclick = function() {
    document.getElementById('editParkingModal').style.display = 'none';
};

// Enviar cambios al backend
document.getElementById('editParkingForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const parkingId = document.getElementById('editParkingId').value;
    const ownerId = localStorage.getItem('userId');
    const address = document.getElementById('editAddress').value;
    const description = document.getElementById('editDescription').value;
    const long = document.getElementById('editLong').value;
    const width = document.getElementById('editWidth').value;
    const price = document.getElementById('editPrice').value;
    // Fotos a borrar
    const filesToDelete = Array.from(document.querySelectorAll('.edit-photo-checkbox:checked')).map(cb => cb.value);
    // Nuevas fotos
    const newFiles = document.getElementById('editNewPhotos').files;
    const msg = document.getElementById('editParkingMsg');
    msg.textContent = 'Procesando...';

    const formData = new FormData();
    formData.append('parkingId', parkingId);
    formData.append('ownerId', ownerId);
    formData.append('address', address);
    formData.append('description', description);
    formData.append('long', long);
    formData.append('width', width);
    formData.append('price', price);
    formData.append('fileToDelete', filesToDelete.join(','));
    for (let i = 0; i < newFiles.length; i++) {
        formData.append('newFiles', newFiles[i]);
    }
    
    try {
        const res = await fetch(API_ROUTES.UPDATE_PARKING, {
            method: 'PATCH',
            body: formData
        });
        const data = await res.json();
        if (res.ok && data.message && data.message.toLowerCase().includes("actualizado")) {
            msg.style.color = 'green';
            msg.textContent = '¡Parqueadero actualizado!';
            setTimeout(() => {
                document.getElementById('editParkingModal').style.display = 'none';
                loadOwnerParkings();
            }, 1200);
        } else {
            msg.style.color = '#d32f2f';
            msg.textContent = data.message || 'Error al actualizar parqueadero';
        }
    } catch (err) {
        msg.style.color = '#d32f2f';
        msg.textContent = 'Error de conexión con el servidor';
    }
});

// Manejar click en botón Eliminar
document.getElementById('ownerParkings').addEventListener('click', async function(e) {
    if (e.target.classList.contains('delete-parking-btn')) {
        const idx = e.target.getAttribute('data-idx');
        const p = currentParkings[idx];
        // Confirmación visual
        if (confirm('¿Estás seguro de que deseas eliminar este parqueadero? Esta acción no se puede deshacer.')) {
            const ownerId = localStorage.getItem('userId');
            try {
                const res = await fetch(API_ROUTES.DELETE_PARKING(ownerId, p.id_parqueadero), {
                    method: 'DELETE'
                });
                const data = await res.json();
                if (res.ok && data.message && data.message.toLowerCase().includes("eliminado")) {
                    alert('¡Parqueadero eliminado correctamente!');
                    loadOwnerParkings();
                } else {
                    alert(data.message || 'Error al eliminar parqueadero');
                }
            } catch (err) {
                alert('Error de conexión con el servidor');
            }
        }
    }
});

// Cargar reservas al abrir la pestaña de reservas
document.querySelector('[data-tab="reservations"]').addEventListener('click', loadOwnerReservations);


// Agregar parqueadero
document.getElementById('addParkingForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const ownerId = localStorage.getItem('userId');
    const address = document.getElementById('address').value;
    const long = document.getElementById('long').value;
    const width = document.getElementById('width').value;
    const price = document.getElementById('price').value;
    const photos = document.getElementById('photos').files;
    const description = document.getElementById('description').value;
    const msg = document.getElementById('addParkingMsg');
    msg.textContent = 'Procesando...';

    const formData = new FormData();
    formData.append('owner', ownerId);
    formData.append('address', address);
    formData.append('long', long);
    formData.append('width', width);
    formData.append('price', price);
    formData.append('description', description);
    const place = citySelect.value; // o usa el nombre si tu backend lo requiere
    formData.append('place', place);
    for (let i = 0; i < photos.length; i++) {
        formData.append('files', photos[i]);
    }

    try {
        const res = await fetch(API_ROUTES.CREATE_PARKING, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (res.ok && data.mensaje && data.mensaje.toLowerCase().includes("exitosa")) {
            msg.style.color = 'green';
            msg.textContent = '¡Parqueadero agregado!';
            window.location.reload();
        } else {
            msg.style.color = '#d32f2f';
            msg.textContent = data.mensaje || 'Error al agregar parqueadero';
        }
    } catch (err) {
        msg.style.color = '#d32f2f';
        msg.textContent = 'Error de conexión con el servidor';
    }
});

// descargar reservas del owner
document.getElementById('downloadReservationsCsv').addEventListener('click', downloadReservationsCsv);

//Registrar como cliente
document.getElementById('registrarComoClienteLink').addEventListener('click', async function(e) {
    e.preventDefault();

    const userId = localStorage.getItem('userId');
    const tipoUsuario = localStorage.getItem('userType'); // Ej: "customer,owner" o "owner,customer" o "owner"
    if (!userId) {
        alert('Debes iniciar sesión primero.');
        return;
    }

    // Si ya es customer y owner, muestra el modal directamente
    if (
        tipoUsuario === "customer,owner" ||
        tipoUsuario === "owner,customer"
    ) {
        showCustomerModal();
        return;
    }

    const formData = new FormData();
    formData.append('user_id', userId);

    // Si no es customer, llama al API para registrar como cliente
    try {
        console.log('Registrando como cliente...');
        const res = await fetch(API_ROUTES.REGISTER_CLIENT, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();

        if (res.ok && (data.status === "success" || data.mensaje?.toLowerCase().includes("cliente registrado"))) {
            // Actualiza el tipo de usuario en localStorage
            localStorage.setItem('userType', 'customer,owner');
            showCustomerModal();
        } else {
            alert(data.mensaje || 'No se pudo registrar como cliente.');
        }
    } catch (err) {
        alert('Error de conexión al registrar como cliente.');
    }
});

function showCustomerModal() {
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100vw';
    modal.style.height = '100vh';
    modal.style.background = 'rgba(0,0,0,0.5)';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.zIndex = '9999';

    modal.innerHTML = `
        <div style="background:#fff; padding:2em 2.5em; border-radius:10px; text-align:center; max-width:90vw;">
            <h2 style="color:#28a745;">¡Ahora eres cliente!</h2>
            <p>Ya puedes buscar y reservar parqueaderos como cliente.</p>
            <button id="closeCustomerModal" style="margin-top:1.5em; padding:0.7em 2em; background:#007bff; color:#fff; border:none; border-radius:5px; font-weight:bold; font-size:1rem; cursor:pointer;">
                Ir a buscar parqueaderos
            </button>
        </div>
    `;
    document.body.appendChild(modal);
    document.getElementById('closeCustomerModal').onclick = () => {
        modal.remove();
        window.location.href = "customer.html";
    };
}

