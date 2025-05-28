from backend.plan_academico import PlanAcademicoDAO
from flask import Blueprint, render_template, session, redirect, url_for, flash
from backend.usuarioDAO import UsuarioDAO
from backend.examenDAO import ExamenDAO

alumno_bp = Blueprint('alumno', __name__, url_prefix='/alumno', template_folder='templates')

def validar_rol(roles):
    if 'usuario' not in session:
        return False
    if isinstance(roles, str):
        roles = [roles]
    return session['usuario']['rol'] in roles

def redireccion_no_autorizado():
    flash("No autorizado")
    return redirect(url_for('auth.login'))


@alumno_bp.route('/dashboard')
def dashboard():
    if not validar_rol('alumno'):
        return redireccion_no_autorizado()

    curso_id = session['usuario'].get('curso_id')
    nombre = session['usuario'].get('nombre')
    horarios = PlanAcademicoDAO.obtener_horarios_por_curso(curso_id)
    examenes = ExamenDAO.obtener_examenes_por_curso(curso_id)

    return render_template(
        'alumno/dashboard.html',
        horarios=horarios,
        examenes=examenes,
        nombre=nombre
    )


@alumno_bp.route('/notas')
def ver_notas():
    if not validar_rol('alumno'):
        return redireccion_no_autorizado()
    notas = UsuarioDAO.obtener_notas(session['usuario']['dni'])
    return render_template('alumno/notas.html', notas=notas)

@alumno_bp.route('/asistencias')
def ver_asistencias():
    if not validar_rol('alumno'):
        return redireccion_no_autorizado()
    asistencias = UsuarioDAO.obtener_asistencias(session['usuario']['dni'])
    return render_template('alumno/asistencias.html', asistencias=asistencias)
