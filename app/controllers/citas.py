from app.models.cita_model import Cita
from app.models.usuario_model import Usuario
from flask import render_template, redirect, request, session, Blueprint, flash

bp = Blueprint('citas', __name__, url_prefix='/citas')

def verificar_sesion():
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", 'error')
        return redirect('/')
    return True

@bp.route('/agregar', methods=['POST'])
def agregar_cita():
    verificar_sesion()

    if not Cita.validar_cita(request.form):
        return redirect('/citas')

    data = {
        **request.form,
        'usuario_id': session['usuario_id']
    }
    Cita.guardar_cita(data)
    flash("¡Cita agregada exitosamente!", 'exito')
    return redirect('/citas')

@bp.route('/editar/<int:id>')
def editar_cita(id):
    verificar_sesion()

    cita = Cita.obtener_por_id(id)
    if not cita or cita.usuario_id != session['usuario_id']:
        flash("No tienes permiso para editar esta cita.", 'error')
        return redirect('/citas')

    return render_template('editar_cita.html', cita=cita)

@bp.route('/procesar_editar', methods=['POST'])
def procesar_editar():
    verificar_sesion()

    if not Cita.validar_cita(request.form):
        return redirect(f"/citas/editar/{request.form['id']}")

    cita_a_editar = Cita.obtener_por_id(request.form['id'])
    if not cita_a_editar or cita_a_editar.usuario_id != session['usuario_id']:
        flash("No tienes permiso para editar esta cita.", 'error')
        return redirect('/citas')
    if not Cita.validar_cita(request.form):
        return redirect(f"/citas/editar/{request.form['id']}")
    Cita.actualizar_cita(request.form)
    return redirect('/citas')

@bp.route('/borrar/<int:id>')
def borrar_cita(id):
    # Ruta para borrar una cita
    # Solo el usuario que creó la cita puede borrarla
    verificar_sesion()

    cita_a_borrar = Cita.obtener_por_id(id)
    if not cita_a_borrar or cita_a_borrar.usuario_id != session['usuario_id']:
        flash("No tienes permiso para borrar esta cita.", 'error')
        return redirect('/citas')
    Cita.borrar_cita(id)
    flash("¡Cita borrada exitosamente!", 'exito')
    return redirect('/citas')

@bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    # Ruta para ver y actualizar el perfil del usuario
    verificar_sesion()
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    citas_usuario = Cita.obtener_por_usuario(session['usuario_id'])
    total_citas = len(citas_usuario)
    if request.method == 'POST':
        if not Usuario.validar_actualizacion(request.form, session['usuario_id']):
            return redirect('/citas/perfil')
        Usuario.actualizar_usuario(request.form, session['usuario_id'])
        flash("¡Perfil actualizado exitosamente!", 'exito')
        return redirect('/citas/perfil')

    return render_template('perfil.html', usuario=usuario, citas=citas_usuario, total_citas=total_citas)

@bp.route('/dashboard', methods=['GET'])
def funcname(self, parameter_list):
    """
    docstring
    """
    pass

