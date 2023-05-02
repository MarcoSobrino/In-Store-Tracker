import cv2
import numpy as np

# Load the classifier
# body_cascade = cv2.CascadeClassifier('/Users/marcosobr/Desktop/Science of Computers/SeniorProject/In-Store-Tracker/LiveTracking/components/haarcascade_fullbody.xml')
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# Start the video capture
cap = cv2.VideoCapture(0)

previous_right_count = 0
previous_left_count = 0

current_right_count = 0
current_left_count = 0

total_right_count = 0
total_left_count = 0
while True:
    # Read the frame from the camera
    ret, frame = cap.read()

    # Resize the frame
    frame = cv2.resize(frame, (640, 480))

    # Define the two ROIs as rectangular regions
    roi_left = (0, 0, int(frame.shape[1]/2), frame.shape[0])
    roi_right = (int(frame.shape[1]/2), 0, int(frame.shape[1]/2), frame.shape[0])

    # Extract the sub-images corresponding to the ROIs
    left_frame = frame[roi_left[1]:roi_left[1]+roi_left[3], roi_left[0]:roi_left[0]+roi_left[2]]
    right_frame = frame[roi_right[1]:roi_right[1]+roi_right[3], roi_right[0]:roi_right[0]+roi_right[2]]

    # Detect bodies in the left ROI
    boxes_left, weights_left = hog.detectMultiScale(left_frame, winStride=(8,8))

    # Detect bodies in the right ROI
    boxes_right, weights_right = hog.detectMultiScale(right_frame, winStride=(8,8))

    current_left_count = 0
    current_right_count = 0

    # Draw a rectangle around each body in the left ROI
    for (x, y, w, h) in boxes_left:
        cv2.rectangle(left_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        current_left_count += 1

    count_left_diff = current_left_count - previous_left_count
    total_left_count += count_left_diff

    # Draw a rectangle around each body in the right ROI
    for (x, y, w, h) in boxes_right:
        cv2.rectangle(right_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        current_right_count += 1
    
    count_right_diff = current_right_count - previous_right_count
    total_right_count += count_right_diff

    # Display the resulting frames with ROIs
    cv2.imshow('left frame', left_frame)
    cv2.imshow('right frame', right_frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

    previous_right_count = current_right_count
    previous_left_count = current_left_count

print("Total number of people who entered the right room: ", total_right_count)
print("Total number of people who entered the left room: ", total_left_count)

# Release the capture and close the window
cap.release()
# out.release()
cv2.destroyAllWindows()
