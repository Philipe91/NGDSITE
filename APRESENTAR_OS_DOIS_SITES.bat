@echo off
title NGD - Apresentacao (VENDA + PORTFOLIO)

REM ================================================================
REM  Sobe os DOIS sites na rede local, pra comparar lado a lado:
REM     porta 8000 = versao VENDA (loja com carrinho e pagamento)
REM     porta 8001 = versao PORTFOLIO (vitrine + orcamento WhatsApp)
REM ================================================================

REM ---- Precisa de admin so na primeira vez, pra liberar o firewall ----
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Pedindo permissao de administrador para liberar as portas no firewall...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

REM ---- Regras de firewall: so rede privada, so a sua faixa de IP ----
netsh advfirewall firewall show rule name="NGD Site 8000" >nul 2>&1
if %errorlevel% neq 0 (
    netsh advfirewall firewall add rule name="NGD Site 8000" dir=in action=allow protocol=TCP localport=8000 profile=private remoteip=localsubnet >nul
    echo [OK] Porta 8000 liberada no firewall.
) else (
    echo [OK] Porta 8000 ja estava liberada.
)
netsh advfirewall firewall show rule name="NGD Site 8001" >nul 2>&1
if %errorlevel% neq 0 (
    netsh advfirewall firewall add rule name="NGD Site 8001" dir=in action=allow protocol=TCP localport=8001 profile=private remoteip=localsubnet >nul
    echo [OK] Porta 8001 liberada no firewall.
) else (
    echo [OK] Porta 8001 ja estava liberada.
)

REM ---- Derruba qualquer servidor velho preso nas portas ----
powershell -NoProfile -Command "8000,8001 ^| ForEach-Object { $p=(Get-NetTCPConnection -LocalPort $_ -State Listen -ErrorAction SilentlyContinue).OwningProcess; if($p){ $p ^| ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue } } }" >nul 2>&1

REM ---- Descobre o IP desta maquina na rede ----
for /f "delims=" %%i in ('powershell -NoProfile -Command "(Get-NetIPAddress -AddressFamily IPv4 ^| Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } ^| Select-Object -First 1).IPAddress"') do set IP=%%i

REM ---- Sobe os dois servidores em janelas separadas ----
start "NGD - VENDA (porta 8000)" cmd /k "cd /d C:\projetos\NGDSITE && venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000"
start "NGD - PORTFOLIO (porta 8001)" cmd /k "cd /d C:\projetos\NGDPORTFOLIO && venv\Scripts\python.exe manage.py runserver 0.0.0.0:8001"

cls
echo.
echo  ==================================================================
echo    NGD - OS DOIS SITES ESTAO NO AR
echo  ==================================================================
echo.
echo    VERSAO VENDA (loja completa, carrinho e pagamento):
echo         http://%IP%:8000
echo.
echo    VERSAO PORTFOLIO (vitrine, orcamento pelo WhatsApp):
echo         http://%IP%:8001
echo.
echo  ------------------------------------------------------------------
echo    Manda esses dois links pra quem vai ver do outro PC.
echo.
echo    Abriram DUAS janelas pretas, uma pra cada site.
echo    Enquanto elas estiverem abertas, os sites ficam no ar.
echo    Feche as duas para desligar.
echo  ==================================================================
echo.
pause
