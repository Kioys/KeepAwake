#!/usr/bin/env python3
"""
Script para mantener la computadora activa y evitar que entre en modo suspensión.
Simula actividad muy sutil cada cierto tiempo.
"""

import pyautogui
import time
import random
import sys
import threading
import keyboard
import os
from datetime import datetime

class KeepAwake:
    def __init__(self, interval_seconds=30):
        """
        Inicializa el sistema para mantener la computadora activa.
        
        Args:
            interval_seconds (float): Intervalo en segundos entre actividades simuladas
        """
        self.interval = interval_seconds
        self.running = False
        self.hotkey_registered = False
        
        # Configurar pyautogui para ser más seguro
        pyautogui.FAILSAFE = False  # Mover el mouse a la esquina superior izquierda para parar
        pyautogui.PAUSE = 0.1
        
        # Establecer título de la ventana
        self.set_window_title()
        
    def set_window_title(self):
        """Establece un título personalizado para la ventana de la consola"""
        try:
            if os.name == 'nt':  # Windows
                window_title = f"KeepAwake - Mantener PC Activa (Intervalo: {self.interval}s)"
                os.system(f'title {window_title}')
            else:  # Linux/macOS
                window_title = f"KeepAwake - Mantener PC Activa (Intervalo: {self.interval}s)"
                print(f'\033]2;{window_title}\033\\', end='')
        except Exception as e:
            print(f"⚠️  No se pudo establecer el título de la ventana: {e}")
        
    def log_activity(self, activity_type):
        """Registra la actividad realizada con timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Actividad: {activity_type}")
        
    def setup_hotkey(self):
        """Configura el hotkey global Ctrl+Alt+F10 para cerrar el programa"""
        try:
            keyboard.add_hotkey('ctrl+alt+f10', self.stop_via_hotkey)
            self.hotkey_registered = True
            print("🔥 Hotkey configurado: Ctrl+Alt+F10 para cerrar")
        except Exception as e:
            print(f"⚠️  No se pudo configurar el hotkey: {e}")
            print("⚠️  Usa Ctrl+C o mouse en esquina superior izquierda para cerrar")
    
    def stop_via_hotkey(self):
        """Detiene el programa cuando se presiona el hotkey"""
        print("\n🔥 Hotkey detectado (Ctrl+Alt+F10) - Cerrando programa...")
        self.running = False
        
    def cleanup_hotkey(self):
        """Limpia el hotkey registrado"""
        if self.hotkey_registered:
            try:
                keyboard.remove_hotkey('ctrl+alt+f10')
                self.hotkey_registered = False
            except:
                pass

    def subtle_mouse_movement(self):
        """Realiza un movimiento muy sutil del mouse"""
        current_x, current_y = pyautogui.position()
        
        # Movimiento muy pequeño (1-3 píxeles)
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        
        new_x = current_x + offset_x
        new_y = current_y + offset_y
        
        # Asegurar que no salga de los límites de la pantalla
        screen_width, screen_height = pyautogui.size()
        new_x = max(0, min(new_x, screen_width - 1))
        new_y = max(0, min(new_y, screen_height - 1))
        
        pyautogui.moveTo(new_x, new_y, duration=0.1)
        self.log_activity(f"Movimiento de mouse: ({current_x},{current_y}) -> ({new_x},{new_y})")
        
    def press_scroll_lock(self):
        """Presiona la tecla Scroll Lock que normalmente no afecta nada"""
        pyautogui.press('scrolllock')
        pyautogui.press('scrolllock')  # La presiona dos veces para que regrese al estado original
        self.log_activity("Presión de tecla Scroll Lock")
        
    def wiggle_cursor(self):
        """Hace un pequeño movimiento de vaivén con el cursor"""
        current_x, current_y = pyautogui.position()
        
        # Movimiento de vaivén muy pequeño
        pyautogui.moveTo(current_x + 1, current_y, duration=0.05)
        pyautogui.moveTo(current_x - 1, current_y, duration=0.05)
        pyautogui.moveTo(current_x, current_y, duration=0.05)
        
        self.log_activity("Movimiento de vaivén del cursor")
        
    def perform_random_activity(self):
        """Realiza una actividad aleatoria para simular presencia"""
        activities = [
            self.subtle_mouse_movement,
            self.press_scroll_lock,
            self.wiggle_cursor
        ]
        
        activity = random.choice(activities)
        activity()
        
    def start(self):
        """Inicia el bucle para mantener la computadora activa"""
        self.running = True
        print("🟢 KeepAwake iniciado")
        print(f"📅 Intervalo: {self.interval} segundos")
        print("❌ Para detener:")
        print("   • Presiona Ctrl+Alt+F10 (desde cualquier lugar)")
        print("   • Presiona Ctrl+C (en esta ventana)")
        print("   • Mueve el mouse a la esquina superior izquierda")
        print("-" * 60)
        
        # Configurar hotkey en un hilo separado
        self.setup_hotkey()
        
        try:
            while self.running:
                self.perform_random_activity()
                
                # Esperar el intervalo especificado, pero revisar si debemos parar
                start_time = time.time()
                while (time.time() - start_time) < self.interval and self.running:
                    time.sleep(0.1)  # Revisar cada 100ms si debemos parar
                
        except pyautogui.FailSafeException:
            print("\n🛑 Detenido por FailSafe (mouse en esquina superior izquierda)")
        except KeyboardInterrupt:
            print("\n🛑 Detenido por el usuario (Ctrl+C)")
        finally:
            self.stop()
            
    def stop(self):
        """Detiene el sistema"""
        self.running = False
        self.cleanup_hotkey()
        print("🔴 KeepAwake detenido")

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

def main():
    """Función principal"""
    print("=" * 60)
    print("🖥️  KEEP AWAKE - Evitar Modo Suspensión")
    print("=" * 60)
    
    # Configuración por defecto: 0.5 minutos (30 segundos)
    default_minutes = 0.5
    interval_seconds = default_minutes * 60
    interval_display = f"{default_minutes} minutos"
    
    if len(sys.argv) > 1:
        try:
            interval_seconds, interval_display = parse_interval_argument(sys.argv[1])
        except ValueError as e:
            print(f"⚠️  Error: {e}")
            print(f"⚠️  Usando valor por defecto: {interval_display}")
    
    print(f"⏱️  Intervalo configurado: {interval_display} ({interval_seconds:.1f} segundos)")
    print()
    print("💡 Ejemplos de uso:")
    print("   python keep_awake.py 1     # 1 minuto")
    print("   python keep_awake.py 2     # 2 minutos") 
    print("   python keep_awake.py 0.5   # 30 segundos")
    print("   python keep_awake.py 0.1   # 6 segundos")
    print()
    
    keeper = KeepAwake(interval_seconds=interval_seconds)
    keeper.start()

if __name__ == "__main__":
    main()