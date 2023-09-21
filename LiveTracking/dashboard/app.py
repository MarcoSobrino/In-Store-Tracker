import sqlite3

from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/heatMap')
def heatMap():
    return render_template('heatMap.html')

@app.route('/license')
def license():
    return render_template('License.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame 
               + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

con = sqlite3.connect('LiveTracking.db')
c = con.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS timeTable (
            customerID integer,
            startTime interger,
            endTime integer
            )""")

# c.execute("INSERT INTO timeTable VALUES (1, 0, 0)")
# c.execute("INSERT INTO timeTable VALUES (2, 0, 0)")
c.execute("SELECT * from timeTable")
print(c.fetchall())

con.commit()



if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port='5000', debug=True)
