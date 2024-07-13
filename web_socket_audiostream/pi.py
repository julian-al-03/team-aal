import time
from adafruit_servokit import ServoKit

# Initialize the ServoKit instance for the PCA9685
kit = ServoKit(channels=16)

# Define a function to set the servo angle
def set_servo_angle(channel, angle):
    kit.servo[channel].angle = angle

# Define the servo channels
servo_channels = [0, 1, 2, 3, 13, 14, 15]

# Set servo angles for testing
try:
    while True:
        for angle in range(0, 181, 30):  # Move from 0 to 180 degrees
            for channel in servo_channels:
                set_servo_angle(channel, angle)
                print(f"Channel {channel}: {angle} degrees")
            time.sleep(1)  # Wait 1 second
        for angle in range(180, -1, -30):  # Move from 180 to 0 degrees
            for channel in servo_channels:
                set_servo_angle(channel, angle)
                print(f"Channel {channel}: {angle} degrees")
            time.sleep(1)  # Wait 1 second
except KeyboardInterrupt:
    print("Script interrupted by user")
finally:
    # Reset the servos to 0 degrees
    for channel in servo_channels:
        set_servo_angle(channel, 0)
