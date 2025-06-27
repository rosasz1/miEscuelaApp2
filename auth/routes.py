from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.usuarioDAO import UsuarioDAO

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dni = request.form.get('dni')
        password = request.form.get('password')
        if not dni or not password:
            flash('Por favor, complete todos los campos.', 'danger')
            return render_template('login.html')
        user = UsuarioDAO.login(dni, password)
        if user:
            session['usuario'] = {
                'id': user.id,
                'dni': user.dni,
                'nombre': user.nombre,
                'apellido': user.apellido,
                'email': user.email,
                'rol': user.rol
            }

            if user.rol == 'alumno':
                session['usuario']['curso_id'] = user.curso_id
                return redirect(url_for('alumno.dashboard'))
            elif user.rol == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.rol == 'profesor':
                return redirect(url_for('profesor.dashboard'))
        else:
            flash('DNI o contraseña incorrectos.')
            return render_template('login.html')

    return render_template('login.html')



@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        resultado = UsuarioDAO.crear_usuario(dni, nombre, apellido, email, 'alumno', password)
        flash(resultado.get('mensaje', 'Error en el registro'))
        return redirect(url_for('auth.login'))
    return render_template('registro.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
