import cv2
import time
import RPi.GPIO as GPIO
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Initialize the GPIO pins for HC-SR04
TRIGGER_PIN = 23
ECHO_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialize the Telegram Bot
TOKEN = "6340811368:AAFpEMfXiwjvexATp1-z8bIw2c4TmpTUS8I"
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Global variable to track the system state
system_on = False

# Function to start the system
def start_system(update: Update, context: CallbackContext):
    global system_on
    system_on = True
    update.message.reply_text("System is now ON.")
    # Add code to turn on HC-SR04 and monitor its readings

# Function to stop the system
def stop_system(update: Update, context: CallbackContext):
    global system_on
    system_on = False
    update.message.reply_text("System is now OFF.")
    # Add code to turn off HC-SR04

# Function to capture and send images
def capture_images(context: CallbackContext):
    if system_on:
        # Add code to capture images using cv2
        # Send images to the bot using update.message.reply_photo()

# Command handlers
dispatcher.add_handler(CommandHandler("systemon", start_system))
dispatcher.add_handler(CommandHandler("systemoff", stop_system))

# Polling for messages and images
updater.start_polling()

# Schedule image capturing every X seconds
CAPTURE_INTERVAL = 30  # Adjust this interval as needed
updater.job_queue.run_repeating(capture_images, interval=CAPTURE_INTERVAL)

# Run the bot
updater.idle()
