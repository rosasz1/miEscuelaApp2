from backend.conexion import Conexion
from datetime import date
import psycopg2
import logging

class AsistenciasDAO:

    @staticmethod
    def obtener_asistencias(dni):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    query = """
                        SELECT m.nombre, a.fecha, a.presente
                        FROM public.asistencias a
                        JOIN public.materias m ON a.materia_id = m.id
                        WHERE a.usuario_id = (SELECT id FROM public.usuarios WHERE dni = %s)
                        ORDER BY a.fecha DESC
                    """
                    cursor.execute(query, (dni,))
                    asistencias = cursor.fetchall()
                    return [
                        f"{materia} - {fecha} - {'Presente' if presente else 'Ausente'}"
                        for materia, fecha, presente in asistencias
                    ] if asistencias else []
        except Exception as e:
            logging.error(f"Error al obtener las asistencias: {e}")
            return []

    @staticmethod
    def registrar_asistencia(dni_alumno, presente=True, materia_id=1):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    # Verificar usuario
                    cursor.execute("SELECT id FROM usuarios WHERE dni = %s", (dni_alumno,))
                    resultado = cursor.fetchone()
                    if resultado is None:
                        return {"mensaje": "Usuario no encontrado"}
                    usuario_id = resultado[0]

                    # Verificar materia
                    cursor.execute("SELECT id FROM materias WHERE id = %s", (materia_id,))
                    if cursor.fetchone() is None:
                        return {"mensaje": "Materia no encontrada"}

                    # Insertar asistencia
                    cursor.execute("""
                        INSERT INTO asistencias (fecha, presente, usuario_id, materia_id)
                        VALUES (%s, %s, %s, %s)
                    """, (date.today(), presente, usuario_id, materia_id))
                    conn.commit()
                    return {"mensaje": "Asistencia registrada correctamente"}

        except psycopg2.DatabaseError as db_error:
            logging.error(f"Error en la base de datos al registrar asistencia: {db_error}")
            return {"mensaje": "Error al registrar asistencia"}
        except Exception as e:
            logging.error(f"Error al registrar asistencia: {e}")
            return {"mensaje": "Error al registrar asistencia"}

    @staticmethod
    def modificar_asistencia(dni_alumno, materia_id, presente):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id FROM asistencias
                        WHERE usuario_id = (SELECT id FROM usuarios WHERE dni = %s)
                        AND materia_id = %s
                        ORDER BY fecha DESC
                        LIMIT 1
                    """, (dni_alumno, materia_id))
                    asistencia = cursor.fetchone()

                    if asistencia is None:
                        return {'mensaje': 'No se encontró asistencia para modificar'}

                    asistencia_id = asistencia[0]

                    cursor.execute("""
                        UPDATE asistencias
                        SET presente = %s
                        WHERE id = %s
                    """, (presente, asistencia_id))
                    conn.commit()
                    return {'mensaje': 'Asistencia modificada exitosamente'}

        except Exception as e:
            logging.error(f"Error al modificar la asistencia: {e}")
            return {'mensaje': 'Error al modificar la asistencia'}



