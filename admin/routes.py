from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.usuarioDAO import UsuarioDAO
from backend.plan_academico import PlanAcademicoDAO
from backend.examenDAO import ExamenDAO
from backend.conexion import Conexion
from datetime import date, timedelta
from collections import defaultdict




admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')

def validar_rol(roles):
    if 'usuario' not in session:
        return False
    if isinstance(roles, str):
        roles = [roles]
    return session['usuario']['rol'] in roles

def redireccion_no_autorizado():
    flash("No autorizado")
    return redirect(url_for('auth.login'))

@admin_bp.route('/dashboard')
def dashboard():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()
    return render_template('admin/dashboard.html')

@admin_bp.route('/crear-usuario', methods=['GET', 'POST'])
def crear_usuario():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        rol = request.form['rol']
        password = request.form['password']
        resultado = UsuarioDAO.crear_usuario(dni, nombre, apellido, email, rol, password)
        flash(resultado.get('mensaje', 'Error'))
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/crear_usuario.html')

@admin_bp.route('/modificar-usuario', methods=['GET', 'POST'])
def modificar_usuario():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        rol = request.form.get('rol')
        password = request.form.get('password')
        resultado = UsuarioDAO.modificar_usuario(dni, nombre, apellido, email, rol, password)
        flash(resultado.get('mensaje', 'Error'))
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/modificar_usuario.html')

@admin_bp.route('/eliminar-usuario', methods=['GET', 'POST'])
def eliminar_usuario():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()
    if request.method == 'POST':
        dni = request.form['dni']
        resultado = UsuarioDAO.eliminar_usuario(dni)
        flash(resultado.get('mensaje', 'Error'))
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/eliminar_usuario.html')

@admin_bp.route('/asignar-profesor', methods=['GET', 'POST'])
def asignar_profesor():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()
    if request.method == 'POST':
        profesor_dni = request.form['profesor_dni']
        materia_id = request.form['materia_id']
        resultado = UsuarioDAO.asignar_profesor_a_materia(materia_id, profesor_dni)
        flash(resultado.get('mensaje', 'Error'))
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/asignar_profesor.html')

@admin_bp.route('/ver-notas', methods=['GET', 'POST'])
def ver_notas():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()
    notas = None
    if request.method == 'POST':
        dni_alumno = request.form['dni_alumno']
        notas = UsuarioDAO.obtener_notas(dni_alumno)
    return render_template('admin/ver_notas_alumno.html', notas=notas)

@admin_bp.route('/agregar-nota', methods=['GET', 'POST'])
def agregar_nota():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()
    if request.method == 'POST':
        dni_alumno = request.form['dni_alumno']
        materia_id = request.form['materia_id']
        nota = request.form['nota']
        resultado = UsuarioDAO.agregar_nota(session['usuario']['dni'], dni_alumno, nota, materia_id)
        flash(resultado.get('mensaje', 'Error'))
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/agregar_nota.html')

@admin_bp.route('/actualizar-nota', methods=['GET', 'POST'])
def actualizar_nota():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()
    if request.method == 'POST':
        dni_alumno = request.form['dni_alumno']
        materia_id = request.form['materia_id']
        nueva_nota = request.form['nueva_nota']
        resultado = UsuarioDAO.actualizar_nota(session['usuario']['dni'], dni_alumno, nueva_nota, materia_id)
        flash(resultado.get('mensaje', 'Error'))
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/actualizar_nota.html')

@admin_bp.route('/ver-asistencias', methods=['GET', 'POST'])
def ver_asistencias():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()
    asistencias = None
    if request.method == 'POST':
        dni_alumno = request.form['dni_alumno']
        asistencias = UsuarioDAO.obtener_asistencias(dni_alumno)
    return render_template('admin/ver_asistencias_alumno.html', asistencias=asistencias)

from backend.plan_academico import PlanAcademicoDAO

@admin_bp.route('/ver-materias')
def ver_materias():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()

    estructura = PlanAcademicoDAO.obtener_materias_estructuradas()
    anios = PlanAcademicoDAO.obtener_anios()
    cursos = PlanAcademicoDAO.obtener_cursos_con_anio()
    return render_template("admin/ver_materias.html", estructura=estructura, anios=anios, cursos=cursos)




@admin_bp.route("/crear-materia", methods=["GET", "POST"])
def crear_materia():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()

    if request.method == 'POST':
        print("➡️ Formulario recibido por POST")

        nombre = request.form.get('nombre')
        curso_id = request.form.get('curso_id')

        print("➡️ Datos recibidos:", nombre, curso_id)

        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    print("➡️ Ejecutando INSERT en la BD")
                    cursor.execute(
                        "INSERT INTO materias (nombre, curso_id) VALUES (%s, %s)",
                        (nombre, curso_id)
                    )
                    conn.commit()
                    flash("Materia registrada exitosamente")
                    return redirect(url_for('admin.ver_materias'))
        except Exception as e:
            flash("Error al registrar materia")
            print("🔥 Error al insertar materia:", e)

    # Solo usás cursos para el select
    anios = PlanAcademicoDAO.obtener_anios()
    cursos = PlanAcademicoDAO.obtener_cursos_completos()
    return render_template("admin/crear_materia.html", anios=anios, cursos=cursos)


@admin_bp.route("/editar-materia/<int:materia_id>", methods=["GET", "POST"])
def editar_materia(materia_id):
    if not validar_rol("admin"):
        return redireccion_no_autorizado()

    try:
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nombre, curso_id FROM materias WHERE id = %s", (materia_id,))
                materia = cursor.fetchone()

        if not materia:
            flash("Materia no encontrada")
            return redirect(url_for("admin.ver_materias"))

        if request.method == "POST":
            nuevo_nombre = request.form.get("nombre")
            nuevo_curso_id = request.form.get("curso_id")

            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE materias SET nombre = %s, curso_id = %s WHERE id = %s",
                        (nuevo_nombre, nuevo_curso_id, materia_id),
                    )
                    conn.commit()
                    flash("Materia actualizada correctamente")
                    return redirect(url_for("admin.ver_materias"))

        cursos = PlanAcademicoDAO.obtener_cursos_completos()
        return render_template("admin/modificar_materia.html", materia={
            'id': materia[0],
            'nombre': materia[1],
            'curso_id': materia[2]
        }, cursos=cursos)

    except Exception as e:
        flash("Error al editar materia")
        print("🔥 Error al editar materia:", e)
        return redirect(url_for("admin.ver_materias"))



@admin_bp.route("/eliminar-materia/<int:id>", methods=["GET", "POST"])
def eliminar_materia(id):
    if not validar_rol('admin'):
        return redireccion_no_autorizado()

    if request.method == "POST":
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM materias WHERE id = %s", (id,))
                    conn.commit()
                    flash("Materia eliminada")
        except Exception:
            flash("Error al eliminar la materia")
        return redirect(url_for('admin.ver_materias'))


    materia = None
    try:
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nombre FROM materias WHERE id = %s", (id,))
                r = cursor.fetchone()
                if r:
                    materia = {"id": r[0], "nombre": r[1]}
    except Exception:
        flash("Error al cargar la materia")

    return render_template("admin/eliminar_materia.html", materia=materia)


@admin_bp.route("/horarios", methods=["GET", "POST"])
def gestionar_horarios():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()

    cursos = []
    materias = []
    horarios = []

    try:
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:

                cursor.execute("""
                    SELECT c.id, CONCAT(a.nombre, ' - ', c.nombre)
                    FROM cursos c
                    JOIN anio a ON c.anio_id = a.id
                    ORDER BY a.id, c.nombre
                """)
                cursos = cursor.fetchall()


                cursor.execute("""
                    SELECT id, nombre FROM materias ORDER BY nombre
                """)
                materias = cursor.fetchall()


                cursor.execute("""
                    SELECT CONCAT(a.nombre, ' - ', c.nombre), m.nombre, h.dia, h.hora_inicio, h.hora_fin
                    FROM horarios h
                    JOIN cursos c ON h.curso_id = c.id
                    JOIN anio a ON c.anio_id = a.id
                    JOIN materias m ON h.materia_id = m.id
                    ORDER BY a.id, c.nombre, h.dia, h.hora_inicio
                """)
                horarios = cursor.fetchall()
    except Exception:
        flash("Error al cargar datos")

    # Registrar nuevo horario
    if request.method == "POST":
        curso_id = int(request.form['curso_id'])
        materia_id = int(request.form['materia_id'])
        dia = request.form['dia']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']

        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO horarios (curso_id, materia_id, dia, hora_inicio, hora_fin)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (curso_id, materia_id, dia, hora_inicio, hora_fin))
                    conn.commit()
                    flash("Horario registrado correctamente")
                    return redirect(url_for('admin.gestionar_horarios'))
        except Exception:
            flash("Error al registrar el horario")

    return render_template("admin/horarios.html", cursos=cursos, materias=materias, horarios=horarios)

from backend.examenDAO import ExamenDAO

@admin_bp.route("/cronograma", methods=["GET", "POST"])
def ver_cronograma():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()

    cursos = []
    cronograma = []
    examenes = []
    fechas_semana = {}

    try:
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT c.id, CONCAT(a.nombre, ' - ', c.nombre)
                    FROM cursos c
                    JOIN anio a ON c.anio_id = a.id
                    ORDER BY a.id, c.nombre
                """)
                cursos = cursor.fetchall()

                if request.method == 'POST':
                    curso_id = request.form['curso_id']

                    cursor.execute("""
                        SELECT m.nombre, h.dia, h.hora_inicio, h.hora_fin
                        FROM horarios h
                        JOIN materias m ON h.materia_id = m.id
                        WHERE h.curso_id = %s
                        ORDER BY 
                          CASE 
                            WHEN h.dia = 'Lunes' THEN 1
                            WHEN h.dia = 'Martes' THEN 2
                            WHEN h.dia = 'Miércoles' THEN 3
                            WHEN h.dia = 'Jueves' THEN 4
                            WHEN h.dia = 'Viernes' THEN 5
                            ELSE 6
                          END,
                          h.hora_inicio
                    """, (curso_id,))
                    cronograma = cursor.fetchall()
                    examenes = ExamenDAO.obtener_examenes_por_curso(curso_id)
                    fechas_semana = obtener_fechas_semana_actual()

    except Exception:
        flash("Error al cargar el cronograma")

    return render_template("admin/cronograma.html", cursos=cursos, cronograma=cronograma, examenes=examenes, fechas_semana=fechas_semana)

@admin_bp.route("/modificar-asistencia", methods=["GET", "POST"])
def modificar_asistencia():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()

    mensaje = None
    materias = []

    try:
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nombre FROM materias ORDER BY nombre")
                materias = cursor.fetchall()
    except Exception:
        flash("Error al cargar materias")

    if request.method == "POST":
        dni_alumno = request.form['dni_alumno']
        materia_id = request.form['materia_id']
        presente = request.form['presente'] == 'true'

        resultado = UsuarioDAO.modificar_asistencia(
            session['usuario']['dni'],
            dni_alumno,
            materia_id,
            presente
        )
        flash(resultado.get('mensaje', 'Error al modificar asistencia'))

    return render_template("admin/modificar_asistencia.html", materias=materias)

@admin_bp.route('/crear-examen', methods=['GET', 'POST'])
def crear_examen():
    if not validar_rol(['admin', 'profesor']):
        return redireccion_no_autorizado()

    cursos = PlanAcademicoDAO.obtener_cursos_completos()
    materias = []
    materia_horarios = {}

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
            return redirect(url_for('admin.dashboard'))
        elif curso_id:
            materias, materia_horarios = obtener_materias_y_horarios_por_curso(curso_id)

    return render_template(
        'admin/crear_examen.html',
        cursos=cursos,
        materias=materias,
        materia_horarios=materia_horarios
    )

def obtener_materias_y_horarios_por_curso(curso_id):
    datos = PlanAcademicoDAO.obtener_horarios_por_curso(curso_id)
    materia_horarios = defaultdict(list)
    materias_vistas = set()
    materias = []

    for materia_id, nombre, dia, h_ini, h_fin in datos:
        hora_texto = f"{dia} - {h_ini.strftime('%H:%M')} a {h_fin.strftime('%H:%M')}"
        materia_horarios[materia_id].append((dia, h_ini.strftime('%H:%M'), h_fin.strftime('%H:%M'), hora_texto))
        if materia_id not in materias_vistas:
            materias.append((materia_id, nombre))
            materias_vistas.add(materia_id)

    return materias, materia_horarios


@admin_bp.route('/ver-examenes', methods=['GET', 'POST'])
def ver_examenes():
    if not validar_rol('admin'):
        return redireccion_no_autorizado()

    cursos = PlanAcademicoDAO.obtener_cursos_completos()
    examenes = []
    curso_id = None

    if request.method == 'POST':
        curso_id = request.form.get('curso_id')
        if curso_id:
            examenes = ExamenDAO.obtener_examenes_por_curso(curso_id)
        else:
            examenes = ExamenDAO.obtener_todos_los_examenes()
    else:
        examenes = ExamenDAO.obtener_todos_los_examenes()

    return render_template('admin/ver_examenes_admin.html', cursos=cursos, examenes=examenes, curso_id=int(curso_id) if curso_id else None)

def obtener_fechas_semana_actual():
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    fechas = {dias[i]: (inicio_semana + timedelta(days=i)) for i in range(5)}
    return fechas



