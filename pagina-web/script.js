const dropdownMenu = document.getElementById("recipientes-dropdown");
let selectedRecipientId;
const url = "http://localhost:3000";
let ultimaCantidad;

const obtenerCantidades = async () => {
    const response = await fetch(`${url}/cantidades`);
    const cantidades = await response.json();
    return cantidades;
}

const obtenerRecipientes = async () => {
    const response = await fetch(`${url}/recipientes`);
    const recipientes = await response.json();
    return recipientes;
}

const mostrarRecipientes = async () => {
    const recipientes = await obtenerRecipientes();
    recipientes.forEach(recipiente => {
        const dropdownItem = document.createElement('a');
        dropdownItem.classList.add('dropdown-item');
        dropdownItem.href = '#';
        dropdownItem.textContent = recipiente.nombre_recipiente;
        dropdownItem.dataset.recipienteId = recipiente.recipiente_id;
        dropdownItem.addEventListener('click', async () => {
            const recipienteId = dropdownItem.dataset.recipienteId;
            selectedRecipientId = recipienteId;
            actualizarTabla(recipienteId);
        });

        dropdownMenu.appendChild(dropdownItem);
    });
    if (recipientes.length > 0) {
        selectedRecipientId = recipientes[0].recipiente_id;
        actualizarTabla(selectedRecipientId);
    }
}

const llenarTablaPorRecipienteId = (cantidades, recipienteId, recipientes) => {
    const tbody = document.querySelector(".table tbody");
    tbody.innerHTML = "";
    const recipiente = recipientes.find(recipiente => recipiente.recipiente_id === recipienteId);
    const longitud = recipiente ? recipiente.longitud : 1;
    cantidades.filter(cantidad => cantidad.recipiente_id === recipienteId).forEach(cantidad => {
        const row = document.createElement("tr");
        const porcentaje = calcularPorcentaje(Number(cantidad.cantidad), longitud);
        row.innerHTML = `
            <td class="text-start">${parseInt(porcentaje)}%</td>
            <td class="text-center">${formatoFecha(cantidad.fecha)}</td>
            <td class="text-end">${formatoHora(cantidad.fecha)}</td>
            <td class="text-end">${parseInt(Math.abs(ultimaCantidad - porcentaje))}%</td>`;
        tbody.appendChild(row);
        ultimaCantidad = calcularPorcentaje(Number(cantidad.cantidad), longitud);
    });
}

const actualizarTabla = async (recipienteId) => {
    const cantidades = await obtenerCantidades();
    const recipientes = await obtenerRecipientes();
    llenarTablaPorRecipienteId(cantidades, recipienteId, recipientes);
}

const calcularPorcentaje = (cantidad, longitud) => {
    const porcentaje = ((longitud - cantidad) / longitud) * 100;
    return porcentaje.toFixed(2);
}

const formatoFecha = (fechaString) => {
    const fecha = new Date(fechaString);
    const options = { timeZone: "UTC" };
    return fecha.toLocaleDateString(undefined, options);
}

const formatoHora = (horaString) => {
    const hora = new Date(horaString);
    const options = { timeZone: "UTC", hour: "2-digit", minute: "2-digit", second: "2-digit" };
    return hora.toLocaleTimeString(undefined, options);
}


function init() {
    mostrarRecipientes();
    setInterval(() => {
        if (selectedRecipientId) {
            actualizarTabla(selectedRecipientId);
        }
    }, 5000);
}

window.onload = init;
