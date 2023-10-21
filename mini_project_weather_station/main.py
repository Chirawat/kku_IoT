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
CH_ID       = "2313579"

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
    wlan.connect("Nott-iPhone11", "hotspotpassword")
    while not wlan.isconnected():
        pass
print("IP Address: ", wlan.ifconfig()[0])


# 2 Connect Broker
client = MQTTClient(CLIENT_ID, server=SERVER, user=USR, password=PWD, keepalive=30)
client.connect()
topic = "channels/" + CH_ID + "/publish"

# Sensor connection
d = dht.DHT22( Pin(4) )

# build-in led
led = Pin(2, Pin.OUT)

while True:

    # meaure humidity and temperature
    led.off()
    d.measure()
    humidity = d.humidity()
    temperature = d.temperature()
    
    # print to screen
    print("temperature:{}".format(temperature))
    print("humidity:{}".format(humidity))
    display.fill(0)
    display.text("Temp: {}".format(temperature), 0, 0, 1)
    display.text("Humidity: {}".format(humidity), 0, 10, 1)
    display.show()

    # publish data
    payload = "field1=" + str(temperature) + "&field2=" + str(humidity)
    client.connect()
    client.publish(topic, payload)
    client.disconnect()

    # Toggle signal on LED
    led.on()
    time.sleep(1)

    