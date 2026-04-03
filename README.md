# 🔐 Smart Face Unlock System with Liveness Detection

A real-time face unlock system built using **Python, OpenCV, and MediaPipe** that provides secure authentication using **facial recognition + blink-based liveness detection**.

---

## 🚀 Features

* 👤 Face Registration with multiple samples
* 🧠 Face Matching using facial landmarks
* 👁️ Blink Detection (Liveness Check)
* 🖱️ Click-based Start Button
* ⏳ Countdown before authentication
* 🔓 Unlock only after valid face + blink
* 🔒 Auto Lock if eyes are closed for more than 5 seconds
* 🎯 Real-time face tracking using webcam
* 🎨 Clean and simple UI

---

## 🧠 How It Works

1. User registers face using `register_face.py`
2. Facial landmarks are stored as numerical data (`face_data.pkl`)
3. During authentication:

   * Face is detected using MediaPipe
   * Landmarks are compared with stored data
   * Eye Aspect Ratio (EAR) detects blinking
4. System unlocks only when:

   * Face matches AND
   * User blinks (liveness verification)
5. If eyes remain closed for 5 seconds → system locks automatically

---

## 🛠️ Tech Stack

* Python 3.x
* OpenCV
* MediaPipe
* NumPy
* Pickle

---

## 📂 Project Structure

```
face-unlock/
│
├── face_unlock.py        # Main face unlock system
├── register_face.py      # Face registration script
├── requirements.txt      # Dependencies
├── .gitignore            # Ignored files
└── README.md             # Project documentation
```

---

## ▶️ How to Run

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/face-unlock.git
cd face-unlock
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Register your face

```bash
python register_face.py
```

* Press **C** to capture samples
* 5 samples will be stored

### 4️⃣ Run the face unlock system

```bash
python face_unlock.py
```

* Click **START button**
* Blink once to unlock 🔓

---

## ⚠️ Important Notes

* Webcam access is required
* Ensure good lighting for better accuracy
* Each user must register their face before using the system

---

## 🔐 Security Features

* ✔ Liveness detection using blink
* ✔ Prevents photo spoofing
* ✔ Auto-lock for suspicious inactivity
* ✔ No image storage (only landmark data stored)

---

## 🎯 Use Cases

* Secure login systems
* Smart device authentication
* Attendance systems
* Basic biometric security applications

---

## 🚀 Future Improvements

* 🔊 Voice feedback (Access Granted / Denied)
* 📊 Lock countdown progress bar
* 👥 Multi-user support
* 🧠 Deep learning-based recognition (FaceNet / DeepFace)
* 📸 Unknown face detection & logging
* 📱 Mobile-style Face ID UI

---

## 🙋‍♀️ Author

**Srimathi Palanisamy**
B.Tech Information Technology
Passionate about AI, Computer Vision & Smart Systems 🚀

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
