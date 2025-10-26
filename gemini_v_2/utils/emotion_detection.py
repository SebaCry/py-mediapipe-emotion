
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
