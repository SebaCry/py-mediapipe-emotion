def reporte_emocional(
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
) -> str:
    return f"""
{'='*80}
REPORTE DE ANÁLISIS EMOCIONAL
{'='*80}

Fecha y hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Duración de la sesión: {DURACION_CAPTURA} segundos
Total de muestras analizadas: {len(datos_sesion)}

{'='*80}
DATOS ESTADÍSTICOS
{'='*80}

Distribución de emociones:
{chr(10).join([f"  - {emocion}: {cantidad} veces ({cantidad/len(datos_sesion)*100:.1f}%)" for emocion, cantidad in conteo_emociones.items()])}

Métricas faciales:
    EAR (Apertura de ojos):
        - Promedio: {np.mean(ear_valores):.3f}
        - Mínimo: {np.min(ear_valores):.3f}
        - Máximo: {np.max(ear_valores):.3f}
    
    MAR (Apertura de boca):
        - Promedio: {np.mean(mar_valores):.3f}
        - Mínimo: {np.min(mar_valores):.3f}
        - Máximo: {np.max(mar_valores):.3f}
    
    Índice de sonrisa:
        - Promedio: {np.mean(sonrisa_valores):.2f}
        - Mínimo: {np.min(sonrisa_valores):.2f}
        - Máximo: {np.max(sonrisa_valores):.2f}
    
    Posición de cejas:
        - Promedio: {np.mean(cejas_valores):.2f}
        - Mínimo: {np.min(cejas_valores):.2f}
        - Máximo: {np.max(cejas_valores):.2f}

{'='*80}
ANÁLISIS GENERADO POR GEMINI AI
{'='*80}

{reporte}

{'='*80}
FIN DEL REPORTE
{'='*80}
"""