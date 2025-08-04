#!/usr/bin/env python3
"""
Versión simple del script para mantener la computadora activa.
Solo usa movimientos sutiles del mouse.
"""

import pyautogui
import time
import random
import sys
import keyboard
from datetime import datetime

def parse_interval_argument(arg_str):
    """
    Convierte el argumento de entrada en segundos.
    - Números >= 1: se interpretan como minutos y se convierten a segundos
    - Números < 1: se interpretan como fracciones de minuto y se convierten a segundos
    
    Ejemplos:
    - 1 = 1 minuto = 60 segundos
    - 2 = 2 minutos = 120 segundos
    - 0.5 = 0.5 minutos = 30 segundos
    - 0.1 = 0.1 minutos = 6 segundos
    """
    try:
        value = float(arg_str)
        
        if value < 0:
            raise ValueError("El intervalo no puede ser negativo")
        
        # Si es menor a 1, se interpreta como fracción de minuto
        if value < 1:
            seconds = value * 60
            unit = f"{value} minutos"
        else:
            # Si es 1 o mayor, se interpreta como minutos completos
            seconds = value * 60
            unit = f"{int(value) if value.is_integer() else value} minutos"
        
        # Intervalo mínimo de 5 segundos
        if seconds < 5:
            print(f"⚠️  Intervalo mínimo: 5 segundos (0.083 minutos)")
            seconds = 5
            unit = "0.083 minutos (mínimo)"
        
        return seconds, unit
        
    except ValueError:
        raise ValueError(f"Valor inválido: '{arg_str}'. Use números como 1, 2, 0.5, etc.")

def simple_keep_awake(interval_seconds, interval_display):
    """
    Versión simple que solo mueve el mouse sutilmente.
    
    Args:
        interval_seconds (float): Segundos entre movimientos
        interval_display (str): Descripción del intervalo para mostrar
    """
    running = True
    hotkey_registered = False
    
    def stop_via_hotkey():
        nonlocal running
        print("\n🔥 Hotkey detectado (Ctrl+Alt+F10) - Cerrando programa...")
        running = False
    
    print("🟢 Keep Awake Simple - INICIADO")
    print(f"⏱️  Movimiento cada {interval_display} ({interval_seconds:.1f} segundos)")
    print("❌ Para detener:")
    print("   • Presiona Ctrl+Alt+F10 (desde cualquier lugar)")
    print("   • Presiona Ctrl+C (en esta ventana)")
    print("-" * 40)
    
    # Configurar hotkey
    try:
        keyboard.add_hotkey('ctrl+alt+f10', stop_via_hotkey)
        hotkey_registered = True
        print("🔥 Hotkey configurado: Ctrl+Alt+F10 para cerrar")
    except Exception as e:
        print(f"⚠️  No se pudo configurar el hotkey: {e}")
    
    pyautogui.FAILSAFE = True
    
    try:
        while running:
            # Obtener posición actual
            x, y = pyautogui.position()
            
            # Movimiento muy pequeño
            new_x = x + random.randint(-1, 1)
            new_y = y + random.randint(-1, 1)
            
            # Mover suavemente
            pyautogui.moveTo(new_x, new_y, duration=0.1)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Mouse movido: ({x},{y}) -> ({new_x},{new_y})")
            
            # Esperar con revisiones periódicas
            start_time = time.time()
            while (time.time() - start_time) < interval_seconds and running:
                time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🔴 Detenido por el usuario")
    except pyautogui.FailSafeException:
        print("\n🔴 Detenido por FailSafe")
    finally:
        # Limpiar hotkey
        if hotkey_registered:
            try:
                keyboard.remove_hotkey('ctrl+alt+f10')
            except:
                pass
        print("🔴 Keep Awake Simple detenido")

def main():
    """Función principal"""
    print("=" * 50)
    print("🖱️  KEEP AWAKE SIMPLE")
    print("=" * 50)
    
    # Configuración por defecto: 1 minuto (60 segundos)
    default_minutes = 1.0
    interval_seconds = default_minutes * 60
    interval_display = f"{int(default_minutes)} minuto"
    
    if len(sys.argv) > 1:
        try:
            interval_seconds, interval_display = parse_interval_argument(sys.argv[1])
        except ValueError as e:
            print(f"⚠️  Error: {e}")
            print(f"⚠️  Usando valor por defecto: {interval_display}")
    
    print(f"⏱️  Intervalo configurado: {interval_display}")
    print()
    print("💡 Ejemplos de uso:")
    print("   python simple_keep_awake.py 1     # 1 minuto")
    print("   python simple_keep_awake.py 2     # 2 minutos") 
    print("   python simple_keep_awake.py 0.5   # 30 segundos")
    print("   python simple_keep_awake.py 0.1   # 6 segundos")
    print()
    
    simple_keep_awake(interval_seconds, interval_display)

if __name__ == "__main__":
    main()