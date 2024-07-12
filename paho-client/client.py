import paho.mqtt.client as mqtt
import time
# Configuration for the original MQTT broker
original_broker_host = "192.168.0.10"
original_broker_port = 1883
original_username = "txt"
original_password = "xtx"

# Configuration for the local MQTT broker on Raspberry Pi
local_broker_host = "192.168.0.5"  # Assuming the broker is running on the same Pi
local_broker_port = 1883
# local_client = mqtt.Client(client_id="Raspberry")

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 5
MAX_RECONNECT_COUNT = 10
MAX_RECONNECT_DELAY = 60


def on_connect_original(client, userdata, flags, rc):
    print("Connected to original broker")
    client.subscribe("#")  # Subscribe to all topics and subtopics on original broker

def on_connect_local(client, userdata, flags, rc):
    print("Connected to local broker")
    # Subscribe to topics on local broker if needed

def on_message_original(client, userdata, msg):
    if msg.topic == "i/cam":
        pass
    else:
        print(f"Topic: {msg.topic} \n Payload: {msg.payload.decode()}")
        # local_client.publish(msg.topic, msg.payload)

def on_message_local(client, userdata, msg):
    if msg.topic == "i/cam":
        pass
    else:
        print(f"Topic: {msg.topic} \n Payload: {msg.payload.decode()}")
        original_client.publish(msg.topic, msg.payload)

def on_disconnect(client, userdata, rc):
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        #print(f"Reconnecting {client.client_id} in {reconnect_delay} seconds...")
        time.sleep(reconnect_delay)
        
        try:
            client.reconnect()
            print("Reconnected successfully!")
            return
        except Exception as err:
            print("{err}. Reconnect failed. Retrying...")

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    client.loop_stop()
    client.disconnect()


original_client = mqtt.Client(client_id="TXT Controller")
# original_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
original_client.username_pw_set(original_username, original_password)

original_client.on_disconnect = on_disconnect
original_client.on_connect = on_connect_original
original_client.on_message = on_message_original

# local_client.on_connect = on_connect_local
# local_client.on_message = on_message_local


original_client.connect("192.168.0.10", 1883, 6000)
# local_client.connect(local_broker_host, local_broker_port, 60)
original_client.subscribe("hbw/#")
original_client.loop_forever()
# local_client.loop_forever()