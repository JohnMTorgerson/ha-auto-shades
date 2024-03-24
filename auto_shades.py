#!/usr/bin/python
# -*- coding: utf-8 -*-

import configure_logging
logger = configure_logging.configure(__name__)
import RPi.GPIO as GPIO
import time
import json
import asyncio

def run(dir): # dir indicates direction to move shade: 'up' for up, or 'down' for down
    if dir not in ["up","down"] :
        logger.error(f"Attempting to run shades, but dir param must be either 'up' or 'down': received '{dir}'")
        raise ValueError("value of dir should be either 'up' or 'down'")

    logger.info(f"Running shades {dir}")

    try:
        window_info = get_window_info()
    except Exception as e:
        logger.error(f"When trying to get window info: {repr(e)}")
        raise e

    # GPIO.cleanup()
    GPIO.setwarnings(False)
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
    '''
    moves window shade up or down

    w -- the json object for the window to move (which includes which gpio pins to use for that window)
        e.g. "dir_pin" : 23,
             "pul_pin" : 24,
             "ena_pin" : 25,
             "steps_per_rev" : 1600,
             "up" : [33,-1],
             "down" : [-32]
    dir -- a string which should be either "up" or "down" to indicate which profile to use
    '''

    name = w["name"]
    logger.debug(f"Running {name} window")

    if dir != "up" and dir != "down" :
        raise ValueError("value of dir should be either 'up' or 'down'")

    dir_pin = w["dir_pin"]
    pul_pin = w["pul_pin"]
    ena_pin = w["ena_pin"]
    steps_per_rev = w["steps_per_rev"]

    GPIO.setup(dir_pin,GPIO.OUT)
    GPIO.setup(pul_pin,GPIO.OUT)
    GPIO.setup(ena_pin,GPIO.OUT)
    GPIO.output(dir_pin,0)
    GPIO.output(pul_pin,0)
    GPIO.output(ena_pin,0)

    # loop through profile for this window
    # the profile is a list of numbers of revolutions of the motor (positive for up, negative for down)
    # and their are two profiles for every window (w["up"] and w["down"])
    for revs in w[dir] :
        logger.debug(f"{name} :: revs == {revs}")

        steps = int(float(revs) * steps_per_rev)
        if steps < 0:
            GPIO.output(dir_pin,1)
            steps = -steps
        else:
            GPIO.output(dir_pin,0)

        logger.debug(f"{name} :: steps == {steps}")

        for i in range(steps):
            if i%steps_per_rev == 0 :
                logger.debug(f"{name} :: {i} -- {i/steps_per_rev}")
            
            GPIO.output(pul_pin, 0)
            GPIO.output(pul_pin, 1)
            time.sleep(0.001)

        logger.debug(f"{name} :: {steps} -- {steps/steps_per_rev}")

    logger.debug(f"{name} :: COMPLETE")

    # turn off power to motor (do not clean up after)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ena_pin,GPIO.OUT)
    GPIO.output(ena_pin,1)

def get_window_info():
    with open("windows.json","r") as f:
        window_info = json.load(f)
    return window_info

if __name__ == "__main__" :
    dir = ""
    while dir != "up" and dir != "down":
        if dir != "" :
            print("Must enter either 'up' or 'down")
        dir = input("Enter 'up' or 'down': ")

    run(dir)
