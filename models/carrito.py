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
        query = "SELECT * FROM carrito_items WHERE usuario_id = %(usuario_id)s;"
        datas = {'usuario_id':usuario_id,}
        results = connectToMySQL('kiosco_saludable').query_db(query, datas)
        if not results:
            return []
        carrito_items = []
        for item in results:
            carrito_items.append(cls(item))
        return carrito_items

    @classmethod
    def add_item(cls, usuario_id, producto_id, cantidad):
        query = "INSERT INTO carrito_items (usuario_id, producto_id, cantidad) VALUES (%(usuario_id)s, %(producto_id)s, %(cantidad)s);"
        data = {'usuario_id':usuario_id, 'producto_id':producto_id, 'cantidad':cantidad}
        result = connectToMySQL('kiosco_saludable').query_db(query, data)
        return result

    @classmethod
    def update_item(cls, id, cantidad):
        query = "UPDATE carrito_items SET cantidad = %(cantidad)s WHERE id = %(id)s;"
        data = {'cantidad':cantidad, 'id':id}
        result = connectToMySQL('kiosco_saludable').query_db(query, data)
        return result

    @classmethod
    def delete_item(cls, id):
        query = "DELETE FROM carrito_items WHERE id = %(id)s;"
        data = {"id": id}
        result = connectToMySQL('kiosco_saludable').query_db(query, data)
        return result

    @staticmethod
    def obtener_items(usuario_id):
        query = """
        SELECT productos.nombre, productos.precio, carrito_items.cantidad,
               (productos.precio * carrito_items.cantidad) AS total,
               productos.id AS producto_id, productos.ruta_imagen
        FROM carrito_items
        JOIN productos ON carrito_items.producto_id = productos.id
        WHERE carrito_items.usuario_id = %(usuario_id)s;
        """
        results = connectToMySQL('kiosco_saludable').query_db(query, {"usuario_id": usuario_id})
        print("Resultado de la consulta SQL:", results)
        carrito_items = []
        total_cantidad = 0
        total_precio = 0
        for row in results:
            print("Fila:", row)
            item = {
                "nombre": row['nombre'],
                "precio": row['precio'],
                "cantidad": row['cantidad'],
                "total": row['total'],
                "producto_id": row['producto_id'],
                "imagen": row['ruta_imagen']  
            }
            carrito_items.append(item)
            total_cantidad += row['cantidad']
            total_precio += row['total']
        return {
            "carrito_items": carrito_items,
            "total_cantidad": total_cantidad,
            "total_precio": total_precio
        }

    @staticmethod
    def agregar_producto(usuario_id, producto_id):
        query = """
        SELECT * FROM carrito_items
        WHERE usuario_id = %(usuario_id)s AND producto_id = %(producto_id)s;
        """
        carrito_item = connectToMySQL('kiosco_saludable').query_db(query, {"usuario_id": usuario_id, "producto_id":producto_id})

        if carrito_item:
            query = """
            UPDATE carrito_items
            SET cantidad = cantidad + 1
            WHERE usuario_id = %(usuario_id)s AND producto_id = %(producto_id)s;
            """
            connectToMySQL('kiosco_saludable').query_db(query, {'usuario_id':usuario_id, 'producto_id':producto_id})
        else:
            query = """
            INSERT INTO carrito_items (usuario_id, producto_id, cantidad)
            VALUES (%(usuario_id)s, %(producto_id)s, 1);
            """
            connectToMySQL('kiosco_saludable').query_db(query, {'usuario_id':usuario_id, 'producto_id':producto_id})

    @staticmethod
    def vaciar_carrito(usuario_id):
        query = """
        DELETE FROM carrito_items
        WHERE usuario_id = %(usuario_id)s;
        """
        connectToMySQL('kiosco_saludable').query_db(query, {'usuario_id':usuario_id,})
