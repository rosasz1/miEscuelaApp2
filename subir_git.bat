@echo off
set /p msg=Escribí tu mensaje de commit: 
git add .
git commit -m "%msg%"
git push
pause
