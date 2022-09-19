import machine


class LED(object):
    def __init__(self, pin=0, color=None, invert=False):
        self.color = color
        self.pin = pin
        self.state = False
        self.invert_pin = invert
        self.led_pin = machine.Pin(pin, machine.Pin.OUT)
        self.led_signal = machine.Signal(self.led_pin, invert=self.invert_pin)

    def set_pin(self, pin):
        self.pin = pin
        self.led_pin = machine.Pin(pin, machine.Pin.OUT)

    @property
    def get_pin(self):
        return self.pin

    def set_color(self, color):
        self.color = color

    @property
    def get_color(self):
        return self.color

    @property
    def get_state(self):
        return self.state

    def turn_on(self):
        self.state = True
        self.led_signal.on()

    def turn_off(self):
        self.state = False
        self.led_signal.off()
