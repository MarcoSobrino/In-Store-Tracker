import cv2
import numpy as np

class VideoCamera(object):
    def __init__(self):
        # Start the video capture
        self.video = cv2.VideoCapture(0)

        # Load the classifier
        # self.body_cascade = cv2.CascadeClassifier('/Users/marcosobr/Desktop/Science of Computers/SeniorProject/In-Store-Tracker/LiveTracking/components/haarcascade_fullbody.xml')
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        self.previous_count = 0
        self.current_count = 0
        self.total_count = 0

    def __del__(self):
        # Release the capture
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        # Read the frame from the camera
        ret, frame = self.video.read()

        # Resize the frame
        frame = cv2.resize(frame, (640, 480))

        # Detect bodies in the frame
        boxes, weights = self.hog.detectMultiScale(frame, winStride=(8,8))

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        self.current_count = 0

        # Draw a rectangle around each body
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
            self.current_count += 1

        count_diff = self.current_count - self.previous_count
        self.total_count += count_diff

        self.previous_count = self.current_count

        # Encode the frame as an image file
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()

