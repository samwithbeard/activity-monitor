# activity monitor
import psutil
import paho.mqtt.client as mqtt
import time
import signal
import sys
import json
import getpass
import platform

# MQTT Configuration
MQTT_BROKER = "192.168.1.114"
MQTT_PORT = 1883
MQTT_TOPIC = "gaming/monitor"
PC_ID = getpass.getuser()  # Unique identifier for each PC

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def send_process_info():
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        process_list.append(proc.info)

    message = json.dumps({'pc_id': PC_ID, 'processes': process_list})
    print(message)
    client.publish(MQTT_TOPIC, message)

def on_exit(sig, frame):
    print("Script beendet")
    client.publish(MQTT_TOPIC, json.dumps({'pc_id': PC_ID, 'message': 'Script beendet'}))
    client.disconnect()
    sys.exit(0)

# Signal handler for script termination
signal.signal(signal.SIGINT, on_exit)
signal.signal(signal.SIGTERM, on_exit)

def main():
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    while True:
        send_process_info()
        time.sleep(10)

if __name__ == "__main__":
    main()
