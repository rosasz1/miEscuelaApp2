from usuarioDAO import UsuarioDAO
from usuario import Usuario
from notas import NotasDAO
from asistencias import AsistenciasDAO

def obtener_usuarios():
    dni_alumno = '12345678'
    dni_profesor = '87654321'
    dni_admin = '11223344'
    alumno = UsuarioDAO.obtener_usuario_por_dni(dni_alumno)
    profesor = UsuarioDAO.obtener_usuario_por_dni(dni_profesor)
    admin = UsuarioDAO.obtener_usuario_por_dni(dni_admin)
    return alumno, profesor, admin

def mostrar_datos_usuario(usuario, rol):
    print(f"{rol}:", usuario)

def obtener_y_mostrar_notas(dni):
    notas = UsuarioDAO.obtener_notas(dni)
    print("Notas actuales del alumno:", notas)
    return notas

def admin_actualiza_nota(admin, dni_alumno, nueva_nota, materia_id):
    print("\n=== ADMIN ACTUALIZA NOTA DEL ALUMNO ===")
    if admin and admin.tiene_permiso_para_modificar_notas():
        resultado = NotasDAO.actualizar_nota(dni_alumno, nueva_nota, materia_id)
        print("Resultado de actualizar nota por admin:", resultado)
    else:
        print("El admin no tiene permisos.")

def profesor_registra_asistencia(profesor, dni_alumno, materia_id):
    print("\n=== PROFESOR REGISTRA ASISTENCIA ===")
    if profesor and profesor.tiene_permiso_para_modificar_asistencias():
        resultado = AsistenciasDAO.registrar_asistencia(dni_alumno, True, materia_id)
        print("Resultado de registrar asistencia por profesor:", resultado)
    else:
        print("El profesor no tiene permisos.")

def verificacion_final(dni_alumno):
    print("\n=== VERIFICACIÓN FINAL DE DATOS ===")
    notas = UsuarioDAO.obtener_notas(dni_alumno)
    asistencias = UsuarioDAO.obtener_asistencias(dni_alumno)
    print("Notas del alumno después:", notas)
    print("Asistencias del alumno después:", asistencias)

def test_proyecto_completo():
    dni_alumno = '12345678'
    dni_profesor = '87654321'
    dni_admin = '11223344'
    materia_id = 1
    nueva_nota = 8.5

    print("=== OBTENER USUARIOS ===")
    alumno, profesor, admin = obtener_usuarios()
    mostrar_datos_usuario(alumno, "Alumno")
    mostrar_datos_usuario(profesor, "Profesor")
    mostrar_datos_usuario(admin, "Admin")

    print("\n=== OBTENER NOTAS DEL ALUMNO ===")
    obtener_y_mostrar_notas(dni_alumno)

    admin_actualiza_nota(admin, dni_alumno, nueva_nota, materia_id)
    profesor_registra_asistencia(profesor, dni_alumno, materia_id)

    verificacion_final(dni_alumno)

if __name__ == "__main__":
    test_proyecto_completo()
