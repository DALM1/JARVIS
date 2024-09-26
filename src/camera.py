import cv2

class Camera:
    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
        if not self.cap.isOpened():
            exit()

        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 150)
        self.cap.set(cv2.CAP_PROP_CONTRAST, 50)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def get_frame(self):
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        self.cap.release()
