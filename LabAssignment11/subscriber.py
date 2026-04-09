import json
import paho.mqtt.client as mqtt
from group_3_util import Util

util = Util()


# part A: handle each incoming message from the broker
def on_message(client, userdata, msg):
    decoded = msg.payload.decode('utf-8')  #decode the raw bytes into a string
    data = json.loads(decoded)  #convert the json string back into a dict

    print(f"received message on '{msg.topic}':")
    util.print_data(data)  #print the record


if __name__ == '__main__':

    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)  #create the mqtt client
    client.on_message = on_message  #wire up the handler

    client.connect("broker.emqx.io", 1883, 60)  #connect to the broker
    client.subscribe("group3/vitals")  #subscribe to the group's topic

    print("listening for messages on 'group3/vitals'...")
    client.loop_forever()  #keep listening for messages
