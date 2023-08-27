import cv2
import mediapipe as mp
from src.checkers.eyecheck import EyeCheck

def _map(ratio, in_min, in_max, out_min, out_max):
    return int((ratio - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

class Blinker:
    def __init__(self, blink_checker, eyes_in_max, eyes_out_max, cap_source = 0) -> None:
        self.blink_checker = blink_checker

        self.eyes_in_max = eyes_in_max
        self.eyes_out_max = eyes_out_max

        self.cap = cv2.VideoCapture(cap_source)
        self.mp_face_mesh = mp.solutions.face_mesh

        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height  = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.eye_checker = EyeCheck(width, height)

        self.config()

    def config(self):
        self.cap.set(cv2.CAP_PROP_FPS, 25.0)

    def blink_things(self, results, image):
        face_landmarks = None
        try:
            face_landmarks = results.multi_face_landmarks[0].landmark
            eye_cords = self.eye_checker.eye_cords(face_landmarks)
        except:
            print("Face not found")
            return

        eye_distancies = self.eye_checker.eyes_distance(eye_cords)
        mediaRatio = self.eye_checker.blink_ratio(eye_distancies[0], eye_distancies[1])

        ratioMapped = _map(mediaRatio, 0, self.eyes_in_max, self.eyes_out_max, 0)

        self.blink_checker.blink(ratioMapped)
        
         # SHOW ON IMAGE
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, str(self.blink_checker.blink_count), (100, 300), font, 10, (100, 0, 255), 5, cv2.LINE_AA)

    def run(self):
        with self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:

            while self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    break

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image)

                # Draw the face mesh annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                self.blink_things(results, image)
                cv2.imshow('MediaPipe Face Mesh', image)

                # Exit
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break
            
        self.cap.release()
