import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import connectToMySQL

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.ps = data['ps']
        self.email = data['email']
        self.contr = data['contraseña']
        self.qr = data['codigo_qr']
        self.fto_perfil = data['fto_perfil']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL('kiosco_saludable').query_db(query)
        if results is False:
            return False
        usuarios = []
        for usuario in results:
            usuarios.append(cls(usuario))
        return usuarios
