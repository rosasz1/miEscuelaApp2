@echo off
echo ===========================
echo   SUBIDA A GITHUB - ProyectoEscuelas
echo ===========================

set /p msg=📝 Escribí tu mensaje de commit:
echo.

git add .
git commit -m "%msg%"
git push origin main

echo.
echo ✅ Cambios subidos correctamente a GitHub.
pause
