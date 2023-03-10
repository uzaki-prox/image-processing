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
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x,y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	pts.appendleft(center)

	for i in xrange(1, len(pts)):
		if pts[i - 1] is None or pts[i] is None:
			continue

		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	cv2.imshow("frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()