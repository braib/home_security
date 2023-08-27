import RPi.GPIO as GPIO
import time

import telepot
import time
import os
import cv2

path = os.getenv("HOME")


# Replace 'your_bot_id' with your actual Telegram Bot token
bot = telepot.Bot('6340811368:AAFpEMfXiwjvexATp1-z8bIw2c4TmpTUS8I')

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the sensor
#set GPIO Pins
TRIG_PIN = 23
ECHO_PIN = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)


def take_picture():
        # Initialize the camera
        camera = cv2.VideoCapture(0)  # 0 for the default camera (Raspberry Pi camera)

        # Allow the camera to warm up
        time.sleep(2)

        # Capture the picture
        ret, frame = camera.read()
        if ret:
            cv2.imwrite(path + '/pic.jpg', frame)

        # Release the camera
        camera.release()

        # Sending picture
        bot.sendPhoto(id, open(path + '/pic.jpg', 'rb'))



def presence_detection():
    # Set trigger to HIGH for a short pulse
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    start_time = time.time()
    stop_time = time.time()

    # Save start time
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    # Save time of arrival
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    # Calculate time difference
    time_elapsed = stop_time - start_time

    # Calculate distance (speed of sound is 34300 cm/s)
    distance = (time_elapsed * 34300) / 2

    return distance

try:
    while True:
        
        distance = presence_detection()
        print(distance)
        # Define a threshold distance below which an object is considered present
        threshold_distance = 20  # Adjust this value as needed
        print(distance)
        if distance < threshold_distance:
            print("Object is present!")
            print("thief alert")
            take_picture()
        else:
            print("No object detected.")
            
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()


