"""
Hough Transformation:
A line in image space can be expressed in two variables - Cartesian & Polar

Process involved: 

1. Edge Detection using Canny Edge Detection
2. Mapping of edge points in Hough space and storing in accumulator
3. Interpretation of infinite lines using Thresholding
4. Conversion of infinite to finite lines


"""

import cv2
import numpy as np

img = cv2.imread('sudoku.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(x0 - 1000 * (a))

    cv2.line(img, (x1,y1), (x2,y2), (0, 0, 255), 2)

cv2.imshow('image', img)
cv2.imshow('edges', edges)
k = cv2.waitKey(0)
cv2.destroyAllWindows()
 