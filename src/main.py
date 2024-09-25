#!/usr/bin/env python3

import cv2
import mediapipe as mp
import os
from camera import Camera
from openai_helper import GPTAgent
from speech_helper import SpeechHelper

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=2)

camera = Camera()
speech = SpeechHelper()
gpt = GPTAgent()

detection_active = True

def is_fist(hand_landmarks, h, w):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    return (thumb_tip.y > thumb_ip.y + 0.02 and
            index_tip.y > index_pip.y + 0.02 and
            middle_tip.y > middle_pip.y + 0.02 and
            ring_tip.y > ring_pip.y + 0.02 and
            pinky_tip.y > pinky_pip.y + 0.02)

def is_paper_without_thumb(hand_landmarks, h, w):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    return (index_tip.y < index_pip.y - 0.02 and
            middle_tip.y < middle_pip.y - 0.02 and
            ring_tip.y < ring_pip.y - 0.02 and
            pinky_tip.y < pinky_pip.y - 0.02)

def is_scissors(hand_landmarks, h, w):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    return (index_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y - 0.02 and
            middle_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y - 0.02 and
            ring_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y + 0.02 and
            pinky_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y + 0.02)

def is_gun(hand_landmarks, h, w):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    return (index_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y - 0.02 and
            thumb_tip.x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x + 0.02 and
            middle_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y + 0.02 and
            ring_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y + 0.02 and
            pinky_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y + 0.02)

while True:
    ret, frame = camera.get_frame()

    if not ret or frame is None:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks and detection_active:
        fists_count = 0
        scissors_count = 0
        guns_count = 0

        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape

            if is_fist(hand_landmarks, h, w):
                fists_count += 1

            if is_scissors(hand_landmarks, h, w):
                scissors_count += 1

            if is_gun(hand_landmarks, h, w):
                guns_count += 1

        if fists_count == 1:
            print("Poing droit fermé détecté, JARVIS ouvre VS Code dans le projet spécifié")
            os.system('/Applications/Visual\\ Studio\\ Code.app/Contents/Resources/app/bin/code /Users/dalm1/Desktop/Reroll/Progra/JARVIS')

        if fists_count == 2:
            print("Deux poings fermés, JARVIS ferme toutes les fenêtres de VS Code")
            os.system("pkill -f 'Visual Studio Code'")

        if scissors_count == 2 or guns_count == 2:
            print("Deux signes ciseaux ou pistolets détectés, fermeture de la session.")
            speech.speak("Fermeture du programme. À bientôt.")
            camera.release()
            cv2.destroyAllWindows()
            exit()

        for hand_landmarks in result.multi_hand_landmarks:
            if is_paper_without_thumb(hand_landmarks, h, w):
                print("Signe feuille sans pouce détecté, démarrage du mode conversation GPT")

                detection_active = False

                speech.speak("Bonjour DALM1")
                user_input = speech.listen_google()
                print(f"Vous avez dit: {user_input}")

                if "jarvis fermeture" in user_input.lower():
                    print("Commande de fermeture détectée. Fermeture de la session.")
                    speech.speak("Fermeture du programme.")
                    camera.release()
                    cv2.destroyAllWindows()
                    exit()

                if "chat ouverture" in user_input.lower():
                    print("Commande pour ouvrir ChatGPT détectée.")
                    speech.speak("GPT Ouverture.")
                    os.system("open -a ChatGPT")

                else:
                    response = gpt.ask_gpt(user_input)
                    print(f"GPT répond: {response}")
                    speech.speak(response)

                detection_active = True


    cv2.imshow('Hand Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
