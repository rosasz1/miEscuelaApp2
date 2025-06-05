@echo off
title Crear nuevo entorno virtual - ProyectoEscuelas

echo =============================
echo Eliminando entorno anterior...
echo =============================

rmdir /S /Q .venv

echo =============================
echo Creando nuevo entorno virtual...
echo =============================

python -m venv .venv

echo =============================
echo Activando entorno e instalando requirements...
echo =============================

call .venv\Scripts\activate.bat
pip install --upgrade pip

IF EXIST requirements.txt (
    pip install -r requirements.txt
) ELSE (
    echo No se encontró requirements.txt, se salta instalación de paquetes.
)

echo =============================
echo   ¡Todo listo bb!
echo =============================
pause
