from flask import Flask, render_template
from base.controllers import citas, usuarios, favoritos
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    
    # Registrar blueprints
    app.register_blueprint(citas.bp)
    app.register_blueprint(usuarios.bp)
    app.register_blueprint(favoritos.bp)
    
    # Filtro personalizado para formatear fechas
    @app.template_filter('format_date')
    def format_date(date_str):
        if isinstance(date_str, str):
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    return date_str
        else:
            date_obj = date_str
            
        return date_obj.strftime('%d/%m/%Y')
    
    @app.route('/')
    def index():
        return render_template('auth.html')
        
    return app