import cv2
import numpy as np

def nothing(x):
	pass

cv2.namedWindow('image')

cap = cv2.VideoCapture(0)

cv2.createTrackbar('H_low', 'image', 0, 255, nothing)
cv2.createTrackbar('H_up', 'image', 255, 255, nothing)
cv2.createTrackbar('S_low', 'image', 0, 255, nothing)
cv2.createTrackbar('S_up', 'image', 255, 255, nothing)
cv2.createTrackbar('V_low', 'image', 0, 255, nothing)
cv2.createTrackbar('V_up', 'image', 255, 255, nothing)

while (1) :
	_, frame = cap.read()

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hlow = cv2.getTrackbarPos('H_low', 'image')
	hup = cv2.getTrackbarPos('H_up', 'image')
	slow = cv2.getTrackbarPos('S_low', 'image')
	sup = cv2.getTrackbarPos('S_up', 'image')
	vlow = cv2.getTrackbarPos('V_low', 'image')
	vup = cv2.getTrackbarPos('V_up', 'image')

	lower = np.array([hlow, slow, vlow])
	upper = np.array([hup, sup, vup])

	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.erode(mask, None, iterations=3)
	mask = cv2.dilate(mask, None, iterations=2)

	res = cv2.bitwise_and(frame, frame, mask= mask)
	res2 = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	res2 = cv2.GaussianBlur(res2, (5, 5), 0)
	res2 = cv2.Canny(res2, 100, 200)

	cv2.imshow('color', res)
	cv2.imshow('binner', res2)

	key = cv2.waitKey(5) & 0xFF
	if key == 27:
		break

cv2.destroyAllWindows()