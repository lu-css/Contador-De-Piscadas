from src.models.PointCord import PointCord

class EyeCord:
    def __init__(self, top_eye, bottom_eye, left_eye, right_eye) -> None:
        self.top = PointCord(top_eye[0], top_eye[1])
        self.bottom = PointCord(bottom_eye[0], bottom_eye[1])
        self.left = PointCord(left_eye[0], left_eye[1])
        self.right = PointCord(right_eye[0], right_eye[1])
