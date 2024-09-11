import sys
import os
import uuid

from flask import request
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
    def insert_one(cls, nombre, ps, email, contraseña, codigo_qr, fto_perfil="default.png"):
        query = """
        INSERT INTO usuarios (nombre, ps, email, contraseña, codigo_qr, fto_perfil)
        VALUES (%(nombre)s, %(ps)s, %(email)s, %(contraseña)s, %(codigo_qr)s, %(fto_perfil)s);
        """

        data = ({"nombre": nombre, "ps": ps, "email": email, "contraseña": contraseña, "codigo_qr": codigo_qr, "fto_perfil": fto_perfil})
        result = connectToMySQL('kiosco_saludable').query_db(query, data)
        return result
    
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
    

    @classmethod
    def select_by_email(cls, email):
        query = f"SELECT * FROM usuarios WHERE email='{email}' "
        results = connectToMySQL("kiosco_saludable").query_db(query)
        usuarios = []
        for usuario in results:
            usuarios.append(cls(usuario))
        return usuarios
        
    @classmethod
    def get_user_by_name(cls, data):
        query = "SELECT * FROM usuarios WHERE nombre = %(nombre)s"
        results = connectToMySQL('kiosco_saludable').query_db(query, data)
        user = None
        if results:
            if len(results) > 0:
                user = cls(results[0])
        return user          
