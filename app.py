import streamlit as st
import cv2
import tempfile
import numpy as np
import mediapipe as mp
import os
import sys

# Import your logic modules
from src.rules import FormEvaluator
from src.utils import draw_dashboard

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smartan AI Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR SETTINGS ---
st.sidebar.title("Smartan AI Coach 🤖")
st.sidebar.markdown("---")

# 1. Exercise Selector
mode = st.sidebar.selectbox(
    "Select Exercise:",
    ["Bicep Curl", "Squat", "Pushup", "Lateral Raise"]
)

# Map UI name to internal code
MODE_MAP = {
    "Bicep Curl": "CURL",
    "Squat": "SQUAT",
    "Pushup": "PUSHUP",
    "Lateral Raise": "LATERAL"
}
exercise_code = MODE_MAP[mode]

# 2. Input Source
input_source = st.sidebar.radio("Video Source:", ("Upload Video", "Webcam"))

st.sidebar.markdown("---")
st.sidebar.info(
    "**Instructions:**\n"
    "1. Select your exercise.\n"
    "2. Upload a video file (MP4/MOV).\n"
    "3. The AI will analyze your form in real-time."
)

# --- MAIN APP LOGIC ---

st.title(f"AI Training Session: {mode}")

# Initialize Logic
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
evaluator = FormEvaluator()

# Helper for Smoothing
class LowPassFilter:
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.prev = None
    def filter(self, val):
        if self.prev is None: self.prev = val
        else: self.prev = self.alpha * val + (1 - self.alpha) * self.prev
        return self.prev

smoother = LowPassFilter(0.2)

def process_video(video_path):
    """
    Main loop to process video and render in Streamlit.
    """
    cap = cv2.VideoCapture(video_path)
    
    # Create a placeholder for the video frame in the UI
    frame_placeholder = st.empty()
    
    # Progress bars in Sidebar (Optional visual)
    st.sidebar.markdown("### Live Stats")
    rep_text = st.sidebar.empty()
    feedback_text = st.sidebar.empty()

    with mp_pose.Pose(min_detection_confidence=0.7, model_complexity=1) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 1. Process Frame
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            reps = 0
            feedback = []
            progress = 0.0

            try:
                # Extract Landmarks
                if results.pose_world_landmarks:
                    lm = results.pose_world_landmarks.landmark
                    def p(idx): return [lm[idx.value].x, lm[idx.value].y, lm[idx.value].z]

                    # --- EXERCISE LOGIC ---
                    if exercise_code == 'CURL':
                        angle, reps = evaluator.evaluate_bicep_curl(
                            p(mp_pose.PoseLandmark.LEFT_SHOULDER),
                            p(mp_pose.PoseLandmark.LEFT_ELBOW),
                            p(mp_pose.PoseLandmark.LEFT_WRIST)
                        )
                        swing_ok, swing_msg = evaluator.check_elbow_swing(
                            p(mp_pose.PoseLandmark.LEFT_SHOULDER),
                            p(mp_pose.PoseLandmark.LEFT_ELBOW),
                            p(mp_pose.PoseLandmark.LEFT_HIP)
                        )
                        feedback.append((swing_ok, swing_msg))
                        progress = np.clip((160 - angle) / (160 - 30), 0, 1)

                    elif exercise_code == 'SQUAT':
                        angle, reps, back_ok, back_msg = evaluator.evaluate_squat(
                            p(mp_pose.PoseLandmark.LEFT_HIP),
                            p(mp_pose.PoseLandmark.LEFT_KNEE),
                            p(mp_pose.PoseLandmark.LEFT_ANKLE),
                            p(mp_pose.PoseLandmark.LEFT_SHOULDER)
                        )
                        feedback.append((back_ok, back_msg))
                        progress = np.clip((170 - angle) / (170 - 80), 0, 1)
                    
                    elif exercise_code == 'PUSHUP':
                         angle, reps, form_ok, form_msg = evaluator.evaluate_pushup(
                            p(mp_pose.PoseLandmark.LEFT_SHOULDER),
                            p(mp_pose.PoseLandmark.LEFT_ELBOW),
                            p(mp_pose.PoseLandmark.LEFT_WRIST),
                            p(mp_pose.PoseLandmark.LEFT_HIP),
                            p(mp_pose.PoseLandmark.LEFT_ANKLE)
                        )
                         feedback.append((form_ok, form_msg))
                         progress = np.clip((170 - angle) / (170 - 80), 0, 1)

                    elif exercise_code == 'LATERAL':
                        ok, msg = evaluator.evaluate_lateral_raise(
                            p(mp_pose.PoseLandmark.LEFT_SHOULDER),
                            p(mp_pose.PoseLandmark.LEFT_ELBOW),
                            p(mp_pose.PoseLandmark.LEFT_WRIST)
                        )
                        feedback.append((ok, msg))
                        reps = "--"

            except Exception as e:
                pass

            # 2. Draw Dashboard (The clean UI we made earlier)
            smooth_prog = smoother.filter(progress)
            draw_dashboard(image, reps, feedback, smooth_prog)

            # 3. Draw Skeleton
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # 4. Streamlit Display
            # Convert BGR (OpenCV) back to RGB (Streamlit)
            frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
            
            # Update Sidebar Stats
            rep_text.metric("Reps", reps)
            
            # Handle Sidebar Feedback Text
            if feedback:
                is_good, msg = feedback[0]
                if is_good:
                    feedback_text.success(f"✅ {msg}")
                else:
                    feedback_text.error(f"⚠️ {msg}")

    cap.release()


# --- INPUT HANDLING ---

if input_source == "Upload Video":
    uploaded_file = st.sidebar.file_uploader("Choose a video...", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        # Save uploaded file to a temporary file
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        
        st.toast("Video uploaded successfully!", icon="🚀")
        
        # Run the processing
        if st.button("Start Analysis"):
            process_video(tfile.name)

elif input_source == "Webcam":
    st.write("### Webcam Feed")
    if st.button("Start Webcam"):
        process_video(0)