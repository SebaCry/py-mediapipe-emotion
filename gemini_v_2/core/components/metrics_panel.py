import tkinter as tk
from tkinter import ttk

class MetricsPanel(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, relief = tk.RIDGE, borderwidth = 2)

        title = ttk.Label(self, text="Metricas en vivo", font=("Arial",12,"bold"))
        title.pack(pady=10)

        metrics_frame = ttk.Frame(self)
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        self.ear_var = tk.StringVar(value="0.00")
        self.mar_var = tk.StringVar(value="0.00")
        self.smile_var = tk.StringVar(value="0.00")
        self.emotion_var = tk.StringVar(value="NEUTRAL")
        self.time_var = tk.StringVar(value="0/30s")

        row = 0
        self._create_metric_row(metrics_frame, "EAR", self.ear_var, row)
        row += 1
        self._create_metric_row(metrics_frame, "MAR", self.mar_var, row)
        row += 1
        self._create_metric_row(metrics_frame, "SONRISA", self.smile_var, row)
        row += 1

        ttk.Separator(metrics_frame, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=10
        )
        row += 1

        emotion_label = ttk.Label(
            metrics_frame,
            text = "Emocion Actual",
            font=("Arial",12,"bold")
        )
        emotion_label.grid(row=row, column=0, columnspan= 2)
        row += 1

        ttk.Separator(metrics_frame, orient=tk.HORIZONTAL).grid(
            row=row, column=0, sticky="ew", pady=10
        )
        row += 1

        time_label = ttk.Label(metrics_frame, text="⏱️ Tiempo:")
        time_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        
        time_value = ttk.Label(
            metrics_frame,
            textvariable=self.time_var,
            font=("Arial", 10, "bold")
        )
        time_value.grid(row=row, column=1, sticky=tk.E, pady=5)
        row += 1

        self.progress = ttk.Progressbar(
            metrics_frame,
            length=200,
            mode="determinate",
            maximum=30
        )
        self.progress.grid(row=row, column=0, columnspan=2, pady=10, sticky="ew")


    def _create_metric_row(self, parent, label_text : str, variable : tk.StringVar, row : int):
        label = tk.Label(parent, text=label_text, font=("Arial", 10))
        label.grid(row=row, column=0, sticky=tk.W, pady=5)

        value = ttk.Label(parent, textvariable=variable, font=("Arial", 10, "bold"))
        value.grid(row = row, column= 1, sticky=tk.E, pady=5)

    def update_metrics(self, ear : float, mar : float, smile : float, emotion : str, elapsed_time : int):
        self.ear_var.set(f"{ear:2f}")
        self.mar_var.set(f"{mar:2f}")
        self.smile_var.set(f"{smile:2f}")
        self.emotion_var.set(f"{emotion}")
        self.time_var.set(f"{elapsed_time:2f}")
        self.progress["value"] = elapsed_time


