import numpy as np

def calcular_distancia(punto1, punto2):
    return np.sqrt((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)

def calcular_EAR(ojo_puntos):
    vertical_1 = calcular_distancia(ojo_puntos[1], ojo_puntos[5])
    vertical_2 = calcular_distancia(ojo_puntos[2], ojo_puntos[4])
    horizontal = calcular_distancia(ojo_puntos[0], ojo_puntos[3])
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear

def calcular_MAR(boca_puntos):
    vertical = calcular_distancia(boca_puntos[2], boca_puntos[6])
    horizontal = calcular_distancia(boca_puntos[0], boca_puntos[4])
    mar = vertical / horizontal
    return mar

def calcular_sonrisa(boca_puntos):
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
        return "Sorpresa", (0, 165, 255)
    if sonrisa > 5 and ear_promedio > 0.2:
        return "Feliz", (0, 255, 0)
    if sonrisa < -3:
        return "Triste", (255, 0, 0)
    if posicion_cejas > -5 and mar < 0.2:
        return "Enojado", (0, 0, 255)
    if ear_promedio < 0.18:
        return "Ojos cerrados", (128, 128, 128)
    return "Neutral", (255, 255, 255)


def get_coords(idx, face_landmarks, width, height):
    punto = face_landmarks.landmark[idx]
    return (int(punto.x * width), int(punto.y * height))