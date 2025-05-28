from usuarioDAO import UsuarioDAO
from notas import NotasDAO
def test_admin_actualiza_nota():
    dni_admin = '11223344'  # Asegurate que existe en tu DB con rol 'admin'
    dni_alumno = '12345678'
    nueva_nota = 9
    materia_id = 1  # Asegurate que exista y esté relacionada con el admin

    admin = UsuarioDAO.verificar_rol(dni_admin, ['admin'])
    if not admin:
        print("El usuario no tiene permisos de admin.")
        return

    # Luego actualizamos la nota del alumno
    resultado = NotasDAO.actualizar_nota(dni_alumno, nueva_nota, materia_id)
    print("Resultado:", resultado)

if __name__ == "__main__":
    test_admin_actualiza_nota()