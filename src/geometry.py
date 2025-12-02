import numpy as np

def calculate_angle_3d(a, b, c):
    """
    Calculates the 3D angle at vertex b given points a, b, c.
    Inputs are [x, y, z] coordinates.
    Uses vector dot product: v1 . v2 = |v1| |v2| cos(theta)
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # Create vectors BA and BC
    v1 = a - b
    v2 = c - b

    # Calculate cosine of the angle
    cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    # Clip to handle potential float precision errors outside -1..1
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    angle = np.arccos(cosine_angle)
    
    # Convert to degrees
    return np.degrees(angle)