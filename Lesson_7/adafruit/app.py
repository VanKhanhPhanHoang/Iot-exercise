import time
import json
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
from Adafruit_IO import MQTTClient

CounterFitConnection.init('127.0.0.1', 5000)

# Adafruit IO 
ADAFRUIT_IO_USERNAME = 'vankhanhhh'
ADAFRUIT_IO_KEY = 'aio_SYJl20f2AD6gidpHtHiy4BJymdUM'

SOIL_FEED = 'soil-moisture'
RELAY_FEED = 'relay-command'

# Relay and sensor
adc = ADC()
relay = GroveRelay(5)

#Handle data from Adafruit
def connected(client):
    print('Connected to Adafruit IO')
    client.subscribe(RELAY_FEED)

def message(client, feed_id, payload):
    print(f'Received message from {feed_id}: {payload}')
    if payload == 'on':
        relay.on()
    elif payload == 'off':
        relay.off()

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.on_connect = connected
client.on_message = message

# Connect to Adafruit IO
client.connect()
client.loop_background()

while True:
    soil_moisture = adc.read(0)
    print("Soil moisture:", soil_moisture)
    
    client.publish(SOIL_FEED, soil_moisture)
    time.sleep(10)
