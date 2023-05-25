import platform
import cv2

# Load the classifier
if platform.system() == 'Windows'   :
    body_cascade = cv2.CascadeClassifier('LiveTracking\\components\\haarcascade_fullbody.xml')
else:
    body_cascade = cv2.CascadeClassifier('LiveTracking\components\haarcascade_fullbody.xml')

# Start the video capture
cap = cv2.VideoCapture(0)

while True:
    # Read the frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect bodies in the frame
    bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(50, 50))

    # Draw a rectangle around each body
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()
