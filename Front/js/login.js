document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const message = document.getElementById('loginMessage');
    message.textContent = 'Procesando...';

    try {
        const response = await fetch(API_ROUTES.LOGIN, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        if (response.ok && (data.mensaje === "login Correcto!" || data.success)) {
            message.style.color = 'green';
            message.textContent = data.tipo_usuario;
            localStorage.setItem('userId', data.id_usuario);
            localStorage.setItem('userName', data.nombre);
            localStorage.setItem('userLastName', data.apellido);
            localStorage.setItem('userPhoto', data.foto_perfil);
            localStorage.setItem('userType', data.tipo_usuario);
            localStorage.setItem('userEmail', email);
            console.log(data.tipo_usuario)
            if(data.tipo_usuario === "customer,owner" || data.tipo_usuario === "owner,customer"){
                document.getElementById('userTypeModal').style.display = 'flex';
                document.getElementById('selectCustomer').onclick = function() {
                    localStorage.setItem('selectedUserType', 'customer');
                    window.location.href = "customer.html";
                };
                document.getElementById('selectOwner').onclick = function() {
                    localStorage.setItem('selectedUserType', 'owner');
                    window.location.href = "owner.html";
                };
            }
            else if(data.tipo_usuario === "customer"){
                window.location.href = "customer.html";
            } else {
                window.location.href = "owner.html";
            }
        } else {
            message.style.color = '#d32f2f';
            message.textContent = data.mensaje || 'Error al iniciar sesión';
        }
    } catch (err) {
        message.style.color = '#d32f2f';
        message.textContent = 'Error de conexión con el servidor';
    }
});