import sqlite3

# Database connection
db_path = 'LiveTracking.db'  # Update this with your database path
  # Number of frames to wait before counting a person again

# Frame dimensions and grid size
frame_width = 1920  # Update with your frame width
frame_height = 1080  # Update with your frame height

# For a 4x4 grid
grid_size_x = 4
grid_size_y = 4  

# Calculate zone dimensions
zone_width = frame_width // grid_size_x
zone_height = frame_height // grid_size_y

def assign_to_zone(x, y):
    # Determine the zone based on x, y coordinates
    zone_x = x // zone_width
    zone_y = y // zone_height
    return zone_y * grid_size_x + zone_x

def get_detections_from_db(start_time):
    # Connect to the database and retrieve detections for a specific start_time
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Ensure the data is ordered by frame_count to process sequentially
    cursor.execute("SELECT x, y, w, h, frame_count FROM persons WHERE start_time = ? ORDER BY frame_count", (start_time,))
    raw_detections = cursor.fetchall()
    conn.close()
    
    detections = []
    for x, y, w, h, frame_count in raw_detections:
        detections.append((x + w // 2, y + h // 2, frame_count))
    return detections



def get_zone_counts(detections):
    # Initialize zone counts
    zone_counts = [0] * (grid_size_x * grid_size_y)
    ret = []
    current_frame = 0
    for x, y, frame_count in detections:
        if(frame_count > current_frame and current_frame != 0):
            ret.append(zone_counts)
            zone_counts = [0] * (grid_size_x * grid_size_y)
        current_frame = frame_count
        zone_index = assign_to_zone(x, y)
        zone_counts[zone_index] += 1
    return ret 

def get_totals(zone_counts):
    ret = []
    for i in zone_counts:
        current = 0
        for j in i:
            current += j
        ret.append(current)
    return ret

def basic_error_correction(zone_counts, grace_period, zone):
    # Apply the grace period
    previouse_count = 0
    for i, counts in enumerate(zone_counts):
        if counts[zone] == previouse_count:
            continue
        for j in range(grace_period):
            if i + j < len(zone_counts):
                if zone_counts[i+j][zone] == previouse_count:
                    for k in range(i,i+j):
                        zone_counts[k][zone] = previouse_count
                    break
        previouse_count = counts[zone]
    return zone_counts
                    
def get_total_zone_entries(zone_counts):
    final_counts = [0] * (grid_size_x * grid_size_y +1)
    previous_counts = [0] * (grid_size_x * grid_size_y +1)

    for i, counts in enumerate(zone_counts):
        for j,count in enumerate(counts):
            if count > previous_counts[j]:
                final_counts[j] += 1
        previous_counts = counts
    return final_counts





def track_simple(start_time = 1699330493, grace_period = 8):

    
    # Process the data
    detections = get_detections_from_db(start_time)
    #print(f"Total detections: {len(detections)}")
    zone_counts = get_zone_counts(detections)
    total_counts = get_totals(zone_counts)

    for i,count in enumerate(zone_counts):
        zone_counts[i].append(total_counts[i])

    for i in range(grid_size_x * grid_size_y + 1):
        zone_counts = basic_error_correction(zone_counts, grace_period, i)

    

    final_counts = get_total_zone_entries(zone_counts)
    # Output the result
    #print("final_counts {}".format(final_counts))
    return final_counts

if __name__ == "__main__":
    track_simple()


