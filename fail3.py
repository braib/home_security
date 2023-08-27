    import RPi.GPIO as GPIO
import time
import cv2

# GPIO pin numbers
TRIG_PIN = 18
ECHO_PIN = 24

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Set threshold distance
THRESHOLD_DISTANCE = 20  # in centimeters

# Initialize the camera
camera = cv2.VideoCapture(0)
camera.set(3, 640)  # Width
camera.set(4, 480)  # Height

def measure_distance():
    # Send a short pulse to the trigger pin
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Measure the time for the ECHO pin to go high
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()

    # Measure the time for the ECHO pin to go low
    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound = 343 m/s
    return distance

try:
    while True:
        distance = measure_distance()
        print("Distance:", distance, "cm")

        if distance < THRESHOLD_DISTANCE:
            # Capture a photo
            ret, frame = camera.read()
            if ret:
                cv2.imwrite("captured_photo.jpg", frame)
                print("Photo captured!")

        time.sleep(1)  # Wait for a moment before taking another measurement

except KeyboardInterrupt:
    GPIO.cleanup()
    camera.release()
    cv2.destroyAllWindows()
