import shutil
import os

def capture_image(destination="captured.jpg"):
    # Simulate capturing by copying a test image
    source = "test_images/banana.jpg"
    if not os.path.exists(source):
        raise FileNotFoundError("Test image not found.")
    shutil.copy(source, destination)
    print("[Camera] Image captured and saved as", destination)
    return destination
