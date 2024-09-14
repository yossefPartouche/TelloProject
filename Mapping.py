from djitellopy import tello
import KeyPressModule as kp
from time import sleep
import numpy as np
import cv2
import math

################## PARAMETERS #################

fSpeed = 510/8  # Forward Speed cm/s
aSpeed = 360/10 # Angular speed degrees/s
interval = 0.25

dInterval = fSpeed*interval
aInterval = aSpeed*interval
################################################
x,y = 500, 500
a = 0
yaw = 0

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    global x, y, yaw, a
    d = 0

    if kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180
    elif kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = -speed
        yaw += aInterval

    elif kp.getKey("d"):
        yv = speed
        yaw -= aInterval

    if kp.getKey("t"): me.takeoff()
    if kp.getKey("q"):  me.land(); sleep(3)

    sleep(interval)
    a += yaw
    x += int(d*math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]

def drawPoints(img, points):
    cv2.circle(img, (points[0], points[1]), 5, (0, 0, 255), cv2.FILLED)
while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = np.zeros((1000, 1000, 3), np.uint8)
    points = (vals[4], vals[5])
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)

