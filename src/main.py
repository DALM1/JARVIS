#!/usr/bin/env python3

import cv2
import mediapipe as mp
import os
from camera import Camera
from openai_helper import GPTAgent
from speech_helper import SpeechHelper

print( "┓ ┏┏┓┓ ┏┓┏┓┳┳┓┏┓  ┳┓┏┓┓ ┳┳┓┓")
print( "┃┃┃┣ ┃ ┃ ┃┃┃┃┃┣   ┃┃┣┫┃ ┃┃┃┃")
print( "┗┻┛┗┛┗┛┗┛┗┛┛ ┗┗┛  ┻┛┛┗┗┛┛ ┗┻")
print( "")


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=2)

camera = Camera()
speech = SpeechHelper()
gpt = GPTAgent()

detection_active = True
nas_path = "/Volumes/partage-1"

def create_folder(folder_name):
    folder_path = os.path.join(nas_path, folder_name)
    try:
        os.makedirs(folder_path, exist_ok=True)
        speech.speak(f"Dossier {folder_name} créé avec succès.")
        print(f"Dossier {folder_name} créé à {nas_path}")
    except Exception as e:
        speech.speak("Erreur lors de la création du dossier.")
        print(f"Erreur lors de la création du dossier: {e}")

def create_file(file_name, content=""):
    file_path = os.path.join(nas_path, file_name)
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        speech.speak(f"Fichier {file_name} créé avec succès.")
        print(f"Fichier {file_name} créé à {nas_path}")
    except Exception as e:
        speech.speak("Erreur lors de la création du fichier.")
        print(f"Erreur lors de la création du fichier: {e}")

def code_file(file_name, code_content):
    file_path = os.path.join(nas_path, file_name)
    try:
        with open(file_path, 'w') as file:
            file.write(code_content)
        speech.speak(f"Code écrit dans {file_name} avec succès.")
        print(f"Code écrit dans {file_name} à {nas_path}")
    except Exception as e:
        speech.speak("Erreur lors de l'écriture du code dans le fichier.")
        print(f"Erreur lors de l'écriture du code: {e}")

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

                speech.speak("Bonjour DALM1, que puis-je faire pour vous ?")
                user_input = speech.listen_google()
                print(f"Vous avez dit: {user_input}")

                if "créer dossier" in user_input.lower():
                    speech.speak("Quel nom pour le dossier ?")
                    folder_name = speech.listen_google()
                    create_folder(folder_name)

                elif "créer fichier" in user_input.lower():
                    speech.speak("Quel nom pour le fichier ?")
                    file_name = speech.listen_google()
                    create_file(file_name)

                elif "coder fichier" in user_input.lower():
                    speech.speak("Quel est le nom du fichier ?")
                    file_name = speech.listen_google()
                    speech.speak("Quel est le contenu du code ?")
                    code_content = speech.listen_google()
                    code_file(file_name, code_content)

                elif "jarvis fermeture" in user_input.lower():
                    print("Commande de fermeture détectée. Fermeture de la session.")
                    speech.speak("Fermeture du programme.")
                    camera.release()
                    cv2.destroyAllWindows()
                    exit()

                elif "chat ouverture" in user_input.lower():
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
