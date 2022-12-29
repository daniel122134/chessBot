import asyncio
import time

from gpiozero import DigitalOutputDevice

from backend.src.hal.config.steps_config import prec_configuration_mapping

INTERVAL = 0.001


class Engine:
    def __init__(self, step_pin, dir_pin, mode1, mode2, mode3, distance_out=0, percision=1, direction=True):
        self.step_pin = DigitalOutputDevice(step_pin)
        self.dir_pin = DigitalOutputDevice(dir_pin)
        self.mode1 = DigitalOutputDevice(mode1)
        self.mode2 = DigitalOutputDevice(mode2)
        self.mode3 = DigitalOutputDevice(mode3)
        self.distance_out = distance_out
        self.direction = direction
        self.precision = percision
        self.apply_percision()

    def engine_move(self, steps=100, interval=INTERVAL):
        sleep_time = interval / self.precision
        if steps < 0:
            self.change_dir()

        for i in range(abs(int(steps))):
            self.step_pin.on()
            time.sleep(interval)
            self.step_pin.off()
            time.sleep(interval*100)
            # await asyncio.sleep(sleep_time)
            if self.direction:
                self.distance_out += 1 / self.precision
            else:
                self.distance_out -= 1 / self.precision

        if steps < 0:
            self.change_dir()

    def change_dir(self):
        self.direction = not self.direction
        self.dir_pin.toggle()

    def apply_percision(self):
        self.mode1.off()
        self.mode2.off()
        self.mode3.off()
        if prec_configuration_mapping[self.precision]["ms0"]:
            self.mode1.on()
        if prec_configuration_mapping[self.precision]["ms1"]:
            self.mode2.on()
        if prec_configuration_mapping[self.precision]["ms2"]:
            self.mode3.on()
