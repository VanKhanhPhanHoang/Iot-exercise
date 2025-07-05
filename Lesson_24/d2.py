import azure.cognitiveservices.speech as speechsdk

# Hàm chuyển văn bản thành giọng nói
def text_to_speech(text, language):
    speech_config = speechsdk.SpeechConfig(subscription="<your_subscription_key>", region="<your_region>")
    speech_config.speech_synthesis_language = language
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)

# Hàm nhận văn bản từ IoT Hub và chuyển thành giọng nói
def main():
    connection_string = "<your_connection_string>"
    client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    
    # Lắng nghe tin nhắn từ IoT Hub
    while True:
        message = client.receive_message()
        received_text = message.data.decode('utf-8')
        
        # Chuyển văn bản thành giọng nói
        text_to_speech(received_text, 'es-ES')  # Giả sử Device 2 sử dụng tiếng Tây Ban Nha
        print(f"Device 2 is speaking: {received_text}")

if __name__ == "__main__":
    main()
