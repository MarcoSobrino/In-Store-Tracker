# app.py
import os
import sqlite3
import pickle
from flask import Flask, render_template, Response, request, jsonify
from heatmap import generateHeatmap  # Import heatmap module
from start import startFunc
from stop import stopFunc
import webbrowser
import subprocess

from HeatMapDataConvert import convert_heatmap_data
from net_cam import VideoCapture

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/call_python_function', methods=['POST'])
def call_python_function():
    data = request.get_json()
    date_parameter = data.get('parameter')

    # Call the convert_heatmap_data function with the date parameter
    result = convert_heatmap_data(date_parameter)
    if(result == -1):
        return jsonify({'result': result})

    # Import heatmap module here and call the function
    from heatmap import generateHeatmap
    generateHeatmap(date_parameter)

    return jsonify({'result': result})

@app.route('/start_script', methods=['POST'])
def start_script():
    from start import startFunc
    startFunc()

    return jsonify({'status': 'success'})

@app.route('/stop_script', methods=['POST'])
def stop_script():
    from stop import stopFunc
    stopFunc()

    return jsonify({'status': 'success'})

@app.route('/heatMap')
def heatMap():

    
    with open("heatmap_data.pkl", "rb") as f:
        totalEntries, entriesVsPresses, date = pickle.load(f)

    return render_template('heatMap.html', totalEntries = totalEntries, entriesVsPresses = entriesVsPresses, date = date)

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
    return Response(gen(VideoCapture("Cam")),
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
#print(c.fetchall())

con.commit()
con.close()



if __name__ == '__main__':
    
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=False)


