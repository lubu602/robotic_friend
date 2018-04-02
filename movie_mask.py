#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
#For ros
#not ross, that guy is the worst
import rospy
from geometry_msgs.msg import Vector3
#For OpenCV
import cv2
import numpy as np

def getCenter(img):
  M = cv2.moments(img)
  if(M["m00"] == 0):
	return (0,0);  
  cx = int(M['m10']/M['m00'])
  cy = int(M['m01']/M['m00'])
  theOut = (cx, cy)
  return theOut

def getCenterSlow(img):
  height, width = img.shape[:2]
  xt = 0.0
  yt = 0.0
  i = 0
  for y in range(height):
    for x in range(width):
      if(img[y,x] > 0):
        xt = xt + x
        yt = yt + y
        i = i+1

  if( i > 0):
    xt = xt / i
    yt = yt / i
  theOut = (int(xt), int(yt))
  return theOut

def fov(img,center):
	global viewW
	global viewH 
	height,width = img.shape[:2];
	x = center[0];
	y = center[1];
	dH = 2.0/height;
	dW = 2.0/width;
	xp = (x - width/2.0)*dW
	yp = (y - height/2.0)*dH
	xpdis = xp*viewW/2.0
	ypdis = yp*viewH/2.0;
	return (xpdis,ypdis);
def runner():
  for frame in camera.capture_continuous(rawCapture,format = "bgr", use_video_port=True):
    tick = time.time() 
    # grab an image from the camera, resize it, and convert to hsv
    
    img = frame.array
    img = cv2.resize(img,(240,160))
    hsv = cv2.cvtColor(img ,cv2.COLOR_BGR2HSV);

    # Get mask
    mask=cv2.inRange(hsv,lowerBound,upperBound)

    # Get center
    center = getCenter(mask)
    degrees = fov(mask,center)
    #print degrees
    # draw circle
    #cv2.circle(img,center,50,(0,0,255),-1)

    #cv2.imshow("Image", img)
    #cv2.imshow("Mask", mask)
 
 
    rawCapture.truncate(0)
    tock = time.time()
    #print "Time to complete = " + str(tock - tick) + " sec"
    cv2.waitKey(1)
    return center
#time.sleep(2.0)
# display the image on screen and wait for a keypress
#cv2.imshow("Image", image)
#cv2.waitKey(0)
def talker():
    pub = rospy.Publisher('euler_ref', Vector3, queue_size=10)
    rospy.init_node('camera', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        euler_ref_msg = Vector3()
        center = runner();
	euler_ref_msg.x = center[0];
	euler_ref_msg.y = center[1];
	
        rospy.loginfo(euler_ref_msg)
        pub.publish(euler_ref_msg)

if __name__ == '__main__':
  viewW = 62.2
  viewH = 48.8
  # initialize the camera and grab a reference to the raw camera capture
  camera = PiCamera()
  camera.framerate = 20
  rawCapture = PiRGBArray(camera)
 
  # allow the camera to warmup
  time.sleep(0.1)

  # Color Paramaters in 8-bit HSV
  lowerBound=np.array([110,50,50])
  upperBound=np.array([130,255,255])
  try:
      talker()
  except rospy.ROSInterruptException:
      pass

cv2.destroyAllWindows();
