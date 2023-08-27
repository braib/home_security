import time
import cv2
import RPi.GPIO as GPIO
from telegram.ext import Updater, CommandHandler

# Initialize the HC-SR04 sensor
TRIG_PIN = 17
ECHO_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialize the Telegram bot
TOKEN = 'your_bot_token'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Global variables
is_system_on = False

# Define the /systemon command handler
def system_on(update, context):
    global is_system_on
    is_system_on = True
    update.message.reply_text("System is now ON. HC-SR04 activated.")

# Define the /systemoff command handler
def system_off(update, context):
    global is_system_on
    is_system_on = False
    update.message.reply_text("System is now OFF. HC-SR04 deactivated.")

# Define the main function to check HC-SR04 readings and take pictures
def check_distance_and_take_pictures(context):
    if not is_system_on:
        return

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.0001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound = 343 m/s

    if distance < 20:
        for i in range(10):
            camera = cv2.VideoCapture(0)
            ret, frame = camera.read()
            if ret:
                image_path = f"image_{i + 1}.jpg"
                cv2.imwrite(image_path, frame)
                context.bot.send_photo(chat_id=update.message.chat_id, photo=open(image_path, 'rb'))
                camera.release()
                time.sleep(1)
            else:
                context.bot.send_message(chat_id=update.message.chat_id, text="Failed to capture image.")
    
    context.job_queue.run_once(check_distance_and_take_pictures, interval=5, context=update)

# Add command handlers to the dispatcher
dispatcher.add_handler(CommandHandler("systemon", system_on))
dispatcher.add_handler(CommandHandler("systemoff", system_off))

# Start checking distance and taking pictures periodically
updater.job_queue.run_once(check_distance_and_take_pictures, 0)

# Start the bot
updater.start_polling()
updater.idle()
