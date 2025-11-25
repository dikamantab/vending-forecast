import json
import threading
import requests
import paho.mqtt.client as mqtt
from app.config import settings

API_ENDPOINT = "http://api:8000/temperature/receive"

def on_connect(client, userdata, flags, rc):
    print("MQTT connected with result code", rc)
    client.subscribe(settings.MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        # forward to API
        requests.post(API_ENDPOINT, json=data, timeout=5)
    except Exception as e:
        print("MQTT message handling failed:", e)

def run_mqtt():
    client = mqtt.Client()
    if settings.MQTT_USERNAME:
        client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, 60)
        client.loop_forever()

def start_in_thread():
    t = threading.Thread(target=run_mqtt, daemon=True)
    t.start()