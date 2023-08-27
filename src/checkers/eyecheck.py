from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates
import math
import numpy as np
from src.models.EyeCord import EyeCord
from src.models.PointCord import PointCord

EYE_TOP_ID = 159
EYE_BOTTOM_ID = 145
EYE_LEFT_ID = 33
EYE_RIGHT_ID = 133

class EyeCheck:
    def __init__(self, width, height, ratios = []) -> None:
        self.width = width
        self.height = height
        self.ratios = ratios

    def eye_cords(self, landmark) -> EyeCord:
        eye_top = landmark[EYE_TOP_ID]
        eye_bottom = landmark[EYE_BOTTOM_ID]
        eye_left = landmark[EYE_LEFT_ID]
        eye_right = landmark[EYE_RIGHT_ID]

        eye_top_cord = _normalized_to_pixel_coordinates(eye_top.x, eye_top.y, self.width, self.height)
        eye_bottom_cord = _normalized_to_pixel_coordinates(eye_bottom.x, eye_bottom.y, self.width, self.height)
        eye_left_cord = _normalized_to_pixel_coordinates(eye_left.x, eye_left.y, self.width, self.height)
        eye_right_cord = _normalized_to_pixel_coordinates(eye_right.x, eye_right.y, self.width, self.height)

        return EyeCord(eye_top_cord, eye_bottom_cord, eye_left_cord, eye_right_cord)

    def eyes_distance(self, eye_cords):
        vertical_distance = _calc_distance(eye_cords.top, eye_cords.bottom)
        horizontal_distance = _calc_distance(eye_cords.right, eye_cords.left)

        return [vertical_distance, horizontal_distance]
    
    def blink_ratio(self, vertical_distance, horizontal_distance):
        ratio = (horizontal_distance / vertical_distance)
        self.ratios.append(ratio)

        if len(self.ratios) == 5:
            self.ratios.pop(0)

        return np.mean(self.ratios)

def _calc_distance(a: PointCord, b: PointCord) -> float:
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
