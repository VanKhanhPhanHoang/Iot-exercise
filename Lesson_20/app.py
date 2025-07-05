import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

# Load the TFLite model
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get model input/output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    img = cv2.resize(frame, (300, 300))
    input_data = np.expand_dims(img, axis=0).astype(np.uint8)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Get detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]

    for i in range(len(scores)):
        if scores[i] > 0.5:
            print(f"Detected: {int(classes[i])}, Confidence: {scores[i]}")

    cv2.imshow("Object Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
