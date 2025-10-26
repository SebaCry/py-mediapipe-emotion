import cv2
import mediapipe as mp
import numpy as np

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

def calcular_distancia(punto1, punto2):
    return np.sqrt((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)

def calcular_EAR(ojo_puntos):
    ''' 
        EAR = Eye Aspect Ratio (EAR)
        Valores típicos:
            - EAR > 0.25: Ojo abierto
            - EAR < 0.20: Ojo cerrado/guiño
    '''

    vertical_1 = calcular_distancia(ojo_puntos[1], ojo_puntos[5])
    vertical_2 = calcular_distancia(ojo_puntos[2], ojo_puntos[4])

    horizontal = calcular_distancia(ojo_puntos[0], ojo_puntos[3])

    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)

    return ear
    

def calcular_MAR(boca_puntos):
    '''
        Mouth Aspect Ratio (MAR) 
        Valores típicos:
            - MAR < 0.3: Boca cerrada
            - MAR 0.3-0.6: Boca ligeramente abierta (hablando/sonriendo)
            - MAR > 0.6: Boca muy abierta (sorpresa/grito)
    '''

    vertical = calcular_distancia(boca_puntos[2], boca_puntos[6])

    horizontal = calcular_distancia(boca_puntos[0], boca_puntos[4])

    mar = vertical / horizontal

    return mar


def calcular_sonrisa(boca_puntos):
    """
    Calcula el índice de sonrisa basado en la curvatura de la boca
    
    Compara la altura de las comisuras con el centro de la boca:
    - Valor positivo: Sonrisa (comisuras arriba)
    - Valor negativo: Tristeza (comisuras abajo)
    - Cercano a 0: Neutral
    """
    comisura_izq = boca_puntos[0]
    
    comisura_der = boca_puntos[4]
    
    centro_boca = boca_puntos[6]
    
    altura_comisuras = (comisura_izq[1] + comisura_der[1]) / 2
    
    sonrisa = centro_boca[1] - altura_comisuras
    
    return sonrisa

def calcular_posicion_cejas(cejas_puntos, ojos_puntos):

    centro_cejas = np.mean(cejas_puntos, axis=0)

    centro_ojos = np.mean(ojos_puntos, axis=0)

    distancia = centro_cejas[1] - centro_ojos[1]

    return distancia

def detectar_emocion(ear_promedio, mar, sonrisa, posicion_cejas):

    if mar > 0.6 and posicion_cejas < -15:
        return "Sorpresa 😲", (0, 165, 255)
    
    if sonrisa > 5 and ear_promedio > 0.2:
        return "Feliz 😊", (0, 255, 0)
    
    if sonrisa < -3:
        return "Triste 😢", (0,0,255)
    
    if posicion_cejas > -5 and mar < 0.2:
        return "Enojado 😠", (0, 0, 255)
    
    
    if ear_promedio < 0.18:
        return "Ojos cerrados 😴", (128, 128, 128) 
    
    # NEUTRAL
    return "Neutral 😐", (255, 255, 255)

OJO_IZQ_IDX = [33, 160, 158, 133, 153, 144]

OJO_DER_IDX = [362, 385, 387, 263, 373, 380]

BOCA_IDX = [61, 39, 0, 269, 291, 17, 405, 321]

CEJA_IZQ_IDX = [70, 63, 105, 66, 107]
CEJA_DER_IDX = [336, 296, 334, 293, 300]

while True:

    ret, frame = camera.read()

    if not ret:
        print("Error al captura el frame")
        break

    height, width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
            )


            def get_coords(idx):
                punto = face_landmarks.landmark[idx]

                return (int(punto.x * width), int(punto.y * height))
            
            ojo_izq = [get_coords(i) for i in OJO_IZQ_IDX]

            ojo_der = [get_coords(i) for i in OJO_DER_IDX]

            boca = [get_coords(i) for i in BOCA_IDX]

            ceja_izq = [get_coords(i) for i in CEJA_IZQ_IDX]
            ceja_der = [get_coords(i) for i in CEJA_DER_IDX]


            ear_izq = calcular_EAR(ojo_izq)
            ear_der = calcular_EAR(ojo_der)
            ear_promedio = (ear_der + ear_izq) / 2.0

            mar = calcular_MAR(boca)

            sonrisa = calcular_sonrisa(boca)

            todos_ojos = ojo_izq + ojo_der
            todas_cejas = ceja_izq + ceja_der
            posicion_cejas = calcular_posicion_cejas(todas_cejas, todos_ojos)


            emocion, color = detectar_emocion(ear_promedio, mar, sonrisa, posicion_cejas)

            cv2.putText(frame, emocion, (width // 2 - 100, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
            
            y_offset = 80
            metricas = [
                f"EAR: {ear_promedio:.3f}",
                f"MAR: {mar:.3f}",
                f"Sonrisa: {sonrisa:.1f}",
                f"Cejas: {posicion_cejas:.1f}"
            ]

            for metrica in metricas:
                cv2.putText(frame, metrica, (10, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                
                y_offset += 25

            for punto in ojo_izq + ojo_der:
                cv2.circle(frame, punto, 2, (255, 0, 0), -1)
            
            # Boca en rojo
            for punto in boca:
                cv2.circle(frame, punto, 2, (0, 0, 255), -1)
            
            # Cejas en verde
            for punto in ceja_izq + ceja_der:
                cv2.circle(frame, punto, 2, (0, 255, 0), -1)
    else:
        cv2.putText(frame, "No se detecta rostro", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
    cv2.putText(frame, "Presiona Q para salir", (10, height - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Mostrar frame
    cv2.imshow("🐢 Detector de Emociones (Modo Tortuga)", frame)
    
    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Cerrando...")
        break

camera.release()
cv2.destroyAllWindows()
face_mesh.close()

