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
                        return Alumno(dni_db, nombre, apellido, email)
                    elif rol == 'profesor':
                        return Profesor(dni_db, nombre, apellido, email)
                    elif rol == 'admin':
                        return Admin(dni_db, nombre, apellido, email)
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

                    from backend.seguridad import verificar_contraseña
                    if not verificar_contraseña(contraseña_plana, contraseña_hash):
                        return None

                    if rol == 'alumno':
                        alumno = Alumno(dni_db, nombre, apellido, email)
                        alumno.id = _id
                        alumno.curso_id = curso_id
                        return alumno
                    elif rol == 'profesor':
                        profesor = Profesor(dni_db, nombre, apellido, email)
                        profesor.id = _id
                        return profesor
                    elif rol == 'admin':
                        admin = Admin(dni_db, nombre, apellido, email)
                        admin.id = _id
                        return admin

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
    def modificar_usuario(dni, nombre, apellido, email, rol, contraseña_plana=None):
        try:
            params = [nombre, apellido, email, rol]
            set_clause = "nombre = %s, apellido = %s, email = %s, rol = %s"
            if contraseña_plana:
                hash_pw = hashear_contraseña(contraseña_plana)
                set_clause += ", contraseña = %s"
                params.append(hash_pw)
            params.append(dni)
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        f"UPDATE public.usuarios SET {set_clause} WHERE dni = %s",
                        tuple(params)
                    )
                    if cursor.rowcount == 0:
                        return {'mensaje': 'Usuario no encontrado'}
                    conn.commit()
                    return {'mensaje': 'Usuario modificado exitosamente'}
        except Exception as e:
            logging.error(f"Error al modificar usuario: {e}")
            return {'mensaje': 'Error al modificar usuario'}

    @staticmethod
    def eliminar_usuario(dni):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM public.usuarios WHERE dni = %s", (dni,))
                    if cursor.rowcount == 0:
                        return {'mensaje': 'Usuario no encontrado'}
                    conn.commit()
                    return {'mensaje': 'Usuario eliminado exitosamente'}
        except Exception as e:
            logging.error(f"Error al eliminar usuario: {e}")
            return {'mensaje': 'Error al eliminar usuario'}

    @staticmethod
    def asignar_profesor_a_materia(materia_id, profesor_dni):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, rol FROM public.usuarios WHERE dni = %s", (profesor_dni,))
                    row = cursor.fetchone()
                    if not row:
                        return {'mensaje': 'Profesor no encontrado'}
                    profesor_id, rol = row
                    if rol != 'profesor':
                        return {'mensaje': 'El DNI no corresponde a un profesor'}
                    cursor.execute("UPDATE public.materias SET profesor_id = %s WHERE id = %s", (profesor_id, materia_id))
                    if cursor.rowcount == 0:
                        return {'mensaje': 'Materia no encontrada'}
                    conn.commit()
                    return {'mensaje': 'Profesor asignado a materia exitosamente'}
        except Exception as e:
            logging.error(f"Error al asignar profesor a materia: {e}")
            return {'mensaje': 'Error al asignar profesor a materia'}

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
            profesor = UsuarioDAO.obtener_usuario_por_dni(dni_profesor)
            if not profesor or profesor.rol != 'profesor':
                return []
            return NotasDAO.obtener_notas(dni_alumno)
        except Exception as e:
            logging.error(f"Error al obtener notas por profesor: {e}")
            return []

    @staticmethod
    def obtener_materias_por_profesor(dni_profesor):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, nombre 
                        FROM public.materias 
                        WHERE profesor_id = (
                            SELECT id FROM public.usuarios WHERE dni = %s
                        )
                    """, (dni_profesor,))
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener materias por profesor: {e}")
            return []

    @staticmethod
    def obtener_materias_con_profesor():
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT m.id, m.nombre, u.nombre AS profesor_nombre
                        FROM public.materias m
                        LEFT JOIN public.usuarios u ON m.profesor_id = u.id
                        ORDER BY m.id
                    """)
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener materias con profesor: {e}")
            return []
