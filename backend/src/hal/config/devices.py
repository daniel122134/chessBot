from backend.src.hal.VerticalLift import VerticalLift
from backend.src.hal.engine import Engine


STEP_PIN_1 = 25
DIR_PIN_1 = 24
vertical_engine1 = Engine(STEP_PIN_1, DIR_PIN_1, direction=False)


STEP_PIN_2 = 18
DIR_PIN_2 = 23
vertical_engine2 = Engine(STEP_PIN_2, DIR_PIN_2)


STEP_PIN_HOR = 15
DIR_PIN_HOR = 14
horizontal_engine1 = Engine(STEP_PIN_HOR, DIR_PIN_HOR)

horizontal_engines = [horizontal_engine1]
vertical_engines = [vertical_engine2,vertical_engine1]

LIFT_PIN_POS = 27
LOWER_PIN_POS = 22
LIFT_PIN_NEG = 10
LOWER_PIN_NEG = 17
lift = VerticalLift(LIFT_PIN_POS, LOWER_PIN_POS, LIFT_PIN_NEG, LOWER_PIN_NEG)
