const API_BASE = "http://127.0.0.1:8000";

const API_ROUTES = {
    LOGIN: `${API_BASE}/login.php/`,
    REGISTER: `${API_BASE}/crearusuario/`,
    COUNTRIES: `${API_BASE}/countries.php/`,
    STATES: (paisId) => `${API_BASE}/states.php/?Pais=${paisId}`,
    CITIES: (estadoId) => `${API_BASE}/cities.php/?Estado=${estadoId}`,
    PARKINGS_BY_OWNER: (ownerId) => `${API_BASE}/get_parkings_by_owner.php/?owner=${ownerId}`,
    CREATE_PARKING: `${API_BASE}/create_parking.php/`,
    UPDATE_PARKING: `${API_BASE}/UPDATE_parking.php/`,
    DELETE_PARKING: (ownerId, parkingId) => `${API_BASE}/delete_parking.php/${ownerId}/${parkingId}`,
    RESERVATIONS_BY_OWNER: (ownerId) => `${API_BASE}/get_reservations_by_owner.php/${ownerId}`,
    RESERVATIONS_BY_CUSTOMER: (customerId) => `${API_BASE}/get_reservations_by_customer.php/${customerId}`,
    DELETE_RESERVATION: (reservationId) => `${API_BASE}/delete_reservation.php/${reservationId}`,
    RANDOM_PARKINGS: `${API_BASE}/get_random_parkings.php/`,
    GET_PARKING: (id) => `${API_BASE}/get_parking.php/?parqueadero=${id}`,
    CREATE_RESERVATION: `${API_BASE}/new_reservation.php/`,
    GET_OWNER_INFO_BY_PARKING: (parkingId) => `${API_BASE}/get_owner_info_by_parking.php/${parkingId}/`,
    PARKINGS_BY_CITY: (cityId) => `${API_BASE}/get_parkings_by_city.php/${cityId}`,
    REGISTER_CLIENT: `${API_BASE}/register_client.php/`,
    REGISTER_OWNER: `${API_BASE}/register_owner.php/`,
    UPDATE_USER_INFO: `${API_BASE}/update_user_info.php/`
};