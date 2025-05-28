
class Usuario:
    def __init__(self, dni, nombre, apellido, email, rol):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.rol = rol

    def tiene_permiso_para_modificar_notas(self):
        # Solo profesores y administradores pueden modificar notas
        return self.rol in ('profesor', 'admin')

    def tiene_permiso_para_modificar_asistencias(self):
        # Solo profesores y administradores pueden modificar asistencias
        return self.rol in ('profesor', 'admin')


class Profesor(Usuario):
    def __init__(self, dni, nombre, apellido, email, rol='profesor'):
        super().__init__(dni, nombre, apellido, email, rol)

    # Hereda permisos de Usuario: profesor puede modificar notas y asistencias


class Admin(Usuario):
    def __init__(self, dni, nombre, apellido, email, rol='admin'):
        super().__init__(dni, nombre, apellido, email, rol)

    # Admin hereda los permisos: siempre True para todas las modificaciones


class Alumno(Usuario):
    def __init__(self, dni, nombre, apellido, email, rol='alumno'):
        super().__init__(dni, nombre, apellido, email, rol)

    def tiene_permiso_para_modificar_notas(self):
        return False  # Los alumnos no pueden modificar notas

    def tiene_permiso_para_modificar_asistencias(self):
        return False  # Los alumnos no pueden modificar asistencias







