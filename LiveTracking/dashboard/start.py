import sqlite3
import time as t
from NetRecog import start_func
from Track_simple import track_simple


def startFunc():

    #connect to the database
    conn = sqlite3.connect('LiveTracking.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM running;")
    cursor.execute("INSERT INTO running (is_running) VALUES (1);")
    conn.commit()
    

    time = start_func()
    array = track_simple(time)
    time_data = t.gmtime(time)
    month = str(time_data.tm_mon)
    day = str(time_data.tm_mday)
    year = str(time_data.tm_year)
    date = month.rjust(2,'0') + "/" + day.rjust(2,'0') + "/" + year[-2:]
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HeatMap WHERE date = ?", (date,))
    result = cursor.fetchone()

    ########################
    result = None
    ########################

    if result == None:
        result = [0] * 19
    cursor.execute("DELETE FROM HeatMap WHERE date = ?", (date,))
    cursor.execute("INSERT INTO HeatMap VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                   , (  date, 
                        array[0] + result[1], array[1] + result[2],
                        array[2] + result[3], array[3] + result[4], 
                        array[4] + result[5], array[5] + result[6],
                        array[6] + result[7], array[7] + result[8],
                        array[8] + result[9], array[9] + result[10],
                        array[10] + result[11], array[11] + result[12],
                        array[12] + result[13], array[13] + result[14],
                        array[14] + result[15], array[15] + result[16],
                        array[16] + result[17], 0))
    conn.commit()
    conn.close()

#start the recording
# start_func()

if __name__ == "__main__":
    startFunc()