import time
from sensor.proximity_sensor import is_fruit_nearby
from camera.capture import capture_image
from classifier.classify import classify_image
from led.control_led import set_led
from storage.save_result import save_result

print(" Fruit Quality Detector Started\n")

try:
    while True:
        if is_fruit_nearby():
            print("[System] Fruit detected!")
            img_path = capture_image()
            fruit, ripeness = classify_image(img_path)
            set_led(ripeness)
            save_result(fruit, ripeness)
            print("[System] Cycle complete.\n")
            time.sleep(5)
        else:
            print("[System] No fruit nearby.\n")
            time.sleep(2)
except KeyboardInterrupt:
    print("\n System stopped.")
