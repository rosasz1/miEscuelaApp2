from usuarioDAO import UsuarioDAO
from conexion import Conexion
import logging

MENU_ALUMNO = '''
Menú Alumno:
1. Ver mis notas
2. Ver mis asistencias
3. Salir
'''

MENU_PROFESOR = '''
Menú Profesor:
1. Ver notas de un alumno
2. Agregar nota a un alumno
3. Actualizar nota de un alumno
4. Ver asistencias de un alumno
5. Registrar asistencia de un alumno
6. Modificar asistencia de un alumno
7. Salir
'''

MENU_ADMIN = '''
Menú Admin:
1. Crear usuario
2. Modificar usuario
3. Eliminar usuario
4. Asignar profesor a materia
5. Ver notas de un alumno
6. Agregar nota a un alumno
7. Actualizar nota de un alumno
8. Ver asistencias de un alumno
9. Registrar asistencia de un alumno
10. Modificar asistencia de un alumno
11. Salir
'''

def obtener_materias():
    try:
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nombre FROM public.materias ORDER BY id")
                return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error al obtener materias: {e}")
        return []

def listar_materias():
    materias = obtener_materias()
    if not materias:
        print("No se encontraron materias.")
        return None
    print("ID  Nombre de la materia")
    for mid, nombre in materias:
        print(f"{mid:<3} {nombre}")
    return materias

def main():
    print("=== Sistema de Gestión Escolar ===")
    dni = input("Ingrese su DNI: ").strip()
    usuario = UsuarioDAO.obtener_usuario_por_dni(dni)

    if not usuario:
        print("Usuario no encontrado. Saliendo...")
        return

    print(f"Bienvenido, {usuario.nombre} {usuario.apellido} ({usuario.rol})")

    if usuario.rol == 'alumno':
        while True:
            print(MENU_ALUMNO)
            opcion = input("Seleccione una opción: ").strip()
            if opcion == '1':
                notas = UsuarioDAO.obtener_notas(dni)
                print("Mis notas:", notas)
            elif opcion == '2':
                asistencias = UsuarioDAO.obtener_asistencias(dni)
                print("Mis asistencias:", asistencias)
            elif opcion == '3':
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")

    elif usuario.rol == 'profesor':
        while True:
            print(MENU_PROFESOR)
            opcion = input("Seleccione una opción: ").strip()
            if opcion == '1':
                dni_alumno = input("DNI del alumno: ").strip()
                notas = UsuarioDAO.obtener_notas_por_profesor(dni, dni_alumno)
                print(f"Notas alumno {dni_alumno}: {notas}")
            elif opcion == '2':
                dni_alumno = input("DNI del alumno: ").strip()
                materias = listar_materias()
                if materias is None:
                    continue
                try:
                    materia_id = int(input("ID de materia: ").strip())
                    nueva_nota = float(input("Nota a agregar: ").strip())
                except ValueError:
                    print("Entrada inválida")
                    continue
                resultado = UsuarioDAO.agregar_nota(dni, dni_alumno, nueva_nota, materia_id)
                print(resultado.get('mensaje', resultado))
            elif opcion == '3':
                dni_alumno = input("DNI del alumno: ").strip()
                materias = listar_materias()
                if materias is None:
                    continue
                try:
                    materia_id = int(input("Seleccione ID de materia: ").strip())
                    nueva_nota = float(input("Nueva nota: ").strip())
                except ValueError:
                    print("Entrada inválida.")
                    continue
                resultado = UsuarioDAO.actualizar_nota(dni, dni_alumno, nueva_nota, materia_id)
                print(resultado.get('mensaje', resultado))
            elif opcion == '4':
                dni_alumno = input("DNI del alumno: ").strip()
                asistencias = UsuarioDAO.obtener_asistencias(dni_alumno)
                print(f"Asistencias alumno {dni_alumno}: {asistencias}")
            elif opcion == '5':
                dni_alumno = input("DNI del alumno: ").strip()
                materias = listar_materias()
                if materias is None:
                    continue
                presente = input("¿Presente? (s/n): ").lower() == 's'
                resultado = UsuarioDAO.registrar_asistencia(dni, dni_alumno, presente, materia_id)
                print(resultado.get('mensaje', resultado))
            elif opcion == '6':
                dni_alumno = input("DNI del alumno: ").strip()
                materias = listar_materias()
                if materias is None:
                    continue
                try:
                    materia_id = int(input("Seleccione ID de materia: ").strip())
                    presente = input("¿Presente? (s/n): ").lower() == 's'
                except ValueError:
                    print("Entrada inválida.")
                    continue
                resultado = UsuarioDAO.modificar_asistencia(dni, dni_alumno, materia_id, presente)
                print(resultado.get('mensaje', resultado))
            elif opcion == '7':
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")

    elif usuario.rol == 'admin':
        while True:
            print(MENU_ADMIN)
            opcion = input("Seleccione una opción: ").strip()
            if opcion == '1':
                # creación de usuario
                pass
            # ... otras opciones
            elif opcion == '6':
                dni_alumno = input("DNI del alumno: ").strip()
                materias = listar_materias()
                if materias is None:
                    continue
                try:
                    materia_id = int(input("Seleccione ID de materia: ").strip())
                    nueva_nota = float(input("Nota a agregar: ").strip())
                except ValueError:
                    print("Entrada inválida.")
                    continue
                resultado = UsuarioDAO.agregar_nota(dni, dni_alumno, nueva_nota, materia_id)
                print(resultado.get('mensaje', resultado))
            elif opcion == '11':
                break
            else:
                print("Opción inválida.")

if __name__ == '__main__':
    main()
