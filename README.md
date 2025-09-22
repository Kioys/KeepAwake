# Keep Awake - Evitar Modo Suspensión

Este proyecto Python evita que tu computadora entre en modo suspensión simulando actividad muy sutil.

## 📥 Descarga Rápida (Archivos .exe)

**¿No tienes Python instalado?** ¡No hay problema!

### [📦 Descargar Última Versión](../../releases/latest)

- **KeepAwake.exe** - Versión completa con múltiples tipos de actividad
- **KeepAwake-Simple.exe** - Versión simple que solo mueve el mouse
- **KeepAwake-vX.X.X-Windows.zip** - Paquete completo con documentación

✅ **Sin instalación requerida** - Solo descarga y ejecuta  
✅ **Compatible con Windows 10/11**  
✅ **Completamente portable**

## 📁 Archivos incluidos

- **`keep_awake.py`** - Script principal con múltiples tipos de actividad simulada
- **`simple_keep_awake.py`** - Versión simple que solo mueve el mouse
- **`run_keep_awake.bat`** - Script por lotes para ejecutar fácilmente en Windows
- **`run_keep_awake_silent.vbs`** - Script VBScript completamente silencioso
- **`build_exe.py`** - Script para construir ejecutables localmente
- **`build_local.bat`** - Script de batch para construcción local
- **`release.bat`** - Script para crear releases automáticamente

## 🚀 Cómo usar

### ⚡ Opción 1: Archivos .exe (Recomendado para usuarios finales)

1. Ve a [Releases](../../releases/latest)
2. Descarga `KeepAwake.exe` o `KeepAwake-Simple.exe`
3. Ejecuta el archivo directamente
4. ¡Listo! Tu PC se mantendrá activa

### 🐍 Opción 2: Script Python (Para desarrolladores)

Primero instala las dependencias:
```bash
pip install -r requirements.txt
```

#### Script principal (recomendado)
```bash
python keep_awake.py
```

**Opciones de tiempo:**
- **Minutos completos**: `python keep_awake.py 1` (1 minuto), `python keep_awake.py 2` (2 minutos)
- **Fracciones de minuto**: `python keep_awake.py 0.5` (30 segundos), `python keep_awake.py 0.1` (6 segundos)
- **Valor por defecto**: 0.5 minutos (30 segundos) sin argumentos

**Ejemplos:**
```bash
python keep_awake.py 1     # Cada 1 minuto
python keep_awake.py 2     # Cada 2 minutos
python keep_awake.py 10    # Cada 10 minutos
python keep_awake.py 0.5   # Cada 30 segundos
python keep_awake.py 0.1   # Cada 6 segundos
python keep_awake.py 0.083 # Cada 5 segundos (mínimo)
```

#### Script simple
```bash
python simple_keep_awake.py
```
- Solo movimientos sutiles del mouse
- **Mismas opciones de tiempo** que el script principal
- Valor por defecto: 1 minuto

### 🪟 Opción 3: Scripts de Windows

#### Script por lotes (Windows)
Haz doble clic en `run_keep_awake.bat`

#### Script VBScript silencioso
Ejecuta `run_keep_awake_silent.vbs` haciendo doble clic

## ⏱️ Sistema de tiempos intuitivo

- **Números ≥ 1**: Se interpretan como **minutos**
  - `1` = 1 minuto (60 segundos)
  - `2` = 2 minutos (120 segundos)
  - `10` = 10 minutos (600 segundos)

- **Números < 1**: Se interpretan como **fracciones de minuto**
  - `0.5` = medio minuto (30 segundos)
  - `0.25` = cuarto de minuto (15 segundos)
  - `0.1` = 0.1 minutos (6 segundos)

## 🛡️ Características de seguridad

- **🔥 Hotkey Global: Ctrl+Alt+F10** - Cierra el programa desde cualquier lugar
- **FailSafe**: Mueve el mouse a la esquina superior izquierda para detener inmediatamente
- **Ctrl+C**: Detiene el programa de forma segura
- **Movimientos mínimos**: Solo 1-3 píxeles de movimiento
- **Actividades discretas**: Usa teclas que no afectan el trabajo (Scroll Lock)
- **Intervalo mínimo**: 5 segundos para evitar sobrecarga del sistema

## 🎯 Tipos de actividad simulada

El script principal incluye:
1. **Movimientos sutiles del mouse** (1-3 píxeles)
2. **Presión de Scroll Lock** (no afecta ninguna aplicación)
3. **Movimientos de vaivén** del cursor

## 🔧 Construcción de ejecutables

### Para desarrolladores que quieren crear sus propios .exe:

#### Construcción local:
```bash
# Usando Python
python build_exe.py

# Usando batch (Windows)
build_local.bat
```

#### Crear release automático:
```bash
# Hacer commit de todos los cambios primero
git add .
git commit -m "Preparar para release"

# Crear y publicar release
release.bat v1.0.0
```

## 🛠️ Dependencias

- `pyautogui` - Control del mouse y teclado
- `keyboard` - Hotkeys globales
- `pillow` - Requerido por pyautogui

## 📋 Instalación manual

```bash
git clone https://github.com/Kioys/KeepAwake.git
cd KeepAwake
pip install -r requirements.txt
python keep_awake.py
```