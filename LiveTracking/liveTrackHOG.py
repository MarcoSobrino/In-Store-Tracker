import cv2
import numpy as np

# Load the classifier
# body_cascade = cv2.CascadeClassifier('/Users/marcosobr/Desktop/Science of Computers/SeniorProject/In-Store-Tracker/LiveTracking/components/haarcascade_fullbody.xml')
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# Start the video capture
cap = cv2.VideoCapture(0)

# Define the two ROIs
roi1 = [(0, 0), (640, 320)]
roi2 = [(0, 320), (640, 480)]

previous_count = 0
current_count = 0
total_count = 0
while True:
    # Read the frame from the camera
    ret, frame = cap.read()

    # Resize the frame
    frame = cv2.resize(frame, (640, 480))

    # Detect bodies in the frame
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8))

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    current_count = 0

    # Draw a rectangle around each body
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
        current_count += 1

    count_diff = current_count - previous_count
    total_count += count_diff
    # print("People count difference: ", count_diff)

    # Write the frame to the output file
    # out.write(frame.astype('uint8'))

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

    previous_count = current_count

print("Total number of people who entered the room: ", total_count)

# Release the capture and close the window
cap.release()
# out.release()
cv2.destroyAllWindows()
