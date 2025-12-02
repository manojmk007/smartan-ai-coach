# Smartan AI Coach – Computer Vision Internship Task

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose-orange)

## 📖 Project Overview
This repository contains the solution for the **Smartan Fittech Private Limited – AI Internship Task (Onsite)**.  
It is a real-time **Computer Vision Fitness Coach** built using **MediaPipe Pose Estimation** and **OpenCV**.

The system performs:
- Real-time body posture & biomechanics analysis  
- Automatic repetition counting  
- Incorrect form detection  
- Real-time feedback inside a modern Streamlit UI  

This allows users to perform exercises safely and effectively using only a webcam.

---

## 🚀 Key Features

### 🔹 Multi-Exercise Support
The AI Coach supports 4 exercises:

#### **1. Bicep Curls**
- Tracks elbow flexion angle  
- Detects improper elbow swinging  
- Measures range of motion  

#### **2. Squats**
- Tracks knee angle & squat depth  
- Detects incorrect back posture  

#### **3. Pushups**
- Detects full arm extension  
- Ensures proper plank body alignment  

#### **4. Lateral Raises**
- Monitors wrist-to-shoulder alignment  
- Detects impingement-risk angles  

---

### 🔹 3D Biomechanics Engine
Unlike 2D pixel-based systems, this project uses:

- `pose_world_landmarks` (3D coordinates in meters)
- 3D vector math +
- Angle calculations using dot products

This provides **camera-angle–independent** accuracy.

---

### 🔹 Interactive Dashboard (Glassmorphism UI)
The interface displays:

- Repetition Counter  
- Angle Measurements  
- Progress Bar  
- Real-Time Form Corrections (e.g., “Go Lower”, “Straighten Back”)  

---

### 🔹 Streamlit Web App
- Choose exercise  
- Use webcam or upload a video  
- View real-time feedback  

All from a simple, user-friendly interface.

---

git clone https://github.com/YOUR_USERNAME/smartan-ai-coach.git
cd smartan-ai-coach
