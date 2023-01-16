import cv2
import numpy as np
import imutils
import argparse
from collections import deque

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", help="max buffer size")
args = vars(ap.parse_args())

greenUp = (64, 255, 255)
greenLow = (29, 86, 0)
pts = deque(maxlen=args["buffer"])

if not args.get("video", False):
	camera = cv2.VideoCapture(0)

else:
	camera = cv2.VideoCapture(args["video"])

while True:
	(grabbed, frame) = camera.read()

	if args.get("video") and not grabbed:
		break

	frame = imutils.resize(frame, width=600)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv, greenLow, greenUp)

	cv2.imshow("frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()