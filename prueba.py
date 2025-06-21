# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp

# Inicializa MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Abre la cámara
cap = cv2.VideoCapture(0)

# Lista para saber qué dedos son
FINGER_TIPS = [4, 8, 12, 16, 20]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convierte a RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibuja los puntos y conexiones
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtiene landmarks
            landmarks = hand_landmarks.landmark

            # Dedos (excepto pulgar)
            for tip_id in FINGER_TIPS[1:]:
                if landmarks[tip_id].y < landmarks[tip_id - 2].y:
                    finger_count += 1

            # Pulgar (en eje x)
            if landmarks[FINGER_TIPS[0]].x < landmarks[FINGER_TIPS[0] - 1].x:
                finger_count += 1

            # Muestra el conteo
            cv2.putText(frame, f"Dedos levantados: {finger_count}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Detection and Finger Counting", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
