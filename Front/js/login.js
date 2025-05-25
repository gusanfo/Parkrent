document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const message = document.getElementById('loginMessage');
    message.textContent = 'Procesando...';

    try {
        const response = await fetch('http://127.0.0.1:8000/login.php/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        if (response.ok && (data.mensaje === "login Correcto!" || data.success)) {
            message.style.color = 'green';
            //message.textContent = '¡Bienvenido!';
            message.textContent = data.tipo_usuario;
            localStorage.setItem('userId', data.id_usuario);
            localStorage.setItem('userName', data.nombre);
            localStorage.setItem('userLastName', data.apellido);
            localStorage.setItem('userPhoto', data.foto_perfil);
            localStorage.setItem('userType', data.tipo_usuario);
            localStorage.setItem('userEmail', email);
            if(data.tipo_usuario === "customer"){
                window.location.href = "customer.html";
            } else {
                window.location.href = "owner.html";
            }
            // Aquí puedes guardar el token o userId si tu backend lo retorna
            // localStorage.setItem('token', data.token);
            // window.location.href = "index.html";
        } else {
            message.style.color = '#d32f2f';
            message.textContent = data.mensaje || 'Error al iniciar sesión';
        }
    } catch (err) {
        message.style.color = '#d32f2f';
        message.textContent = 'Error de conexión con el servidor';
    }
});