document.addEventListener('DOMContentLoaded', function() {
    // Recupera los datos del usuario desde localStorage
    const nombre = localStorage.getItem('userName') || '';
    const apellido = localStorage.getItem('userLastName') || '';
    const correo = localStorage.getItem('userEmail') || '';
    const telefono = localStorage.getItem('userCellphone') || '';
    const tipoUsuario = localStorage.getItem('userType') || '';
    const navCustomer = document.getElementById('navCustomer');
    const navOwner = document.getElementById('navOwner');

    // Asigna los valores a los campos del formulario
    document.getElementById('profileName').value = nombre;
    document.getElementById('profileLastName').value = apellido;
    document.getElementById('profileEmail').value = correo;
    document.getElementById('profileCellphone').value = telefono;

    // Oculta ambos por defecto
    if (navCustomer) navCustomer.style.display = "none";
    if (navOwner) navOwner.style.display = "none";

    // Muestra según el tipo de usuario
    if (tipoUsuario === "customer") {
        if (navCustomer) navCustomer.style.display = "inline-block";
    } else if (tipoUsuario === "owner") {
        if (navOwner) navOwner.style.display = "inline-block";
    } else if (
        tipoUsuario === "customer,owner" ||
        tipoUsuario === "owner,customer"
    ) {
        if (navCustomer) navCustomer.style.display = "inline-block";
        if (navOwner) navOwner.style.display = "inline-block";
    }

    const editCheck = document.getElementById('editProfileCheck');
    const editPasswordCheck = document.getElementById('editPasswordCheck');
    const passwordFieldsDiv = document.getElementById('passwordFields');
    const passwordInput = document.getElementById('profilePassword');
    const passwordConfirmInput = document.getElementById('profilePasswordConfirm');
    const saveBtn = document.getElementById('saveProfileBtn');
    const formFields = [
        document.getElementById('profileName'),
        document.getElementById('profileLastName'),
        document.getElementById('profileCellphone')
    ];

    // Inicialmente, los campos están deshabilitados
    saveBtn.disabled = true;
    formFields.forEach(f => f.disabled = true);
    editPasswordCheck.disabled = true;
    passwordInput.disabled = true;
    passwordConfirmInput.disabled = true;

    // Al marcar "Editar información"
    editCheck.addEventListener('change', function() {
        const enabled = editCheck.checked;
        formFields.forEach(f => f.disabled = !enabled);
        saveBtn.disabled = !enabled;
        editPasswordCheck.disabled = !enabled;
        if (!enabled) {
            editPasswordCheck.checked = false;
            passwordFieldsDiv.style.display = "none";
            passwordInput.disabled = true;
            passwordConfirmInput.disabled = true;
            passwordInput.value = "";
            passwordConfirmInput.value = "";
        }
    });

    // Al marcar "Modificar contraseña"
    editPasswordCheck.addEventListener('change', function() {
        const enabled = editPasswordCheck.checked && editCheck.checked;
        passwordFieldsDiv.style.display = enabled ? "block" : "none";
        passwordInput.disabled = !enabled;
        passwordConfirmInput.disabled = !enabled;
        if (!enabled) {
            passwordInput.value = "";
            passwordConfirmInput.value = "";
        }
    });

});

document.getElementById('profileForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    console.log("Enviando formulario de perfil");
    const editPasswordCheck = document.getElementById('editPasswordCheck');
    const passwordInput = document.getElementById('profilePassword');
    const passwordConfirmInput = document.getElementById('profilePasswordConfirm');
    const msg = document.getElementById('profileMsg');

    // Validación de contraseña
    if (editPasswordCheck.checked) {
        if (passwordInput.value !== passwordConfirmInput.value) {
            msg.textContent = "Las contraseñas no coinciden.";
            msg.style.color = "#d32f2f";
            return;
        }
    }

    const userId = localStorage.getItem('userId');
    const nombre = document.getElementById('profileName').value;
    const apellido = document.getElementById('profileLastName').value;
    const password = editPasswordCheck.checked ? passwordInput.value : ""; // Solo envía si se va a cambiar
    const cellphone = document.getElementById('profileCellphone').value;

    msg.textContent = 'Guardando...';

    // Usa FormData en vez de JSON
    const formData = new FormData();
    formData.append('userId', userId);
    formData.append('userName', nombre);
    formData.append('lastName', apellido);
    formData.append('password', password);
    formData.append('cellphone', cellphone);
    console.log(formData)

    try {
        console.log(userId, nombre, apellido, password, cellphone);
        const res = await fetch(API_ROUTES.UPDATE_USER_INFO, {
            method: 'PATCH',
            body: formData
        });
        const data = await res.json();
        if (res.ok && (data.status === "success" || data.message?.toLowerCase().includes("actualizado"))) {

            localStorage.setItem('userName', nombre);
            localStorage.setItem('userLastName', apellido);
            localStorage.setItem('userCellphone', cellphone);
            msg.style.color = 'green';
            msg.textContent = '¡Datos actualizados!';
        } else {
            msg.style.color = '#d32f2f';
            msg.textContent = data.message || 'Error al actualizar datos';
        }
    } catch (err) {
        console.error(err)
        msg.style.color = '#d32f2f';
        msg.textContent = 'Error de conexión con el servidor';
    }
});