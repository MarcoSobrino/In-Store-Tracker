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
    # if a[1] + a[3] > 240:
    #     ret +=2
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

        
        self.past_humans = []
        self.unchanged_history = []

        with open("output.txt", "w") as file:      
            file.write("\n")



    

    def __del__(self):
        # Release the capture
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self, count):
        # Read the frame from the camera
        ret, frame = self.video.read()

        # Resize the frame
        frame = cv2.resize(frame, dimensions)
        cv2.line(frame, (0, 240), (600,240), (0, 0, 255), 1)
        cv2.line(frame, (300,0), (300,480), (0, 0, 255), 1)
        


        # Detect humans in the frame
        human, weights = self.hog.detectMultiScale(frame, winStride=(8,8))

        for i,history in enumerate(self.unchanged_history):
            self.unchanged_history[i] += 1

        # Add unknown humans to list
        for (x,y,w,h) in human:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            bbox = (x,y,w,h)
            inList = False
            for i, tracker in enumerate(self.past_humans):
                if max_intersect(bbox,tracker) > 0.8:
                    inList = True
                    self.past_humans[i] = bbox
                    self.unchanged_history[i] = 0
            if not inList:

                #add things the lists
                self.past_humans.append(bbox)
                self.unchanged_history.append(0)

        for i,history in enumerate(self.unchanged_history):
            if history > 10:
                self.unchanged_history.pop(i)
                self.past_humans.pop(i)



        # Encode the frame as an image file
        ret, jpeg = cv2.imencode('.jpg', frame)

        #push locations to file
        
        if count%10 == 0:    
            with open("output.txt", "a") as file:      
                for location in self.past_humans:
                    file.write(str(get_region(location)))
                file.write("\n")

        return jpeg.tobytes()

