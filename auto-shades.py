#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import json
import asyncio


def run(dir): # dir indicates direction to move shade: 1 for up, -1 for down
    window_info = get_window_info()

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    async def loop_windows() :
        # loop through each window controlled by this computer
        # and run each window shade (up or down) concurrently
        for window in window_info :
            w = window_info[window]
            task = asyncio.create_task(run_window(w,dir))
            await task

    asyncio.run(loop_windows())


async def run_window(w,dir):

    dir_pin = w["dir_pin"]
    pul_pin = w["pul_pin"]
    ena_pin = w["ena_pin"]
    steps_per_rev = w["steps_per_rev"]
    revs = w["revs"] * dir # the number of revs to bring the shade all the way up or all the way down (dir being either 1 or -1 to indicate direction up or down, respectively)


    GPIO.setup(dir_pin,GPIO.OUT)
    GPIO.setup(pul_pin,GPIO.OUT)
    GPIO.setup(ena_pin,GPIO.OUT)
    GPIO.output(dir_pin,0)
    GPIO.output(pul_pin,0)
    GPIO.output(ena_pin,0)


    print(f"revs == {revs}")

    steps = int(float(revs) * steps_per_rev)
    if steps < 0:
        GPIO.output(dir_pin,1)
        steps = -steps
    else:
        GPIO.output(dir_pin,0)

    print(f"steps == {steps}")

    for i in range(steps):
        if i%steps_per_rev == 0 :
            print(f"{i} -- {i/steps_per_rev}")
        
        GPIO.output(pul_pin, 0)
        GPIO.output(pul_pin, 1)
        time.sleep(0.001)

    print (f"{steps} -- {steps/steps_per_rev}")

    # turn off power to motor (do not clean up after)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ena_pin,GPIO.OUT)
    GPIO.output(ena_pin,1)

def get_window_info():
    with open("windows.json","r") as f:
        window_info = json.load(f)
    return window_info

if __name__ == "__main__" :
    dir = 1.414
    while dir != 1 and dir != -1:
        if dir != 1.414 :
            print("Must enter either 1 or -1")
        dir = input("Enter '1' for up, '-1' for down: ")
        try:
            dir = int(dir)
        except:
            dir = 0

    run(dir)
