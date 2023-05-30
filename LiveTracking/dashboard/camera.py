import cv2
import numpy as np

dimensions = (600,480)

def intersection_area(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<0 or h<0: return 0
    return w*h

def max_intersect(a,b):
    area = intersection_area(a,b)
    a_ratio = area/(a[2]*a[3])
    b_ratio = area/(b[2]*b[3])
    return max(a_ratio,b_ratio)

def get_region(a):
    ret = 1
    if a[1] + a[3] > 240:
        ret +=2
    if a[0] + a[2] > 300:
        ret+=1
    return ret




class VideoCamera(object):
    def __init__(self):
        # Start the video capture
        self.video = cv2.VideoCapture(0)

        # Load the classifier
        # self.body_cascade = cv2.CascadeClassifier('/Users/marcosobr/Desktop/Science of Computers/SeniorProject/In-Store-Tracker/LiveTracking/components/haarcascade_fullbody.xml')
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        self.tracker = cv2.legacy.TrackerMOSSE_create()
        self.active_trackers = []
        self.active_trackers_bbox = []
        self.active_trackers_locations = []

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
        frame = cv2.resize(frame, dimensions)
        cv2.line(frame, (0, 240), (600,240), (0, 0, 255), 1)
        cv2.line(frame, (300,0), (300,480), (0, 0, 255), 1)
        

        #update list of trackers
        for i, tracker in enumerate(self.active_trackers):
            if tracker != 0:
                success, bbox = self.active_trackers[i].update(frame)
                if success:
                    x, y, w, h = [int(v) for v in bbox]
                    self.active_trackers_locations[i] = get_region(bbox)
                    self.active_trackers_bbox[i] = bbox
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                else:
                    self.active_trackers[i] = 0
                    self.active_trackers_locations[i] = 0

        # Detect bodies in the frame
        human, weights = self.hog.detectMultiScale(frame, winStride=(8,8))
        for (x,y,w,h) in human:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        

        # Add unknown humans to tracker list
        for (x,y,w,h) in human:
            bbox = (x,y,w,h)
            inList = False
            for i, tracker in enumerate(self.active_trackers_bbox):
                if max_intersect(bbox,tracker) > 0.8:
                    inList = True
            if not inList:
                #create new tracker
                new_tracker = cv2.legacy.TrackerMOSSE_create()
                new_tracker.init(frame, bbox)

                #add things to all the lists
                self.active_trackers.append(new_tracker)
                self.active_trackers_bbox.append(bbox)
                self.active_trackers_locations.append(get_region(bbox))

                #draw box
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)    


        # Encode the frame as an image file
        ret, jpeg = cv2.imencode('.jpg', frame)

        #push locations to file
        
            
        
        # file = open("locations.txt", "w")
        # for i,location in enumerate(self.active_trackers_locations):
        #     file.write(location[i])
        # file.close()

        return jpeg.tobytes()

