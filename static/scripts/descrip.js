// carrito.js
const DescripcionCarrito = {
    cambiarCantidad: function(productoId, cambio) {
        let cantidadElement = document.getElementById('cantidad-descripcion-' + productoId);
        let cantidad = parseInt(cantidadElement.textContent) + cambio;
        if (cantidad < 1) cantidad = 1;
        cantidadElement.textContent = cantidad;

        this.actualizarTotales(productoId, cantidad);
    },

    actualizarTotales: function(productoId, cantidad) {
        let precioUnitario = parseFloat(document.getElementById('precio-unitario-' + productoId).textContent);
        let psUnitario = parseInt(document.getElementById('ps-unitario-' + productoId).textContent);

        let totalPrecio = precioUnitario * cantidad;
        let totalPs = psUnitario * cantidad;

        document.getElementById('total-precio-descripcion-' + productoId).textContent = totalPrecio.toFixed(2);
        document.getElementById('total-ps-descripcion-' + productoId).textContent = totalPs;
    },

    agregarAlCarrito: function(productoId) {
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
                this.cerrarDescripcion(document.querySelector('.descripcion-overlay'));
                this.actualizarNumeroCarrito(data.total_items);
                this.actualizarTotalesCarrito(data.precio_final, data.total_ps);
            } else {
                alert('Error al agregar al carrito: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al agregar al carrito');
        });
    },

    actualizarNumeroCarrito: function(totalItems) {
        let numeroCarritos = document.querySelectorAll('#num-cant, #num-cantr, #num-cantrr');
        numeroCarritos.forEach(elemento => {
            if (elemento) {
                elemento.textContent = totalItems;
            }
        });
    },

    actualizarTotalesCarrito: function(precioFinal, totalPs) {
        let precioFinalElements = document.querySelectorAll('[id^="precio-final"]');
        let totalPsElements = document.querySelectorAll('[id^="total-ps"]');
        
        precioFinalElements.forEach(element => {
            element.textContent = '$' + precioFinal;
        });
        
        totalPsElements.forEach(element => {
            element.textContent = totalPs;
        });
    },

    cerrarDescripcion: function(overlay) {
        if (overlay) {
            overlay.classList.remove('active');
        }
    }
};