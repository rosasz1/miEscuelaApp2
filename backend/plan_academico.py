import logging
from backend.conexion import Conexion
from collections import defaultdict

class PlanAcademicoDAO:

    @staticmethod
    def obtener_anios():
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, nombre FROM anio ORDER BY id")
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener años: {e}")
            return []

    @staticmethod
    def obtener_cursos_con_anio():
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT c.id, c.nombre, c.anio_id
                        FROM cursos c
                    """)
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener cursos con año: {e}")
            return []

    @staticmethod
    def obtener_horarios_por_curso(curso_id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT m.id, m.nombre, h.dia, h.hora_inicio, h.hora_fin
                        FROM horarios h
                        JOIN materias m ON h.materia_id = m.id
                        WHERE h.curso_id = %s
                        ORDER BY
                          CASE 
                            WHEN h.dia = 'Lunes' THEN 1
                            WHEN h.dia = 'Martes' THEN 2
                            WHEN h.dia = 'Miércoles' THEN 3
                            WHEN h.dia = 'Jueves' THEN 4
                            WHEN h.dia = 'Viernes' THEN 5
                            ELSE 6
                          END,
                          h.hora_inicio
                    """, (curso_id,))
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener horarios por curso: {e}")
            return []

    @staticmethod
    def obtener_materias():
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, nombre FROM materias ORDER BY nombre")
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener materias: {e}")
            return []

    @staticmethod
    def obtener_materias_estructuradas():
        estructura = defaultdict(lambda: defaultdict(list))
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                            SELECT m.id, m.nombre, a.nombre, c.nombre, m.curso_id
                            FROM materias m
                            JOIN cursos c ON m.curso_id = c.id
                            JOIN anio a ON c.anio_id = a.id
                            ORDER BY a.id, c.nombre, m.nombre
                        """)
                    resultados = cursor.fetchall()
                    for materia_id, nombre, anio, curso, curso_id in resultados:
                        estructura[anio][curso].append({
                            "id": materia_id,
                            "nombre": nombre,
                            "curso_id": curso_id
                        })
        except Exception as e:
            logging.error(f"Error al obtener materias estructuradas: {e}")
        return estructura

    @staticmethod
    def obtener_cursos_completos():
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT c.id, c.nombre, c.anio_id
                        FROM cursos c
                        ORDER BY c.anio_id, c.nombre
                    """)
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener cursos completos: {e}")
            return []

    @staticmethod
    def obtener_materias_por_curso(curso_id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT m.id, m.nombre, c.nombre, a.nombre
                        FROM materias m
                        JOIN cursos c ON m.curso_id = c.id
                        JOIN anios a ON c.anio_id = a.id
                        WHERE c.id = %s
                    """, (curso_id,))
                    rows = cursor.fetchall()

                    estructura = defaultdict(lambda: defaultdict(list))
                    for materia_id, materia_nombre, curso_nombre, anio_nombre in rows:
                        estructura[anio_nombre][curso_nombre].append({
                            "id": materia_id,
                            "nombre": materia_nombre
                        })
                    return estructura
        except Exception as e:
            logging.error(f"Error al obtener materias por curso: {e}")
            return defaultdict(lambda: defaultdict(list))

    @staticmethod
    def obtener_cursos_por_profesor(profesor_id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT DISTINCT c.id, c.nombre, c.anio_id
                        FROM cursos c
                        JOIN materias m ON m.curso_id = c.id
                        WHERE m.profesor_id = %s
                        ORDER BY c.anio_id, c.nombre
                    """, (profesor_id,))
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener cursos del profesor {profesor_id}: {e}")
            return []

    @staticmethod
    def insertar_curso_con_materia_para_profesor(profesor_id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    # Insertar curso de prueba (si no existe ya uno con mismo nombre)
                    cursor.execute("""
                        INSERT INTO cursos (nombre, anio_id)
                        VALUES ('Curso de Prueba', 1)
                        RETURNING id
                    """)
                    curso_id = cursor.fetchone()[0]

                    # Insertar materia asociada
                    cursor.execute("""
                        INSERT INTO materias (nombre, curso_id, profesor_id)
                        VALUES ('Materia de Prueba', %s, %s)
                        RETURNING id
                    """, (curso_id, profesor_id))
                    materia_id = cursor.fetchone()[0]

                    # Insertar horario de prueba (lunes 8:00 a 10:00)
                    cursor.execute("""
                        INSERT INTO horarios (curso_id, materia_id, dia, hora_inicio, hora_fin)
                        VALUES (%s, %s, 'Lunes', '08:00', '10:00')
                    """, (curso_id, materia_id))

                    return curso_id
        except Exception as e:
            logging.error(f"Error al insertar curso de prueba para profesor {profesor_id}: {e}")
            return None

    @staticmethod
    def obtener_usuarios_por_rol_y_curso(rol, curso_id):
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, nombre, apellido
                        FROM usuarios
                        WHERE rol = %s AND curso_id = %s
                    """, (rol, curso_id))
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener usuarios por rol y curso: {e}")
            return []

