import azure.cognitiveservices.speech as speechsdk
from azure.iot.device import IoTHubDeviceClient, Message

# Hàm nhận diện giọng nói
def speech_to_text(language, audio_file):
    speech_config = speechsdk.SpeechConfig(subscription="<your_subscription_key>", region="<your_region>")
    speech_config.speech_recognition_language = language
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once()
    return result.text

# Hàm gửi tin nhắn qua IoT Hub
def send_message_to_device(text, language):
    connection_string = "<your_connection_string>"
    client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    
    message = Message(f'{{"text": "{text}", "language": "{language}"}}')
    client.send_message(message)
    print("Sent message to Device 2")

# Chạy chương trình
if __name__ == "__main__":
    text = speech_to_text('en-US', 'audio.wav')  # Chuyển giọng nói thành văn bản (ở đây là tiếng Anh)
    send_message_to_device(text, 'en')  # Gửi văn bản qua IoT Hub
