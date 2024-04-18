from time import time
import cv2

# Create a new VideoCapture object
#cam = cv2.VideoCapture(0)
cam = cv2.VideoCapture("rtsp://OBuser:OnvifBr!dge@DELWP22@13.70.186.16:13285/live/8e22f68b-7ca7-4cf7-8fce-b18c8905a0c6")
# Initialise variables to store current time difference as well as previous time call value
previous = time()
delta = 0

# Keep looping
while True:
    # Get the current time, increase delta and update the previous variable
    current = time()
    delta += current - previous
    previous = current
    
    # Check if 3 (or some other value) seconds passed
    if delta > 10:
    #    # Operations on image
        # Reset the time counter
        delta = 0
        print(previous,current,delta)

    # Show the image and keep streaming
    #    _, img = cam.read()
    #cv2.imshow("Frame", img)
    #cv2.waitKey(1)