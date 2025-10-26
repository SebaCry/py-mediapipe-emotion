import cv2

def draw_metrics(frame, metrics, emotion, color):
    """Dibuja las métricas en el frame"""
    h, w = frame.shape[:2]
    
    # Fondo semi-transparente para las métricas
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (250, 150), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
    
    # Texto de métricas
    y_offset = 30
    cv2.putText(frame, f"EAR: {metrics['ear']:.2f}", (20, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    y_offset += 25
    cv2.putText(frame, f"MAR: {metrics['mar']:.2f}", (20, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    y_offset += 25
    cv2.putText(frame, f"Sonrisa: {metrics['smile']:.2f}", (20, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    y_offset += 25
    cv2.putText(frame, f"Cejas: {metrics['eyebrow_pos']:.2f}", (20, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Emoción con color
    y_offset += 30
    cv2.putText(frame, f"Emocion: {emotion}", (20, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    return frame