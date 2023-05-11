import cv2

cap = cv2.VideoCapture(0)


tracker = cv2.legacy.TrackerMOSSE_create()

# get the first frame
ret, frame = cap.read()

# select the ROI
roi = cv2.selectROI("Tracking", frame, False)

# initialize the tracker with the ROI
tracker.init(frame, roi)

def draw_box(roi, frame):
    x,y,w,h = int(roi[0]),int(roi[1]),int(roi[2]),int(roi[3])
    cv2.rectangle(frame,(x,y),((w+x),(h+y)),(255,0,255),3,1)
    cv2.putText(frame,"seen",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

while True:
    timer = cv2.getTickCount()
    ret, frame = cap.read()

    # update the tracker
    success, roi = tracker.update(frame)

    if success:
        draw_box(roi,frame)
    else:
        cv2.putText(frame,"lost",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(frame,str(int(fps)),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    cv2.imshow('Tracking', frame)

    # check for key press
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, break from the loop
    if key == ord('q'):
        break

# release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()