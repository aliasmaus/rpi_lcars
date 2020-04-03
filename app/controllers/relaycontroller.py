from gpiozero import OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import time

class relaycontroller():
    relay=None
    def __init__(self, pin, remote=False, remotehost=None):
        if not remote:
            self.relay=OutputDevice(pin, active_high=False, initial_value=False)
        else:
            factory=PiGPIOFactory(host=remotehost)
            self.relay=OutputDevice(pin, active_high=False, initial_value=False, pin_factory=factory)

    def dothething(self):
        self.relay.on()
        time.sleep(0.5)
        self.relay.off()