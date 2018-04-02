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

# find object's edges and their centers

edges = [0];
for i in range(len(hsvImage)):
	x = 0;
	prevhue = -1
	pos = 0;
	for j in range(len(hsvImage[i])):
		hue = hsvImage[i][j][0];
		if(hue in range(0,10) or hue in range(160,180)):
			hue = 1;
		else:
			hue = 0;
		if((hue != prevhue)   and prevhue != -1):
			pos = pos + j;			
			x = x + 1;
		prevhue = hue;
	print(100*i/len(hsvImage));
	if(x != 0):
		edges.append( pos/x);

#find x center
middle = 0;
for i in range(len(edges)):
	if(edges[i] != 0):
		middle += edges[i];
		x = x + 1;

middle = middle/x;
print ("x-axis middle");
print middle;
print ("out of");
print(len(hsvImage));
cv2.imshow("Image",image);
cv2.waitkey(0);
