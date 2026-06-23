const API_URL = "http://127.0.0.1:8000/articulos/";

obtenerArticulos();
mostrarFavoritos();

async function obtenerArticulos() {

    try {

        const respuesta = await fetch(API_URL);
        const datos = await respuesta.json();

        const lista = document.getElementById("lista-articulos");
        lista.innerHTML = "";

        const favoritos = obtenerFavoritos();

        datos.forEach(articulo => {

            const card = document.createElement("div");

            card.className = "border p-3 rounded mb-3";

            const esFavorito = favoritos.includes(articulo.id);

            card.innerHTML = `
                <h3><b>${articulo.nombre}</b></h3>

                <p><b>ID:</b> ${articulo.id}</p>

                <p><b>Precio:</b> $${articulo.precio}</p>

                <p><b>Receta:</b> ${articulo.receta ? "Si" : "No"}</p>

                <p><b>Activo:</b> ${articulo.activo ? "Si" : "No"}</p>

                <button class="mt-2 bg-orange-500 text-white px-3 py-1">
                    ${esFavorito ? "Quitar favorito" : "Agregar favorito"}
                </button>
            `;

            const boton = card.querySelector("button");

            boton.addEventListener("click", () => {
                toggleFavorito(articulo.id);
            });

            lista.appendChild(card);

        });

    } catch (error) {
    console.error("Error al obtener los artículos:", error);
    }
}

async function crearArticulo(articulo) {
    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(articulo)
    });

    obtenerArticulos();
    mostrarFavoritos();
}

document.getElementById("form-crear").addEventListener("submit", (e) => {

    e.preventDefault();

    const articulo = {
        id: parseInt(document.getElementById("id").value),
        nombre: document.getElementById("nombre").value,
        precio: parseFloat(document.getElementById("precio").value),
        receta: document.getElementById("receta").checked,
        activo: document.getElementById("activo").checked
    };

    crearArticulo(articulo);

    e.target.reset();

});

async function buscarPorId() {

    const id = document.getElementById("buscar-id").value;

    if (!id) {
        alert("Ingrese un ID válido.");
        return;
    }

    const respuesta = await fetch(API_URL + id);

    if (!respuesta.ok) {
        alert("No existe ese medicamento.");
        return;
    }

    const articulo = await respuesta.json();

    document.getElementById("edit-id").value = articulo.id;
    document.getElementById("edit-nombre").value = articulo.nombre;
    document.getElementById("edit-precio").value = articulo.precio;
    document.getElementById("edit-receta").checked = articulo.receta;
    document.getElementById("edit-activo").checked = articulo.activo;

}

async function editarArticulo(id, articulo) {
    await fetch(API_URL + id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(articulo)
    });

    obtenerArticulos();
    mostrarFavoritos();
}

document.getElementById("form-editar").addEventListener("submit", (e) => {

    e.preventDefault();

    const id = document.getElementById("edit-id").value;

    const articulo = {
        nombre: document.getElementById("edit-nombre").value,
        precio: parseFloat(document.getElementById("edit-precio").value),
        receta: document.getElementById("edit-receta").checked,
        activo: document.getElementById("edit-activo").checked
    };

    editarArticulo(id, articulo);

});

async function borrarArticulo() {

    const id = document.getElementById("buscar-id").value;

    if (!id) {
        alert("Ingrese un ID válido.");
        return;
    }

    if (!confirm("¿Está seguro de que desea borrar este medicamento?")) {
        return;
    }

    await fetch(API_URL + id, {
        method: "DELETE"
    });

    obtenerArticulos();
    mostrarFavoritos();
}

function obtenerFavoritos() {
    return JSON.parse(localStorage.getItem("favoritos")) || [];
}

function guardarFavoritos(favoritos) {
    localStorage.setItem("favoritos", JSON.stringify(favoritos));
}

function toggleFavorito(id){

    let favoritos = obtenerFavoritos();

    if(favoritos.includes(id)){
        favoritos = favoritos.filter(f => f != id);
    }else{
        favoritos.push(id);
    }

    guardarFavoritos(favoritos);

    obtenerArticulos();
    mostrarFavoritos();
}

async function mostrarFavoritos() {

    const favoritos = obtenerFavoritos();

    const respuesta = await fetch(API_URL);
    const articulos = await respuesta.json();

    const div = document.getElementById("favoritos");
    div.innerHTML = "";

    articulos.forEach(articulo => {

        if (favoritos.includes(articulo.id)) {

            const p = document.createElement("p");

            p.textContent = `ID: ${articulo.id} - ${articulo.nombre} - $${articulo.precio}`;

            div.appendChild(p);

        }

    });

}