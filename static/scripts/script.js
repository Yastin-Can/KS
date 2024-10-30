let menuVisible = false;

function mostrar() {
    const mobileMenu = document.getElementById('mobile-menu');
    const menuMobile = document.getElementById('menu-mobile');

    if (!menuVisible) {
        mobileMenu.style.display = 'flex';
        menuMobile.classList.add('show-mobile-menu');
        menuVisible = true;
    } else {
        mobileMenu.style.display = 'none';
        menuMobile.classList.remove('show-mobile-menu');
        menuVisible = false;
    }
}
// Función para alternar la visibilidad del menú
document.addEventListener('DOMContentLoaded', function() {
    const perfilButton = document.getElementById('btn-perfil');
    const carritoButton = document.getElementById('btn-carrito');
    
    const perfilButtonInside = document.getElementById('btn-perfill');
    const carritoButtonInside = document.getElementById('btn-carritor');
    
    const perfilButtonInsideR = document.getElementById('btn-perfillr');
    const carritoButtonInsideR = document.getElementById('btn-carritorr');
    
    const menuPerfil = document.getElementById('menu-containerr');
    const menuCarrito = document.getElementById('menu-containerrr');

    function toggleMenuPerfil() {
        menuPerfil.classList.toggle('open');
        if (menuCarrito.classList.contains('open')) {
            menuCarrito.classList.remove('open');
        }
    }

    function toggleMenuCarrito() {
        menuCarrito.classList.toggle('open');
        if (menuPerfil.classList.contains('open')) {
            menuPerfil.classList.remove('open');
        }
    }

    perfilButton.addEventListener('click', toggleMenuPerfil);
    carritoButton.addEventListener('click', toggleMenuCarrito);

    perfilButtonInside.addEventListener('click', toggleMenuPerfil);
    carritoButtonInside.addEventListener('click', toggleMenuCarrito);
    
    perfilButtonInsideR.addEventListener('click', toggleMenuPerfil);
    carritoButtonInsideR.addEventListener('click', toggleMenuCarrito);

    window.addEventListener('click', function(e) {
        if (!menuPerfil.contains(e.target) && !perfilButton.contains(e.target) && !perfilButtonInside.contains(e.target) && !perfilButtonInsideR.contains(e.target)) {
            menuPerfil.classList.remove('open');
        }
        if (!menuCarrito.contains(e.target) && !carritoButton.contains(e.target) && !carritoButtonInside.contains(e.target) && !carritoButtonInsideR.contains(e.target)) {
            menuCarrito.classList.remove('open');
        }
    });
});

// Añadir un evento para manejar el cambio de tamaño de la ventana
window.addEventListener('resize', function () {
    const mobileMenu = document.getElementById('mobile-menu');
    const menuMobile = document.getElementById('menu-mobile');

    if (window.innerWidth > 768) {
        mobileMenu.style.display = 'none';
        menuMobile.classList.remove('show-mobile-menu');
        menuVisible = false;
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('.navbar-center a');

    function activateLink(activeId) {
        navLinks.forEach(link => link.classList.remove('active'));
        const activeLink = document.getElementById(activeId);
        activeLink.classList.add('active');
        sessionStorage.setItem('activeLink', activeId);
    }

    const savedActiveLink = sessionStorage.getItem('activeLink');
    if (savedActiveLink) {
        document.getElementById(savedActiveLink)?.classList.add('active');
    }

    window.activateLink = activateLink;
});

document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('.navbar-center a');
    const currentUrl = window.location.href;

    function activateLink() {
        navLinks.forEach(link => {
            if (link.href === currentUrl) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    activateLink();

    window.activateLink = activateLink;
});

const signUpButton = document.getElementById('singUp');
const signInButton = document.getElementById('singIn');
const main = document.getElementById('main');

signUpButton.addEventListener('click', () => {
    main.classList.add('right-panel-active');
});

signInButton.addEventListener('click', () => {
    main.classList.remove('right-panel-active');
});

function toggleFAQ(button) {
    const faq = button.nextElementSibling;
    const icon = button.querySelector('.d-arrow');

    faq.classList.toggle('show');
    icon.classList.toggle('rotate');
}

let date=document.getElementById("date");

let cur_date=new Date();
let day=cur_date.getDate();
let year=cur_date.getFullYear();
let month=cur_date.getMonth();

console.log(day, month+1, year)
if (month+1<10){
    month="0"+month.toString();
}
let minDate=year+'-'+(month+1)+'-'+day
let maxDate=year+'-'+(month+1)+'-'+(day+3)

date.setAttribute("min",minDate)
date.setAttribute("max",maxDate)

function validate(){
    let name=document.getElementById("name").value;
    let email=document.getElementById("email");
    let phone=document.getElementById("phone");
    let date=document.getElementById("date");
    let time=document.getElementById("time").value;  

    if (name.length <3){
        error_message.innerHTML="El nombre ingresado no es valido"
        return;
    }

    if (email.value.indexOf("@")==-1 || email.value.length<7){
        error_message.innerHTML="El email ingresado no es valido"
        return;
    }

    if (phone.value.length!==7){
        error_message.innerHTML="El numero ingresado no es valido"
        return;
    }
    console.log("Name: "+name,"Email: "+email.value,"Phone: "+phone.value, "Date: "+date.value, "Time: "+time);
    error_message.style.background="green"
    error_message.style.color="white"
    error_message.innerHTML="You will get a callback soon!"
    alert("Tu comentario se a enviado con exito!")
}

//CATEGORIAS

function mostrarCategoria(categoriaId) {
    // Obtener todas las divisiones de productos y ocultarlas
    var productosDivs = document.querySelectorAll('.Productos');
    productosDivs.forEach(div => {
        div.style.display = 'none';
    });

    // Mostrar solo la categoría seleccionada
    var categoriaSeleccionada = document.getElementById('categoria-' + categoriaId);
    if (categoriaSeleccionada) {
        categoriaSeleccionada.style.display = 'block';
    }
}

/////////////////////////////
//MOSTRAR/OCULTAR DECRIPCION
/////////////////////////////
function mostrarDescripcion(button) {
    const productoElement = button.closest('li');
    const descripcionOverlay = productoElement.querySelector('.descripcion-overlay');
    
    descripcionOverlay.classList.add('active');
    
    descripcionOverlay.addEventListener('click', function(event) {
        if (event.target === descripcionOverlay) {
            cerrarDescripcion(descripcionOverlay);
        }
    });
}

function cerrarDescripcion(descripcionOverlay) {
    // Oculta el overlay
    descripcionOverlay.classList.remove('active');
}
function disminuirCantidad(btn, productoId) {
    let cantidadElemento = document.getElementById('cantidad-' + productoId);
    let cantidad = parseInt(cantidadElemento.textContent);
    if (cantidad > 1) {
        cantidad -= 1;
        actualizarCarrito(productoId, cantidad);
    }
}

function aumentarCantidad(btn, productoId) {
    let cantidadElemento = document.getElementById('cantidad-' + productoId);
    let cantidad = parseInt(cantidadElemento.textContent);
    cantidad += 1;
    actualizarCarrito(productoId, cantidad);
}

function actualizarCarrito(productoId, cantidad) {
    fetch('/carrito/actualizar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            producto_id: productoId,
            cantidad: cantidad
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Datos recibidos del servidor:', data);  
        if (data.success) {
            actualizarInterfazCarrito(data.carrito);
        }
    })
    .catch(error => console.error('Error:', error));
}

function actualizarInterfazCarrito(carrito) {
    carrito.items.forEach(item => {
        let cantidadElement = document.getElementById('cantidad-' + item.producto_id);
        let precioElement = document.getElementById('precio-' + item.producto_id);
        let puntosElement = document.getElementById('puntos-' + item.producto_id);
        
        if (cantidadElement) cantidadElement.textContent = item.cantidad;
        if (precioElement) precioElement.textContent = '$' + item.precio_total;
        if (puntosElement) puntosElement.textContent = item.puntos;
    });

    let precioFinalElement = document.getElementById('precio-final');
    let totalPsElement = document.getElementById('total-ps');
    
    if (precioFinalElement) precioFinalElement.textContent = '$' + carrito.total_precio;
    if (totalPsElement) totalPsElement.textContent = carrito.total_ps;
}

function cambiarCantidadDescripcion(productoId, cambio) {
    let cantidadElement = document.getElementById('cantidad-descripcion-' + productoId);
    let cantidad = parseInt(cantidadElement.textContent) + cambio;
    if (cantidad < 1) cantidad = 1;
    cantidadElement.textContent = cantidad;

    actualizarTotalesDescripcion(productoId, cantidad);
}

function actualizarTotalesDescripcion(productoId, cantidad) {
    let precioUnitario = parseFloat(document.getElementById('precio-unitario-' + productoId).textContent);
    let psUnitario = parseInt(document.getElementById('ps-unitario-' + productoId).textContent);

    let totalPrecio = precioUnitario * cantidad;
    let totalPs = psUnitario * cantidad;

    document.getElementById('total-precio-descripcion-' + productoId).textContent = totalPrecio.toFixed(2);
    document.getElementById('total-ps-descripcion-' + productoId).textContent = totalPs;
}

function agregarAlCarritoDesdeDescripcion(productoId) {
    let cantidad = parseInt(document.getElementById('cantidad-descripcion-' + productoId).textContent);
    
    fetch('/carrito/agregar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            producto_id: productoId,
            cantidad: cantidad
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Producto agregado al carrito');
            cerrarDescripcion(document.getElementById('descripcion-producto'));
            // Actualizar el número en el icono del carrito si es necesario
            actualizarNumeroCarrito(data.total_items);
        } else {
            alert('Error al agregar al carrito: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al agregar al carrito');
    });
}

function actualizarNumeroCarrito(totalItems) {
    let numeroCarrito = document.getElementById('num-cant');
    if (numeroCarrito) {
        numeroCarrito.textContent = totalItems;
    }
}

function eliminarProducto(productoId) {
    fetch('/carrito/eliminar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            producto_id: productoId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Eliminar el elemento del carrito de la interfaz
            const elementoCarrito = document.querySelector(`.carContent[data-producto-id="${productoId}"]`);
            if (elementoCarrito) {
                elementoCarrito.remove();
            }

            // Actualizar totales
            document.getElementById('precio-final').textContent = data.precio_final;
            document.getElementById('total-ps').textContent = data.total_ps;

            // Actualizar contador del carrito
            const numCantElements = document.querySelectorAll('#num-cant, #num-cantr, #num-cantrr');
            numCantElements.forEach(el => {
                el.textContent = data.total_items;
            });

            // Si el carrito está vacío, mostrar un mensaje
            if (data.total_items === 0) {
                const carritoContainer = document.querySelector('.carrito-container');
                carritoContainer.innerHTML = '<p>El carrito está vacío</p>';
            }
        } else {
            alert('Error al eliminar el producto');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al eliminar el producto');
    });
}