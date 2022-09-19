import sensor
import machine
from time import sleep_ms


class GarageDoor:
    def __init__(self, sensor_trig, sensor_echo, control_pin):
        
        self.trig = sensor_trig
        self.echo = sensor_echo
        self.controlPin = control_pin
        self.open_sensor = sensor.HCSR04(trigger_pin=self.trig, echo_pin=self.echo)
        self.opened = False
        self.control = machine.Pin(self.controlPin, machine.Pin.OUT)
            
            
    @property
    def get_opened(self):
        return self.opened
    
    def update_opened(self):
        try:
            dist = self.open_sensor.distance_cm()
            if dist < 50:
                self.opened = True
            else:
                self.opened = False
        except:
            self.opened = False
            print("failure occurred")
            
    def door_toggle(self):
        self.control.value(1)
        
        sleep_ms(50)
        self.control.value(0)
        
        self.update_opened()
        