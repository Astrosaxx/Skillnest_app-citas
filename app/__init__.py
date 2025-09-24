from flask import Flask, render_template
from datetime import datetime
from dotenv import load_dotenv
import os
from app.controllers import usuarios, citas

load_dotenv()

# Importar controllers

# Formatear fechas
def format_date(date, format='%Y-%m-%d'):
    """Formatea una fecha a un formato específico"""
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime(format)

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        FLASK_ENV=os.getenv('FLASK_ENV'),
    )
    
    # Registrar blueprints
    app.register_blueprint(usuarios.bp)
    app.register_blueprint(citas.bp)
    
    # Registrar filtro fecha
    app.add_template_filter(format_date)
    
    @app.route('/')
    def index():
        return render_template('auth.html')
    