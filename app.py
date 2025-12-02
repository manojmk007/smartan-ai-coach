import streamlit as st
import cv2
import tempfile
import numpy as np
import mediapipe as mp
import time
import os
from src.rules import FormEvaluator
from src.utils import draw_dashboard

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Smartan AI Coach",
    page_icon="💪",
    layout="wide"
)

# --- SIDEBAR ---
st.sidebar.title("Smartan AI Coach 🤖")
st.sidebar.markdown("Computer Vision Fitness Analysis")
st.sidebar.divider()

mode = st.sidebar.selectbox("Select Exercise:", ["Bicep Curl", "Squat", "Pushup", "Lateral Raise"])
MODE_MAP = {"Bicep Curl": "CURL", "Squat": "SQUAT", "Pushup": "PUSHUP", "Lateral Raise": "LATERAL"}
exercise_code = MODE_MAP[mode]

input_source = st.sidebar.radio("Video Input:", ("Upload Video", "Webcam"))

st.sidebar.divider()
st.sidebar.info("Processed videos will be saved to the 'output' folder.")

# --- HELPERS ---
class LowPassFilter:
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.prev = None
    def filter(self, val):
        if self.prev is None: self.prev = val
        else: self.prev = self.alpha * val + (1 - self.alpha) * self.prev
        return self.prev

# --- PROCESSING ENGINE ---
def process_video_stream(video_source):
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    evaluator = FormEvaluator()
    smoother = LowPassFilter(0.15)

    cap = cv2.VideoCapture(video_source)
    
    # --- VIDEO WRITER SETUP (NEW) ---
    # 1. Get video properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0: fps = 30 # Default if webcam fails to report FPS

    # 2. Define output path
    if not os.path.exists('output'): os.makedirs('output')
    output_filename = f"output/processed_{exercise_code.lower()}.mp4"
    
    # 3. Initialize Writer
    out = cv2.VideoWriter(output_filename, 
                          cv2.VideoWriter_fourcc(*'mp4v'), 
                          fps, 
                          (frame_width, frame_height))
    
    # UI Layout
    col_vid, col_stats = st.columns([3, 1])
    
    with col_vid:
        st_frame = st.empty()
    
    with col_stats:
        st.markdown("### Live Stats")
        st_reps = st.metric("Reps", 0)
        st_feedback = st.empty()
        st.caption(f"Saving to: `{output_filename}`")

    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: 
                break
            
            # Prep Image
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            reps = 0
            feedback = []
            progress = 0.0

            try:
                if results.pose_world_landmarks:
                    lm = results.pose_world_landmarks.landmark
                    def p(idx): return [lm[idx.value].x, lm[idx.value].y, lm[idx.value].z]

                    # LOGIC ROUTING
                    if exercise_code == 'CURL':
                        angle, reps = evaluator.evaluate_bicep_curl(
                            p(mp_pose.PoseLandmark.LEFT_SHOULDER),
                            p(mp_pose.PoseLandmark.LEFT_ELBOW),
                            p(mp_pose.PoseLandmark.LEFT_WRIST))
                        swing_ok, swing_msg = evaluator.check_elbow_swing(
                            p(mp_pose.PoseLandmark.LEFT_SHOULDER),
                            p(mp_pose.PoseLandmark.LEFT_ELBOW),
                            p(mp_pose.PoseLandmark.LEFT_HIP))
                        feedback.append((swing_ok, swing_msg))
                        progress = np.clip((160 - angle) / (160 - 30), 0, 1)

                    elif exercise_code == 'SQUAT':
                        angle, reps, back_ok, back_msg = evaluator.evaluate_squat(
                            p(mp_pose.PoseLandmark.LEFT_HIP),
                            p(mp_pose.PoseLandmark.LEFT_KNEE),
                            p(mp_pose.PoseLandmark.LEFT_ANKLE),
                            p(mp_pose.PoseLandmark.LEFT_SHOULDER))
                        feedback.append((back_ok, back_msg))
                        progress = np.clip((170 - angle) / (170 - 80), 0, 1)
                    
                    elif exercise_code == 'PUSHUP':
                         angle, reps, form_ok, form_msg = evaluator.evaluate_pushup(
                            p(mp_pose.PoseLandmark.LEFT_SHOULDER),
                            p(mp_pose.PoseLandmark.LEFT_ELBOW),
                            p(mp_pose.PoseLandmark.LEFT_WRIST),
                            p(mp_pose.PoseLandmark.LEFT_HIP),
                            p(mp_pose.PoseLandmark.LEFT_ANKLE))
                         feedback.append((form_ok, form_msg))
                         progress = np.clip((170 - angle) / (170 - 80), 0, 1)

                    elif exercise_code == 'LATERAL':
                        ok, msg = evaluator.evaluate_lateral_raise(
                            p(mp_pose.PoseLandmark.LEFT_SHOULDER),
                            p(mp_pose.PoseLandmark.LEFT_ELBOW),
                            p(mp_pose.PoseLandmark.LEFT_WRIST))
                        feedback.append((ok, msg))
                        reps = "--"
            except Exception: pass

            # Draw Dashboard
            smooth_prog = smoother.filter(progress)
            draw_dashboard(image, reps, feedback, smooth_prog)
            
            # Draw Skeleton
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # --- SAVE FRAME TO VIDEO ---
            out.write(image)

            # Render to Streamlit
            frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            st_frame.image(frame_rgb, channels="RGB", use_container_width=True)
            
            st_reps.metric("Reps", reps)
            if feedback:
                is_good, msg = feedback[0]
                if is_good: st_feedback.success(msg)
                else: st_feedback.error(msg)

    # Cleanup
    cap.release()
    out.release() # <--- IMPORTANT: Saves the file
    st.success(f"Video saved successfully to: {output_filename}")

# --- MAIN APP LOGIC ---

st.title(f"Analysis Mode: {mode}")

if input_source == "Upload Video":
    uploaded_file = st.sidebar.file_uploader("Upload MP4/MOV", type=["mp4", "mov", "avi"])
    if uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        if st.button("▶️ Start Analysis", type="primary"):
            process_video_stream(tfile.name)

elif input_source == "Webcam":
    if st.button("📷 Start Webcam", type="primary"):
        process_video_stream(0)
