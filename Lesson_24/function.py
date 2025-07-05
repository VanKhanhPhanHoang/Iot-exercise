import logging
import azure.functions as func
import requests
from azure.iot.device import IoTHubMessage

# Hàm dịch văn bản bằng Translator API
def translate_text(text, from_lang, to_lang):
    subscription_key = "<your_subscription_key>"
    endpoint = "https://api.cognitive.microsofttranslator.com/translate"
    params = {
        'api-version': '3.0',
        'from': from_lang,
        'to': to_lang
    }
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/json'
    }
    body = [{'text': text}]
    response = requests.post(endpoint, params=params, headers=headers, json=body)
    return response.json()[0]['translations'][0]['text']

# Hàm xử lý sự kiện từ IoT Hub
def main(msg: IoTHubMessage):
    text = msg.get_body().decode('utf-8')
    # Giả sử chúng ta nhận được JSON có dạng {'text': 'hello', 'language': 'en'}
    text_data = json.loads(text)
    original_text = text_data['text']
    language = text_data['language']
    
    translated_text = translate_text(original_text, language, 'es')  # Dịch sang tiếng Tây Ban Nha
    print(f"Translated Text: {translated_text}")
    
    # Gửi văn bản đã dịch về Device 2
    send_message_to_device(translated_text)

# Gửi văn bản dịch qua IoT Hub
def send_message_to_device(text):
    connection_string = "<your_connection_string>"
    client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    
    message = Message(f'{{"text": "{text}"}}')
    client.send_message(message)
    print("Sent translated message to Device 2")
