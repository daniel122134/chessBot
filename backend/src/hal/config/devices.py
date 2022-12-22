from backend.src.hal.VerticalLift import VerticalLift
from backend.src.hal.engine import Engine

STEP_PIN_VER = 15
DIR_PIN_VER = 14

STEP_PIN_HOR = 1
DIR_PIN_HOR = 5

MODE_PIN1 = 6
MODE_PIN2 = 7
MODE_PIN3 = 8

vertical_engine1 = Engine(STEP_PIN_VER, DIR_PIN_VER, MODE_PIN1, MODE_PIN2, MODE_PIN3)
horizontal_engine1 = Engine(STEP_PIN_HOR, DIR_PIN_HOR, 9, 10, 11)

LIFT_PIN_POS = 2
LOWER_PIN_POS = 3
LIFT_PIN_NEG = 4
LOWER_PIN_NEG = 17
lift = VerticalLift(LIFT_PIN_POS, LOWER_PIN_POS, LIFT_PIN_NEG, LOWER_PIN_NEG)
