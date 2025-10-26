import cv2
import mediapipe as mp

print("Iniciando detector de puntos faciales")

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces = 1,
    refine_landmarks = True,
    min_detection_confidence= 0.5,
    min_tracking_confidence = 0.5
)

print("Mediapipe Face Mesh Cargando")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: No se pudo abrir la camara")
    exit()

print("✅ Cámara abierta")
print("📹 Presiona 'q' para salir")
print("🐢 Detectando puntos faciales lentamente pero con precisión...")

PUNTOS_OJOS = {
    'ojo_izq': [33, 133, 160, 159, 158, 157, 173],
    'ojo_der': [362, 263, 387, 386, 385, 384, 398]
}

PUNTOS_BOCA = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
PUNTOS_CEJAS = {
    'ceja_izq': [70, 63, 105, 66, 107], 
    'ceja_der': [336, 296, 334, 293, 300]  
}

while True:
    ret, frame = camera.read()

    if not ret:
        print("Error al capturar el frame")
        break

    height, width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        """
            La siguiente parte del codigo es la mas compleja
            Debido a que es el dibujo de los puntos y las mallas faciales
        
        """

        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image = frame, ## Imagen
                landmark_list = face_landmarks, ## Puntos para conectar
                connections = mp_face_mesh.FACEMESH_TESSELATION, ## Malla Triangular Completa
                landmark_drawing_spec = None, # No dibuja puntos individuales
                connection_drawing_spec = mp_drawing_styles.get_default_face_mesh_tesselation_style() # Usar el estulo predefinido
            )

            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections = mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec = None,
                connection_drawing_spec = mp_drawing_styles.get_default_face_mesh_contours_style()
            )
        
            for punto_idx in PUNTOS_OJOS['ojo_izq'] + PUNTOS_OJOS["ojo_der"]:
                punto = face_landmarks.landmark[punto_idx]
                x = int(punto.x * width)
                y = int(punto.y * height)

                cv2.circle(frame, (x,y), 2, (255,0,0), -1)
            
            for punto_idx in PUNTOS_BOCA:
                punto = face_landmarks.landmark[punto_idx]
                x = int(punto.x * width)
                y = int(punto.y * height)

                cv2.circle(frame, (x,y), 2, (0,0,255), -1)

            for punto_idx in PUNTOS_CEJAS['ceja_izq'] + PUNTOS_CEJAS['ceja_der']:
                    punto = face_landmarks.landmark[punto_idx]
                    x = int(punto.x * width)
                    y = int(punto.y * height)
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            nariz = face_landmarks.landmark[1]
            nariz_x = int(nariz.x + width)
            nariz_y = int(nariz.y + height)

            cv2.circle(frame, (nariz_x, nariz_y), 5, (255,255, 0), -1)
            cv2.putText(frame, "Nariz", (nariz_x + 10, nariz_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)
        
        cv2.putText(frame, "Rostro detectado con 468 puntos", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    else:
        cv2.putText(frame, "No se detecto ningun rostro", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    
    cv2.putText(frame, 'Presiona Q para salir', (10, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow("Detector de Puntos faciales", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Cerrando...")
        break

camera.release()
cv2.destroyAllWindows()
face_mesh.close()

