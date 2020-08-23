# Self Driving Car Lane Detection

## Transformations & Techniques used

### ✅Hough Transformation

➡️ Yields us **`infinite lines`** on edges detected by Canny Edge Detection Method

Applying on Soduku Image:

![PHough-Soduku](./OutputImg/Hough-Soduku.png)


### ✅Probabilistic Hough Transformation

➡️ Yields us **`finite lines`** on edges detected by Canny Edge Detection Method vs infinite as in case of Hough Transformation

Lets apply on a simple Soduku image: 

![PHough-Soduku](./OutputImg/ProbabilisticHough.png)

As you can see finite lines. Now let's apply on our Road Image :

![PHoughTransform](./OutputImg/OutputOnRoad.png)

### ✅Building out Region of Interest aka ROI

![Masked Image](./OutputImg/MaskedImage.png)

Further edge detected

![Edges detected](./OutputImg/Canny-1.png)

Removing corner edges which are unwanted requires edge detection first then masking

![Perfect Edge Detection](./OutputImg/CannyPerfect.png)

Finally upon masking, 

![Masked Image](./OutputImg/EdgesDetected.png)
 
 **Video Dataset**: [Click here](https://www.youtube.com/playlist?list=PLPuW_E3R2ZUltRVlWuM3ngtL3jvScTj-Y)

 **Output image**: 
 
 ![Lane Detection Output](OutputImage.png)