@echo off
title NGD - Gerar catalogo em PDF
cd /d "C:\projetos\NGDPORTFOLIO"

echo ============================================
echo   GERANDO O CATALOGO EM PDF
echo ============================================
echo.
echo   Pega todos os produtos ATIVOS do site
echo   e monta o PDF com as fotos atuais.
echo.
echo   Pode demorar um minuto. Aguarde...
echo.

"C:\projetos\NGDPORTFOLIO\venv\Scripts\python.exe" gerar_catalogo_pdf.py

echo.
echo ============================================
echo   O arquivo Catalogo_NGD.pdf esta na pasta
echo   C:\projetos\NGDPORTFOLIO
echo ============================================
echo.
pause
