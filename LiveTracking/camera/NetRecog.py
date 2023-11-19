import time
import cv2
import numpy as np
import sqlite3

def calculate_overlap(box_a, box_b):
    # Determine the coordinates of the intersection rectangle
    left = max(box_a[0], box_b[0])
    top = max(box_a[1], box_b[1])
    right = min(box_a[0] + box_a[2], box_b[0] + box_b[2])
    bottom = min(box_a[1] + box_a[3], box_b[1] + box_b[3])

    # Check if there is an overlap
    if right > left and bottom > top:
        # The intersection area
        intersection_area = (right - left) * (bottom - top)
        if intersection_area == 0:
            return 0
        # Calculate the overlap as a ratio of the intersection area to the smallest box's area
        area_a = box_a[2] * box_a[3]
        area_b = box_b[2] * box_b[3]
        min_area = min(area_a, area_b)
        overlap = intersection_area / min_area
        return overlap
    else:
        # No overlap
        return 0

def filter_overlapping_boxes(list1, list2, threshold):
    # We will store the indices of boxes to remove in these sets
    to_remove_list1 = set()
    to_remove_list2 = set()

    # Compare every box in list1 with all boxes in list2
    for i, box1 in enumerate(list1):
        for j, box2 in enumerate(list2):
            overlap = calculate_overlap(box1[1], box2[1])
            if overlap >= threshold:
                # If they overlap, discard the one with the lower certainty
                if box1[0] < box2[0]:
                    to_remove_list1.add(i)
                else:
                    to_remove_list2.add(j)

    # Filter and keep only boxes that were not marked for removal
    filtered_list1 = [box for i, box in enumerate(list1) if i not in to_remove_list1]
    filtered_list2 = [box for i, box in enumerate(list2) if i not in to_remove_list2]

    # Return the combined list of non-overlapping boxes
    combined_filtered_list = filtered_list1 + filtered_list2
    return combined_filtered_list

class CaffeModelLoader:	
    @staticmethod
    def load(proto, model):
        net = cv2.dnn.readNetFromCaffe(proto, model)
        return net
 
class FrameProcessor:	
    def __init__(self, size, scale, mean):
        self.size = size
        self.scale = scale
        self.mean = mean
     
    def get_blobs(self, frame):
        (h, w, c) = frame.shape
        crop_size = h  # Assuming we are cropping square regions

        # Crop the frame
        left_img = frame[:, 0:crop_size]
        right_img = frame[:, w - crop_size:w]

        left_resized = cv2.resize(left_img, (self.size, self.size), cv2.INTER_AREA)
        right_resized = cv2.resize(right_img, (self.size, self.size), cv2.INTER_AREA)

        left_blob = cv2.dnn.blobFromImage(left_resized, self.scale, (self.size, self.size), self.mean)
        right_blob = cv2.dnn.blobFromImage(right_resized, self.scale, (self.size, self.size), self.mean)

        return left_blob, right_blob


class SSD:	
    def __init__(self, frame_proc, ssd_net):
        self.proc = frame_proc
        self.net = ssd_net
	
    def detect_left(self, frame):
        blob = self.proc.get_blobs(frame)[0]
        self.net.setInput(blob)
        detections = self.net.forward()
            # detected object count
        k = detections.shape[2]
        obj_data = []
        for i in np.arange(0, k):
            obj = detections[0, 0, i, :]
            obj_data.append(obj)
        	
        return obj_data
    
    def detect_right(self, frame):
        blob = self.proc.get_blobs(frame)[1]
        self.net.setInput(blob)
        detections = self.net.forward()
            # detected object count
        k = detections.shape[2]
        obj_data = []
        for i in np.arange(0, k):
            obj = detections[0, 0, i, :]
            obj_data.append(obj)
        	
        return obj_data
    


    def get_object_left(self, frame, data):
        confidence = int(data[2]*100.0)
        (h, w, c) = frame.shape
        r_x = int(data[3]*h)
        r_y = int(data[4]*h)
        r_w = int((data[5]-data[3])*h)
        r_h = int((data[6]-data[4])*h)

        obj_rect = (r_x, r_y, r_w, r_h)
        return (confidence, obj_rect)
    
    def get_object_right(self, frame, data):
        confidence = int(data[2]*100.0)
        (h, w, c) = frame.shape
        r_x = int(data[3]*h)
        r_y = int(data[4]*h)
        r_w = int((data[5]-data[3])*h)
        r_h = int((data[6]-data[4])*h)
    	
        if w>h :
            dx = int(w-h)
            r_x = r_x+dx

        obj_rect = (r_x, r_y, r_w, r_h)
        return (confidence, obj_rect)


    def get_objects_left(self, frame, obj_data, class_num, min_confidence):
        objects = []
        for (i, data) in enumerate(obj_data):
            obj_class = int(data[1])
            obj_confidence = data[2]
            if obj_class==class_num and obj_confidence>=min_confidence :
                obj = self.get_object_left(frame, data)
                objects.append(obj)
            	
        return objects
    
    def get_objects_right(self, frame, obj_data, class_num, min_confidence):
        objects = []
        for (i, data) in enumerate(obj_data):
            obj_class = int(data[1])
            obj_confidence = data[2]
            if obj_class==class_num and obj_confidence>=min_confidence :
                obj = self.get_object_right(frame, data)
                objects.append(obj)
            	
        return objects
    
class Utils:	
    @staticmethod
    def draw_object(obj, label, color, frame):
        (confidence, (x1, y1, w, h)) =  obj
        x2 = x1+w
        y2 = y1+h
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        y3 = y1-12
        text = label + " " + str(confidence)+"%"
        cv2.putText(frame, text, (x1, y3), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1, cv2.LINE_AA)
    	
    @staticmethod
    def draw_objects(objects, label, color, frame):
        for (i, obj) in enumerate(objects):
            Utils.draw_object(obj, label, color, frame) 


def start_func():
    proto_file = "Nets/mobilenet.prototxt"
    model_file = "Nets/mobilenet.caffemodel"
    ssd_net = CaffeModelLoader.load(proto_file, model_file)
    print("Caffe model loaded from:", model_file)

    proc_frame_size = 300
    ssd_proc = FrameProcessor(proc_frame_size, 1.0/127.5, 127.5)
    person_class = 15

    ssd = SSD(ssd_proc, ssd_net)

    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_video.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    conn = sqlite3.connect('LiveTracking.db')
    cursor = conn.cursor()
    start_time = int(time.time())
    frame_count = 0

    running = conn.execute("SELECT * FROM running")

    while cap.isOpened() and running.fetchone()[0] == 1:
        running = conn.execute("SELECT * FROM running")
        frame_count += 1
        ret, frame = cap.read()
        if not ret:
            break

        left_obj_data = ssd.detect_left(frame)
        right_obj_data = ssd.detect_right(frame)

        left_persons = ssd.get_objects_left(frame, left_obj_data, person_class, 0.5)
        right_persons = ssd.get_objects_right(frame, right_obj_data, person_class, 0.5)

        # Filter out overlapping boxes
        combined_list = filter_overlapping_boxes(left_persons, right_persons, 0.5)

        print("Person count:", len(combined_list))
        print("All persons:", combined_list)
        
        Utils.draw_objects(combined_list, "PERSON", (0, 0, 255), frame)

        # Write to database
        for person in combined_list:
            (confidence, (x1, y1, w, h)) = person
            cursor.execute("INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?, ?)", (frame_count, start_time, confidence, x1, y1, w, h))
        conn.commit()

        # Display the frame
        cv2.imshow('Video', frame)

        # Write the frame to the output video
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    # out.release()  # save output video
    cv2.destroyAllWindows()
    conn.close()
    return start_time
