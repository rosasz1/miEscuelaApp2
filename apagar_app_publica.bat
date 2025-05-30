@echo off
title Apagar Flask y Ngrok

echo Cerrando servidores Flask y Ngrok...

REM Mata cualquier proceso llamado flask
taskkill /F /IM python.exe /T >nul 2>&1

REM Mata cualquier proceso llamado ngrok
taskkill /F /IM ngrok.exe /T >nul 2>&1

echo Servidor detenido correctamente.
pause
