import cv2
import numpy as np

def draw_dashboard(image, reps, feedback_list, progress=0.0):
    """
    Draws a professional 'Glassmorphism' style dashboard on the left side of the frame.
    
    Args:
        image: The video frame (image array).
        reps: Integer or String (e.g., 10 or "--") for the counter.
        feedback_list: List of tuples -> [(True, "Good Job"), (False, "Fix Form")]
        progress: Float (0.0 to 1.0) representing the completion of a rep (ROM).
    """
    h, w, _ = image.shape
    
    # --- 1. SETTINGS & COLORS ---
    # Colors (B, G, R)
    COLOR_BG = (20, 20, 20)      # Dark Gray Background
    COLOR_TEXT_MAIN = (255, 255, 255) # White
    COLOR_TEXT_DIM = (180, 180, 180)  # Light Gray
    COLOR_GOOD = (0, 255, 0)     # Green
    COLOR_BAD = (50, 50, 255)    # Red
    COLOR_BAR_BG = (50, 50, 50)  # Darker Gray for empty bar
    COLOR_BAR_FILL = (0, 255, 255) # Yellow/Cyan mix for visibility

    # Dimensions
    panel_width = 320
    
    # --- 2. DRAW BACKGROUND PANEL (Glass Effect) ---
    overlay = image.copy()
    cv2.rectangle(overlay, (0, 0), (panel_width, h), COLOR_BG, -1)
    
    # Apply transparency (0.85 means 85% original image, but here we want dark overlay)
    # Actually: alpha=0.8 for overlay means it's mostly the overlay color
    alpha = 0.8
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
    
    # Draw a thin border line on the right of the panel
    cv2.line(image, (panel_width, 0), (panel_width, h), (100, 100, 100), 1)

    # --- 3. REP COUNTER SECTION ---
    # Label
    cv2.putText(image, "REPS", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, COLOR_TEXT_DIM, 1, cv2.LINE_AA)
    
    # Big Number
    cv2.putText(image, str(reps), (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 
                2.5, COLOR_TEXT_MAIN, 3, cv2.LINE_AA)

    # --- 4. PROGRESS BAR (Vertical) ---
    # Located to the right of the rep counter
    bar_x = 260
    bar_y = 50
    bar_w = 25
    bar_h = 100
    
    # Empty Bar container
    cv2.rectangle(image, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), COLOR_BAR_BG, -1)
    cv2.rectangle(image, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (150,150,150), 1) # Border
    
    # Filled portion (fills from bottom up)
    if progress > 0:
        fill_h = int(bar_h * progress)
        # Clamp fill to stay within bar
        fill_h = max(0, min(fill_h, bar_h))
        
        start_point = (bar_x, bar_y + bar_h - fill_h)
        end_point = (bar_x + bar_w, bar_y + bar_h)
        
        cv2.rectangle(image, start_point, end_point, COLOR_BAR_FILL, -1)

    # --- 5. SEPARATOR LINE ---
    cv2.line(image, (30, 170), (panel_width - 30, 170), (80, 80, 80), 1)

    # --- 6. FEEDBACK LIST (Dynamic) ---
    y_start = 210
    spacing = 45
    
    # If list is empty (e.g., waiting for user to start)
    if not feedback_list:
        cv2.putText(image, "Ready...", (30, y_start), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, COLOR_TEXT_DIM, 1, cv2.LINE_AA)
    
    for is_good, message in feedback_list:
        # 1. Draw Status Dot (Circle)
        circle_color = COLOR_GOOD if is_good else COLOR_BAD
        cv2.circle(image, (40, y_start - 8), 6, circle_color, -1)
        
        # 2. Draw Message Text
        text_color = COLOR_TEXT_MAIN if is_good else COLOR_BAD
        cv2.putText(image, message, (65, y_start), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, text_color, 1, cv2.LINE_AA)
        
        y_start += spacing

    return image