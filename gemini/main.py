from datetime import datetime
import cv2
import time
import numpy as np
from collections import Counter

from gemini.config.config import face_mesh, mp_drawing, mp_face_mesh, mp_drawing_styles, modelo_gemini
from gemini.config.constants import (
    OJO_DER_IDX,
    OJO_IZQ_IDX, 
    CEJA_DER_IDX, 
    CEJA_IZQ_IDX, 
    BOCA_IDX
)
from gemini.utils import (
    get_coords,
    calcular_EAR,
    calcular_MAR,
    calcular_sonrisa,
    calcular_posicion_cejas,
    detectar_emocion
)
from gemini.context.prompt import give_prompt
from gemini.context.report import reporte_emocional



def main():
    print(">>> Intentando abrir la camara...")
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Error: No se pudo abrir la cámara")
        exit()

    print("✅ Cámara abierta")

    datos_sesion = []
    tiempo_inicio = time.time()
    DURACION_CAPTURA = 30

    print("\n" + "="*60)
    print(f"📊 Iniciando captura de {DURACION_CAPTURA} segundos")
    print("🐢 Haz diferentes expresiones faciales:")
    print("   - Sonríe 😊")
    print("   - Sorpréndete 😲")
    print("   - Pon cara seria 😐")
    print("   - Pon cara triste 😢")
    print("="*60 + "\n")

    capturando = True
    frame_count = 0

    while True:
        ret, frame = camera.read()

        if not ret:
            break

        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        tiempo_transcurrido = time.time() - tiempo_inicio
        tiempo_restante = max(0, DURACION_CAPTURA - tiempo_transcurrido)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                
                ojo_izq = [get_coords(i, face_landmarks, width, height) for i in OJO_IZQ_IDX]
                ojo_der = [get_coords(i, face_landmarks, width, height) for i in OJO_DER_IDX]
                boca = [get_coords(i, face_landmarks, width, height) for i in BOCA_IDX]
                ceja_izq = [get_coords(i, face_landmarks, width, height) for i in CEJA_IZQ_IDX]
                ceja_der = [get_coords(i, face_landmarks, width, height) for i in CEJA_DER_IDX]

                ear_izq = calcular_EAR(ojo_izq)
                ear_der = calcular_EAR(ojo_der)
                ear_promedio = (ear_izq + ear_der) / 2.0
                mar = calcular_MAR(boca)
                sonrisa = calcular_sonrisa(boca)
                todos_ojos = ojo_izq + ojo_der
                todas_cejas = ceja_izq + ceja_der
                posicion_cejas = calcular_posicion_cejas(todas_cejas, todos_ojos)
                
                # Detectar emoción
                emocion, color = detectar_emocion(ear_promedio, mar, sonrisa, posicion_cejas)

                if capturando and frame_count % 5 == 0:
                    datos_sesion.append({
                        "timestamp" : tiempo_transcurrido,
                        'emocion': emocion,
                        'ear': ear_promedio,
                        'mar': mar,
                        'sonrisa': sonrisa,
                        'cejas': posicion_cejas
                    })

                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                )

                cv2.putText(frame, emocion, (width//2 - 100, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
            
                # Mostrar métricas
                y_offset = 90
                metricas = [
                    f"EAR: {ear_promedio:.3f}",
                    f"MAR: {mar:.3f}",
                    f"Sonrisa: {sonrisa:.1f}",
                    f"Cejas: {posicion_cejas:.1f}"
                ]
                for metrica in metricas:
                    cv2.putText(frame, metrica, (10, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    y_offset += 25

        
        if capturando:
            cv2.putText(frame, f"Capturando: {tiempo_restante:.1f}s",(10,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
            
            if tiempo_transcurrido >= DURACION_CAPTURA:
                capturando = False
                print("\n🎉 ¡Captura completada!")
                print(f"📊 Se capturaron {len(datos_sesion)} muestras")
        else:
            cv2.putText(frame, "Analisis completo - Presiona R para reporte", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.putText(frame, "Q=Salir | R=Generar reporte", (10, height - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
        cv2.imshow("🐢 Detector con Gemini AI", frame)
        
        frame_count += 1
        
        # Controles de teclado
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r") or key == ord("R"):
            if len(datos_sesion) > 0:
                emociones_detectadas = [d["emocion"] for d in datos_sesion]
                ear_valores = [d['ear'] for d in datos_sesion]
                mar_valores = [d['mar'] for d in datos_sesion]
                sonrisa_valores = [d['sonrisa'] for d in datos_sesion]
                cejas_valores = [d['cejas'] for d in datos_sesion]
                
                conteo_emociones = Counter(emociones_detectadas)

                prompt = give_prompt(np, 
                    DURACION_CAPTURA,
                    datos_sesion,
                    conteo_emociones,
                    ear_valores,
                    mar_valores,
                    sonrisa_valores,
                    cejas_valores
                )

                try:
                    respuesta = modelo_gemini.generate_content(prompt)

                    reporte = respuesta.text

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nombre_archivo = f"reporte_emocional_{timestamp}.txt"

                    contenido_completo = reporte_emocional(
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
                    )

                    with open(nombre_archivo, "w", encoding="utf-8") as f:
                        f.write(contenido_completo)

                except Exception as e:
                    print(f"\n❌ Error al generar reporte: {e}")
                print("Verifica que tu API Key de Gemini sea correcta")
            else:
                print("⚠️ No hay datos capturados todavía")
    camera.release()
    cv2.destroyAllWindows()
    face_mesh.close()

if __name__ == "__main__":
    main()