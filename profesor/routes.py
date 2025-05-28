from backend.examenDAO import ExamenDAO
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.usuarioDAO import UsuarioDAO

profesor_bp = Blueprint('profesor', __name__, url_prefix='/profesor', template_folder='templates')

def validar_rol(roles):
    if 'usuario' not in session:
        return False
    if isinstance(roles, str):
        roles = [roles]
    return session['usuario']['rol'] in roles

def redireccion_no_autorizado():
    flash("No autorizado")
    return redirect(url_for('auth.login'))

@profesor_bp.route('/dashboard')
def dashboard():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()
    return render_template('profesor/dashboard.html')

# ----- NOTAS -----
@profesor_bp.route('/notas', methods=['GET', 'POST'])
def ver_notas():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()
    notas = None
    if request.method == 'POST':
        dni_alumno = request.form['dni_alumno']
        notas = UsuarioDAO.obtener_notas_por_profesor(session['usuario']['dni'], dni_alumno)
    return render_template("profesor/ver_notas_alumno.html", notas=notas)

@profesor_bp.route('/agregar-nota', methods=['GET', 'POST'])
def agregar_nota():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()
    if request.method == 'POST':
        dni_alumno = request.form['dni_alumno']
        materia_id = request.form['materia_id']
        nota = request.form['nota']
        resultado = UsuarioDAO.agregar_nota(session['usuario']['dni'], dni_alumno, nota, materia_id)
        flash(resultado.get('mensaje', 'Error'))
        return redirect(url_for('profesor.dashboard'))
    return render_template("profesor/agregar_nota.html")

@profesor_bp.route('/actualizar-nota', methods=['GET', 'POST'])
def actualizar_nota():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()
    if request.method == 'POST':
        dni_alumno = request.form['dni_alumno']
        materia_id = request.form['materia_id']
        nueva_nota = request.form['nueva_nota']
        resultado = UsuarioDAO.actualizar_nota(session['usuario']['dni'], dni_alumno, nueva_nota, materia_id)
        flash(resultado.get('mensaje', 'Error'))
        return redirect(url_for('profesor.dashboard'))
    return render_template("profesor/actualizar_nota.html")

# ----- ASISTENCIAS -----
@profesor_bp.route('/ver-asistencias', methods=['GET', 'POST'])
def ver_asistencias():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()
    asistencias = None
    if request.method == 'POST':
        dni_alumno = request.form['dni_alumno']
        asistencias = UsuarioDAO.obtener_asistencias(dni_alumno)
    return render_template("profesor/ver_asistencias_alumno.html", asistencias=asistencias)

@profesor_bp.route('/registrar-asistencia', methods=['GET', 'POST'])
def registrar_asistencia():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()
    if request.method == 'POST':
        dni_alumno = request.form['dni_alumno']
        materia_id = request.form['materia_id']
        presente = request.form['presente'].lower() == 'true'
        resultado = UsuarioDAO.registrar_asistencia(session['usuario']['dni'], dni_alumno, presente, materia_id)
        flash(resultado.get('mensaje', 'Error'))
        return redirect(url_for('profesor.dashboard'))
    return render_template("profesor/registrar_asistencia.html")

@profesor_bp.route('/modificar-asistencia', methods=['GET', 'POST'])
def modificar_asistencia():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()
    if request.method == 'POST':
        dni_alumno = request.form['dni_alumno']
        materia_id = request.form['materia_id']
        presente = request.form['presente'].lower() == 'true'
        resultado = UsuarioDAO.modificar_asistencia(session['usuario']['dni'], dni_alumno, materia_id, presente)
        flash(resultado.get('mensaje', 'Error'))
        return redirect(url_for('profesor.dashboard'))
    return render_template("profesor/modificar_asistencia.html")

@profesor_bp.route('/crear-examen', methods=['GET', 'POST'])
def crear_examen():
    if not validar_rol(['admin', 'profesor']):
        return redireccion_no_autorizado()

    cursos = PlanAcademicoDAO.obtener_cursos_con_anio()
    materias = []
    materia_horarios = {}
    horarios_disponibles = []

    if request.method == 'POST':
        curso_id = request.form.get('curso_id')
        materia_id = request.form.get('materia_id')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        titulo = request.form.get('titulo')
        dni = session['usuario']['dni']

        if fecha and hora and materia_id:
            resultado = ExamenDAO.crear_examen(curso_id, materia_id, fecha, hora, titulo, dni)
            flash(resultado.get('mensaje', 'Error al crear examen'))
            return redirect(url_for('profesor.dashboard'))
        elif curso_id:
            materias, materia_horarios = obtener_materias_y_horarios_por_curso(curso_id)

    return render_template(
        'admin/crear_examen.html',
        cursos=cursos,
        materias=materias,
        materia_horarios=materia_horarios
    )

# Función auxiliar (puede ir arriba)
from collections import defaultdict

def obtener_materias_y_horarios_por_curso(curso_id):
    datos = PlanAcademicoDAO.obtener_horarios_por_curso(curso_id)
    materia_horarios = defaultdict(list)
    materias_vistas = set()
    materias = []

    for materia, dia, h_ini, h_fin in datos:
        hora_texto = f"{dia} - {h_ini.strftime('%H:%M')} a {h_fin.strftime('%H:%M')}"
        materia_horarios[materia].append((dia, h_ini.strftime('%H:%M'), h_fin.strftime('%H:%M'), hora_texto))
        if materia not in materias_vistas:
            materias.append(materia)
            materias_vistas.add(materia)

    return materias, materia_horarios

@profesor_bp.route('/ver-examenes')
def ver_examenes():
    dni = session['usuario']['dni']
    examenes = ExamenDAO.obtener_examenes_por_profesor(dni)
    return render_template('profesor/ver_examenes_profesor.html', examenes=examenes)

