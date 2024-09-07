from djitellopy import tello
from time import sleep

d1 = tello.Tello()
d1.connect()
# Testing connection

print(d1.get_battery())

"""
The logic sequence for testing myst always be:
    1) take-off to get some height
    2) apply flying tests
    3) reduce directional speed to 0
    4) land
"""
d1.takeoff()
sleep(5)
d1.send_rc_control(0,0,0,0)
d1.land()
