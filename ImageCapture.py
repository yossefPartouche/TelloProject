from djitellopy import tello
import cv2

d1 = tello.Tello()
d1.connect()
# Testing connection

d1.streamon()

while True:
    img = d1.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
