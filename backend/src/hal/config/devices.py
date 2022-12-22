from backend.src.hal.VerticalLift import VerticalLift
from backend.src.hal.engine import Engine

STEP_PIN_VER = 1
DIR_PIN_VER = 2

STEP_PIN_HOR = 1
DIR_PIN_HOR = 2

MODE_PIN1 = 3
MODE_PIN2 = 4
MODE_PIN3 = 5

vertical_engine1 = Engine(STEP_PIN_VER, DIR_PIN_VER, MODE_PIN1, MODE_PIN2, MODE_PIN3)
horizontal_engine1 = Engine(STEP_PIN_HOR, DIR_PIN_HOR, MODE_PIN1, MODE_PIN2, MODE_PIN3)

LIFT_PIN = 1
LOWER_PIN = 2
lift = VerticalLift(LIFT_PIN, LOWER_PIN)
