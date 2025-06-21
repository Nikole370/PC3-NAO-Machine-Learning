# -*- coding: utf-8 -*-
import sys
import cv2
import mediapipe as mp

def detect_fingers(image_path, output_path="output.png"):
    # Inicializa MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.7
    )
    mp_draw = mp.solutions.drawing_utils

    FINGER_TIPS = [4, 8, 12, 16, 20]

    frame = cv2.imread(image_path)
    if frame is None:
        print("No hay imagen!")
        return None

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            # Dedos excepto el pulgar
            for tip_id in FINGER_TIPS[1:]:
                if landmarks[tip_id].y < landmarks[tip_id - 2].y:
                    finger_count += 1

            # Pulgar
            if landmarks[FINGER_TIPS[0]].x < landmarks[FINGER_TIPS[0] - 1].x:
                finger_count += 1

        # Dibuja el texto
        cv2.putText(frame, f"Dedos levantados: {finger_count}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    else:
        print("No se detectó una mano")

    # Guarda la imagen con keypoints y texto
    cv2.imwrite(output_path, frame)
    #print(f"Imagen guardada en: {output_path}")
    return finger_count

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: debes pasar el path de la imagen")
    else:
        image_path = sys.argv[1]
        output_path = "output.png"
        count = detect_fingers(image_path, output_path)
        if count is not None:
            print(count)

