import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class VideoPanel(ttk.Frame):
    def __init__(self, parent, width : int = 640, height: int = 480):
        super().__init__(parent)
        self.width = width
        self.height = height

        self.video_label = ttk.Label(self, text="Esperando camara...")

        self.video_label.pack(fill=tk.BOTH, expand=True)

        self.current_image = None


    def update_frame(self, frame):
        if frame is None:
            return
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.width, self.height))

        pill_image = Image.fromarray(frame_resized)

        tk_image = ImageTk.PhotoImage(pill_image)

        self.video_label.configure(image=tk_image, text="")
        
        # Paso 6: Guardar referencia (importante!)
        self.current_image = tk_image

    def show_image(self, message : str):
        self.video_label.configure(image="", text=message)
        self.current_image = None
