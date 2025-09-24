from base.models.cita_model import Cita
from base.models.usuario_model import Usuario
from base.models.favorito_model import Favorito
from flask import render_template, redirect, request, session, Blueprint, flash

bp = Blueprint('favoritos', __name__, url_prefix='/favoritos')

def verificar_sesion():
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", 'error')
        return redirect('/')
    return True

@bp.route('/agregar/<int:cita_id>', methods=['POST'])
def agregar_favorito(cita_id):
    verificar_sesion()

    data = {
        'usuario_id': session['usuario_id'],
        'cita_id': cita_id
    }

    favorito_existente = Favorito.obtener_por_id(data)
    if favorito_existente:
        flash("Esta cita ya está en tus favoritos.", 'error')
        return redirect('/citas')

    Favorito.guardar_favorito(data)
    flash("¡Cita agregada a favoritos exitosamente!", 'exito')
    return redirect('/citas')

@bp.route('/borrar/<int:cita_id>', methods=['POST'])
def borrar_favorito(cita_id):
    verificar_sesion()

    data = {
        'usuario_id': session['usuario_id'],
        'cita_id': cita_id
    }

    favorito_existente = Favorito.obtener_por_id(data)
    if not favorito_existente:
        flash("Este favorito no existe.", 'error')
        return redirect('/citas')

    Favorito.eliminar_favorito(data)
    flash("¡Favorito eliminado exitosamente!", 'exito')
    return redirect('/citas')


