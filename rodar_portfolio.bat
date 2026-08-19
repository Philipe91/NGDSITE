@echo off
title NGD - PORTFOLIO (porta 8001)
cd /d "C:\projetos\NGDPORTFOLIO"

echo ============================================
echo   NGD - VERSAO PORTFOLIO (vitrine/orcamento)
echo ============================================
echo.
echo   Neste PC:  http://127.0.0.1:8001
echo   Na rede:   http://192.168.15.10:8001
echo.
echo   Feche esta janela para desligar o servidor.
echo ============================================
echo.

"C:\projetos\NGDPORTFOLIO\venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8001

pause
