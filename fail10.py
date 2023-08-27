##pip install python-telegram-bot opencv-python RPi.GPIO


import time
import telebot
import RPi.GPIO as GPIO
import cv2

# Telegram Bot Token
# TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Initialize the Telegram Bot
bot = telebot.Bot('6340811368:AAFpEMfXiwjvexATp1-z8bIw2c4TmpTUS8I')


# GPIO pins for HC-SR04
TRIG_PIN = 17
ECHO_PIN = 27

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Set threshold distance
DISTANCE_THRESHOLD = 20  # in centimeters

# Initialize camera
camera = cv2.VideoCapture(0)

# Flag to track system status
system_on = False

# Function to handle "/systemon" command
@bot.message_handler(commands=['systemon'])
def system_on_command(message):
    global system_on
    system_on = True
    bot.send_message(message.chat.id, "System is now ON.")
    start_hcsr04()

# Function to handle "/systemoff" command
@bot.message_handler(commands=['systemoff'])
def system_off_command(message):
    global system_on
    system_on = False
    bot.send_message(message.chat.id, "System is now OFF.")

# Function to start HC-SR04 measurements
def start_hcsr04():
    while system_on:
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)

        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound is 34300 cm/s

        if distance < DISTANCE_THRESHOLD:
            for _ in range(10):
                _, frame = camera.read()
                cv2.imwrite("image.jpg", frame)
                bot.send_photo(message.chat.id, open('image.jpg', 'rb'))
                time.sleep(1)  # Wait for a second between images

# Start the bot
bot.polling()
