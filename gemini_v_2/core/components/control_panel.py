import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

class ControlPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.on_start : Optional[Callable] = None
        self.on_pause : Optional[Callable] = None
        self.on_report : Optional[Callable] = None
        self.on_exit : Optional[Callable] = None

        self.is_running = False

        button_frame = ttk.Frame(self)
        button_frame.pack(expand=True)

        self.start_pause_btn = ttk.Button(
            button_frame,
            text="▶️ Iniciar",
            command=self._toggle_start_pause,
            width=15
        )
        self.start_pause_btn.pack(side=tk.LEFT, padx=5,pady=10)

        self.report_btn = ttk.Button(
            button_frame,
            text = "📊 Generar Reporte",
            command=self._on_report_click,
            width=20,
            state = tk.DISABLED
        )
        self.report_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.exit_btn = ttk.Button(
            button_frame,
            text="🚪 Salir",
            command=self._on_exit_click,
            width=15
        )
        self.exit_btn.pack(side=tk.LEFT, padx=5, pady=10)

    def _toggle_start_pause(self):
        if self.is_running:
            # Está corriendo → Pausar
            if self.on_pause:
                self.on_pause()
            self.is_running = False
            self.start_pause_btn.configure(text="▶️ Iniciar")
            self.report_btn.configure(state=tk.NORMAL)  # ✅ HABILITAR cuando pausa
        else:
            # Está pausado → Iniciar
            if self.on_start:
                self.on_start()
            self.is_running = True
            self.start_pause_btn.configure(text="⏸️ Pausar")
            self.report_btn.configure(state=tk.DISABLED)  # ✅ DESHABILITAR cuando inicia

    def _on_report_click(self):
        # ✅ CAMBIO: No verificar is_running (ya está deshabilitado cuando corre)
        if self.on_report:
            self.on_report()

    def _on_exit_click(self):
        if self.on_exit:
            self.on_exit()

    def set_callbacks(self, on_start=None, on_pause=None, on_report=None, on_exit=None):
        """Conecta los callbacks desde el exterior"""
        if on_start:
            self.on_start = on_start
        if on_pause:
            self.on_pause = on_pause
        if on_report:
            self.on_report = on_report
        if on_exit:
            self.on_exit = on_exit
