import pynmea2
from geopy.distance import geodesic
from twilio.rest import Client
import json

data = """
$GPGGA,101437.371,1037.045,N,25303.545,W,1,12,1.0,0.0,M,0.0,M,,*7E
$GPGSA,A,3,01,02,03,04,05,06,07,08,09,10,11,12,1.0,1.0,1.0*30
$GPRMC,101437.371,A,1037.045,N,25303.545,W,280290.6,042.9,280525,000.0,W*5A
$GPGGA,101438.371,1133.969,N,25209.492,W,1,12,1.0,0.0,M,0.0,M,,*73
$GPRMC,101438.371,A,1133.969,N,25209.492,W,317532.0,210.0,280525,000.0,W*5D
$GPGGA,101439.371,1017.598,N,25254.316,W,1,12,1.0,0.0,M,0.0,M,,*74
$GPGSA,A,3,01,02,03,04,05,06,07,08,09,10,11,12,1.0,1.0,1.0*30
$GPRMC,101439.371,A,1017.598,N,25254.316,W,317532.0,210.0,280525,000.0,W*5A
"""

config = json.load(open("config.json"))
center = (config["geofence"]["lat"], config["geofence"]["lon"])
radius = config["geofence"]["radius_m"]

for line in data.strip().split('\n'):
    if line.startswith("$GPGGA") or line.startswith("$GPRMC"):
        try:
            msg = pynmea2.parse(line)
            lat = msg.latitude
            lon = msg.longitude
            point = (lat, lon)
            dist = geodesic(center, point).meters
            if dist > radius:
                tw = config["twilio"]
                Client(tw["account_sid"], tw["auth_token"]).messages.create(
                    body=f"Device is outside geofence ({dist:.2f} m)",
                    from_=tw["from_number"],
                    to=tw["to_number"]
                )
        except:
            continue
