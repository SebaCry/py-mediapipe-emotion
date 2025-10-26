import cv2
import threading
from typing import Optional

class CameraCapture:
    def __init__(self, camera_index : int = 0):
        self.camera_index = camera_index
        self.cap : Optional[cv2.VideoCapture] = None
        self.frame = None
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()

    def start(self) -> bool:
        if self.running:
            return True
        
        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            print("Error: No se puede abrir la camara")
            return False
        
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        print("Camara iniciada correctamente")
        return True
    
    def _capture_loop(self):
        while self.running:
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()

                if ret:
                    with self.lock:
                        self.frame = frame

    def get_frame(self) -> bool:
        with self.lock:
            return self.frame.copy() if self.frame is not None else None
        
    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join(timeout=1.0)
        if self.cap:
            self.cap.release()
        print("Camara Detenida")

    def is_running(self) -> bool:
        return self.running