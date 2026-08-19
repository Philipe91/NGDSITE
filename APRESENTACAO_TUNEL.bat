@echo off
title NGD - Apresentacao com Tunnel
cd /d "%~dp0"

echo.
echo  ============================================================
echo    NGD GRAFICA - MODO APRESENTACAO (link publico)
echo  ============================================================
echo.
echo  [1/2] Iniciando servidor Django em background...
start "NGD Server" /min cmd /c "venv\Scripts\python.exe manage.py runserver 8000"

echo  Aguardando o servidor subir (6 segundos)...
timeout /t 6 /nobreak >nul

echo.
echo  [2/2] Criando o link publico (Cloudflare Tunnel)...
echo.
echo  ============================================================
echo   COPIE a URL que aparecer abaixo (termina em
echo   .trycloudflare.com) e envie para o seu chefe.
echo.
echo   O link funciona enquanto esta janela estiver aberta.
echo   Para encerrar: feche esta janela.
echo  ============================================================
echo.
cloudflared.exe tunnel --url http://localhost:8000

pause
