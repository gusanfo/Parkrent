document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const nombre = document.getElementById('registerName').value;
    const apellido = document.getElementById('registerLastName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const tipo_usuario = document.getElementById('registerType').value;
    const message = document.getElementById('registerMessage');
    const userType = (tipo_usuario === 'customer') ? 1 : 2;
    message.textContent = 'Procesando...';

    try {
        const response = await fetch(API_ROUTES.REGISTER, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nombre,
                apellido,
                correo: email.toLowerCase(),
                contrasenia: password,
                tipo: userType
            })
        });
        const data = await response.json();
        if (response.ok && data.mensaje && (data.mensaje.toLowerCase().includes("exitosamente") || data.success)) {
            message.style.color = 'green';
            message.textContent = '¡Registro exitoso! Ahora puedes iniciar sesión.';
            setTimeout(() => {
                window.location.href = "login.html";
            }, 1500);
        } else {
            message.style.color = '#d32f2f';
            message.textContent = data.mensaje || 'Error al registrar usuario';
        }
    } catch (err) {
        message.style.color = '#d32f2f';
        message.textContent = 'Error de conexión con el servidor';
    }
});