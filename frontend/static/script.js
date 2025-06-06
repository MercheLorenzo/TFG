document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".toggle-btn");
    const containers = document.querySelectorAll(".options-container");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const targetId = button.getAttribute("data-target");

            // Ocultar todos los contenedores antes de mostrar el seleccionado
            containers.forEach(container => {
                container.style.display = "none";
            });

            // Mostrar el contenedor seleccionado
            const targetContainer = document.getElementById(targetId);
            if (targetContainer) {
                targetContainer.style.display = "flex";
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".option-btn");
    const responseContainer = document.getElementById("response-container");
    const responseContent = document.getElementById("response-content");

    buttons.forEach(button => {
        button.addEventListener("click", async () => {
            const url = button.getAttribute("data-url");
            if (!url) return;

            try {
                const response = await fetch(url);
                const data = await response.json();

                // Mostrar la respuesta en el div
                responseContent.textContent = JSON.stringify(data, null, 2);
                responseContainer.style.display = "block"; // Hacer visible el contenedor

            } catch (error) {
                responseContent.textContent = "Error al obtener la respuesta.";
                responseContainer.style.display = "block";
                console.error(error);
            }
        });
    });
    
    // Ocultar el contenedor al hacer clic fuera del recuadro
    document.addEventListener("click", (event) => {
        if (!responseContainer.contains(event.target)) {
            responseContainer.style.display = "none";
        }
    });

    // Evitar que se oculte cuando se hace clic dentro del contenedor
    responseContainer.addEventListener("click", (event) => {
        event.stopPropagation(); // Detener la propagación del evento de clic para que no se oculte
    });

    /*// Ocultar el contenedor al hacer clic en cualquier parte de la pantalla
    responseContainer.addEventListener("click", () => {
        responseContainer.style.display = "none";
    });*/
});

// Acción cuando se hace clic en el botón "Get Version"
document.getElementById("getVersionBtn").addEventListener("click", async () => {

    // El problema está en que lang se declara como const, pero luego intentas reasignarle "es" si el idioma ingresado no es válido. 
    // En JavaScript, no se puede reasignar un const, por lo que debes declararlo con let en lugar de const

    // Pedir al usuario que ingrese el idioma
    let lang = prompt("Ingresa el idioma (es, en, it, de, fr, ch):");

    // Validar el idioma ingresado
    const validLanguages = ["es", "en", "it", "de", "fr", "ch"];
    if (!validLanguages.includes(lang)) {
        alert("Idioma no válido. Se usará español por defecto.");
        lang = "es";
    }

    // Construir la URL con el idioma
    const url = `http://localhost:8000/mainRoutes/get-version?lang=${lang}`;
    
    try {
        // Realizar la solicitud GET
        const response = await fetch(url);
        const data = await response.json();

        // Mostrar la respuesta en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al obtener la respuesta.";
        responseContainer.style.display = "block";
        console.error(error);
    }
});

// Acción cuando se hace clic en el botón "Sumar 2 números"
document.getElementById("sumNumbersBtn").addEventListener("click", async () => {
    // Pedir al usuario que ingrese el primer número
    const num1 = prompt("Ingresa el primer número:");
    // Pedir al usuario que ingrese el segundo número
    const num2 = prompt("Ingresa el segundo número:");

    // Validar que los valores no estén vacíos y sean números
    if (!num1.trim() || !num2.trim() || isNaN(num1) || isNaN(num2)) {
        alert("Por favor, ingresa solo números y no dejes campos vacíos.");
        return;
    }

    // Construir la URL con los dos números
    const url = `http://localhost:8000/sampleRoutes/sum?num1=${num1}&num2=${num2}`;
    
    try {
        // Realizar la solicitud GET
        const response = await fetch(url);
        const data = await response.json();

        // Mostrar la respuesta en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al obtener la respuesta.";
        responseContainer.style.display = "block";
        console.error(error);
    }
});

// Acción cuando se hace clic en el botón "Generar string aleatorio"
document.getElementById("generateRandomStringBtn").addEventListener("click", async () => {
    // Pedir al usuario que ingrese la longitud de la cadena
    const length = prompt("Ingresa la longitud de la cadena aleatoria:");

    // Validar que el valor ingresado sea un número
    if (isNaN(length) || length <= 0) {
        alert("Por favor ingresa un número válido mayor que 0.");
        return;
    }

    // Construir la URL con la longitud proporcionada
    const url = `http://localhost:8000/sampleRoutes/generate-random-string?length=${length}`;

    try {
        // Realizar la solicitud GET
        const response = await fetch(url);
        const data = await response.json();

        // Mostrar la respuesta en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al obtener la respuesta.";
        responseContainer.style.display = "block";
        console.error(error);
    }
});

// Acción cuando se hace clic en el botón "Info caldera"
document.getElementById("infoCalderaBtn").addEventListener("click", async () => {
    // Pedir al usuario que ingrese el idioma
    const sala = prompt("Ingresa el nombre de la sala o caldera:");

    // Construir la URL con la sala
    const url = `http://localhost:8000/sampleRoutes/get-weather?room=${sala}`;

    try {
        // Realizar la solicitud GET
        const response = await fetch(url);
        const data = await response.json();

        // Mostrar la respuesta en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al obtener la respuesta.";
        responseContainer.style.display = "block";
        console.error(error);
    }
});

document.getElementById("generateTokenBtn").addEventListener("click", async () => {
    //const username = document.getElementById("usernameInput").value;

    const username = prompt("Ingresa el nombre:");

    // Validar que el campo no esté vacío
    if (!username) {
        alert("Por favor ingresa un nombre de usuario.");
        return;
    }

    // Construir la URL
    const url = 'http://localhost:8000/sampleRoutes/generate-token';

    // Realizar la solicitud POST con el username
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ username: username })
        });

        const data = await response.json();

        // Mostrar el token en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al obtener el token.";
        responseContainer.style.display = "block";
        console.error(error);
    }
});

document.getElementById("verifyTokenBtn").addEventListener("click", async () => {
    //const username = document.getElementById("usernameInput").value;

    const token = prompt("Ingresa el token:");

    // Validar que el campo no esté vacío
    if (!token) {
        alert("Por favor ingresa un token.");
        return;
    }

    // Construir la URL
    const url = 'http://localhost:8000/sampleRoutes/verify-token';

    // Realizar la solicitud POST con el token
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ token: token })
        });

        const data = await response.json();

        // Mostrar el token en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al obtener el token.";
        responseContainer.style.display = "block";
        console.error(error);
    }
});

document.getElementById("createUserBtn").addEventListener("click", async () => {
    // Solicitar los datos del usuario mediante prompts
    const email = prompt("Ingresa el email:");
    const first = prompt("Ingresa el nombre:");
    const last = prompt("Ingresa los apellidos:");

    // Validar que los campos no estén vacíos
    if (!email || !first || !last) {
        alert("Por favor no dejes ningún campo vacío.");
        return;
    }

    // Validar que el email tenga formato correcto (contenga "@")
    if (!email.includes("@")) {
        alert("El email no es válido. Asegúrate de que contiene '@'.");
        return;
    }

    // Construir la URL
    const url = 'http://localhost:8000/userRoutes/create-user';

    // Crear el objeto con los datos
    const userData = {
        email: email,
        firstName: first,
        lastName: last
    };

    // Verificar los datos antes de hacer la solicitud
    console.log("Datos enviados:", userData);

    // Realizar la solicitud POST con los datos
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(userData)  // Enviar los datos como JSON
        });

        // Verificar la respuesta del servidor
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }

        const data = await response.json();

        // Mostrar la respuesta en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al crear el usuario.";
        responseContainer.style.display = "block";
        console.error("Error en la solicitud:", error);
    }
});

document.getElementById("createWorkerBtn").addEventListener("click", async () => {
    // Solicitar los datos del trabajador mediante prompts
    const email = prompt("Ingresa el email:");
    const first = prompt("Ingresa el nombre:");
    const last = prompt("Ingresa los apellidos:");

    // Validar que los campos no estén vacíos
    if (!email || !first || !last) {
        alert("Por favor no dejes ningún campo vacío.");
        return;
    }

    // Validar que el email tenga formato correcto (contenga "@")
    if (!email.includes("@")) {
        alert("El email no es válido. Asegúrate de que contiene '@'.");
        return;
    }

    // Construir la URL
    const url = 'http://localhost:8000/workerRoutes/create-worker';

    // Crear el objeto con los datos
    const workerData = {
        email: email,
        firstName: first,
        lastName: last
    };

    // Verificar los datos antes de hacer la solicitud
    console.log("Datos enviados:", workerData);

    // Realizar la solicitud POST con los datos
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(workerData)  // Enviar los datos como JSON
        });

        // Verificar la respuesta del servidor
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }

        const data = await response.json();

        // Mostrar la respuesta en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al crear el usuario.";
        responseContainer.style.display = "block";
        console.error("Error en la solicitud:", error);
    }
});

document.getElementById("searchUserEmailBtn").addEventListener("click", async () => {
    
    const email = prompt("Ingresa el email del usuario a buscar:");

    if (!email) {
        alert("Por favor no dejes el campo vacío.");
        return;
    }

    // Validar que el email tenga formato correcto (contenga "@")
    if (!email.includes("@")) {
        alert("El email no es válido. Asegúrate de que contiene '@'.");
        return;
    }

    // Construir la URL con la sala
    const url = `http://localhost:8000/userRoutes/get-user-by-email?email=${email}`;

    try {
        // Realizar la solicitud GET
        const response = await fetch(url);
        const data = await response.json();

        // Mostrar la respuesta en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al obtener la respuesta.";
        responseContainer.style.display = "block";
        console.error(error);
    }
});

document.getElementById("searchWorkerEmailBtn").addEventListener("click", async () => {
    
    const email = prompt("Ingresa el email del trabajador a buscar:");

    if (!email) {
        alert("Por favor no dejes el campo vacío.");
        return;
    }

    // Validar que el email tenga formato correcto (contenga "@")
    if (!email.includes("@")) {
        alert("El email no es válido. Asegúrate de que contiene '@'.");
        return;
    }

    // Construir la URL con la sala
    const url = `http://localhost:8000/workerRoutes/get-worker-by-email?email=${email}`;

    try {
        // Realizar la solicitud GET
        const response = await fetch(url);
        const data = await response.json();

        // Mostrar la respuesta en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al obtener la respuesta.";
        responseContainer.style.display = "block";
        console.error(error);
    }
});

document.getElementById("searchUserBtn").addEventListener("click", async () => {
    
    const nombre = prompt("Ingresa nombre o apellido del usuario a buscar:");

    if (!nombre) {
        alert("Por favor no dejes el campo vacío.");
        return;
    }

    // Construir la URL
    const url = `http://localhost:8000/userRoutes/search-users?query=${nombre}`;

    try {
        // Realizar la solicitud GET
        const response = await fetch(url);
        const data = await response.json();

        // Mostrar la respuesta en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al obtener la respuesta.";
        responseContainer.style.display = "block";
        console.error(error);
    }
});

document.getElementById("searchWorkerBtn").addEventListener("click", async () => {
    
    const nombre = prompt("Ingresa nombre o apellido del usuario a buscar:");

    if (!nombre) {
        alert("Por favor no dejes el campo vacío.");
        return;
    }

    // Construir la URL
    const url = `http://localhost:8000/workerRoutes/search-workers?query=${nombre}`;

    try {
        // Realizar la solicitud GET
        const response = await fetch(url);
        const data = await response.json();

        // Mostrar la respuesta en el contenedor
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseContainer.style.display = "block"; // Hacer visible el contenedor

    } catch (error) {
        const responseContainer = document.getElementById("response-container");
        const responseContent = document.getElementById("response-content");
        responseContent.textContent = "Error al obtener la respuesta.";
        responseContainer.style.display = "block";
        console.error(error);
    }
});

// para redirigir en azure ai a sus paginas correspondientes PERO main users etc NO
document.querySelectorAll('.option-btn').forEach(button => {
    button.addEventListener('click', () => {
        const url = button.getAttribute('data-url');
        if (url) {
            if (button.classList.contains('redirect-btn')) {
                // SI es de Azure AI → REDIRIGIR a otra página
                window.location.href = url;
            } else {
                // SI es de otros (Main, Usuarios, etc) → HACER FETCH
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('response-content').textContent = JSON.stringify(data, null, 2);
                    })
                    .catch(error => {
                        console.error('Error al obtener la respuesta:', error);
                        document.getElementById('response-content').textContent = 'Error al obtener la respuesta.';
                    });
            }
        }
    });
});
