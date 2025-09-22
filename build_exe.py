#!/usr/bin/env python3
"""
Script de construcción para crear ejecutables de KeepAwake
"""

import subprocess
import sys
import os
import shutil

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("📦 Instalando dependencias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_exe(script_name, exe_name):
    """Construye un ejecutable con PyInstaller"""
    print(f"🔨 Construyendo {exe_name}...")
    
    cmd = [
        "pyinstaller",
        "--onefile",  # Un solo archivo
        "--noconsole",  # Sin ventana de consola (comentar si quieres ver la consola)
        "--name", exe_name,
        "--distpath", "dist",
        "--workpath", "build",
        "--specpath", "build",
        script_name
    ]
    
    # Para mantener la consola visible, usa esta línea en lugar de la anterior:
    # cmd = ["pyinstaller", "--onefile", "--name", exe_name, "--distpath", "dist", "--workpath", "build", "--specpath", "build", script_name]
    
    subprocess.check_call(cmd)

def clean_build_files():
    """Limpia archivos temporales de construcción"""
    print("🧹 Limpiando archivos temporales...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")

def main():
    print("=" * 60)
    print("🏗️  CONSTRUCTOR DE KEEP AWAKE")
    print("=" * 60)
    
    try:
        # Instalar dependencias
        install_dependencies()
        
        # Crear directorio dist si no existe
        os.makedirs("dist", exist_ok=True)
        
        # Construir ejecutables
        build_exe("keep_awake.py", "KeepAwake")
        build_exe("simple_keep_awake.py", "KeepAwake-Simple")
        
        # Limpiar archivos temporales
        clean_build_files()
        
        print("\n✅ ¡Construcción completada!")
        print("📁 Los ejecutables están en la carpeta 'dist/':")
        print("   • KeepAwake.exe - Versión completa")
        print("   • KeepAwake-Simple.exe - Versión simple")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la construcción: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()