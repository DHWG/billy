import paho.mqtt.client as mqtt
import logging
import subprocess
import time
import configuration
import movement
import speech

_log = logging.getLogger(__name__)

def on_mqtt_connect(client, userdata, flags, rc):
    _log.info('Connected to MQTT')
    client.subscribe('billy/speak')

def on_mqtt_message(client, userdata, msg):
    _log.info('Received MQTT message on "{}": {}'.format(msg.topic, str(msg.payload)))
    movement.turn_head()
    time.sleep(0.8)
    movement.speak(3)
    speech.say(msg.payload.decode('utf8'))
    time.sleep(0.2)
    movement.stop_all()

logging.basicConfig(level=logging.INFO)
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_mqtt_connect
mqtt_client.on_message = on_mqtt_message

mqtt_client.connect(configuration.MQTT_HOST, configuration.MQTT_PORT, 60)

mqtt_client.loop_forever()
