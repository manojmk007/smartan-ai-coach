import numpy as np
from math import acos, degrees

class FormEvaluator:

    def __init__(self):
        # counters
        self.curl_stage = "down"
        self.curl_count = 0

        self.squat_stage = "up"
        self.squat_count = 0

        self.pushup_stage = "up"
        self.pushup_count = 0

    def _angle(self, a, b, c):
        """
        Returns angle ABC (in degrees).
        """
        a, b, c = np.array(a), np.array(b), np.array(c)
        ba = a - b
        bc = c - b
        
        norm_ba = np.linalg.norm(ba)
        norm_bc = np.linalg.norm(bc)

        if norm_ba == 0 or norm_bc == 0:
            return 0.0

        dot = np.dot(ba, bc)
        # Calculate cosine
        cosine_angle = dot / (norm_ba * norm_bc)
        # Clip to prevent NaN errors due to floating point precision
        angle = degrees(acos(np.clip(cosine_angle, -1.0, 1.0)))
        return angle

    # ======================================================
    #                      BICEP CURL
    # ======================================================
    def evaluate_bicep_curl(self, shoulder, elbow, wrist):
        angle = self._angle(shoulder, elbow, wrist)

        # Identify stages
        if angle > 150:
            self.curl_stage = "down"
        if angle < 40 and self.curl_stage == "down":
            self.curl_stage = "up"
            self.curl_count += 1

        return angle, self.curl_count

    def check_elbow_swing(self, shoulder, elbow, hip):
        """
        Fixed: Checks angle between Torso (Shoulder-Hip) and Arm (Shoulder-Elbow).
        """
        # Calculate Angle between Torso vector and Upper Arm vector
        # Ideally, this should be close to 0 (parallel) or small.
        # Note: We use the Shoulder as the vertex.
        swing_angle = self._angle(hip, shoulder, elbow)

        # If arm is tight to body, angle is small (< 20-30 degrees)
        # If elbow swings forward, angle increases.
        if swing_angle < 30:
            return True, "Elbows Stable"
        return False, "Lock Elbows!"

    # ======================================================
    #                    LATERAL RAISE
    # ======================================================
    def evaluate_lateral_raise(self, shoulder, elbow, wrist):
        # Check alignment: Wrist shouldn't be higher than shoulder
        # Using Y-coordinate check is often more stable than angles for this specific rule
        # in 3D landmark space (where Y is often Up/Down).
        
        # However, using your angle logic against vertical:
        # Create a virtual vertical point above the shoulder
        vertical_point = [shoulder[0], shoulder[1] - 0.5, shoulder[2]] # Moving up in Y
        
        # Measure angle between Vertical-Shoulder-Elbow
        raise_angle = self._angle(vertical_point, shoulder, elbow)

        # Ideally close to 90 degrees
        if 80 <= raise_angle <= 110:
            return True, "Good Alignment"
        elif raise_angle < 80:
            return False, "Lift Higher"
        else:
            return False, "Too High!"

    # ======================================================
    #                          SQUAT
    # ======================================================
    def evaluate_squat(self, hip, knee, ankle, shoulder):
        knee_angle = self._angle(hip, knee, ankle)

        # detect stage
        if knee_angle > 160:
            self.squat_stage = "up"
        if knee_angle < 90 and self.squat_stage == "up":
            self.squat_stage = "down"
            self.squat_count += 1

        # Back straightness (Torso vs Vertical)
        # Create virtual point above hip
        vertical_point = [hip[0], hip[1] - 0.5, hip[2]]
        
        torso_inclination = self._angle(vertical_point, hip, shoulder)
        
        # In a squat, you lean forward, but not too much. 
        # 0 deg = vertical. > 45 deg = likely too much lean.
        back_ok = torso_inclination < 45

        msg = "Back Stable" if back_ok else "Chest Up!"

        return knee_angle, self.squat_count, back_ok, msg

    # ======================================================
    #                         PUSHUP
    # ======================================================
    def evaluate_pushup(self, shoulder, elbow, wrist, hip, ankle):
        elbow_angle = self._angle(shoulder, elbow, wrist)

        # detect stage
        if elbow_angle > 160:
            self.pushup_stage = "up"
        if elbow_angle < 90 and self.pushup_stage == "up":
            self.pushup_stage = "down"
            self.pushup_count += 1

        # Torso straightness (Shoulder-Hip-Ankle line)
        body_angle = self._angle(shoulder, hip, ankle)
        
        # Should be close to 180
        form_ok = body_angle > 160

        msg = "Form Good" if form_ok else "Fix Hips!"

        return elbow_angle, self.pushup_count, form_ok, msg