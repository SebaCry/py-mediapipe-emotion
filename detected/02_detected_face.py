import cv2

print("Iniciando el detector de rostros...")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') 

if face_cascade.empty():
    print("Error al cargar el clasificador de rostros")
    exit()

print("Clasificador cargado correctamente")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: No se pudo abrir la camara")
    exit()

print("✅ Cámara abierta")
print("📹 Presiona 'q' para salir")
print("🐢 Buscando rostros lentamente pero seguro...")

while True:

    ret, frame = camera.read()

    if not ret:
        print("❌ Error al capturar frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    num_faces = len(faces)

    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0))

        cv2.putText(frame, "Rostro detectado", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
    
    texto_contador = f"Rostros: {num_faces}"
    cv2.putText(frame, texto_contador, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.imshow("Detector de Rostros", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Saliendo...")
        break

camera.release()
cv2.destroyAllWindows()

print("✅ Programa finalizado - ¡La tortuga descansa! 🐢")