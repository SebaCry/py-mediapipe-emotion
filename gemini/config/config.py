import os
# Suprimir logs de MediaPipe/TensorFlow ANTES de importar
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['GLOG_minloglevel'] = '2'

import mediapipe as mp
import google.generativeai as genai

#================Gemini Config==========================

GEMINI_API_KEY = "AIzaSyDt_S0JBKPf-6F9hOEGf1moS_xSp28p1x0"

genai.configure(api_key=GEMINI_API_KEY)

modelo_gemini = genai.GenerativeModel("gemini-2.0-flash")


#================MediaPipe Config==========================

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


