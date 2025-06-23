if (window.loadCountries) loadCountries();

// Mostrar parqueaderos aleatorios al cargar la página
window.addEventListener('DOMContentLoaded', loadRandomParkings);

async function loadRandomParkings() {
    const container = document.getElementById('customerParkings');
    container.innerHTML = 'Cargando parqueaderos destacados...';
    try {
        const res = await fetch(API_ROUTES.RANDOM_PARKINGS);
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
            container.innerHTML = '';
            data.forEach(p => {
                let fotos = [];
                try { fotos = JSON.parse(p.fotos); } catch (e) { fotos = []; }
                const primeraFoto = fotos && fotos.length > 0
                    ? `../../Back/${fotos[0]}`
                    : '../assets/images/parking1.jpeg';
                container.innerHTML += `
                    <div class="parking-item" data-id="${p.id_parqueadero}" style="cursor:pointer;">
                        <img src="${primeraFoto}" alt="Foto parqueadero">
                        <h3>${p.direccion}</h3>
                        <p><strong>Ciudad:</strong> ${p.nombre_lugar}</p>
                        <p><strong>Dimensiones:</strong> ${p.largo}m x ${p.ancho}m</p>
                        <p><strong>Precio/día:</strong> $${p.costo_dia}</p>
                    </div>
                `;
            });
            // Agregar listeners después de renderizar
            document.querySelectorAll('.parking-item').forEach(item => {
                item.addEventListener('click', function() {
                    const id = this.getAttribute('data-id');
                    window.location.href = `parking_detail.html?id=${id}`;
                });
            });
        } else {
            container.innerHTML = 'No hay parqueaderos destacados en este momento.';
        }
    } catch (err) {
        container.innerHTML = 'Error al cargar parqueaderos destacados.';
    }
}

// Buscar parqueaderos por ciudad seleccionada
document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const cityId = document.getElementById('citySelect').value;
    const container = document.getElementById('customerParkings');
    container.innerHTML = 'Buscando parqueaderos...';
    if (!cityId) {
        container.innerHTML = 'Por favor selecciona una ciudad.';
        return;
    }
    try {
        const res = await fetch(API_ROUTES.PARKINGS_BY_CITY(cityId));
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
            container.innerHTML = '';
            data.forEach(p => {
                let fotos = [];
                try { fotos = JSON.parse(p.fotos); } catch (e) { fotos = []; }
                const primeraFoto = fotos.length > 0
                    ? `../../Back/${fotos[0]}`
                    : '../assets/images/parking1.jpeg';
                container.innerHTML += `
                    <div class="parking-item" data-id="${p.id_parqueadero}" style="cursor:pointer;">
                        <img src="${primeraFoto}" alt="Foto parqueadero">
                        <h3>${p.direccion}</h3>
                        <p><strong>Dimensiones:</strong> ${p.largo}m x ${p.ancho}m</p>
                        <p><strong>Precio/día:</strong> $${p.costo_dia}</p>
                    </div>
                `;
            });
            // Agregar listeners después de renderizar
            document.querySelectorAll('.parking-item').forEach(item => {
                item.addEventListener('click', function() {
                    const id = this.getAttribute('data-id');
                    window.location.href = `parking_detail.html?id=${id}`;
                });
            });
        } else {
            container.innerHTML = 'No hay parqueaderos disponibles en esta ciudad.';
        }
    } catch (err) {
        container.innerHTML = 'Error al buscar parqueaderos.';
    }
});

document.getElementById('registrarComoOwnerLink').addEventListener('click', async function(e) {
    e.preventDefault();

    const userId = localStorage.getItem('userId');
    const tipoUsuario = localStorage.getItem('userType'); // Ej: "customer,owner" o "owner,customer" o "customer"
    if (!userId) {
        alert('Debes iniciar sesión primero.');
        return;
    }

    // Si ya es owner, muestra el modal directamente
    if (
        tipoUsuario === "customer,owner" ||
        tipoUsuario === "owner,customer"
    ) {
        showOwnerModal();
        return;
    }

    // Si no es owner, llama al API para registrar como dueño
    const formData = new FormData();
    formData.append('user_id', userId);

    try {
        const res = await fetch(API_ROUTES.REGISTER_OWNER, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();

        if (res.ok && (data.status === "success" || data.mensaje?.toLowerCase().includes("dueño registrado"))) {
            // Actualiza el tipo de usuario en localStorage
            localStorage.setItem('userType', 'customer,owner');
            showOwnerModal();
        } else {
            alert(data.mensaje || 'No se pudo registrar como dueño.');
        }
    } catch (err) {
        alert('Error de conexión al registrar como dueño.');
    }
});

function showOwnerModal() {
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
            <h2 style="color:#007bff;">¡Ahora eres dueño!</h2>
            <p>Ya puedes publicar y administrar tus parqueaderos.</p>
            <button id="closeOwnerModal" style="margin-top:1.5em; padding:0.7em 2em; background:#007bff; color:#fff; border:none; border-radius:5px; font-weight:bold; font-size:1rem; cursor:pointer;">
                Ir a mi panel de dueño
            </button>
        </div>
    `;
    document.body.appendChild(modal);
    document.getElementById('closeOwnerModal').onclick = () => {
        modal.remove();
        window.location.href = "owner.html";
    };
}
