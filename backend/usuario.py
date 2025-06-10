
class Usuario:
    def __init__(self, id, dni, nombre, apellido, email, rol):
        self.id = id
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.rol = rol

    def tiene_permiso_para_modificar_notas(self):
        return self.rol in ('profesor', 'admin')

    def tiene_permiso_para_modificar_asistencias(self):
        return self.rol in ('profesor', 'admin')


class Profesor(Usuario):
    def __init__(self, id, dni, nombre, apellido, email):
        super().__init__(id, dni, nombre, apellido, email, 'profesor')


class Admin(Usuario):
    def __init__(self, id, dni, nombre, apellido, email):
        super().__init__(id, dni, nombre, apellido, email, 'admin')


class Alumno(Usuario):
    def __init__(self, id, dni, nombre, apellido, email, curso_id=None):
        super().__init__(id, dni, nombre, apellido, email, 'alumno')
        self.curso_id = curso_id

    def tiene_permiso_para_modificar_notas(self):
        return False

    def tiene_permiso_para_modificar_asistencias(self):
        return False
