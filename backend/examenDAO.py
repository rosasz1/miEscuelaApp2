from backend.conexion import Conexion
import logging

class ExamenDAO:

    @staticmethod
    def crear_examen(curso_id, materia_id, fecha, hora, titulo, dni):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO examenes (curso_id, materia_id, fecha, hora, titulo, creado_por_dni)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """, (curso_id, materia_id, fecha, hora, titulo, dni)
                    )
                    conn.commit()
                    return {"mensaje": "Examen creado correctamente"}
        except Exception as e:
            logging.error(f"Error al crear examen: {e}")
            return {"mensaje": "Error al crear examen"}

    @staticmethod
    def obtener_examenes_por_curso(curso_id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id, materia_id, fecha, hora, titulo
                        FROM examenes
                        WHERE curso_id = %s
                        ORDER BY fecha, hora
                        """, (curso_id,)
                    )
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener examenes: {e}")
            return []

    @staticmethod
    def modificar_examen(id, fecha, hora, titulo):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE examenes
                        SET fecha = %s, hora = %s, titulo = %s
                        WHERE id = %s
                        """, (fecha, hora, titulo, id)
                    )
                    conn.commit()
                    return {"mensaje": "Examen modificado correctamente"}
        except Exception as e:
            logging.error(f"Error al modificar examen: {e}")
            return {"mensaje": "Error al modificar examen"}

    @staticmethod
    def eliminar_examen(id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM examenes WHERE id = %s", (id,))
                    conn.commit()
                    return {"mensaje": "Examen eliminado correctamente"}
        except Exception as e:
            logging.error(f"Error al eliminar examen: {e}")
            return {"mensaje": "Error al eliminar examen"}

    @staticmethod
    def obtener_examenes_por_profesor(profesor_id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT m.nombre AS materia, c.nombre AS curso, e.fecha, e.hora, e.titulo
                        FROM examenes e
                        JOIN materias m ON e.materia_id = m.id
                        JOIN cursos c ON e.curso_id = c.id
                        WHERE m.profesor_id = %s
                        ORDER BY e.fecha, e.hora
                    """, (profesor_id,))
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener exámenes por profesor: {e}")
            return []

    @staticmethod
    def obtener_todos_los_examenes():
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT m.nombre, c.nombre, e.fecha, e.hora, e.titulo, e.creado_por_dni, e.id
                        FROM examenes e
                        JOIN materias m ON e.materia_id = m.id
                        JOIN cursos c ON e.curso_id = c.id
                        ORDER BY e.fecha, e.hora
                    """)
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener todos los exámenes: {e}")
            return []

    @staticmethod
    def obtener_examenes_por_curso(curso_id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT m.nombre, c.nombre, e.fecha, e.hora, e.titulo, e.creado_por_dni, e.id
                        FROM examenes e
                        JOIN materias m ON e.materia_id = m.id
                        JOIN cursos c ON e.curso_id = c.id
                        WHERE e.curso_id = %s
                        ORDER BY e.fecha, e.hora
                    """,(curso_id,))
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener exámenes por curso: {e}")
            return []

    @staticmethod
    def eliminar_examen_por_id(examen_id):
        with Conexion.obtener_conexion() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM examenes WHERE id = %s", (examen_id,))
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                return False
            finally:
                cursor.close()

    @staticmethod
    def obtener_examen_por_id(examen_id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT fecha, hora, titulo
                        FROM examenes
                        WHERE id = %s
                    """, (examen_id,))
                    return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error al obtener examen por ID: {e}")
            return None

    @staticmethod
    def obtener_examenes_por_profesor_y_curso(profesor_id, curso_id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT e.fecha, e.hora_inicio, m.nombre AS materia
                        FROM examenes e
                        JOIN materias m ON e.materia_id = m.id
                        WHERE e.profesor_dni = %s AND e.curso_id = %s
                    """, (profesor_id, curso_id))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener exámenes por profesor y curso: {e}")
            return []
