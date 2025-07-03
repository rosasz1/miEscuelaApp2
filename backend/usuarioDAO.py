
from backend.notas import NotasDAO
from backend.asistencias import AsistenciasDAO
from backend.conexion import Conexion
from backend.usuario import Usuario, Alumno, Profesor, Admin
from backend.seguridad import hashear_contraseña, verificar_contraseña
import logging

class UsuarioDAO:
    @staticmethod
    def obtener_usuario_por_dni(dni):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id, nombre, apellido, email, dni, rol
                        FROM public.usuarios
                        WHERE dni = %s
                        """,
                        (dni,)
                    )
                    row = cursor.fetchone()
                    if not row:
                        return None
                    _id, nombre, apellido, email, dni_db, rol = row
                    if rol == 'alumno':
                        return Alumno(_id, dni_db, nombre, apellido, email)
                    elif rol == 'profesor':
                        return Profesor(_id, dni_db, nombre, apellido, email)
                    elif rol == 'admin':
                        return Admin(_id, dni_db, nombre, apellido, email)
        except Exception as e:
            logging.error(f"Error al obtener usuario_por_dni: {e}")
        return None

    @staticmethod
    def login(dni, contraseña_plana):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, nombre, apellido, email, dni, rol, contraseña, curso_id
                        FROM usuarios
                        WHERE dni = %s
                    """, (dni,))
                    row = cursor.fetchone()
                    if not row:
                        return None

                    _id, nombre, apellido, email, dni_db, rol, contraseña_hash, curso_id = row

                    if not verificar_contraseña(contraseña_plana, contraseña_hash):
                        return None

                    if rol == 'alumno':
                        return Alumno(_id, dni_db, nombre, apellido, email, curso_id)
                    elif rol == 'profesor':
                        return Profesor(_id, dni_db, nombre, apellido, email)
                    elif rol == 'admin':
                        return Admin(_id, dni_db, nombre, apellido, email)

        except Exception as e:
            logging.error(f"Error en login: {e}")
            return None

    @staticmethod
    def crear_usuario(dni, nombre, apellido, email, rol, contraseña_plana):
        try:
            hash_pw = hashear_contraseña(contraseña_plana)
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO public.usuarios (dni, nombre, apellido, email, rol, contraseña)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (dni, nombre, apellido, email, rol, hash_pw)
                    )
                    conn.commit()
                    return {'mensaje': 'Usuario creado exitosamente'}
        except Exception as e:
            logging.error(f"Error al crear usuario: {e}")
            return {'mensaje': 'Error al crear usuario'}

    @staticmethod
    def obtener_notas(dni_alumno):
        try:
            return NotasDAO.obtener_notas(dni_alumno) or []
        except Exception as e:
            logging.error(f"Error al obtener notas: {e}")
            return []

    @staticmethod
    def agregar_nota(dni_editor, dni_alumno, nota, materia_id=None):
        try:
            editor = UsuarioDAO.obtener_usuario_por_dni(dni_editor)
            if not editor or not editor.tiene_permiso_para_modificar_notas():
                return {'mensaje': 'Permiso denegado'}
            return NotasDAO.agregar_nota(dni_alumno, nota, materia_id)
        except Exception as e:
            logging.error(f"Error al agregar nota: {e}")
            return {'mensaje': 'Error al agregar nota'}

    @staticmethod
    def actualizar_nota(dni_editor, dni_alumno, nueva_nota, materia_id=None):
        try:
            editor = UsuarioDAO.obtener_usuario_por_dni(dni_editor)
            if not editor or not editor.tiene_permiso_para_modificar_notas():
                return {'mensaje': 'Permiso denegado'}
            return NotasDAO.actualizar_nota(dni_alumno, nueva_nota, materia_id)
        except Exception as e:
            logging.error(f"Error al actualizar nota: {e}")
            return {'mensaje': 'Error al actualizar nota'}

    @staticmethod
    def eliminar_nota(dni_alumno, materia_id):
        return NotasDAO.eliminar_nota(dni_alumno, materia_id)


    @staticmethod
    def obtener_asistencias(dni_alumno):
        try:
            return AsistenciasDAO.obtener_asistencias(dni_alumno) or []
        except Exception as e:
            logging.error(f"Error al obtener asistencias: {e}")
            return []

    @staticmethod
    def registrar_asistencia(dni_editor, dni_alumno, presente=True, materia_id=None):
        try:
            editor = UsuarioDAO.obtener_usuario_por_dni(dni_editor)
            if not editor or not editor.tiene_permiso_para_modificar_asistencias():
                return {'mensaje': 'Permiso denegado'}
            return AsistenciasDAO.registrar_asistencia(editor, dni_alumno, presente, materia_id)
        except Exception as e:
            logging.error(f"Error al registrar asistencia: {e}")
            return {'mensaje': 'Error al registrar asistencia'}

    @staticmethod
    def modificar_asistencia(dni_editor, dni_alumno, materia_id, presente):
        try:
            editor = UsuarioDAO.obtener_usuario_por_dni(dni_editor)
            if not editor or not editor.tiene_permiso_para_modificar_asistencias():
                return {'mensaje': 'Permiso denegado'}
            return AsistenciasDAO.modificar_asistencia(editor, dni_alumno, materia_id, presente)
        except Exception as e:
            logging.error(f"Error al modificar asistencia: {e}")
            return {'mensaje': 'Error al modificar asistencia'}

    @staticmethod
    def obtener_notas_por_profesor(dni_profesor, dni_alumno):
        try:
            print("💥 ENTRÓ A obtener_notas_por_profesor")
            profesor = UsuarioDAO.obtener_usuario_por_dni(dni_profesor)
            if not profesor or profesor.rol != 'profesor':
                return []
            return NotasDAO.obtener_notas(dni_alumno)
        except Exception as e:
            logging.error(f"Error al obtener notas por profesor: {e}")
            return []

    @staticmethod
    def obtener_cursos():
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, nombre FROM cursos ORDER BY nombre")
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener cursos: {e}")
            return []

    @staticmethod
    def obtener_materias_asignadas_alumno(dni_alumno):
        try:
            print(f"Buscando materias para DNI: '{dni_alumno}'")  # PRINT
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT m.id, m.nombre
                        FROM materias m
                        JOIN usuarios u ON m.curso_id = u.curso_id
                        WHERE u.dni = %s AND u.rol = 'alumno'
                        ORDER BY m.nombre
                    """, (dni_alumno,))
                    materias = [{'id': row[0], 'nombre': row[1]} for row in cursor.fetchall()]
                    print(f"Materias encontradas: {materias}")  # PRINT
                    return materias
        except Exception as e:
            logging.error(f"Error al obtener materias asignadas al alumno: {e}")
            return []




