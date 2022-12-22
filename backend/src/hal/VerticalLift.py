import time

from gpiozero import DigitalOutputDevice


class VerticalLift:
    def __init__(self, lift_pin_pos, lower_pin_pos, lift_pin_neg, lower_pin_neg):
        self.lift_pin_device_pos = DigitalOutputDevice(lift_pin_pos)
        self.lift_pin_device_neg = DigitalOutputDevice(lift_pin_neg)
        self.lower_pin_device_pos = DigitalOutputDevice(lower_pin_pos)
        self.lower_pin_device_neg = DigitalOutputDevice(lower_pin_neg)

    def lift(self):
        self.lift_pin_device_pos.on()
        self.lift_pin_device_neg.on()
        time.sleep(1)
        self.lift_pin_device_pos.off()
        self.lift_pin_device_neg.off()

    def lower(self):
        self.lower_pin_device_pos.on()
        self.lower_pin_device_neg.on()
        time.sleep(1)
        self.lower_pin_device_pos.off()
        self.lower_pin_device_neg.off()
