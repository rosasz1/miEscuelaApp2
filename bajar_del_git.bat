
@echo off
title Actualizar Repo - MiEscuelaApp2

cd /d D:\apps\ProjectoEcuelas

REM Activar entorno virtual
call .venv\Scripts\activate.bat

echo =============================
echo  Verificando actualizaciones del repositorio...
echo =============================

REM Guardar la salida de git pull en una variable temporal
git pull > temp_git_output.txt

REM Mostrar la salida
type temp_git_output.txt

REM Buscar si ya estaba actualizado
findstr /C:"Already up to date." temp_git_output.txt > nul
if %errorlevel%==0 (
    echo =============================
    echo  ✅ Ya estás al día con el repo
    echo =============================
) else (
    echo =============================
    echo  🔄 Se bajaron cambios del repositorio
    echo =============================
)

REM Borrar el archivo temporal
del temp_git_output.txt

pause
