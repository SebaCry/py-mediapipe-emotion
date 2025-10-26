import cv2


camera = cv2.VideoCapture(0)

if not camera.isOpened():
        print("Error: No se pudo abrir la camara")
        exit()

print("Camara abierta correctamente")
print("Presiona q para salir")

while True:

    ret, frame = camera.read()
        
    if not ret:
        print("Error al capturar el frame")
        break

    cv2.imshow("Camara en vivo", frame)

    if cv2.waitKey(1) and 0xFF == ord("q"):
        print("Cerrando aplicacion")
        break

camera.release()

cv2.destroyAllWindows()

print("Programa cerrado correctamente")


