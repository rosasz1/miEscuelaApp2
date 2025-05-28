from backend.conexion import Conexion
import logging

class NotasDAO:

    @staticmethod
    def obtener_notas(dni):
        """
        Devuelve una lista de notas con el nombre de la materia, p.ej.: ['Matematica (9.50)', 'Historia (8.00)', ...].
        """
        try:
            with Conexion.obtener_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT m.nombre AS materia_nombre, n.nota
                        FROM public.notas n
                        JOIN public.materias m ON n.materia_id = m.id
                        WHERE n.usuario_id = (
                            SELECT id FROM public.usuarios WHERE dni = %s
                        )
                        """,
                        (dni,)
                    )
                    filas = cursor.fetchall()
                    return [f"{materia} ({nota})" for materia, nota in filas] if filas else []
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
