import tkinter as tk
from tkinter import ttk, messagebox
import time

from gemini_v_2.core.components.video_panel import VideoPanel
from gemini_v_2.core.components.metrics_panel import MetricsPanel
from gemini_v_2.core.components.control_panel import ControlPanel
from gemini_v_2.core.camera import CameraCapture
from gemini_v_2.core.detector import EmotionDetector

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("🐢 Detector de Emociones con Gemini AI")
        self.geometry("1100x650")
        self.resizable(False, False)
        
        # Variables de estado
        self.camera = CameraCapture()
        self.detector = EmotionDetector()
        self.is_capturing = False
        self.start_time = None
        
        # Crear la interfaz
        self._create_widgets()
        
        # Iniciar cámara automáticamente
        self._init_camera()
        
        # Vincular cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _init_camera(self):
        """Inicia la cámara al abrir la aplicación"""
        print("📹 Inicializando cámara...")
        success = self.camera.start()
        if success:
            print("✅ Cámara iniciada")
            self._preview_camera()
        else:
            print("❌ Error al iniciar cámara")
            self.video_panel.show_message("❌ Error: No se pudo acceder a la cámara")
    
    def _preview_camera(self):
        """Muestra preview de la cámara sin capturar"""
        if not self.camera.is_running():
            return
        
        frame = self.camera.get_frame()
        
        if frame is not None:
            self.video_panel.update_frame(frame)
        
        if not self.is_capturing:
            self.after(30, self._preview_camera)

    def _create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        main_frame.columnconfigure(0, weight=7)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(0, weight=1)
        
        # Panel de video
        self.video_panel = VideoPanel(main_frame, width=640, height=480)
        self.video_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Panel de métricas
        self.metrics_panel = MetricsPanel(main_frame)
        self.metrics_panel.grid(row=0, column=1, sticky="nsew")
        
        # Panel de control
        self.control_panel = ControlPanel(self)
        self.control_panel.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
        
        # Conectar callbacks
        self.control_panel.set_callbacks(
            on_start=self._on_start,
            on_pause=self._on_pause,
            on_report=self._on_generate_report,
            on_exit=self._on_closing
        )

    def _on_start(self):
        """Callback cuando se presiona Iniciar"""
        print("▶️ Iniciando captura...")
        
        if not self.camera.is_running():
            success = self.camera.start()
            if not success:
                messagebox.showerror("Error", "No se pudo iniciar la cámara")
                return
        
        self.is_capturing = True
        self.start_time = time.time()
        self.detector.start_capture()
        
        self._update_frame()

    def _on_pause(self):
        """Callback cuando se presiona Pausar"""
        print("⏸️ Pausando captura...")
        self.is_capturing = False
        self.detector.stop_capture()
        
        # ✅ AGREGAR ESTO: Actualizar el estado del botón manualmente
        self.control_panel.is_running = False
        self.control_panel.start_pause_btn.configure(text="▶️ Iniciar")
        self.control_panel.report_btn.configure(state=tk.NORMAL)
        print("✅ Botón de reporte habilitado")

    def _on_generate_report(self):
        """Callback cuando se presiona Generar Reporte"""
        print("📊 Generando reporte...")
        
        try:
            report = self.detector.generate_report()
            
            # Mostrar reporte en ventana emergente
            report_window = tk.Toplevel(self)
            report_window.title("📊 Reporte de Emociones")
            report_window.geometry("600x500")
            
            # Text widget con scroll
            text_frame = ttk.Frame(report_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            scrollbar = ttk.Scrollbar(text_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
            text_widget.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=text_widget.yview)
            
            text_widget.insert(tk.END, report)
            text_widget.config(state=tk.DISABLED)
            
            # Botón cerrar
            ttk.Button(report_window, text="Cerrar", command=report_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n{str(e)}")

    def _on_closing(self):
        """Callback cuando se cierra la ventana"""
        print("🚪 Cerrando aplicación...")
        self.is_capturing = False
        self.detector.stop_capture()
        self.camera.stop()
        self.destroy()

    def _update_frame(self):
        """Loop principal que actualiza el frame"""
        if not self.is_capturing:
            return
            
        frame = self.camera.get_frame()
        
        if frame is not None:
            # Procesar con detector
            processed_frame, metrics, emotion = self.detector.process_frame(frame)
            
            # Actualizar video
            self.video_panel.update_frame(processed_frame)
            
            # Calcular tiempo transcurrido
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
            
            # Actualizar métricas
            self.metrics_panel.update_metrics(
                ear=metrics.get('ear', 0.0),
                mar=metrics.get('mar', 0.0),
                smile=metrics.get('smile', 0.0),
                emotion=emotion,
                elapsed_time=min(elapsed, 30)
            )
            
            # Detener automáticamente después de 30 segundos
            if elapsed >= 30:
                print("⏱️ 30 segundos completados, deteniendo captura...")
                self._on_pause()  # ✅ Ahora _on_pause() actualiza el botón
                return  # ✅ IMPORTANTE: No continuar el loop
        
        self.after(30, self._update_frame)

def run_core():
    """Función para iniciar la GUI"""
    app = MainWindow()
    app.mainloop()