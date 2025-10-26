import time
from collections import Counter
from datetime import datetime
import threading
import cv2
import numpy as np

from gemini_v_2.core.config import face_mesh, mp_drawing, mp_face_mesh, mp_drawing_styles, modelo_gemini
from gemini_v_2.utils.face_processing import compute_metrics_from_landmarks
from gemini_v_2.utils.emotion_detection import detectar_emocion
from gemini_v_2.utils.visualization import draw_metrics

# ✅ ÍNDICES EXACTOS DE TU CÓDIGO ORIGINAL (gemini/utils.py)
DEFAULT_IDX = {
    "left_eye": [33, 160, 158, 133, 153, 144],      # OJO IZQUIERDO
    "right_eye": [362, 385, 387, 263, 373, 380],    # OJO DERECHO
    "mouth": [61, 291, 0, 17, 269, 405, 314, 17, 84, 181, 91, 146],  # BOCA
    "left_eyebrow": [70, 63, 105, 66, 107],         # CEJA IZQUIERDA
    "right_eyebrow": [336, 296, 334, 293, 300]      # CEJA DERECHA
}

DURACION_CAPTURA = 30  # segundos

class EmotionDetector:
    def __init__(self, idx=None):
        self.idx = idx or DEFAULT_IDX
        self.face_mesh = face_mesh
        self.counter = Counter()
        self.lock = threading.Lock()
        self.capturing = False
        self.start_ts = None
        
        # Almacenar todas las métricas durante la sesión
        self.datos_sesion = []
        self.ear_valores = []
        self.mar_valores = []
        self.sonrisa_valores = []
        self.cejas_valores = []

    def process_frame(self, frame_bgr):
        """Procesa un frame BGR y devuelve (frame_annotated, metrics, emotion)"""
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        h, w = frame_bgr.shape[:2]

        results = self.face_mesh.process(frame_rgb)
        emotion = "No face"
        emotion_color = (255, 255, 255)
        metrics = {"ear": 0.0, "mar": 0.0, "smile": 0.0, "eyebrow_pos": 0.0}

        if results and results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            
            # Calcular métricas
            metrics = compute_metrics_from_landmarks(face_landmarks, w, h, self.idx)

            # Detectar emoción
            emotion, emotion_color = detectar_emocion(
                metrics['ear'], 
                metrics['mar'], 
                metrics['smile'], 
                metrics['eyebrow_pos']
            )

            # Dibujar mesh de MediaPipe
            mp_drawing.draw_landmarks(
                frame_bgr, 
                face_landmarks, 
                mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )

            # Dibujar contornos
            mp_drawing.draw_landmarks(
                frame_bgr, 
                face_landmarks, 
                mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
            )

            # Guardar métricas si estamos capturando
            with self.lock:
                if self.capturing:
                    self.counter[emotion] += 1
                    self.datos_sesion.append({
                        'timestamp': time.time(),
                        'emotion': emotion,
                        'metrics': metrics.copy()
                    })
                    self.ear_valores.append(metrics['ear'])
                    self.mar_valores.append(metrics['mar'])
                    self.sonrisa_valores.append(metrics['smile'])
                    self.cejas_valores.append(metrics['eyebrow_pos'])

        # Dibujar métricas en el frame
        frame_bgr = draw_metrics(frame_bgr, metrics, emotion, emotion_color)

        return frame_bgr, metrics, emotion

    def start_capture(self):
        """Inicia la captura de emociones"""
        with self.lock:
            self.counter.clear()
            self.datos_sesion.clear()
            self.ear_valores.clear()
            self.mar_valores.clear()
            self.sonrisa_valores.clear()
            self.cejas_valores.clear()
            self.capturing = True
            self.start_ts = time.time()
        print("✅ Captura iniciada")

    def stop_capture(self):
        """Detiene la captura de emociones"""
        with self.lock:
            self.capturing = False
        print("⏸️ Captura detenida")

    def get_stats(self):
        """Obtiene estadísticas de emociones"""
        with self.lock:
            return dict(self.counter)

    def generate_report(self):
        """Genera reporte usando Gemini con las funciones correctas"""
        with self.lock:
            stats = dict(self.counter)
            datos_sesion = self.datos_sesion.copy()
            ear_valores = self.ear_valores.copy()
            mar_valores = self.mar_valores.copy()
            sonrisa_valores = self.sonrisa_valores.copy()
            cejas_valores = self.cejas_valores.copy()
        
        if not datos_sesion:
            return "❌ No hay datos para generar reporte. Ejecuta una captura primero."
        
        if modelo_gemini is None:
            return "❌ Gemini no está configurado. Verifica tu API_KEY en config.py"
        
        try:
            print("🤖 Generando análisis con Gemini...")
            
            # Generar prompt usando la función correcta
            prompt = self._give_prompt(
                np,
                DURACION_CAPTURA,
                datos_sesion,
                stats,
                ear_valores,
                mar_valores,
                sonrisa_valores,
                cejas_valores
            )
            
            # Llamar a Gemini correctamente
            response = modelo_gemini.generate_content(prompt)
            reporte_gemini = response.text
            
            # Generar reporte final formateado
            reporte_final = self._reporte_emocional(
                datetime,
                np,
                DURACION_CAPTURA,
                datos_sesion,
                stats,
                ear_valores,
                mar_valores,
                sonrisa_valores,
                cejas_valores,
                reporte_gemini
            )
            
            return reporte_final
            
        except Exception as e:
            return f"❌ Error al generar reporte: {str(e)}"

    def _give_prompt(
            self,
            np,
            DURACION_CAPTURA,
            datos_sesion,
            conteo_emociones,
            ear_valores,
            mar_valores,
            sonrisa_valores,
            cejas_valores
    ) -> str:
        """Genera el prompt para Gemini"""
        return f"""
Eres un psicólogo experto en análisis de expresiones faciales. Analiza los siguientes datos de una sesión de {DURACION_CAPTURA} segundos:

DATOS RECOPILADOS:
- Total de muestras: {len(datos_sesion)}
- Frecuencia de muestreo: aproximadamente cada 0.16 segundos

EMOCIONES DETECTADAS:
{dict(conteo_emociones)}

MÉTRICAS PROMEDIO:
- EAR (Apertura de ojos): Promedio={np.mean(ear_valores):.3f}, Min={np.min(ear_valores):.3f}, Max={np.max(ear_valores):.3f}
- MAR (Apertura de boca): Promedio={np.mean(mar_valores):.3f}, Min={np.min(mar_valores):.3f}, Max={np.max(mar_valores):.3f}
- Índice de sonrisa: Promedio={np.mean(sonrisa_valores):.2f}, Min={np.min(sonrisa_valores):.2f}, Max={np.max(sonrisa_valores):.2f}
- Posición de cejas: Promedio={np.mean(cejas_valores):.2f}, Min={np.min(cejas_valores):.2f}, Max={np.max(cejas_valores):.2f}

Por favor, genera un reporte profesional que incluya:

1. RESUMEN EJECUTIVO: Estado emocional general de la persona
2. ANÁLISIS DETALLADO: Interpretación de cada métrica y su significado
3. PATRONES IDENTIFICADOS: Cambios emocionales durante la sesión
4. OBSERVACIONES: Comportamientos destacables (parpadeo, tensión, etc.)
5. CONCLUSIONES: Evaluación del bienestar emocional
6. RECOMENDACIONES: Sugerencias basadas en los datos

Haz el reporte profesional pero amigable, como si fueras un psicólogo explicándole a un paciente.
"""

    def _reporte_emocional(
            self,
            datetime,
            np,
            DURACION_CAPTURA,
            datos_sesion,
            conteo_emociones,
            ear_valores,
            mar_valores,
            sonrisa_valores,
            cejas_valores,
            reporte
    ) -> str:
        """Formatea el reporte final"""
        return f"""
{'='*80}
REPORTE DE ANÁLISIS EMOCIONAL
{'='*80}

Fecha y hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Duración de la sesión: {DURACION_CAPTURA} segundos
Total de muestras analizadas: {len(datos_sesion)}

{'='*80}
DATOS ESTADÍSTICOS
{'='*80}

Distribución de emociones:
{chr(10).join([f"  - {emocion}: {cantidad} veces ({cantidad/len(datos_sesion)*100:.1f}%)" for emocion, cantidad in conteo_emociones.items()])}

Métricas faciales:
    EAR (Apertura de ojos):
        - Promedio: {np.mean(ear_valores):.3f}
        - Mínimo: {np.min(ear_valores):.3f}
        - Máximo: {np.max(ear_valores):.3f}
    
    MAR (Apertura de boca):
        - Promedio: {np.mean(mar_valores):.3f}
        - Mínimo: {np.min(mar_valores):.3f}
        - Máximo: {np.max(mar_valores):.3f}
    
    Índice de sonrisa:
        - Promedio: {np.mean(sonrisa_valores):.2f}
        - Mínimo: {np.min(sonrisa_valores):.2f}
        - Máximo: {np.max(sonrisa_valores):.2f}
    
    Posición de cejas:
        - Promedio: {np.mean(cejas_valores):.2f}
        - Mínimo: {np.min(cejas_valores):.2f}
        - Máximo: {np.max(cejas_valores):.2f}

{'='*80}
ANÁLISIS GENERADO POR GEMINI AI
{'='*80}

{reporte}

{'='*80}
FIN DEL REPORTE
{'='*80}
"""