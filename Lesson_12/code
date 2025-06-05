from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
import counterfit_shims_serial
import pynmea2
import json
import paho.mqtt.client as mqtt

# Replace these with your actual Adafruit IO credentials
ADAFRUIT_IO_USERNAME = 'vankhanhhh'
ADAFRUIT_IO_KEY = 'aio_SYJl20f2AD6gidpHtHiy4BJymdUM'
FEED_NAME = 'gps-location'

# Adafruit IO MQTT broker info
broker = 'io.adafruit.com'
port = 1883
topic = f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_NAME}"

# Set up MQTT client
client = mqtt.Client()
client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

print("Connecting to Adafruit IO...")
client.connect(broker, port, 60)
print("Connected to Adafruit IO")

serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')

def send_gps_data(line):
    try:
        msg = pynmea2.parse(line)
        if msg.sentence_type == 'GGA':
            lat = pynmea2.dm_to_sd(msg.lat)
            lon = pynmea2.dm_to_sd(msg.lon)

            if msg.lat_dir == 'S':
                lat = lat * -1
            if msg.lon_dir == 'W':
                lon = lon * -1

            # Adafruit IO prefers flat data for simple feeds
            payload = json.dumps({"lat": lat, "lon": lon})
            print("Sending to Adafruit IO:", payload)
            client.publish(topic, payload)
    except pynmea2.ParseError:
        print("Failed to parse NMEA sentence")

while True:
    line = serial.readline().decode('utf-8').strip()

    while len(line) > 0:
        send_gps_data(line)
        line = serial.readline().decode('utf-8').strip()

    time.sleep(1)
