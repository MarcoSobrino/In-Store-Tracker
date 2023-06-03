from flask import Flask, render_template, Response
from camera_copy import VideoCamera

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
