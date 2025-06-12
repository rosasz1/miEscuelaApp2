from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.comunicadoDAO import ComunicadoDAO
from backend.plan_academico import PlanAcademicoDAO

comunicados_bp = Blueprint('comunicados', __name__, url_prefix='/comunicados', template_folder='templates')


def validar_sesion():
    if 'usuario' not in session:
        flash("Sesión no iniciada.")
        return False
    return True


@comunicados_bp.route("/ver")
def ver_comunicados():
    if not validar_sesion():
        return redirect(url_for("auth.login"))

    usuario = session['usuario']
    comunicados = ComunicadoDAO.obtener_comunicados_recibidos(usuario['id'])
    return render_template("ver_comunicados.html", comunicados=comunicados, usuario=usuario)


@comunicados_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_comunicado():
    if not validar_sesion():
        return redirect(url_for("auth.login"))

    usuario = session['usuario']
    if usuario['rol'] not in ['admin', 'profesor']:
        flash("No autorizado.")
        return redirect(url_for("comunicados.ver_comunicados"))

    if request.method == "POST":
        curso_id = request.form.get("curso_id")
        rol_destinatario = request.form.get("rol_destinatario")
        mensaje = request.form.get("mensaje")

        if not curso_id or not rol_destinatario:
            flash("Debes seleccionar un curso y un tipo de destinatario.")
            return redirect(url_for("comunicados.nuevo_comunicado"))

        if not mensaje.strip():
            flash("El mensaje no puede estar vacío.")
            return redirect(url_for("comunicados.nuevo_comunicado"))

        destinatarios = []

        if rol_destinatario == "alumno":
            destinatarios = PlanAcademicoDAO.obtener_usuarios_por_rol_y_curso("alumno", curso_id)
        elif rol_destinatario == "profesor":
            destinatarios = PlanAcademicoDAO.obtener_usuarios_por_rol_y_curso("profesor", curso_id)
        elif rol_destinatario == "ambos":
            destinatarios = PlanAcademicoDAO.obtener_usuarios_por_rol_y_curso("alumno", curso_id)
            destinatarios += PlanAcademicoDAO.obtener_usuarios_por_rol_y_curso("profesor", curso_id)

        for r in destinatarios:
            ComunicadoDAO.crear_comunicado(usuario['id'], r[0], mensaje)

        flash(f"Comunicado enviado a {len(destinatarios)} usuario(s).")
        return redirect(url_for("comunicados.ver_comunicados"))

    cursos = PlanAcademicoDAO.obtener_cursos_completos()
    return render_template("nuevo_comunicado.html", cursos=cursos)


@comunicados_bp.route("/responder/<int:comunicado_id>", methods=["GET", "POST"])
def responder_comunicado(comunicado_id):
    if not validar_sesion():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        respuesta = request.form.get("respuesta")
        ComunicadoDAO.responder_comunicado(comunicado_id, respuesta)
        flash("Respuesta enviada correctamente.")
        return redirect(url_for("comunicados.ver_comunicados"))

    return render_template("responder_comunicado.html", comunicado_id=comunicado_id)

