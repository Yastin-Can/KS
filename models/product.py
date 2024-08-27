import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import connectToMySQL

class Producto:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.precio = data['precio']
        self.categoria_id = data['categoria_id']
        self.stock = data['stock']
        self.imagen = data['ruta_imagen']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM productos;"
        results = connectToMySQL('kiosco_saludable').query_db(query)
        if not results:
            return []
        productos = []
        for producto in results:
            productos.append(cls(producto))
        return productos

    @classmethod
    def get_by_category(cls, categoria_id):
        query = "SELECT * FROM productos WHERE categoria_id = %s;"
        data = (categoria_id,)
        results = connectToMySQL('kiosco_saludable').query_db(query, data)
        if not results:
            return []
        productos = []
        for producto in results:
            productos.append(cls(producto))
        return productos
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM productos WHERE id = %s"
        data = (id,)
        result = connectToMySQL('kiosco_saludable').query_db(query, data)
        if result:
            return cls(result[0])
        return None


class Categoria:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM categorias;"
        results = connectToMySQL('kiosco_saludable').query_db(query)
        if not results:
            return []
        categorias = []
        for categoria in results:
            categorias.append(cls(categoria))
        return categorias