from base.config.mysqlconnection import connectToMySQL
from flask import flash
from dotenv import load_dotenv
import os

load_dotenv()
db = os.getenv("MYSQL_DB")

class Favorito:
    def __init__(self, data):
        # Constructor: inicializa los atributos del favorito
        self.id = data['id']
        self.usuario_id = data['usuario_id']
        self.cita_id = data['cita_id']

    @classmethod
    def obtener_favoritos_usuarios(cls, usuario_id):
        # Obtener todos los favoritos creados por el usuario.
        query = """
        SELECT * FROM favoritos WHERE usuario_id = %(usuario_id)s;
        """
        data = {'usuario_id': usuario_id}
        resultados = connectToMySQL(db).query_db(query, data)
        favoritos = []
        for row in resultados:
            favoritos.append(cls(row))
        return favoritos

    @classmethod
    def guardar_favorito(cls, data):
        # Guardar una cita como favorito en la base de datos
        query = """
        INSERT INTO favoritos (usuario_id, cita_id)
        VALUES (%(usuario_id)s, %(cita_id)s);
        """
        resultado = connectToMySQL(db).query_db(query, data)
        return resultado

    @classmethod
    def obtener_por_id(cls, data):
        # Buscar un favorito por usuario_id y cita_id
        query = "SELECT * FROM favoritos WHERE usuario_id = %(usuario_id)s AND cita_id = %(cita_id)s;"
        resultado = connectToMySQL(db).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])

    @classmethod
    def eliminar_favorito(cls, data):
        # Eliminar los favoritos de un usuario por el ID del favorito
        query = "DELETE FROM favoritos WHERE usuario_id = %(usuario_id)s AND cita_id = %(cita_id)s;"
        resultado = connectToMySQL(db).query_db(query, data)
        return resultado

    @classmethod
    def obtener_todos(cls):
        # Obtener todos los favoritos de la base de datos
        query = "SELECT * FROM favoritos;"
        resultados = connectToMySQL(db).query_db(query)
        favoritos = []
        for row in resultados:
            favoritos.append(cls(row))
        return favoritos

    @classmethod
    def obtener_no_favoritos_usuario(cls, usuario_id):
        # Obtener todas las citas que no son favoritas del usuario.
        query = """
        SELECT c.*, u.nombre, u.apellido, 
               CONCAT(u.nombre, ' ', u.apellido) as autor
        FROM citas c 
        JOIN usuarios u ON c.autor_id = u.id 
        WHERE c.id NOT IN (
            SELECT cita_id FROM favoritos WHERE usuario_id = %(usuario_id)s
        )
        ORDER BY c.creado_en DESC;
        """
        data = {'usuario_id': usuario_id}
        resultados = connectToMySQL(db).query_db(query, data)
        citas = []
        for row in resultados:
            citas.append(row)
        return citas



    
