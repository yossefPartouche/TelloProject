from djitellopy import tello
import KeyPressModule as kp
from time import sleep
import numpy as np
import cv2
import math

################## PARAMETERS #################

fSpeed = 510 / 8  # Forward Speed cm/s
aSpeed = 360 / 10  # Angular speed degrees/s
interval = 0.25

dInterval = fSpeed * interval
aInterval = aSpeed * interval
################################################
x, y = 500, 500
a = 0
yaw = 270

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

# This is track the positions of the points
points = [(0, 0), (0, 0)]


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 15
    aSpeed = 50

    global x, y, yaw, a
    d = 0

    if kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 270
    elif kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = 270

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 0

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = 0

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = -aSpeed
        yaw -= aInterval

    elif kp.getKey("d"):
        yv = aSpeed
        yaw += aInterval

    if kp.getKey("t"):
        me.takeoff()
    if kp.getKey("q"):
        me.land()
        sleep(1)

    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y, yaw]


def drawPoints(img, points, yaw):
    # Draw drone's position as a circle
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    # Draw an arrow representing the drone's heading (yaw)

    if points:
        center = points[-1]
        length = 30
        # Calculate the endpoint of the arrow based on yaw
        end_point = (int(center[0] + length * math.cos(math.radians(yaw))),
                     int(center[1] + length * math.sin(math.radians(yaw))))

        cv2.arrowedLine(img, center, end_point, (255, 0, 0), 2, tipLength=0.3)  # Blue arrow for direction

# Could be background image - to Confirm

img = np.zeros((1000, 1000, 3), np.uint8)

while True:

    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    points.append((vals[4], vals[5]))

    img = np.zeros((1000, 1000, 3), np.uint8)

    drawPoints(img, points, vals[6])

    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break
cv2.destroyAllWindows()

