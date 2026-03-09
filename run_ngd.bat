@echo off
REM Muda para o diretório raiz do projeto garantindo que o caminho com espaços seja interpretado corretamente
cd /d "C:\Users\Pc Fechamento\Documents\NGDSITE"

REM Ativa o ambiente virtual de forma silenciosa e com aspas para evitar erros de espaço no caminho
call "C:\Users\Pc Fechamento\Documents\NGDSITE\venv\Scripts\activate.bat" >nul 2>&1

REM Instala as dependências necessárias garantindo o uso do pip de dentro da venv
"C:\Users\Pc Fechamento\Documents\NGDSITE\venv\Scripts\python.exe" -m pip install django django-environ pillow psycopg2-binary python-dotenv --quiet

REM Roda as migrações forçando o uso do executável Python da venv para evitar ImportError
"C:\Users\Pc Fechamento\Documents\NGDSITE\venv\Scripts\python.exe" manage.py migrate

REM Inicia o servidor local forçando o executável Python da venv
"C:\Users\Pc Fechamento\Documents\NGDSITE\venv\Scripts\python.exe" manage.py runserver

pause
