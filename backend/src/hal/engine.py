import asyncio
import time

from gpiozero import DigitalOutputDevice

from backend.src.hal.config.steps_config import prec_configuration_mapping

INTERVAL = 0.0001


class Engine:
    def __init__(self, step_pin, dir_pin,  distance_out=0, direction=True):
        self.step_pin = DigitalOutputDevice(step_pin)
        self.dir_pin = DigitalOutputDevice(dir_pin)

        self.distance_out = distance_out
        self.direction = direction
        if direction:
            self.change_dir()

    async def engine_move(self, steps=100, interval=INTERVAL):
        sleep_time = interval 
        print(steps)
        print(self.direction)
        print(self.dir_pin.is_active)
        if steps < 0:
            self.change_dir()

        for i in range(abs(int(steps))):
            self.step_pin.toggle()
            # time.sleep(interval)
            await asyncio.sleep(interval)
            
        self.distance_out += steps
        
        if steps < 0:
            self.change_dir()

    def change_dir(self):
        self.direction = not self.direction
        self.dir_pin.toggle()

