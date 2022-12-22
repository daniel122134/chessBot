import asyncio

from gpiozero import DigitalOutputDevice

from backend.hal.config.steps_config import prec_configuration_mapping

INTERVAL = 0.001


class Engine:
    def __init__(self, step_pin, dir_pin, mode1, mode2, mode3, distance_out, percision=1, direction=True):
        self.step_pin = DigitalOutputDevice(step_pin)
        self.dir_pin = DigitalOutputDevice(dir_pin)
        self.mode1 = DigitalOutputDevice(mode1)
        self.mode2 = DigitalOutputDevice(mode2)
        self.mode3 = DigitalOutputDevice(mode3)
        self.distance_out = distance_out
        self.direction = direction
        self.precision = percision
        self.apply_percision()

    async def engine_move(self, steps=100):
        sleep_time = INTERVAL / self.precision
        if steps <0:
            self.change_dir()

        for i in range(abs(steps)):
            self.step_pin.toggle()
            await asyncio.sleep(sleep_time)
            if self.direction:
                self.distance_out += 1/self.precision
            else:
                self.distance_out -= 1/self.precision

        if steps<0:
            self.change_dir()

    def change_dir(self):
        self.direction = not self.direction
        self.dir_pin.toggle()

    def apply_percision(self):
        self.mode1.off()
        self.mode2.off()
        self.mode3.off()
        if prec_configuration_mapping[self.precision]["m0"]:
            self.mode1.on()
        if prec_configuration_mapping[self.precision]["m1"]:
            self.mode2.on()
        if prec_configuration_mapping[self.precision]["m2"]:
            self.mode3.on()
