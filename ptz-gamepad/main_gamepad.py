""" Gamepad -> PTZ


"""

import time
import pygame
import yaml

from ptzipcam.ptz_camera import PtzCam

from handle_events import GamepadHandler
from mockup import DummyPtzCam


use_cam_mockup = False

pygame.init()

#initialise the joystick module
pygame.joystick.init()

#create empty list to store joysticks
joysticks = []

# used for graceful shutdown (not implemented)
run = True

# init camera object

if use_cam_mockup:
    cam = DummyPtzCam()

else:
    config_file = 'cam_config.yml'

    with open(config_file, 'r') as f:
        cam_config = yaml.safe_load(f)

    # ptz camera networking constants
    IP = cam_config['IP']
    PORT = cam_config['PORT']
    USER = cam_config['USER']
    PASS = cam_config['PASS']

    cam = PtzCam(IP, PORT, USER, PASS)

# init object that execute functions on events
gh = GamepadHandler(cam)

# so initialisieren, dass die Bedingung in der while schleife erstmal nicht zuschlägt
t0 = time.perf_counter() - 1000

while run:
    event = pygame.event.wait()

    # in den ersten 0.5 sek nach erkennen des Gamepads die events ignorieren, wegen spurious button events
    if time.perf_counter() - t0 < 0.5:
        print(f'ignoriere event direkt nach startup: {event}')
        continue

    if event.type == pygame.JOYDEVICEADDED:
        joy = pygame.joystick.Joystick(event.device_index)
        joysticks.append(joy)

        # Nullstellung speichern (kalibrierung)
        for i in range(10):
            ax0 = joy.get_axis(0)
            ax1 = joy.get_axis(1)
            print(f'calibration: {ax0}, {ax1}')

        gh.axis_0_1_calibrate(ax0, ax1)

        # für 1/2 sek alle Events ignorieren, weil da manchmal spurious button events kommen
        t0 = time.perf_counter()

    elif event.type == pygame.QUIT:
      run = False

    elif event.type == pygame.JOYBUTTONDOWN:
        print(f"Button {event.button} pressed")

        gh.handle_button_down_event(event.button)

    elif event.type == pygame.JOYBUTTONUP:
        # maybe use for debouncing
        # or easier: after BUTTONDOWN event have a time window of 10-20 ms where
        # the same event is just discarded
        print(f"Button {event.button} released")

        gh.handle_button_up_event(event.button)

    elif event.type == pygame.JOYAXISMOTION:

        # ignore -- too much nonsense, and too slow motion right now
        #continue
    
        print(f"Axis {event.axis} motion, pos {event.value}")

        gh.handle_joyaxis_event(event.axis, event.value)

    elif event.type == pygame.JOYHATMOTION:
        print("Hat motion")
        print(event)

    elif event.type == pygame.KEYDOWN:
        # Key-Event (zum Abbrechen) -> das geht nur mit einem Window, das von pygame gemanagt wird
        # aber man kann zum Unterbrechen auch einfach Ctrl-C drücken,
        # und dann eine Taste am Gamepad drücken
        
        if event.key == pygame.K_q:
            print("Button q pressed, exiting.")
            run = False
    

