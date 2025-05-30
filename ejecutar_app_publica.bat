@echo off
title Flask + Ngrok + VirtualEnv

REM Iniciar ngrok
cd /d D:\apps\ngrok-v3-stable-windows-amd64
start cmd /k ".\ngrok http 5000"

REM Activar entorno virtual y ejecutar Flask
cd /d D:\apps\ProjectoEcuelas
call .venv\Scripts\activate.bat
start cmd /k "flask run --host=0.0.0.0 --port=5000"
