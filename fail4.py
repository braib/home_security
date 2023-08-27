# python
import telepot

import time

import cv2

import os
path = os.getenv("HOME")

# initialize HCSR04 sensor

import RPi.GPIO as GPIO

import time

bot = telepot.Bot('6340811368:AAFpEMfXiwjvexATp1-z8bIw2c4TmpTUS8I')

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)

GPIO.setup(24, GPIO.IN)


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


# initialize camera

camera = cv2.VideoCapture(0)


# set threshold value

threshold = 20


while True:
    # get distance value
    distance_value = distance()
    print(distance_value)
    # check if distance value is less than threshold value
    if distance_value < threshold:
        time.sleep(2)
        # take a photo using cv2
        ret, frame = camera.read()
        if ret :
            cv2.imwrite(path + '/pic.jpg', frame)
        camera.release()
        bot.sendPhoto(id, open(path + '/pic.jpg', 'rb'))
        # cv2.imwrite("photo.jpg", frame)
        # print("Photo taken")
        # bot.sendPhoto(id, "photo.jpg")

    # wait for 1 second before checking again
    time.sleep(1)
    