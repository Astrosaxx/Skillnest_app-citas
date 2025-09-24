from app.config.mysqlconnection import connectToMySQL
from flask import flash
from dotenv import load_dotenv
import os

load_dotenv()
db = os.getenv("MYSQL_DB")

class Cita:
    @classmethod
    def obtener_citas_usuarios(cls, usuario_id):
        # Obtener todas las citas creadas por el usuario.
        query = """
        SELECT citas * FROM citas WHERE usuario_id = %(usuario_id)s;
        """
        data = {'usuario_id': usuario_id}
        resultados = connectToMySQL(db).query_db(query, data)
        citas = []
        for row in resultados:
            citas.append(cls(row))
        return citas
    
# Clase que representa una cita y sus operaciones en la base de datos.


def __init__(self, data):
    # Constructor: inicializa los atributos de la cita
    self.id = data['id']
    self.cita = data['cita']
    self.autor_id = data['autor_id']
    self.usuario_id = data['usuario_id']
    self.creado_en = data['creado_en']
    self.actualizado_en = data['actualizado_en']

@classmethod
def guardar_cita(cls, data):
    # Guardar una nueva cita en la base de datos
    query = """
    INSERT INTO citas (cita, autor_id, usuario_id) 
    VALUES (%(cita)s, %(autor_id)s);
    """
    resultado = connectToMySQL(cls.db).query_db(query, data)
    return resultado

@classmethod
def obtener_por_id(cls, cita_id):
    # Buscar una cita por su ID
    query = "SELECT * FROM citas WHERE id = %(id)s;"
    data = {'id': cita_id}
    resultado = connectToMySQL(cls.db).query_db(query, data)
    if not resultado:
        return None
    return cls(resultado[0])  

@classmethod
def obtener_todas(cls):
    # Obtener todas las citas de la base de datos
    query = "SELECT * FROM citas;"
    resultados = connectToMySQL(cls.db).query_db(query)
    citas = []
    for row in resultados:
        citas.append(cls(row))
    return citas

@classmethod
def actualizar_cita(cls, data):
    # Actualizar una cita existente
    query = """
    UPDATE citas SET cita = %(cita)s, actualizado_en = NOW() 
    WHERE id = %(id)s;
    """
    resultado = connectToMySQL(cls.db).query_db(query, data)
    return resultado

@classmethod
def eliminar_cita(cls, cita_id):
    # Eliminar una cita por su ID
    query = "DELETE FROM citas WHERE id = %(id)s;"
    data = {'id': cita_id}
    resultado = connectToMySQL(cls.db).query_db(query, data)
    return resultado

@staticmethod
def validar_cita(cita):
    # Validar los datos de la cita
    is_valid = True
    if len(cita['cita']) < 5:
        flash("La cita debe tener al menos 5 caracteres.", "alert")
        is_valid = False
    return is_valid