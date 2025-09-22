@echo off
echo ================================================
echo          CONSTRUCCION LOCAL DE KEEPAWAKE
echo ================================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo.
echo Construyendo ejecutables...

REM Crear directorio dist si no existe
if not exist "dist" mkdir dist

REM Construir versión completa con consola
echo Construyendo KeepAwake.exe...
pyinstaller --onefile --console --name "KeepAwake" keep_awake.py

REM Construir versión simple con consola
echo Construyendo KeepAwake-Simple.exe...
pyinstaller --onefile --console --name "KeepAwake-Simple" simple_keep_awake.py

REM Limpiar archivos temporales
echo Limpiando archivos temporales...
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.spec" del "*.spec"

echo.
echo ================================================
echo        CONSTRUCCION COMPLETADA CON EXITO
echo ================================================
echo.
echo Los archivos .exe estan en la carpeta 'dist':
echo   - KeepAwake.exe (Version completa)
echo   - KeepAwake-Simple.exe (Version simple)
echo.
pause