import cv2 
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""

    img = cv2.imread("road.jpg")
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
    frame = cv2.imencode('.jpg', img)[1].tobytes()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# set FLASK_ENV = development
# set FLASK_APP = testImage.py


if __name__ == '__main__':
    app.run(debug=True)
