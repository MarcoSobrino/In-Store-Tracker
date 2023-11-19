import sqlite3

def stopFunc():
    print("Stopping the Recording!")

    conn = sqlite3.connect('LiveTracking.db')
    cursor = conn.cursor()

    #remove the running flag
    cursor.execute("DELETE FROM running;")
    cursor.execute("INSERT INTO running (is_running) VALUES (0);")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    stopFunc()