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
    const cityId = document.getElementById('citySelectCustomer').value;
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