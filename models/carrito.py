import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import connectToMySQL

class Carrito:
    def __init__(self, data):
        self.id = data['id']
        self.usuario_id = data['usuario_id']
        self.producto_id = data['producto_id']
        self.cantidad = data['cantidad']
        self.fecha_agregado = data['fecha_agregado']

    @classmethod
    def get_by_user(cls, usuario_id):
        query = "SELECT * FROM carrito_items WHERE usuario_id = %s;"
        data = (usuario_id,)
        results = connectToMySQL('kiosco_saludable').query_db(query, data)
        if not results:
            return []
        carrito_items = []
        for item in results:
            carrito_items.append(cls(item))
        return carrito_items

    @classmethod
    def add_item(cls, usuario_id, producto_id, cantidad):
        query = "INSERT INTO carrito_items (usuario_id, producto_id, cantidad) VALUES (%s, %s, %s);"
        data = (usuario_id, producto_id, cantidad)
        result = connectToMySQL('kiosco_saludable').query_db(query, data)
        return result

    @classmethod
    def update_item(cls, id, cantidad):
        query = "UPDATE carrito_items SET cantidad = %s WHERE id = %s;"
        data = (cantidad, id)
        result = connectToMySQL('kiosco_saludable').query_db(query, data)
        return result

    @classmethod
    def delete_item(cls, id):
        query = "DELETE FROM carrito_items WHERE id = %s;"
        data = (id,)
        result = connectToMySQL('kiosco_saludable').query_db(query, data)
        return result

    @staticmethod
    def obtener_items(usuario_id):
        query = """
        SELECT productos.nombre, productos.precio, carrito_items.cantidad,
               (productos.precio * carrito_items.cantidad) AS total
        FROM carrito_items
        JOIN productos ON carrito_items.producto_id = productos.id
        WHERE carrito_items.usuario_id = %s;
        """
        return connectToMySQL('kiosco_saludable').query_db(query, (usuario_id,))

    @staticmethod
    def agregar_producto(usuario_id, producto_id):
        query = """
        SELECT * FROM carrito_items
        WHERE usuario_id = %s AND producto_id = %s;
        """
        carrito_item = connectToMySQL('kiosco_saludable').query_db(query, (usuario_id, producto_id))

        if carrito_item:
            query = """
            UPDATE carrito_items
            SET cantidad = cantidad + 1
            WHERE usuario_id = %s AND producto_id = %s;
            """
            connectToMySQL('kiosco_saludable').query_db(query, (usuario_id, producto_id))
        else:
            query = """
            INSERT INTO carrito_items (usuario_id, producto_id, cantidad)
            VALUES (%s, %s, 1);
            """
            connectToMySQL('kiosco_saludable').query_db(query, (usuario_id, producto_id))

    @staticmethod
    def vaciar_carrito(usuario_id):
        query = """
        DELETE FROM carrito_items
        WHERE usuario_id = %s;
        """
        connectToMySQL('kiosco_saludable').query_db(query, (usuario_id,))
