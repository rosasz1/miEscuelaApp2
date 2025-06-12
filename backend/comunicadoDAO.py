from backend.conexion import Conexion
from datetime import datetime

class ComunicadoDAO:

    @staticmethod
    def crear_comunicado(emisor_id, receptor_id, mensaje):
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO public.comunicados (emisor_id, receptor_id, mensaje)
                    VALUES (%s, %s, %s)
                """, (emisor_id, receptor_id, mensaje))
                conn.commit()
        return {"ok": True, "mensaje": "Comunicado enviado correctamente."}

    @staticmethod
    def obtener_comunicados_recibidos(usuario_id):
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT c.id, u.nombre, u.apellido, c.mensaje, c.fecha_envio, c.leido, c.respuesta
                    FROM public.comunicados c
                    JOIN public.usuarios u ON u.id = c.emisor_id
                    ORDER BY c.fecha_envio DESC
                """)
                return cursor.fetchall()

    @staticmethod
    def responder_comunicado(comunicado_id, respuesta):
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE public.comunicados
                    SET respuesta = %s, fecha_respuesta = %s
                    WHERE id = %s
                """, (respuesta, datetime.now(), comunicado_id))
                conn.commit()
        return {"ok": True, "mensaje": "Respuesta enviada correctamente."}

    @staticmethod
    def marcar_como_leido(comunicado_id):
        with Conexion.obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE public.comunicados
                    SET leido = TRUE
                    WHERE id = %s
                """, (comunicado_id,))
                conn.commit()
