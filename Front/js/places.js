const countrySelect = document.getElementById('countrySelect');
const stateSelect = document.getElementById('stateSelect');
const citySelect = document.getElementById('citySelect');

// Cargar países al iniciar
async function loadCountries() {
    const res = await fetch(API_ROUTES.COUNTRIES);
    const data = await res.json();
    countrySelect.innerHTML = '<option value="">Selecciona país</option>';
    data.forEach(pais => {
        countrySelect.innerHTML += `<option value="${pais.id_lugar}">${pais.nombre_lugar}</option>`;
    });
    countrySelect.disabled = false;
}
window.loadCountries = loadCountries; // Para poder llamarla desde otros archivos

// Al seleccionar país, cargar estados
countrySelect.addEventListener('change', async function() {
    stateSelect.innerHTML = '<option value="">Selecciona estado</option>';
    citySelect.innerHTML = '<option value="">Selecciona ciudad</option>';
    if (this.value) {
        const res = await fetch(API_ROUTES.STATES(this.value));
        const data = await res.json();
        data.forEach(estado => {
            stateSelect.innerHTML += `<option value="${estado.id_lugar}">${estado.nombre_lugar}</option>`;
        });
        stateSelect.disabled = false;
    } else {
        stateSelect.disabled = true;
    }
});

// Al seleccionar estado, cargar ciudades
stateSelect.addEventListener('change', async function() {
    citySelect.innerHTML = '<option value="">Selecciona ciudad</option>';
    if (this.value) {
        const res = await fetch(API_ROUTES.CITIES(this.value));
        const data = await res.json();
        data.forEach(ciudad => {
            citySelect.innerHTML += `<option value="${ciudad.id_lugar}">${ciudad.nombre_lugar}</option>`;
        });
        citySelect.disabled = false;
    } else {
        citySelect.disabled = true;
    }
});

// Inicializa países al cargar el archivo
if (countrySelect) loadCountries();