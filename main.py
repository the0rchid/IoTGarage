from time import sleep
from time import sleep_ms

import machine
import network
from machine import Pin

import umqttsimple
from LED import LED
# Import separate constants file for usernames and passwords as well as internal IPs.
from constants import *
from garagedoor import GarageDoor

__version__ = '0.0.1'
__author__ = 'Andrew Core'

BUTTON_PIN = 5

DOOR_SENSOR_TRIG = 4
DOOR_SENSOR_ECHO = 0
DOOR_TOGGLE = 2
SENSOR_ACTIVATOR = 14

redLed = LED(13, 'RED')
button_press = False

i = 1


# Connection method, called to start a wifi connection

def connect():
    i = 0
    while i < 5:
        i += 1
        print("Connecting")
        wlan.connect(WIFI_NAME, WIFI_PASS)
        sleep(5)
        if wlan.isconnected():
            print("Connected")
            print(wlan.ifconfig())
            return
        else:
            print("Still disconnected. Retrying")
            print("Attempts left: ", 5 - i)


# Button interrupt handler, must be changed to False in code after execution

def button_interrupt(pin):
    print("Interrupt")
    global button_press
    button_press = True


# Updates door status and publishes to MQTT
def update_door():
    garage_door.update_opened()
    if garage_door.get_opened:
        mqtt_client.publish(topic="GStatus", msg="door_opened")
    else:
        mqtt_client.publish(topic="GStatus", msg="door_closed")


# MQTT Command processing code. All MQTT control messages are handled by this.
def process_command(topic, msg):
    print(topic)
    print(str(msg, 'UTF-8'))

    if msg == b'open_door':
        garage_door.update_opened()
        if not garage_door.get_opened:
            garage_door.door_toggle()
            print("opening door")
            sleep(10)
            update_door()
    elif msg == b'close_door':
        garage_door.update_opened()
        if garage_door.get_opened:
            garage_door.door_toggle()
            print("closing door")
            sleep(10)
            update_door()
    elif msg == b'force_update':
        update_door()

    else:
        mqtt_client.publish(topic="Errors", msg="Garage Door bad message received")


# _______________________________MAIN METHOD_____________________
if __name__ == '__main__':

    # Set up button and handler code, note that handler does not get an execution of the function, it will be called in code after interrupt happens.
    button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    button.irq(handler=button_interrupt, trigger=Pin.IRQ_RISING)

    # Early testing and small code here, this simply is here to make sure the board is initialized properly
    led = Pin(2, Pin.OUT)
    j = 0

    # Start of the running code for the door opener control, will run until failure.
    try:

        # Connection initiation code
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        connect()
        # Sensor activation prevents failure due to attempting to run sensor during boot-up. Once boot happens, the pin goes LOW, which allows the PNP N gate to drain and activate transistor.
        # Installed LED indicates sensor is active.

        garage_door = GarageDoor(DOOR_SENSOR_TRIG, DOOR_SENSOR_ECHO, DOOR_TOGGLE)

        sensor_activator = Pin(SENSOR_ACTIVATOR, Pin.OUT, value=0)

        mqtt_client = umqttsimple.MQTTClient(MQTT_CLIENT, MQTT_IP, user=MQTT_USER, password=MQTT_PASS)
        mqtt_client.set_last_will(topic="DeviceStatus", msg="garage_door_controller offline")
        mqtt_client.connect()
        mqtt_client.publish(topic="DeviceStatus", msg="garage_door_controller online", retain=True)
        mqtt_client.set_callback(process_command)
        mqtt_client.subscribe(topic="GControl")

        while True:

            # Iterating loop, this is simply to make sure we arent checking the door status every .1 seconds, but instead every 10 seconds. We want to check all other messages more frequently, so they get different iteration intervals.
            i %= 100

            if i == 0:
                update_door()

            if button_press:
                # Debugging print
                # print("Interrupt")
                if redLed.get_state:
                    redLed.turn_off()
                else:
                    redLed.turn_on()
                sleep_ms(100)
                garage_door.door_toggle()
                button_press = False

            if not wlan.isconnected():
                wlan.connect()

            mqtt_client.check_msg()
            sleep_ms(100)
            i += 1




    except:
        print("An error occurred")
