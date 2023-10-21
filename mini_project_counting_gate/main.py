from machine import Pin, I2C
import network
import ssd1306
import dht
import time
from umqtt.simple import MQTTClient

SERVER      = "mqtt3.thingspeak.com"
CLIENT_ID   = "NQsOMB4WAh8OOAU3KAY2NQ0"
USR         = "NQsOMB4WAh8OOAU3KAY2NQ0"
PWD         = "i343xvHx0LuqhiB+ZhvFdSPE"
CH_ID       = "2314653"

#define LCD
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# 1 Connect WIFI
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("Connecting...")
    display.fill(0)
    display.text("Connecting...", 0, 0, 1)
    display.show()
    wlan.connect("@LINPHA-WIFI_2.4GHz", "")
    while not wlan.isconnected():
        pass
print("IP Address: ", wlan.ifconfig()[0])


# 2 Connect Broker
client = MQTTClient(CLIENT_ID, server=SERVER, user=USR, password=PWD, keepalive=30)
client.connect()
topic = "channels/" + CH_ID + "/publish"

in_sensor = Pin(4, Pin.IN)
out_sensor = Pin(5, Pin.IN)

# build-in led
led = Pin(2, Pin.OUT)
cnt_in = 0
cnt_out = 0
print("ready")

def publish_data():
    # publish data
    payload = "field1=" + str(cnt_in) + "&field2=" + str(cnt_out)
    client.connect()
    client.publish(topic, payload)
    client.disconnect()
    
while True:
    if( in_sensor.value() == 0):
        cnt_in = cnt_in + 1
        print("in: {}".format(cnt_in))
        publish_data()
        while(in_sensor.value() == 0):
            time.sleep(0.1)
            
    if( out_sensor.value() == 0):
        cnt_out = cnt_out + 1
        print("out: {}".format(cnt_out))
        publish_data()
        while(out_sensor.value() == 0):
            time.sleep(0.1)
        
    time.sleep(0.1)
        

#     
#     # print to screen
#     print("temperature:{}".format(temperature))
#     print("humidity:{}".format(humidity))
#     display.fill(0)
#     display.text("Temp: {}".format(temperature), 0, 0, 1)
#     display.text("Humidity: {}".format(humidity), 0, 10, 1)
#     display.show()
# 
#     # publish data
#     payload = "field1=" + str(temperature) + "&field2=" + str(humidity)
#     client.connect()
#     client.publish(topic, payload)
#     client.disconnect()
# 
#     # Toggle signal on LED
#     led.on()
#     time.sleep(1)

    