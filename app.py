#!/usr/bin/python
# Control openxc-vehicle-simulator from a Logitech G27 controller
# by Juergen Schmerder (@schmerdy)

import sys

DEBUG = False

if len(sys.argv) > 1:
  HOST = sys.argv[1] 
else:
  HOST = "localhost"

import urllib2,urllib
import pygame
import math
import os
import traceback
from wheel_config import WheelConfig

# make sure pygame doesn't try to open an output window
os.environ["SDL_VIDEODRIVER"] = "dummy"

ignition_status_values = {
  0: "off",
  1: "accessory",
  2: "start",
  3: "run"
}

gear_lever_positions = {
  -1: "reverse",
  0: "neutral",
  1: "first",
  2: "second",
  3: "third",
  4: "fourth",
  5: "fifth",
  6: "sixth"
}

pedals = {
  WheelConfig.ACCELERATOR_PEDAL_AXIS: "accelerator", 
  WheelConfig.BRAKE_PEDAL_AXIS: "brake",
  WheelConfig.CLUTCH_PEDAL_AXIS: None
}

status_buttons = {
  WheelConfig.PARKING_BRAKE_BUTTON: "parking_brake_status",
  WheelConfig.HEADLAMP_BUTTON: "headlamp_status",
  WheelConfig.HIGH_BEAM_BUTTON: "high_beam_status",
  WheelConfig.WINDSHIELD_WIPER_BUTTON: "windshield_wiper_status"
}

def send_data(name, value, HOST):
  print name, ": ", value
  if HOST is None:
    return
  url = "http://" + HOST + ":50000/_set_data"
  post_data = urllib.urlencode([('name',name),('value',value)])
  if DEBUG: 
    print post_data
  try:
    req = urllib2.urlopen(url, post_data)
  except Exception as ex:
    if DEBUG:
      print ex

ignition_status = 0
gear_lever_position = 0
parking_brake_status = False
headlamp_status = False
high_beam_status = False
windshield_wiper_status = False

def get_wheel():
  wheel = None
  for j in range(0,pygame.joystick.get_count()):
    if pygame.joystick.Joystick(j).get_name() == WheelConfig.WHEEL_NAME:
      wheel = pygame.joystick.Joystick(j)
      wheel.init()
      print "Found", wheel.get_name()

  if not wheel:
    print "No ", WheelConfig.WHEEL_NAME, " found"
    exit(-1)
  return wheel

def is_simulator_running(HOST):
  url = "http://" + HOST + ":50000"
  try:
    req = urllib2.urlopen(url)
  except Exception as ex:
    print ex
    print traceback.format_exc()
    print "No openxc-vehicle-simulator running on", url
    print "switching to wheel trace"
    return False
  return True
 
def cycle_ignition_status(old_status):
  if old_status == 3:
    return 0
  return old_status + 1

pygame.init()                        

try: 

  wheel = get_wheel()
  if not is_simulator_running(HOST):
    HOST = None
  else:
    print "Found car on", HOST 

  clock = pygame.time.Clock()
  wheel_config = WheelConfig()
  keep_going = True
  while keep_going:
    for event in pygame.event.get(pygame.JOYAXISMOTION):
      if DEBUG:
        print "Motion on axis: ", event.axis, event.value
      if event.axis == WheelConfig.STEERING_WHEEL_AXIS:
        send_data("angle", wheel_config.get_steering_Wheel_angle(event.value), HOST)
      elif event.axis in (WheelConfig.ACCELERATOR_PEDAL_AXIS, WheelConfig.BRAKE_PEDAL_AXIS, WheelConfig.CLUTCH_PEDAL_AXIS):
        send_data(pedals[event.axis], wheel_config.get_pedal_percentage(event.axis, event.value), HOST)

    for event in pygame.event.get(pygame.JOYBUTTONUP):
      if DEBUG:
        print "Released button ", event.button
      if event.button == WheelConfig.IGNITION_BUTTON and ignition_status == 2:
        ignition_status = cycle_ignition_status(ignition_status)
        send_data("ignition_status", ignition_status_values[ignition_status], HOST)
      elif event.button == WheelConfig.HIGH_BEAM_BUTTON and not headlamp_status:
        high_beam_status = False
        send_data("high_beam_status", high_beam_status, HOST)
      elif wheel_config.is_gear_lever(event.button):
        gear_lever_position = 0
        send_data("gear_lever_position", gear_lever_positions[gear_lever_position], HOST)

    for event in pygame.event.get(pygame.JOYBUTTONDOWN):
      if DEBUG:
        print "Pressed button ", event.button
      if event.button == WheelConfig.IGNITION_BUTTON:
        ignition_status = cycle_ignition_status(ignition_status)
        send_data("ignition_status", ignition_status_values[ignition_status], HOST)
      elif wheel_config.is_gear_lever(event.button):
        gear_lever_position = wheel_config.get_gear_from_button(event.button)
        send_data("gear_lever_position", gear_lever_positions[gear_lever_position], HOST)
      elif event.button in status_buttons:
        vars()[status_buttons[event.button]] = not vars()[status_buttons[event.button]]
        send_data(status_buttons[event.button],str(vars()[status_buttons[event.button]]).lower(), HOST)
    clock.tick(25)       
 
except Exception as e:
  print e
  print traceback.format_exc()
