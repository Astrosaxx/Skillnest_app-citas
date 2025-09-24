from app.config.mysqlconnection import connectToMySQL
from flask import flash
from dotenv import load_dotenv
import os

load_dotenv()
db = os.getenv("MYSQL_DB")

class Favorito:
    @classmethod
    def obtener_favoritos_usuarios(cls, usuario_id):
        # Obtener todos los favoritos creados por el usuario.
        query = """
        SELECT favoritos * FROM favoritos WHERE usuario_id = %(usuario_id)s;
        """
        data = {'usuario_id': usuario_id}
        resultados = connectToMySQL(db).query_db(query, data)
        favoritos = []
        for row in resultados:
            favoritos.append(cls(row))
        return favoritos
    
def __init__(self, data):
    # Constructor: inicializa los atributos del favorito
    self.id = data['id']
    self.usuario_id = data['usuario_id']
    self.cita_id = data['cita_id']

@classmethod
def
    
