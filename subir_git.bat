@echo off
echo ===========================
echo    SUBIDA A GITHUB
echo ===========================

REM Activar entorno virtual
call .venv\Scripts\activate

REM Mostrar rama actual
for /f "delims=" %%i in ('git branch --show-current') do set branch=%%i
echo Rama actual: %branch%

REM Pedir mensaje de commit
set /p msg=📝 Escribí tu mensaje de commit:
echo.

REM Ejecutar comandos Git
git add .
git commit -m "%msg%"
git push origin %branch%

echo.
echo ✅ Cambios subidos a GitHub correctamente.
pause

