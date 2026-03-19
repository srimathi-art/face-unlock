import cv2
import mediapipe as mp
import numpy as np
import pickle
import time

# -------- Load saved faces --------
with open("face_data.pkl", "rb") as f:
    saved_faces = pickle.load(f)

# -------- MediaPipe --------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def match_face(current_face):
    distances = [np.linalg.norm(face - current_face) for face in saved_faces]
    return min(distances)

# -------- Thresholds --------
EYE_OPEN_THRESH = 0.28
EYE_CLOSED_THRESH = 0.25
FACE_THRESH = 5

# -------- States --------
unlock_mode = False
countdown = False
count_start = 0

eyes_closed = False
blink_count = 0

closed_start_time = None
locked = True

# -------- Mouse Click --------
def click_event(event, x, y, flags, param):
    global countdown, count_start
    if event == cv2.EVENT_LBUTTONDOWN:
        if 10 < x < 150 and 10 < y < 60:
            countdown = True
            count_start = time.time()

# -------- Camera --------
cap = cv2.VideoCapture(0)

cv2.namedWindow("Face Unlock")
cv2.setMouseCallback("Face Unlock", click_event)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    # -------- Draw Button --------
    cv2.rectangle(frame, (10, 10), (150, 60), (0, 255, 0), -1)
    cv2.putText(frame, "START", (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

    # -------- Countdown --------
    if countdown:
        elapsed = int(time.time() - count_start)
        if elapsed < 3:
            cv2.putText(frame, f"{3 - elapsed}",
                        (300, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,255,255), 4)
        else:
            unlock_mode = True
            countdown = False
            blink_count = 0

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]

        # -------- Face box --------
        x_coords = [lm.x for lm in landmarks.landmark]
        y_coords = [lm.y for lm in landmarks.landmark]

        x_min, x_max = int(min(x_coords)*w), int(max(x_coords)*w)
        y_min, y_max = int(min(y_coords)*h), int(max(y_coords)*h)

        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255,0,0), 2)

        # -------- Face match --------
        current_face = np.array([[lm.x, lm.y, lm.z] for lm in landmarks.landmark])
        face_distance = match_face(current_face)
        face_match = face_distance < FACE_THRESH

        # -------- Eye detection --------
        left_eye = np.array([[int(landmarks.landmark[i].x * w),
                              int(landmarks.landmark[i].y * h)] for i in LEFT_EYE])

        right_eye = np.array([[int(landmarks.landmark[i].x * w),
                               int(landmarks.landmark[i].y * h)] for i in RIGHT_EYE])

        ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2

        cv2.putText(frame, f"EAR: {ear:.2f}", (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        # -------- Blink detection --------
        if ear < EYE_CLOSED_THRESH and not eyes_closed:
            eyes_closed = True

        elif ear > EYE_OPEN_THRESH and eyes_closed:
            blink_count += 1
            eyes_closed = False

        # -------- Track eye closed time --------
        if ear < EYE_CLOSED_THRESH:
            if closed_start_time is None:
                closed_start_time = time.time()
        else:
            closed_start_time = None

        # -------- Unlock --------
        if unlock_mode:
            if face_match and blink_count >= 1:
                locked = False

        # -------- Auto Lock --------
        if closed_start_time is not None:
            if time.time() - closed_start_time > 5:
                locked = True
                blink_count = 0
                unlock_mode = False
                closed_start_time = None

        # -------- UI --------
        cv2.putText(frame, f"Blinks: {blink_count}", (20, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2)

        # Status below blinks (NO background)
        status_text = "LOCKED" if locked else "UNLOCKED"
        color = (0,0,255) if locked else (0,255,0)

        cv2.putText(frame, status_text,
                    (20, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    color,
                    2)

        # -------- Lock countdown (bottom center) --------
        if closed_start_time and not locked:
            remaining = 5 - int(time.time() - closed_start_time)
            if remaining > 0:
                text = f"Locking in: {remaining}s"

                (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)

                x = (w - tw) // 2
                y = h - 30

                cv2.putText(frame, text, (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

    else:
        cv2.putText(frame, "NO FACE DETECTED", (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Face Unlock", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()