import RPi.GPIO as GPIO
import time
import telepot
import os
import cv2

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the sensor
TRIG_PIN = 23
ECHO_PIN = 24

# Set up GPIO direction (IN / OUT)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Replace 'your_bot_id' with your actual Telegram Bot token
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
bot = telepot.Bot(TELEGRAM_BOT_TOKEN)

# Get the home directory path
path = os.getenv("HOME")

def take_picture(file_name):
    # Initialize the camera
    camera = cv2.VideoCapture(0)  # 0 for the default camera (Raspberry Pi camera)

    # Allow the camera to warm up
    time.sleep(2)

    # Capture the picture
    ret, frame = camera.read()
    if ret:
        image_path = os.path.join(path, file_name)
        cv2.imwrite(image_path, frame)

        # Release the camera
        camera.release()

        # Sending picture
        with open(image_path, 'rb') as photo_file:
            bot.sendPhoto('YOUR_CHAT_ID', photo_file)

        os.remove(image_path)

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
    photo_count = 0
    while photo_count < 50:  # Limit the number of photos to 50
        distance = presence_detection()
        print(distance)

        threshold_distance = 20  # Adjust this value as needed

        if distance < threshold_distance:
            print("Object is present!")
            print("Taking a picture...")
            photo_file_name = f'pic{photo_count}.jpg'
            take_picture(photo_file_name)
            photo_count += 1

        time.sleep(2)  # Wait for 2 seconds before the next iteration

except KeyboardInterrupt:
    GPIO.cleanup()
