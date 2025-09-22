@echo off
setlocal enabledelayedexpansion

echo ================================================
echo           PUBLICAR RELEASE EN GITHUB
echo ================================================
echo.

if "%1"=="" (
    echo ERROR: Debes proporcionar una version
    echo Uso: release.bat v1.0.0
    echo Ejemplo: release.bat v1.2.3
    pause
    exit /b 1
)

set VERSION=%1

echo Preparando release %VERSION%...
echo.

REM Verificar que estamos en un repositorio git
git status >nul 2>&1
if errorlevel 1 (
    echo ERROR: No estas en un repositorio Git
    pause
    exit /b 1
)

REM Verificar que no hay cambios sin commit
git diff --quiet
if errorlevel 1 (
    echo ERROR: Hay cambios sin hacer commit
    echo Por favor, haz commit de todos los cambios primero
    pause
    exit /b 1
)

REM Crear el tag
echo Creando tag %VERSION%...
git tag -a %VERSION% -m "Release %VERSION%"

if errorlevel 1 (
    echo ERROR: No se pudo crear el tag
    pause
    exit /b 1
)

REM Subir el tag a GitHub
echo Subiendo tag a GitHub...
git push origin %VERSION%

if errorlevel 1 (
    echo ERROR: No se pudo subir el tag a GitHub
    echo Eliminando tag local...
    git tag -d %VERSION%
    pause
    exit /b 1
)

echo.
echo ================================================
echo            RELEASE CREADO CON EXITO
echo ================================================
echo.
echo Tag %VERSION% creado y subido a GitHub
echo GitHub Actions construira automaticamente los archivos .exe
echo El release estara disponible en unos minutos en:
echo https://github.com/Kioys/KeepAwake/releases
echo.
pause