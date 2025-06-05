from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.comunicadoDAO import ComunicadoDAO
from backend.usuarioDAO import UsuarioDAO  # para obtener lista de usuarios si hace falta

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
        flash("No autorizado")
        return redirect(url_for("ver_comunicados"))

    if request.method == "POST":
        receptor_id = request.form.get("receptor_id")
        mensaje = request.form.get("mensaje")
        ComunicadoDAO.crear_comunicado(usuario['id'], receptor_id, mensaje)
        flash("Comunicado enviado correctamente.")
        return redirect(url_for("ver_comunicados"))

    usuarios = UsuarioDAO.obtener_todos()
    return render_template("nuevo_comunicado.html", usuarios=usuarios)


@comunicados_bp.route("/responder/<int:comunicado_id>", methods=["GET", "POST"])
def responder_comunicado(comunicado_id):
    if not validar_sesion():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        respuesta = request.form.get("respuesta")
        ComunicadoDAO.responder_comunicado(comunicado_id, respuesta)
        flash("Respuesta enviada correctamente.")
        return redirect(url_for("ver_comunicados"))

    return render_template("responder_comunicado.html", comunicado_id=comunicado_id)
