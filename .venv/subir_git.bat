@echo off
git config user.name "rosasz1"
git config user.email "agusrosasmoncada408@gmail.com"
echo Escribí tu mensaje de commit:
set /p msg=
git add .
git commit -m "%msg%"
git pull origin master --rebase
git push origin master
pause
