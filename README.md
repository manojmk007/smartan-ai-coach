Smartan AI Coach – Computer Vision Internship Task






📖 Project Overview

This repository contains the solution for the Smartan Fittech Private Limited – AI Internship Task (Onsite).
It is a real-time Computer Vision Fitness Coach that uses MediaPipe Pose Estimation and OpenCV to:

Analyze body posture and biomechanics

Count exercise repetitions

Detect incorrect form

Provide real-time feedback

The system runs inside an interactive Streamlit web app for easy usability.

🚀 Key Features
🔹 Multi-Exercise Support

The AI Coach currently supports 4 exercises with automated rep counting and form validation:

Bicep Curls

Tracks elbow flexion angle

Detects "elbow swinging" cheating

Calculates ROM (range of motion)

Squats

Measures knee angle and squat depth

Monitors lower-back stability

Pushups

Ensures proper plank alignment

Checks elbow extension range

Lateral Raises

Tracks shoulder–wrist elevation

Prevents shoulder impingement due to improper lifting angle

🔹 3D Biomechanics Engine

The system uses:

pose_world_landmarks (3D in meters)

3D vectors & angle calculations

Robust orientation-invariant measurements

This makes rep counting accurate even if the camera angle changes.

🔹 Interactive Dashboard

A modern glassmorphism-style UI overlays the video feed to show:

Rep Counter

Current Angle

Progress Bar

Real-Time Feedback (e.g., “Go Lower”, “Full Extension Needed”, “Don’t Swing Elbow”)

🔹 Streamlit Web Application

Users can:

Select exercise

Enable webcam

Upload video files

View real-time feedback

🛠️ Installation & Usage
1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/smartan-ai-coach.git
cd smartan-ai-coach

2️⃣ Install Dependencies

Make sure Python 3.8+ is installed, then run:

pip install -r requirements.txt

3️⃣ Run the Application
streamlit run app.py


Your browser will open:
👉 http://localhost:8501

📂 Project Structure
smartan-ai-coach/
├── app.py               # Main Streamlit Web Application
├── requirements.txt     # Python Dependencies
├── README.md            # Project Documentation
├── assets/              # Sample Videos for Testing
│   └── test_curl.mp4
└── src/                 # Source Code Modules
    ├── geometry.py      # 3D Vector Math & Angle Calculations
    ├── rules.py         # Exercise Logic & Finite-State Machine
    └── utils.py         # OpenCV Drawing & Dashboard UI

🧠 Logic Overview
✔️ Angle Calculation (3D)

All biomechanical measurements use:

3D vectors from MediaPipe

Dot-product angle computation

Normalization for stable results

Example:

Bicep Curl → Elbow angle

Squat → Knee angle

Pushup → Arm extension angle

Lateral Raise → Shoulder abduction angle

✔️ Finite-State Machine for Rep Counting

Each exercise uses a state machine:

DOWN → UP → DOWN (Pushups, Squats)

FLEX → EXTEND → FLEX (Curls, Raises)

This avoids double-counting reps.

✔️ Handling Multiple People

The system supports multiple-person scenarios by:

Selecting person with largest bounding box (closest to camera)

Stabilizing pose selection to avoid switching

Ignoring partial / poor detections
