import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import math
import os
import json

# --- 1. BACKEND SETTINGS ---
config_file = 'settings.json'
default_settings = {
    "sensitivity": 5,
    "frame_padding": 100,
    "camera_id": 0,
    "volume_trigger_up": 100,
    "volume_trigger_down": 30
}

if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        json.dump(default_settings, f)
    config = default_settings
else:
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except:
        config = default_settings

# Apply Config
wCam, hCam = 640, 480
frameR = config["frame_padding"]
smoothening = config["sensitivity"]

# --- 2. SETUP ---
cap = cv2.VideoCapture(config["camera_id"])
cap.set(3, wCam)
cap.set(4, hCam)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils
wScr, hScr = pyautogui.size()

plocX, plocY = 0, 0
clocX, clocY = 0, 0

# --- 3. MAIN LOOP ---
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
                x_thumb, y_thumb = lmList[4][1:]

                fingers = []
                # Thumb
                if lmList[4][0] > lmList[3][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # Index
                if lmList[8][2] < lmList[6][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # Middle
                if lmList[12][2] < lmList[10][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # Pinky
                if lmList[20][2] < lmList[18][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # MODE 1: VOLUME (Pinky Up)
                if fingers[3] == 1:
                    cv2.putText(img, "VOLUME MODE", (20, 50),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
                    length = math.hypot(x1 - x_thumb, y1 - y_thumb)
                    cv2.putText(
                        img, f'Dist: {int(length)}', (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)
                    cv2.line(img, (x_thumb, y_thumb),
                             (x1, y1), (255, 0, 255), 3)

                    if length < config["volume_trigger_down"]:
                        cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                        pyautogui.press("volumedown")
                    elif length > config["volume_trigger_up"]:
                        cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                        pyautogui.press("volumeup")

                # MODE 2: MOUSE (Pinky Down)
                else:
                    if fingers[1] == 1 and fingers[2] == 0:
                        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening
                        pyautogui.moveTo(clocX, clocY)
                        cv2.circle(img, (x1, y1), 15,
                                   (255, 0, 255), cv2.FILLED)
                        plocX, plocY = clocX, clocY

                    if fingers[1] == 1 and fingers[2] == 1:
                        length = math.hypot(x2 - x1, y2 - y1)
                        if length < 40:
                            cv2.circle(img, (x1, y1), 15,
                                       (0, 255, 0), cv2.FILLED)
                            pyautogui.click()

    # --- 4. DRAW WINDOW FIRST ---
    cv2.imshow("VisionTouch AI", img)

    # --- 5. THEN CHECK FOR CLOSING (Corrected Location) ---
    # Check "X" button
    if cv2.getWindowProperty("VisionTouch AI", cv2.WND_PROP_VISIBLE) < 1:
        break
    # Check 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
