from gpiozero import Servo
from time import sleep

# Initialize the servo on GPIO pin 17
servo = Servo(17)

print("Starting servo test on GPIO 17. Press Ctrl+C to stop.")

try:
    while True:
        print("Setting servo to minimum position.")
        servo.min()  # Move the servo to its minimum position (-1.0)
        sleep(1)

        print("Setting servo to middle position.")
        servo.mid()  # Move the servo to its middle position (0.0)
        sleep(1)

        print("Setting servo to maximum position.")
        servo.max()  # Move the servo to its maximum position (1.0)
        sleep(1)

except KeyboardInterrupt:
    print("\nTest stopped. Resetting servo to middle position.")
    servo.mid()
    sleep(1)
