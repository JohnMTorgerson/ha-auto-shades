#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dir_pin = 23
pul_pin = 24
steps_per_rev = 1600

GPIO.setup(dir_pin,GPIO.OUT)
GPIO.setup(pul_pin,GPIO.OUT)
GPIO.output(dir_pin,0)
GPIO.output(pul_pin,0)


try:
  while True:
    revs = input("How many revolutions forward? ")
    steps = revs * steps_per_rev
    if int(steps) < 0:
        GPIO.output(dir_pin,1)
        steps = -steps
    else:
        GPIO.output(dir_pin,0)

    for i in range(int(steps)):
        if i%steps_per_rev == 0 :
           print(i/steps_per_rev)
           
        GPIO.output(pul_pin, 0)
        GPIO.output(pul_pin, 1)
        time.sleep(0.001)

# End program cleanly with keyboard
except KeyboardInterrupt:
  print("  Quit")
  GPIO.cleanup()