from backend.conexion import Conexion
import logging

class NotasDAO:

    @staticmethod
    def obtener_notas(dni_alumno):
        """
        Devuelve una lista de dicts: [{'materia_id':..., 'materia_nombre':..., 'valor':...}, ...]
        """
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT n.materia_id, m.nombre AS materia_nombre, n.nota
                        FROM public.notas n
                        JOIN public.materias m ON n.materia_id = m.id
                        WHERE n.usuario_id = (
                            SELECT id FROM public.usuarios WHERE dni = %s
                        )
                        """,
                        (dni_alumno,)
                    )
                    filas = cursor.fetchall()
                    return [
                        {'materia_id': row[0], 'materia_nombre': row[1], 'valor': row[2]}
                        for row in filas
                    ]
        except Exception as e:
            logging.error(f"Error al obtener las notas: {e}")
            return []

    @staticmethod
    def agregar_nota(dni_alumno, nota, materia_id):
        """
        Agrega una nueva nota para el alumno, permitiendo múltiples notas por materia.
        """
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    # Obtener usuario_id
                    cursor.execute(
                        "SELECT id FROM public.usuarios WHERE dni = %s",
                        (dni_alumno,)
                    )
                    res_usuario = cursor.fetchone()
                    if not res_usuario:
                        return {'mensaje': 'Alumno no encontrado'}
                    usuario_id = res_usuario[0]

                    # Verificar que la materia exista
                    cursor.execute(
                        "SELECT id FROM public.materias WHERE id = %s",
                        (materia_id,)
                    )
                    if not cursor.fetchone():
                        return {'mensaje': 'Materia no encontrada'}

                    # Insertar nueva nota sin validar duplicados
                    cursor.execute(
                        "INSERT INTO public.notas (usuario_id, nota, materia_id) VALUES (%s, %s, %s)",
                        (usuario_id, nota, materia_id)
                    )
                    conn.commit()
                    return {'mensaje': 'Nota agregada exitosamente'}
        except Exception as e:
            logging.error(f"Error al agregar la nota: {e}")
            return {'mensaje': 'Error al agregar la nota'}

    @staticmethod
    def actualizar_nota(dni_alumno, nueva_nota, materia_id):
        """
        Actualiza la nota existente para el alumno y materia especificados.
        """
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE public.notas
                        SET nota = %s
                        WHERE usuario_id = (
                            SELECT id FROM public.usuarios WHERE dni = %s
                        )
                          AND materia_id = %s
                        """,
                        (nueva_nota, dni_alumno, materia_id)
                    )
                    if cursor.rowcount == 0:
                        return {'mensaje': 'No existe nota previa para actualizar'}
                    conn.commit()
                    return {'mensaje': 'Nota actualizada exitosamente'}
        except Exception as e:
            logging.error(f"Error al actualizar la nota: {e}")
            return {'mensaje': 'Error al actualizar la nota'}

    @staticmethod
    def eliminar_nota(dni_alumno, materia_id):
        """
        Elimina la nota para el alumno y materia especificados.
        """
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM public.notas
                        WHERE usuario_id = (
                            SELECT id FROM public.usuarios WHERE dni = %s
                        ) AND materia_id = %s
                        """,
                        (dni_alumno, materia_id)
                    )
                    if cursor.rowcount == 0:
                        return {'mensaje': 'No existe nota previa para eliminar'}
                    conn.commit()
                    return {'mensaje': 'Nota eliminada exitosamente'}
        except Exception as e:
            logging.error(f"Error al eliminar la nota: {e}")
            return {'mensaje': 'Error al eliminar la nota'}

