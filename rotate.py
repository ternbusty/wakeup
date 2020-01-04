import RPi.GPIO as GPIO
import time
import sys


def init_gpio():
    GPIO.setmode(GPIO.BCM)
    channel_list = [24, 25]
    GPIO.setup(channel_list, GPIO.OUT)


def stop():
    GPIO.output(24, False)
    GPIO.output(25, False)


def cleanup():
    GPIO.cleanup()


def rotate_right(duration):
    init_gpio()
    stop()
    GPIO.output(24, True)
    GPIO.output(25, False)
    time.sleep(duration)
    stop()
    cleanup()


def rotate_left(duration):
    init_gpio()
    stop()
    GPIO.output(24, False)
    GPIO.output(25, True)
    time.sleep(duration)
    stop()
    cleanup()


if __name__ == '__main__':
    args = sys.argv
    if args[1] == 'lock':
        rotate_right(5)
    elif args[1] == 'unlock':
        rotate_left(5)
