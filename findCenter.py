# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
 
# allow the camera to warmup
time.sleep(2)
 
# grab an image from the camera
camera.capture(rawCapture, format="rgb")
image = rawCapture.array

#convert to hsv
hsvImage = cv2.cvtColor(image,cv2.COLOR_RGB2HSV);

# find object


for i in range(len(hsvImage)):
	x = 0;
	prevhue = -1
	for j in range(len(hsvImage[i])):
		hue = havsImage[i][j][0];
		if(abs(hue - prevhue) > 30  && prevhue != -1):
			edges[i][x] = j;
			x++;
		prevhue = hue;

#find x center
for i in range(len(edges)):
	if(len(edges[i]) != 0):
		for x in range(len(edges[i])):
			temp += edges[i][x]
		centers[i] = temp/len(edges[i])

for i in range(len(centers)):
	if(centers[i] != 0):
		middle += centers[i];
		x++;

middle = middle/x;
