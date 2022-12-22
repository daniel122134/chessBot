import time

from gpiozero import DigitalOutputDevice


class VerticalLift:
    def __init__(self, lift_pin, lower_pin):
        self.lift_pin_device = DigitalOutputDevice(lift_pin)
        self.lower_pin_device = DigitalOutputDevice(lower_pin)

    def lift(self):
        self.lift_pin_device.on()
        time.sleep(1)
        self.lift_pin_device.off()

    def lower(self):
        self.lower_pin_device.on()
        time.sleep(1)
        self.lower_pin_device.off()
