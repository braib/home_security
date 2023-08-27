import telepot
import time
import cv2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

# Initialize the Telegram Bot
bot = telepot.Bot('YOUR_BOT_TOKEN')

# Define the default path where images will be saved
default_path = '/default/path/to/save/images'

# Initialize the camera
camera = cv2.VideoCapture(0)

# Set threshold value
threshold = 20

# Flag to keep track of system status
system_on = False

def handle_message(msg):
    global system_on
    
    chat_id = msg['chat']['id']
    command = msg['text']
    
    if command == '/systemon':
        if not system_on:
            bot.sendMessage(chat_id, "System is now ON. Monitoring distance.")
            system_on = True
            monitor_distance(chat_id)
        else:
            bot.sendMessage(chat_id, "System is already ON.")
    elif command == '/systemoff':
        bot.sendMessage(chat_id, "System is now OFF. HCSR04 sensor is turned off.")
        system_on = False
        GPIO.output(23, GPIO.LOW)  # Turn off HCSR04 sensor

def monitor_distance(chat_id):
    while system_on:
        distance_value = distance()
        print(distance_value)
        
        if distance_value < threshold:
            time.sleep(2)
            for _ in range(10):  # Capture and send 10 images
                ret, frame = camera.read()
                if ret:
                    img_path = default_path + '/pic.jpg'
                    cv2.imwrite(img_path, frame)
                    bot.sendPhoto(chat_id, photo=open(img_path, 'rb'))
                    time.sleep(1)  # Wait between capturing images
        
        time.sleep(1)

def distance():
    GPIO.output(23, True)
    time.sleep(0.00001)
    GPIO.output(23, False)
    while GPIO.input(24) == 0:
        signaloff = time.time()
    while GPIO.input(24) == 1:
        signalon = time.time()
    timepassed = signalon - signaloff
    distance = timepassed * 17000
    return distance

# Start listening for messages
bot.message_loop(handle_message)

# Keep the script running
while True:
    time.sleep(1)
