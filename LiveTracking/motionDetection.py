import cv2

# Set up video capture
cap = cv2.VideoCapture(0)

# Initialize background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

# Loop over frames
while True:
    # Read a frame
    ret, frame = cap.read()

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Apply thresholding to the foreground mask
    thresh = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)[1]

    # Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over contours and draw a rectangle around each one
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Show the frame
    cv2.imshow('frame', frame)

    # Check for exit
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
