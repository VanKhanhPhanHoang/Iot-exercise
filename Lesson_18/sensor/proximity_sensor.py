import random
import time

def is_fruit_nearby(threshold_cm=10):
    # Simulate distance measurement
    distance = random.uniform(5, 20)
    print(f"[Sensor] Measured distance: {distance:.2f} cm")
    return distance < threshold_cm
