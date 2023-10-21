from machine import Pin
import network
import time
from umqtt.simple import MQTTClient

SERVER      = "mqtt3.thingspeak.com"
CLIENT_ID   = "CLIENT_ID"
USR         = "USERNAME"
PWD         = "PASSWORD"
CH_ID       = "CHANNEL_ID"

topic = "channels/" + CH_ID + "/publish"

# 1 Connect WIFI
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("Connecting...")
    wlan.connect("Wokwi-GUEST", "")
    while not wlan.isconnected():
        pass
print("IP Address: ", wlan.ifconfig()[0])


def sub_cb(topic_t, msg):
  print(topic_t)
  print(msg)

  client.publish(topic, "field1={}".format(msg))

# 2 Connect Broker
client = MQTTClient(CLIENT_ID, server=SERVER, user=USR, password=PWD, keepalive=30)
client.set_callback(sub_cb)
client.connect()

client.subscribe('channels/' + CH_ID + '/subscribe/fields/field3')

while True:
    client.check_msg()

    