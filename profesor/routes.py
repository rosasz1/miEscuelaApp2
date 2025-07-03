from backend.notas import NotasDAO
from backend.examenDAO import ExamenDAO
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.usuarioDAO import UsuarioDAO
from backend.plan_academico import PlanAcademicoDAO
from collections import defaultdict
from datetime import date, timedelta


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

# ========================
# 🏠 DASHBOARD
# ========================
@profesor_bp.route('/dashboard')
def dashboard():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()
    return render_template('profesor/dashboard.html')

# ========================
# 📝 NOTAS
# ========================
@profesor_bp.route('/ver-notas', methods=['GET', 'POST'])
def ver_notas():
    notas = None
    materias = []
    filtro_materia = None
    dni_alumno = None

    if request.method == 'POST':
        dni_alumno = request.form.get('dni_alumno', '').strip()
        filtro_materia = request.form.get('filtro_materia')
    else:
        dni_alumno = request.args.get('dni_alumno', '').strip()
        filtro_materia = request.args.get('filtro_materia')

    if dni_alumno:
        notas_crudas = NotasDAO.obtener_notas(dni_alumno)
        materias = UsuarioDAO.obtener_materias_asignadas_alumno(dni_alumno)
        print("notas_crudas:", notas_crudas)
        print("filtro_materia:", filtro_materia)
        print("materia_ids:", [n['materia_id'] for n in notas_crudas])

        if filtro_materia:
            # El filtro robusto para cualquier combinación de tipos
            notas = [n for n in notas_crudas if str(n['materia_id']).strip() == str(filtro_materia).strip()]
        else:
            notas = notas_crudas
    else:
        notas = None

    return render_template(
        "profesor/ver_notas_alumno.html",
        notas=notas,
        materias=materias,
        filtro_materia=filtro_materia,
        dni_alumno=dni_alumno
    )
@profesor_bp.route('/agregar-nota', methods=['GET', 'POST'])
def agregar_nota():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()

    materias = None
    dni_alumno = None

    if request.method == 'POST':
        dni_alumno = request.form.get('dni_alumno', '').strip()
        materia_id = request.form.get('materia_id')
        titulo_nota = request.form.get('titulo_nota')
        nota = request.form.get('nota')

        # Si ya seleccionó materia y nota, guardar la nota
        if materia_id and nota and titulo_nota:
            resultado = UsuarioDAO.agregar_nota(
                session['usuario']['dni'],
                dni_alumno,
                nota,
                materia_id,
                titulo_nota=titulo_nota
            )
            flash(resultado.get('mensaje', 'Nota agregada exitosamente'))
            # Vuelve a mostrar el form, no redirecciona
            materias = UsuarioDAO.obtener_materias_asignadas_alumno(dni_alumno)
        # Si solo mandó DNI, buscar materias asignadas
        elif dni_alumno:
            materias = UsuarioDAO.obtener_materias_asignadas_alumno(dni_alumno)
            if not materias:
                flash("El alumno no tiene materias asignadas o el DNI es incorrecto.")

    return render_template(
        "profesor/agregar_nota.html",
        materias=materias,
        dni_alumno=dni_alumno
    )

@profesor_bp.route('/eliminar-nota', methods=['POST'])
def eliminar_nota():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()
    dni_alumno = request.form.get('dni_alumno')
    materia_id = request.form.get('materia_id')
    resultado = UsuarioDAO.eliminar_nota(dni_alumno, materia_id)
    flash(resultado.get('mensaje', 'Error'))
    return redirect(url_for('profesor.ver_notas', dni_alumno=dni_alumno))

@profesor_bp.route('/modificar-nota', methods=['POST'])
def modificar_nota():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()
    dni_editor = session['usuario']['dni']
    dni_alumno = request.form.get('dni_alumno')
    materia_id = request.form.get('materia_id')
    nueva_nota = request.form.get('nueva_nota')
    resultado = UsuarioDAO.actualizar_nota(dni_editor, dni_alumno, nueva_nota, materia_id)
    flash(resultado.get('mensaje', 'Error'))
    return redirect(url_for('profesor.ver_notas', dni_alumno=dni_alumno))

# ========================
# 📋 ASISTENCIAS
# ========================
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

# ========================
# 📆 CRONOGRAMA
# ========================
@profesor_bp.route("/cronograma", methods=["GET", "POST"])
def cronograma_profesor():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()

    profesor_id = session['usuario']['id']
    cursos = PlanAcademicoDAO.obtener_cursos_por_profesor(profesor_id)
    curso_id = None
    cronograma = []
    examenes = []
    fechas_semana = {}

    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horas = [f"{h}:00" for h in range(8, 19)]
    cronograma_dict = {dia: {hora: [] for hora in horas} for dia in dias_semana}

    try:
        if request.method == 'POST':
            curso_id = int(request.form['curso_id'])
        elif cursos:
            curso_id = cursos[0].id

        if curso_id:
            cronograma = PlanAcademicoDAO.obtener_horarios_por_curso(curso_id)
            examenes = ExamenDAO.obtener_examenes_por_profesor_y_curso(profesor_id, curso_id)
            fechas_semana = obtener_fechas_semana_actual()

            for materia, dia, h_ini, h_fin in cronograma:
                for h in range(int(h_ini.split(":")[0]), int(h_fin.split(":")[0])):
                    hora_str = f"{h}:00"
                    if dia in cronograma_dict and hora_str in cronograma_dict[dia]:
                        cronograma_dict[dia][hora_str].append({
                            "nombre": materia,
                            "tipo": "materia"
                        })

            for ex in examenes:
                dia = ex['fecha'].strftime("%A").capitalize()
                hora = ex['hora'].strftime("%H:%M")
                if dia in cronograma_dict and hora in cronograma_dict[dia]:
                    cronograma_dict[dia][hora].append({
                        "nombre": f"Ex: {ex['materia']}",
                        "tipo": "examen"
                    })

    except Exception as e:
        flash("Error al cargar el cronograma")
        print("🔥 Error en cronograma_profesor:", e)

    return render_template("profesor/cronograma_profesor.html",
                           cursos=cursos,
                           curso_seleccionado=curso_id,
                           cronograma=cronograma_dict,
                           examenes=examenes,
                           fechas_semana=fechas_semana,
                           dias_semana=dias_semana,
                           horas=horas)

def obtener_fechas_semana_actual():
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    return {dias[i]: (inicio_semana + timedelta(days=i)) for i in range(5)}

# ========================
# 🧪 EXÁMENES
# ========================
@profesor_bp.route('/crear-examen', methods=['GET', 'POST'])
def crear_examen():
    if not validar_rol('profesor'):
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

        if materia_id:
            horarios_disponibles = materia_horarios.get(int(materia_id), [])

    return render_template(
        'profesor/crear_examen.html',
        cursos=cursos,
        materias=materias,
        materia_horarios=materia_horarios,
        horarios_disponibles=horarios_disponibles
    )
def obtener_materias_y_horarios_por_curso(curso_id):
    datos = PlanAcademicoDAO.obtener_horarios_por_curso(curso_id)

    materias = []
    materia_horarios = defaultdict(list)

    for mid, nombre, dia, h_ini, h_fin in datos:
        if (mid, nombre) not in materias:
            materias.append((mid, nombre))
        materia_horarios[mid].append((dia, h_ini, h_fin))

    return materias, materia_horarios



@profesor_bp.route("/ver-examenes")
def ver_examenes():
    if not validar_rol('profesor'):
        return redireccion_no_autorizado()

    profesor_id = session['usuario']['id']
    examenes = ExamenDAO.obtener_examenes_por_profesor(profesor_id)
    return render_template("profesor/ver_examenes_profesor.html", examenes=examenes)

def obtener_materias_y_horarios_por_curso(curso_id):
    datos = PlanAcademicoDAO.obtener_horarios_por_curso(curso_id)

    materias = []
    materia_horarios = defaultdict(list)

    for mid, nombre, dia, h_ini, h_fin in datos:
        if (mid, nombre) not in materias:
            materias.append((mid, nombre))
        materia_horarios[mid].append((dia, h_ini, h_fin))

    return materias, materia_horarios
