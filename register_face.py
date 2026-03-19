import cv2
import mediapipe as mp
import numpy as np
import pickle
import time

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

print("📸 Press 'C' to start capturing (5 samples), ESC to exit")

faces = []
capture_mode = False
countdown = False
count_start = 0
sample_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    key = cv2.waitKey(1) & 0xFF

    # -------- Start Capture --------
    if key == ord('c') and not capture_mode:
        countdown = True
        count_start = time.time()

    # -------- Countdown --------
    if countdown:
        elapsed = int(time.time() - count_start)
        if elapsed < 3:
            cv2.putText(frame, f"{3 - elapsed}",
                        (300, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,255,255), 4)
        else:
            countdown = False
            capture_mode = True
            print("📸 Capturing samples...")

    # -------- Face Detection --------
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]

        # Draw face box
        x_coords = [lm.x for lm in landmarks.landmark]
        y_coords = [lm.y for lm in landmarks.landmark]

        x_min, x_max = int(min(x_coords)*w), int(max(x_coords)*w)
        y_min, y_max = int(min(y_coords)*h), int(max(y_coords)*h)

        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255,0,0), 2)
        cv2.putText(frame, "Face Detected",
                    (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        # -------- Capture multiple samples --------
        if capture_mode and sample_count < 5:
            face_data = np.array([[lm.x, lm.y, lm.z] for lm in landmarks.landmark])
            faces.append(face_data)
            sample_count += 1

            print(f"✅ Sample {sample_count}/5 captured")
            time.sleep(0.5)  # small delay

        if sample_count == 5:
            with open("face_data.pkl", "wb") as f:
                pickle.dump(faces, f)

            print("🎉 Face registered successfully with 5 samples!")
            capture_mode = False
            sample_count = 0
            faces.clear()

    else:
        cv2.putText(frame, "No Face Detected",
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    # -------- UI Text --------
    cv2.putText(frame, "Press 'C' to Register",
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("Register Face", frame)

    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()