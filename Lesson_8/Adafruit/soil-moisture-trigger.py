from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import paho.mqtt.client as mqtt
import json

#Adafruit IO 
ADAFRUIT_IO_USERNAME = 'vankhanhhh'
ADAFRUIT_IO_KEY = 'aio_SYJl20f2AD6gidpHtHiy4BJymdUM'
BROKER = 'io.adafruit.com'
PORT = 1883
FEED_SOIL = 'soil-moisture'
FEED_RELAY = 'relay-command'

# Connect Counterfit
adc = ADC()
relay = GroveRelay(5)

# MQTT setup 
def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Command received: {command}")
    if command == 'on':
        relay.on()
        print("Relay turned ON")
    elif command == 'off':
        relay.off()
        print("Relay turned OFF")

client = mqtt.Client()
client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

# Subscribe to relay command
client.subscribe(f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_RELAY}")

print("Running")
try:
    while True:
        # Đọc dữ liệu cảm biến giả lập
        soil = adc.read(0)
        print(f"Soil moisture: {soil}")

        # Gửi lên Adafruit IO
        client.publish(f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_SOIL}", soil)

        time.sleep(5)

except KeyboardInterrupt:
    print("Stopping")
    client.loop_stop()
    client.disconnect()
