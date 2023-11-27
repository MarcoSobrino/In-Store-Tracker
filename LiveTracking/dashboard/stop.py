import sqlite3

def safe_calls(conn, sql, sql2):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.execute(sql2)
        conn.commit()
    except sqlite3.Error as e:
        print("Error: ", e.args[0])
        safe_calls(conn, sql, sql2)


def stopFunc():
    print("Stopping the Recording!")

    conn = sqlite3.connect('LiveTracking.db')
    # cursor = conn.cursor()

    # #remove the running flag
    # cursor.execute("DELETE FROM running;")
    # cursor.execute("INSERT INTO running (is_running) VALUES (0);")
    # conn.commit()

    safe_calls(conn, "DELETE FROM running;", "INSERT INTO running (is_running) VALUES (0);")

    conn.close()


if __name__ == "__main__":
    stopFunc()