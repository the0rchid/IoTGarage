# IoTGarage
SmartHome Garage Door opener utilizing ESP8266 and Micropython

To run this, for now, simply amend the constants.py file and upload all to an ESP8266 board. 

This code utilizes an ESP8266 with an ultrasonic rangefinder for door detection, a button for manual dooor activation, and a configured MQTT server for remote commands.
The MQTT server I use is a HomeAssistant Mosquitto Add-on which I have configured with automations in my HA instance to utilize the messages provided by and to the 8266 here.

There are still some parts to be completed such as LED functionality and final testing, but this is currently working correctly enough to make for viable testing.
Notably, I would like to test the US rangefinder and make sure it works for valid door position detection, which may require a separate device altogether,
depending on how well this functions utilizing long copper wires. If the resistance is too high, I may need a separate device. This shouldnt be an issue really, but it could be.

Finally, I need to build and test the circuit board and complete final code for multicolored LED functionality, which is what my LED.py was written to complete. If all
goes well, this should connect properly to wifi, add itself to the network, and seamlessly allow for control of my garage door via IoT and HA. 
