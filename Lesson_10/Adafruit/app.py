from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import paho.mqtt.client as mqtt
import json

# Adafruit IO Credentials
ADAFRUIT_IO_USERNAME = "vankhanhhh"
ADAFRUIT_IO_KEY = "aio_SYJl20f2AD6gidpHtHiy4BJymdUM"

# Feed names 
FEED_SOIL = "soil-moisture"
FEED_RELAY = "relay-command"

# Device Setup 
adc = ADC()
relay = GroveRelay(5)

# MQTT Setup 
def on_connect(client, userdata, flags, rc):
    print("Connected to Adafruit IO")
    client.subscribe(f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_RELAY}")

def on_message(client, userdata, msg):
    command = msg.payload.decode().lower()
    print(f"Relay Command: {command}")
    if command == "on":
        relay.on()
        print("Relay turned ON")
    elif command == "off":
        relay.off()
        print("Relay turned OFF")

client = mqtt.Client()
client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect = on_connect
client.on_message = on_message

client.connect("io.adafruit.com", 1883, 60)
client.loop_start()

print("Publishing soil moisture readings...")

try:
    while True:
        # Read moisture from ADC 
        soil_moisture = adc.read(0)
        print(f"Soil Moisture: {soil_moisture}")

        # Send to Adafruit IO
        client.publish(f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_SOIL}", soil_moisture)

        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping")
    client.loop_stop()
    client.disconnect()
