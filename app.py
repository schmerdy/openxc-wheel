#!/usr/bin/python
# Control openxc-vehicle-simulator from a Logitech G27 controller
# by Juergen Schmerder (@schmerdy)

import sys
from wheel import Wheel

DEBUG = True

# first command line parameter can be hostname
# if simulator runs on different computer
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

pedal_names = {
  Wheel.config.ACCELERATOR: "accelerator", 
  Wheel.config.BRAKE: "brake",
  Wheel.config.CLUTCH: None
}

button_names = {
  Wheel.config.IGNITION: "ignition_status",
  Wheel.config.PARKING_BRAKE: "parking_brake_status",
  Wheel.config.HEADLAMP: "headlamp_status",
  Wheel.config.HIGH_BEAM: "high_beam_status",
  Wheel.config.WINDSHIELD_WIPER: "windshield_wiper_status"
}

def send_data(name, value, HOST='localhost'):
  url = "http://" + HOST + ":50000/_set_data"
  post_data = urllib.urlencode([('name',name),('value',value)])
  if DEBUG: 
    print post_data
  try:
    req = urllib2.urlopen(url, post_data)
  except Exception as ex:
    if DEBUG:
      print ex

def is_simulator_running(HOST):
  url = "http://" + HOST + ":50000"
  try:
    req = urllib2.urlopen(url)
  except Exception as ex:
    print ex
    print traceback.format_exc()
    print "No openxc-vehicle-simulator running on", url
    print "logging wheel input instead"
    return False
  return True
 
def cycle_ignition_status(old_status):
  if old_status == 3:
    return 0
  return old_status + 1

def on_accelerator(val):
  send_data(pedal_names[g27.config.ACCELERATOR], val)
def on_brake(val):
  send_data(pedal_names[g27.config.BRAKE], val)
def on_clutch(val):
  # clutch not supported by simulator
  pass
def on_angle(val):
  send_data('angle', val)
def on_ignition(val):
  send_data(button_names[g27.config.IGNITION], str(val))
def on_parking_brake(val):
  send_data(button_names[g27.config.PARKING_BRAKE], str(val).lower())
def on_headlamp(val):
  send_data(button_names[g27.config.HEADLAMP], str(val).lower())
def on_high_beam(val):
  send_data(button_names[g27.config.HIGH_BEAM], str(val).lower())
def on_windshied_wiper(val):
  send_data(button_names[g27.config.WINDSHIELD_WIPER], str(val).lower())
def on_gear_shift(gear):
  send_data("gear_lever_position", gear)

g27 = Wheel()

g27.register_steering_wheel(on_angle)
g27.register_pedal(g27.config.ACCELERATOR, on_accelerator)
g27.register_pedal(g27.config.BRAKE, on_brake)
g27.register_pedal(g27.config.CLUTCH, on_clutch)
g27.register_button(g27.config.IGNITION, on_ignition)
g27.register_button(g27.config.PARKING_BRAKE, on_parking_brake)
g27.register_button(g27.config.HEADLAMP, on_headlamp)
g27.register_button(g27.config.HIGH_BEAM, on_high_beam)
g27.register_button(g27.config.WINDSHIELD_WIPER, on_windshied_wiper)
g27.register_gear_shift(on_gear_shift)

try: 

  if not is_simulator_running(HOST):
    HOST = None
  else:
    print "Found car on", HOST 

  g27.loop()
  
except Exception as e:
  print e
  print traceback.format_exc()
