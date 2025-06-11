from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

from counterfit_shims_picamera import PiCamera
from counterfit_shims_grove.grove_led import GroveLed

from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import io

# Khởi tạo LED ở virtual pin 0
led = GroveLed(0)

# Khởi tạo camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0

# Chụp ảnh và lưu thành file
image_stream = io.BytesIO()
camera.capture(image_stream, 'jpeg')
image_stream.seek(0)

with open("image.jpg", "wb") as f:
    f.write(image_stream.read())

print("✅ Ảnh đã được chụp từ camera và lưu thành công!")

# Load model và nhãn
model = load_model("keras_Model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()

# Chuẩn bị ảnh để phân loại
image = Image.open("image.jpg").convert("RGB")
size = (224, 224)
image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
image_array = np.asarray(image)
normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
data[0] = normalized_image_array

# Phân loại ảnh
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index].strip()
confidence_score = prediction[0][index]

# In kết quả
print(f"\n🔍 Kết quả phân loại:")
print(f"🍎 Trái cây: {class_name}")
print(f"📊 Độ tin cậy: {confidence_score:.2f}")

# Bật/tắt LED mô phỏng trong CounterFit
if "unripe" in class_name.lower():
    led.on()
    print("🔆 LED ON - Phát hiện trái cây CHƯA chín")
else:
    led.off()
    print("💤 LED OFF - Trái cây ĐÃ chín")