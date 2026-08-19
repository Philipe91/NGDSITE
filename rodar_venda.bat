@echo off
title NGD - VENDA (porta 8000)
cd /d "C:\projetos\NGDSITE"

echo ============================================
echo   NGD - VERSAO COM VENDA ONLINE
echo ============================================
echo.
echo   Neste PC:  http://127.0.0.1:8000
echo   Na rede:   http://192.168.15.10:8000
echo.
echo   Feche esta janela para desligar o servidor.
echo ============================================
echo.

"C:\projetos\NGDSITE\venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000

pause
