"""Script de entrada para ejecutar el detector de emociones"""
import sys
import os
import traceback

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Asegurar que el directorio actual está en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print(">>> Importando modulos...")
    from gemini_v_2.core.main_window import run_core
    print(">>> Modulos importados correctamente")
    print(">>> Iniciando programa...")
    run_core()
except Exception as e:
    print(f"\n>>> ERROR FATAL: {e}")
    print("\n>>> Traceback completo:")
    traceback.print_exc()
    input("\nPresiona Enter para salir...")
