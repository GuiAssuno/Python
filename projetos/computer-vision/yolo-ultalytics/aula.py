import cv2
import numpy as np
from ultralytics import YOLO
import time
from collections import defaultdict

# Configurações melhoradas
CONFIDENCE_MIN = 0.6  # Aumentado para detecções mais estáveis
MODEL_SIZE = "yolov8n.pt"
RESOLUCAO_ENTRADA = (320, 320)  # Aumentada para melhor detecção
URL_DROIDCAM = "http://192.168.15.86:4747/video"

# Sistema de tracking simples
track_history = defaultdict(lambda: [])
max_track_length = 30  # Número máximo de pontos no histórico

# Inicializa o modelo YOLO
try:
    model = YOLO(MODEL_SIZE).to('cpu')
    print("Modelo YOLO carregado com sucesso na CPU")
except Exception as e:
    print(f"Erro ao carregar modelo: {e}")
    exit()

# Configurações de captura de vídeo
cap = cv2.VideoCapture(URL_DROIDCAM)
if not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Variáveis para controle de performance
frame_count = 0
start_time = time.time()
fps = 0

print("Iniciando detecção. Pressione 'q' para sair.")

while True:
    # Limpa buffer da câmera
    for _ in range(2):
        cap.grab()
    
    ret, frame = cap.retrieve()
    if not ret:
        print("Erro ao capturar frame.")
        break

    frame_count += 1
    
    # Redimensiona o frame para entrada do modelo
    frame_resized = cv2.resize(frame, RESOLUCAO_ENTRADA)

    # Executa inferência com YOLO
    try:
        results = model.track(frame_resized, 
                            verbose=False, 
                            conf=CONFIDENCE_MIN, 
                            imgsz=320,
                            persist=True)  # Habilita tracking
    except Exception as e:
        print(f"Erro durante inferência: {e}")
        break

    # Processa resultados
    if results and results[0].boxes is not None and results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        track_ids = results[0].boxes.id.cpu().numpy().astype(int)
        confidences = results[0].boxes.conf.cpu().numpy()
        class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
        
        # Desenha caixas e labels
        for box, track_id, confidence, cls_id in zip(boxes, track_ids, confidences, class_ids):
            # Escala as coordenadas para o frame original
            scale_x = frame.shape[1] / RESOLUCAO_ENTRADA[0]
            scale_y = frame.shape[0] / RESOLUCAO_ENTRADA[1]
            
            x1, y1, x2, y2 = box
            x1 = int(x1 * scale_x)
            y1 = int(y1 * scale_y)
            x2 = int(x2 * scale_x)
            y2 = int(y2 * scale_y)
            
            # Calcula o centro da caixa para tracking
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            
            # Atualiza histórico de tracking
            track = track_history[track_id]
            track.append((center_x, center_y))
            if len(track) > max_track_length:
                track.pop(0)
            
            # Desenha a caixa
            color = (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Desenha label com ID de tracking
            label = f"ID:{track_id} {model.names[cls_id]} {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Desenha trajetória
            if len(track) > 1:
                points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
                cv2.polylines(frame, [points], isClosed=False, color=color, thickness=2)

    # Calcula e exibe FPS
    current_time = time.time()
    elapsed = current_time - start_time
    
    if elapsed > 0:
        fps = frame_count / elapsed
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Exibe frame
    cv2.imshow('DroidCam YOLO Detection', frame)

    # Finaliza com 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Captura finalizada")
