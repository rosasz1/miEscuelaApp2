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
