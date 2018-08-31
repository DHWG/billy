import paho.mqtt.client as mqtt
from espeak import espeak
import time
import configuration
import movement

def on_mqtt_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe('billy/speak')

def on_mqtt_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))
    movement.turn_head()
    time.sleep(1)
    movement.speak(3)
    espeak.synth(str(msg.payload))
    while espeak.is_playing:
        time.sleep(0.1)
    time.sleep(0.2)
    movement.stop_all()

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_mqtt_connect
mqtt_client.on_message = on_mqtt_message

mqtt_client.connect(configuration.MQTT_HOST, configuration.MQTT_PORT, 60)

mqtt_client.loop_forever()
