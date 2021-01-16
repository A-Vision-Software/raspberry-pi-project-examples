import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RED = 26
YELLOW = 5
GREEN = 9

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

BUZZER = 22

GPIO.setup(BUZZER, GPIO.OUT)

TRIG = 18
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def red_light():
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)

def yellow_light():
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.LOW)

def green_light():
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(GREEN, GPIO.HIGH)

def buzz(duration):
    GPIO.output(BUZZER, True)
    time.sleep(duration)
    GPIO.output(BUZZER, False)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = 0
    end = 0

    start = time.time()
    end = time.time()
    while GPIO.input(ECHO) == False and (end - start) < 1:
        end = time.time()

    start = time.time()
    while GPIO.input(ECHO) == True:
        end = time.time()

    sig_time = end - start
    distance = sig_time / 0.000058

    return distance

try:
    while True:
        distance = get_distance()
        time.sleep(0.05)
        print('Distance in cm: ' + str(distance))

        if distance >= 30:
            green_light()
        elif 30 > distance > 15:
            yellow_light()
            buzz(0.3)
        else:
            red_light()
            buzz(0.1)

finally:
    GPIO.cleanup()
