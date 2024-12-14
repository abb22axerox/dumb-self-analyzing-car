from gpiozero import PWMOutputDevice
from time import sleep

# GPIO Pin for MOSFET SIG connection
MOTOR_PIN = 18  # Connect SIG to GPIO18 (Pin 12)

# Initialize the motor PWM control
motor = PWMOutputDevice(MOTOR_PIN)

def set_motor_speed(speed):
    """
    Set the motor speed using PWM.
   
    :param speed: float, 0.0 (stop) to 1.0 (full speed)
    """
    speed = max(0.0, min(1.0, speed))  # Clamp speed between 0.0 and 1.0
    motor.value = speed
    print(f"Motor speed set to {speed * 100:.1f}%")

# Example usage
if __name__ == "__main__":
    try:
        print("Starting motor...")
        set_motor_speed(0.5)  # 50% speed
        sleep(3)  # Run for 3 seconds
       
        print("Stopping motor...")
        set_motor_speed(0.0)  # Stop the motor
        sleep(2)
       
        print("Running motor at full speed...")
        set_motor_speed(1.0)  # 100% speed
        sleep(2)
       
        print("Stopping motor...")
        set_motor_speed(0.0)

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        motor.value = 0  # Ensure motor is stopped