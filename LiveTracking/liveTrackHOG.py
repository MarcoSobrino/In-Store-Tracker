import cv2
import numpy as np

# Load the classifier
# body_cascade = cv2.CascadeClassifier('/Users/marcosobr/Desktop/Science of Computers/SeniorProject/In-Store-Tracker/LiveTracking/components/haarcascade_fullbody.xml')
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# Start the video capture
cap = cv2.VideoCapture(0)

# Output will be written to output.avi
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (640, 480))

while True:
    # Read the frame from the camera
    ret, frame = cap.read()

    # Resize the frame
    frame = cv2.resize(frame, (640, 480))

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to the frame
    #ret, thresh = cv2.threshold(frame, 80, 255, cv2.THRESH_BINARY)

    # Detect bodies in the frame
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8))

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    # Draw a rectangle around each body
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)

    # Write the frame to the output file
    out.write(frame.astype('uint8'))

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and close the window
cap.release()
out.release()
cv2.destroyAllWindows()
