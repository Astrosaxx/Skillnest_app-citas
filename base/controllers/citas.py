from base.models.cita_model import Cita
from base.models.usuario_model import Usuario
from base.models.favorito_model import Favorito
from flask import render_template, redirect, request, session, Blueprint, flash

bp = Blueprint('citas', __name__, url_prefix='/citas')

def verificar_sesion():
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", 'error')
        return redirect('/')
    return True

@bp.route('/', methods=['GET'])
def citas_home():
    verificar_sesion()
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    citas_propias = Cita.obtener_citas_usuarios(session['usuario_id'])
    citas_todas = Cita.obtener_todas()
    favoritos = Favorito.obtener_favoritos_usuarios(session['usuario_id'])
    favoritos_todos = Favorito.obtener_todos()
    
    # Obtener IDs de citas favoritas del usuario
    citas_favoritas_ids = [f.cita_id for f in favoritos]
    
    # Filtrar citas que NO están en favoritos
    citas_no_favoritas = [cita for cita in citas_todas if cita.id not in citas_favoritas_ids]
    
    # Obtener citas favoritas con información completa
    citas_favoritas_completas = []
    for favorito in favoritos:
        for cita in citas_todas:
            if cita.id == favorito.cita_id:
                citas_favoritas_completas.append(cita)
                break
    
    return render_template('dashboard.html', 
                         usuario=usuario, 
                         citas_todas=citas_todas,
                         citas_no_favoritas=citas_no_favoritas,
                         citas_favoritas=citas_favoritas_completas,
                         favoritos=favoritos,
                         citas_favoritas_ids=citas_favoritas_ids,
                         citas_totales=len(citas_todas),
                         citas_propias_totales=len(citas_propias),
                         favoritos_totales=len(favoritos))

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
    if not cita or cita.autor_id != session['usuario_id']:
        flash("No tienes permiso para editar esta cita.", 'error')
        return redirect('/citas')

    return render_template('editar_cita.html', cita=cita)

@bp.route('/procesar_editar', methods=['POST'])
def procesar_editar():
    verificar_sesion()

    if not Cita.validar_cita(request.form):
        return redirect(f"/citas/editar/{request.form['id']}")

    cita_a_editar = Cita.obtener_por_id(request.form['id'])
    if not cita_a_editar or cita_a_editar.autor_id != session['usuario_id']:
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
    if not cita_a_borrar or cita_a_borrar.autor_id != session['usuario_id']:
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

@bp.route('/agregar_favorito/<int:cita_id>')
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

@bp.route('/eliminar_favorito/<int:cita_id>')
def eliminar_favorito(cita_id):
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
    flash("¡Cita eliminada de favoritos exitosamente!", 'exito')
    return redirect('/citas')

@bp.route('/dashboard', methods=['GET'])
def dashboard():
    # Ruta para ver el dashboard con todas las citas y favoritos
    verificar_sesion()
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    citas_todas = Cita.obtener_todas()
    favoritos = Favorito.obtener_favoritos_usuarios(session['usuario_id'])
    favoritos_todos = Favorito.obtener_todos()
    
    return render_template('dashboard.html', 
                         usuario=usuario, 
                         citas=citas_todas, 
                         favoritos=favoritos,
                         citas_totales=len(citas_todas),
                         favoritos_totales=len(favoritos_todos))


