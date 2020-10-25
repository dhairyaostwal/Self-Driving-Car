import matplotlib.pylab as plt
import cv2
import numpy as np
import time
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    # Video streaming home page.
    return render_template('index.html')


# generating region of interest

def roi(img, vertices):
    mask = np.zeros_like(img)
    # channel_count = img.shape[2]
    match_mask_color = (255)
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

# drawing lines as lanes detected

def draw_lines(img, lines):
    img = np.copy(img)
    line_image = np.zeros((img.shape[0], img.shape[1], 3), dtype = np.uint8) 
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), thickness=4)
            # cv2.fillPoly(line_image, pts = ((x1,y1), (x2,y2)), color = (0, 255,120))
    img = cv2.addWeighted(img, 0.8, line_image, 1, 0.0)        
    return img

# image = cv2.imread('road5.png')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# process includes
# 1. Grascaling the image
# 2. Canny Edge Detection
# 3. Cropping Image acc to roi 
# 4. Drawing lines on the cropped image
# 5. Super imposing it on original image using BITWISE AND

def process(image):
    print(image.shape)
    height = image.shape[0]
    width = image.shape[1]
    # (704, 1279, 3)

    region_of_interest_vertices = [
        (0, height),
        (width/2, height/2),
        (width, height)
    ]


    gray_cropped_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cannyImage = cv2.Canny(gray_cropped_image, 100, 120)
    cropped_image = roi(cannyImage, np.array([region_of_interest_vertices], np.int32))

    lines = cv2.HoughLinesP(cropped_image, 
                            rho = 2, 
                            theta = np.pi/60, 
                            threshold = 160, 
                            lines=np.array([]), 
                            minLineLength = 40, 
                            maxLineGap=25)

    imageWithLines = draw_lines(image, lines)
    # colorAddition = cv2.fillPoly(imageWithLines, np.array([region_of_interest_vertices], np.int32), (120,200,200))

    return imageWithLines

# plt.imshow(imageWithLines)
# plt.show()

# rescaling frame due to different sizes

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# cap.release()
# cv2.destroyAllWindows()

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture('P1_example.mp4')

    # Read until video is completed
    while(cap.isOpened()):
        ret, frame = cap.read()  # import image
        if not ret: #if vid finish repeat
            frame = cv2.VideoCapture("P1_example.mp4")
            continue
        if ret:  # if there is a frame continue with code
            frame = process(frame)
            frame = rescale_frame(frame, percent=100)
            image = cv2.resize(frame, (0, 0), None, 1, 1)  # resize image
            
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #time.sleep(0.1)
        key = cv2.waitKey(20)
        if key == 27:
           break
   
        

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
