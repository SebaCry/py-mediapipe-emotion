
def give_prompt(
        np,
        DURACION_CAPTURA,
        datos_sesion,
        conteo_emociones,
        ear_valores,
        mar_valores,
        sonrisa_valores,
        cejas_valores
) -> str:
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