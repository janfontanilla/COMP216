from group_3_util import Util
import json
import paho.mqtt.client as mqtt
import time

util = Util()
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.connect("broker.emqx.io", 1883, 60) #connects to host, on port 1883. kept alive for 60 sec

for i in range(5):

    payload = util.create_data()
    #converts python into json
    message = json.dumps(payload)
    #sends message to anyone subscribed 
    client.publish("group3/vitals", message)
    print("Published: ", message)
    time.sleep(2)

client.disconnect()
