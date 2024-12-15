from gpiozero import PWMOutputDevice, Servo

# GPIO Pin Definitions
MOTOR_PIN = 18  # Replace with your motor GPIO pin
SERVO_PIN = 17  # Replace with your servo GPIO pin

# Initialize components
motor = PWMOutputDevice(MOTOR_PIN)
servo = Servo(SERVO_PIN)

def drive_car(steering_direction, motor_speed):
    """
    Control the RC car's steering and speed.

    :param steering_direction: float, -1.0 (full left) to 1.0 (full right)
    :param motor_speed: float, 0.0 (stop) to 1.0 (full speed forward)
    """
    # Clamp steering and speed values to valid ranges
    clamped_steering_direction = max(-1.0, min(1.0, steering_direction))
    clamped_motor_speed = max(0.0, min(1.0, motor_speed))

    if (clamped_steering_direction != steering_direction or clamped_motor_speed != motor_speed):
        print("invalid motor_speed or steering_direction values. Clamped to valid range.")

    # Set the servo position for steering
    servo.value = clamped_steering_direction  # -1.0 is full left, 0.0 is center, 1.0 is full right

    # Set the motor speed
    motor.value = clamped_motor_speed  # 0.0 is off, 1.0 is full speed