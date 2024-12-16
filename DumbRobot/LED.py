import gpiozero
from gpiozero import LED
import time

led = LED(27)  # Replace with your GPIO pin

while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
