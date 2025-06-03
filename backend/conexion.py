# -*- coding: utf-8 -*-

from psycopg2 import pool
import sys
from backend.logger_base import log
from contextlib import contextmanager

class Conexion:
    _DATABASE = 'postgres'
    _USERNAME = 'postgres'
    _PASSWORD = 'tinocastaldi1'
    _DB_PORT = '5432'
    _HOST = '127.0.0.1'
    _MIN_CON = 1
    _MAX_CON = 20
    _pool = None

    @classmethod
    def obtenerPool(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(cls._MIN_CON, cls._MAX_CON,
                                                       host=cls._HOST,
                                                       user=cls._USERNAME,
                                                       password=cls._PASSWORD,
                                                       port=cls._DB_PORT,
                                                       database=cls._DATABASE)
                log.debug(f'Creación del pool exitosa {cls._pool}')
                return cls._pool
            except Exception as e:
                log.error("Ocurrió un error al obtener el pool: %s", repr(e))

            sys.exit()
        else:
            return cls._pool

    @classmethod
    def obtenerConexion(cls):
        conexion = cls.obtenerPool().getconn()
        log.debug(f'Conexión obtenida del pool: {conexion}')
        return conexion

    @classmethod
    @contextmanager
    def obtener_conexion(cls):
        conexion = None
        try:
            conexion = cls.obtenerConexion()
            yield conexion
        finally:
            if conexion:
                cls.liberarConexion(conexion)

    @classmethod
    def liberarConexion(cls, conexion):
        cls.obtenerPool().putconn(conexion)
        log.debug(f'Regresamos la conexión al pool: {conexion}')

    @classmethod
    def cerrarConexion(cls):
        cls.obtenerPool().closeall()
