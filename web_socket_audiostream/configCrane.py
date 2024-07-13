import time
from adafruit_servokit import ServoKit
from multiprocessing import Process

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=8)

positions = {
    "park": (75, 110, 50, 24),
    "bin": (2, 150, 50, 24),
    "storage3": (108, 180, 65, 0),
    "storage2": (70, 180, 70, 0),
    "storage1": (42, 175, 70, 0),
}

def grab():
    moveSlow(craneMotor4, 24)

def chill():
    # sleep one second
    time.sleep(1)

def throw():
    moveSlowTo((75, 180, 130, 24))
    moveFastTo((180, 90, 180, 24))
    time.sleep(0.2)
    moveFast(craneMotor4, 0)

def park():
   moveSlow(2, 110)
   moveSlowTo(positions["park"])

def drop():
    moveFast(craneMotor4, 0)

def moveSlow(port, angle):
    currentAngle = int(kit.servo[port].angle)
    while not currentAngle == angle:
        print(currentAngle)
        kit.servo[port].angle = currentAngle
        if currentAngle < angle:
            currentAngle += 1
        else:
            currentAngle -= 1
        time.sleep(0.02)

def moveFast(port, angle):
    kit.servo[port].angle = angle


def moveSlowTo(coordinates: list[int, int, int, int]):
    one, two, three, four = coordinates
    # do the movements in parallel
    p1 = Process(target=moveSlow, args=(craneMotor1, one))
    p2 = Process(target=moveSlow, args=(craneMotor2, two))
    p3 = Process(target=moveSlow, args=(craneMotor3, three))
    p4 = Process(target=moveSlow, args=(craneMotor4, four))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()


def moveFastTo(coordinates: list[int, int, int, int]):
    one, two, three, four = coordinates
    # do the movements in parallel
    p1 = Process(target=moveFast, args=(craneMotor1, one))
    p2 = Process(target=moveFast, args=(craneMotor2, two))
    p3 = Process(target=moveFast, args=(craneMotor3, three))
    p4 = Process(target=moveFast, args=(craneMotor4, four))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()


craneMotor1 = 0
craneMotor2 = 1
craneMotor3 = 2
craneMotor4 = 4

craneMotor1angle = 0
craneMotor2angle = 0
craneMotor3angle = 0
craneMotor4angle = 0

def execute(isThrow, color):
    moveSlowTo(positions["park"])
    if color == Â"red" or color = "rat":
        moveSlowTo(positions["storage1"])
    elif color == "white":
        moveSlowTo(positions["storage2"])
    elif color == "blue":
        moveSlowTo(positions["storage3"])
    chill()
    grab()
    park()
    if isThrow:
        throw()
        park()
    else:
        moveSlowTo(positions["bin"])
        drop()
        park()

# moveSlowTo(positions["park"])
# moveSlowTo(positions["storage1"])
# chill()
# grab()
# moveSlowTo(positions["park"])
# throw()
# moveSlowTo(positions["park"])
# moveSlowTo(positions["storage3"])
# chill()
# grab()
# moveSlowTo(positions["park"])
# throw()
# moveSlowTo(positions["park"])
# moveSlowTo(positions["storage2"])
# chill()
# grab()
# moveSlowTo(positions["park"])
# throw()

# while True:
#     req = input()
#     motor = int(req.split(" ")[0])
#     angle = int(req.split(" ")[1])
#     motorPort = motor - 1
#     if len(req.split(" ")) > 2:
#         moveFastTo([int(req.split(" ")[0]), int(req.split(" ")[1]), int(req.split(" ")[2]), int(req.split(" ")[3])])
#         moveSlowTo([int(req.split(" ")[0]), int(req.split(" ")[1]), int(req.split(" ")[2]), int(req.split(" ")[3])])
#         print(f"Motor 1: {craneMotor1angle}")
#         print(f"Motor 2: {craneMotor2angle}")
#         print(f"Motor 3: {craneMotor3angle}")
#         print(f"Motor 4: {craneMotor4angle}")
#         continue
#     elif motor == 1:
#         craneMotor1angle = angle
#         motorPort = craneMotor1
#     elif motor == 2:
#         craneMotor2angle = angle
#         motorPort = craneMotor2
#     elif motor == 3:
#         craneMotor3angle = angle
#         motorPort = craneMotor3
#     elif motor == 4:
#         craneMotor4angle = angle
#         motorPort = craneMotor4
#     # kit.servo[motorPort].angle = angle
#     moveSlow(motorPort, angle)
#     # print agnle of each motor
#     print(f"Motor 1: {craneMotor1angle}")
#     print(f"Motor 2: {craneMotor2angle}")
#     print(f"Motor 3: {craneMotor3angle}")
#     print(f"Motor 4: {craneMotor4angle}")
