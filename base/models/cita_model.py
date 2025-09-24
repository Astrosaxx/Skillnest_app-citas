from base.config.mysqlconnection import connectToMySQL
from flask import flash
from dotenv import load_dotenv
import os

load_dotenv()
db = os.getenv("MYSQL_DB")

class Cita:
    def __init__(self, data):
        self.id = data['id']
        self.cita = data['cita']
        self.autor_id = data['autor_id']
        self.creado_en = data['creado_en']
        self.actualizado_en = data['actualizado_en']
        # Agregar autor si está disponible en los datos
        if 'autor' in data:
            self.autor = data['autor']

    @classmethod
    def obtener_citas_usuarios(cls, usuario_id):
        # Obtener todas las citas creadas por el usuario.
        query = """
        SELECT c.*, u.nombre, u.apellido, 
               CONCAT(u.nombre, ' ', u.apellido) as autor
        FROM citas c 
        JOIN usuarios u ON c.autor_id = u.id 
        WHERE c.autor_id = %(usuario_id)s
        ORDER BY c.creado_en DESC;
        """
        data = {'usuario_id': usuario_id}
        resultados = connectToMySQL(db).query_db(query, data)
        citas = []
        if resultados and isinstance(resultados, list):
            for row in resultados:
                cita = cls(row)
                cita.autor = row['autor']
                citas.append(cita)
        return citas

    @classmethod
    def obtener_por_usuario(cls, usuario_id):
        # Alias para mantener compatibilidad
        return cls.obtener_citas_usuarios(usuario_id)

    @classmethod
    def guardar_cita(cls, data):
        query = """
        INSERT INTO citas (cita, autor_id) 
        VALUES (%(cita)s, %(usuario_id)s);
        """
        resultado = connectToMySQL(db).query_db(query, data)
        return resultado

    @classmethod
    def obtener_por_id(cls, cita_id):
        query = "SELECT * FROM citas WHERE id = %(id)s;"
        data = {'id': cita_id}
        resultado = connectToMySQL(db).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])  

    @classmethod
    def obtener_todas(cls):
        query = """
        SELECT c.*, u.nombre, u.apellido, 
               CONCAT(u.nombre, ' ', u.apellido) as autor
        FROM citas c 
        JOIN usuarios u ON c.autor_id = u.id 
        ORDER BY c.creado_en DESC;
        """
        resultados = connectToMySQL(db).query_db(query)
        citas = []
        if resultados and isinstance(resultados, list):
            for row in resultados:
                cita = cls(row)
                cita.autor = row['autor']
                citas.append(cita)
        return citas

    @classmethod
    def actualizar_cita(cls, data):
        query = """
        UPDATE citas SET cita = %(cita)s, actualizado_en = NOW() 
        WHERE id = %(id)s;
        """
        resultado = connectToMySQL(db).query_db(query, data)
        return resultado

    @classmethod
    def borrar_cita(cls, cita_id):
        query = "DELETE FROM citas WHERE id = %(id)s;"
        data = {'id': cita_id}
        resultado = connectToMySQL(db).query_db(query, data)
        return resultado

    @staticmethod
    def validar_cita(cita):
        is_valid = True
        if len(cita['cita']) < 5:
            flash("La cita debe tener al menos 5 caracteres.", "alert")
            is_valid = False
        return is_valid