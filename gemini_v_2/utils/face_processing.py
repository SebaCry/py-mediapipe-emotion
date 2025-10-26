import numpy as np

def calcular_distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calcular_EAR(ojo_puntos):
    vertical_1 = calcular_distancia(ojo_puntos[1], ojo_puntos[5])
    vertical_2 = calcular_distancia(ojo_puntos[2], ojo_puntos[4])
    horizontal = calcular_distancia(ojo_puntos[0], ojo_puntos[3])
    return (vertical_1 + vertical_2) / (2.0 * horizontal) if horizontal != 0 else 0.0

def calcular_MAR(boca_puntos):
    vertical = calcular_distancia(boca_puntos[2], boca_puntos[6])
    horizontal = calcular_distancia(boca_puntos[0], boca_puntos[4])
    return vertical / horizontal if horizontal != 0 else 0.0

def calcular_sonrisa(boca_puntos):
    comisura_izq = boca_puntos[0]
    comisura_der = boca_puntos[4]
    centro_boca = boca_puntos[6]
    altura_comisuras = (comisura_izq[1] + comisura_der[1]) / 2
    return centro_boca[1] - altura_comisuras

def calcular_posicion_cejas(cejas_puntos, ojos_puntos):
    centro_cejas = np.mean(cejas_puntos, axis=0)
    centro_ojos = np.mean(ojos_puntos, axis=0)
    return centro_cejas[1] - centro_ojos[1]

def get_points(face_landmarks, idx, width, height):
    pts = []
    for idx in idx:
        lm = face_landmarks.landmark[idx]
        pts.append((int(lm.x * width), int(lm.y * height)))
    return pts

def compute_metrics_from_landmarks(face_landmarks, width, height, idx) -> dict:
    left_eye = get_points(face_landmarks, idx['left_eye'], width, height)
    right_eye = get_points(face_landmarks, idx['right_eye'], width, height)
    mouth = get_points(face_landmarks, idx['mouth'], width, height)
    left_eyebrow = get_points(face_landmarks, idx['left_eyebrow'], width, height)
    right_eyebrow = get_points(face_landmarks, idx['right_eye'], width, height)

    ear_left = calcular_EAR(left_eye)
    ear_right = calcular_EAR(right_eye)
    ear = (ear_left + ear_right) / 2.0
    mar = calcular_MAR(mouth)
    smile = calcular_sonrisa(mouth)
    eyebrow_pos = calcular_posicion_cejas(left_eyebrow + right_eyebrow, left_eye + right_eye)

    return {
        "ear" : ear,
        "mar" : mar,
        "smile" : smile,
        "eyebrow_pos" : eyebrow_pos,
    }

