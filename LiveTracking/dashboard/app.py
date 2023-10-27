import sqlite3
import pickle

from flask import Flask, render_template, Response
from camera_copy import VideoCamera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/heatMap')
def heatMap():

    with open(r".\heatmap_data.pkl", "rb") as f:
        largest_value, largest_value_row = pickle.load(f)

    return render_template('heatMap.html', largest_value=largest_value, largest_value_row=largest_value_row )

@app.route('/license')
def license():
    return render_template('License.html')

def gen(camera):
    frame_count = 0
    while True:
        frame_count+= 1
        frame = camera.get_frame(frame_count)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame 
               + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def runCommand(command):
    con = sqlite3.connect('LiveTracking.db')
    c = con.cursor()
    c.execute(command)
    con.commit()
    con.close()

con = sqlite3.connect('LiveTracking.db')
c = con.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS timeTable (
            customerID integer,
            startTime interger,
            endTime integer
            )""")

# c.execute("DELETE FROM timeTable WHERE customerID = 2")
# c.execute("INSERT INTO timeTable VALUES (2, 0, 0)")
c.execute("SELECT * from timeTable")
print(c.fetchall())

con.commit()
con.close()



if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port='5000', debug=True)
