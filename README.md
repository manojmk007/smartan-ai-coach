# Smartan AI Coach - Computer Vision Internship Task

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B) ![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose-orange)

## 📖 Project Overview
This repository contains the solution for the **Smartan Fittech Private Limited** AI Internship Task (Onsite). It is a real-time Computer Vision application that acts as a personal AI fitness coach.

Using **MediaPipe Pose Estimation** and **OpenCV**, the system analyzes biomechanical form, counts repetitions, and provides corrective feedback for multiple exercises. The application is wrapped in a **Streamlit** web interface for easy usage.

## 🚀 Key Features
* **Multi-Exercise Support:**
    * **Bicep Curls:** Tracks range of motion (ROM) and detects "Elbow Swinging" (cheating).
    * **Squats:** Monitors squat depth (knee angle) and back stability.
    * **Pushups:** Checks for proper plank form and elbow extension.
    * **Lateral Raises:** Ensures wrist-shoulder alignment to prevent impingement.
* **3D Biomechanics:** Utilizes `pose_world_landmarks` (meters) rather than just 2D pixel coordinates, ensuring accurate angle calculation regardless of camera perspective.
* **Interactive Dashboard:** A "Glassmorphism" style UI overlay that displays reps, a progress bar, and real-time form alerts.
* **Streamlit Web App:** Allows users to easily switch exercises and upload video files or use a webcam.

---

## 🛠️ Installation & Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/smartan-ai-coach.git](https://github.com/YOUR_USERNAME/smartan-ai-coach.git)
cd smartan-ai-coach
smartan-ai-coach/
├── app.py               # Main Streamlit Web Application
├── requirements.txt     # Python dependencies
├── README.md            # Project Documentation
├── assets/              # Sample videos for testing
│   └── test_curl.mp4
└── src/                 # Source Code Modules
    ├── geometry.py      # 3D Vector Math & Angle Calculations
    ├── rules.py         # State Machine & Form Logic for 4 Exercises
    └── utils.py         # OpenCV Drawing & UI (Dashboard)
