from src.checkers.blinkcheck import BlinkCheck
from src.blinker import Blinker

EYE_IN_MAX = 20
EYE_OUT_MIN = 40

EYES_CLOSE_ON = 31
EYES_OPEN_ON = 33

def main():
    blink_checker = BlinkCheck(EYES_CLOSE_ON, EYES_OPEN_ON, True)
    blinker = Blinker(blink_checker, EYE_IN_MAX, EYE_OUT_MIN)

    blinker.run()
main()
