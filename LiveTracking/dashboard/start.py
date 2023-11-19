import sqlite3
import time
from NetRecog import start_func
from Track_simple import track_simple


def startFunc():

    #connect to the database
    conn = sqlite3.connect('LiveTracking.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM running;")
    cursor.execute("INSERT INTO running (is_running) VALUES (1);")
    conn.commit()
    conn.close()

    time = start_func()
    array = track_simple(time)
    time_data = time.gmtime(time)
    month = time_data.tm_mon
    day = time_data.tm_mday
    year = time_data.tm_year
    
    print(array)

#start the recording
# start_func()

if __name__ == "__main__":
    startFunc()