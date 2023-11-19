import sqlite3
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
    
    print(array)

#start the recording
# start_func()

if __name__ == "__main__":
    startFunc()