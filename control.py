#!/usr/bin/python
# Control openxc-vehicle-simulator from a Logitech G27 controller
# by Juergen Schmerder (@schmerdy)
# inspired by https://github.com/moozer/CameraBot/blob/master/src/deviceinfo.py

import pygame
import math
import os
import urllib, urllib2
from cookielib import CookieJar

# make sure pygame doesn't try to open an output window
os.environ["SDL_VIDEODRIVER"] = "dummy"

DEBUG = False
HOST = "localhost"
PORT = "50000"
WHEEL = "G27 Racing Wheel"
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

status_buttons = {
  10: "parking_brake_status",
  1: "headlamp_status",
  3: "high_beam_status",
  2: "windshield_wiper_status"
}

gear_lever_position = 0
parking_brake_status = False
headlamp_status = False
high_beam_status = False
windshield_wiper_status = False
axis_mode = 1

def send_data(name, value):
  url = 'http://localhost:50000/_set_data'
  #print name,value
  post_data = urllib.urlencode([('name',name),('value',value)])
  print post_data
  try:
    req = urllib2.urlopen(url, post_data)
  except Exception as ex:
    print ex
    exit(-1)

def pedal_value(value):
  '''Steering Wheel returns pedal reading as value 
  between -1 (fully pressed) and 1 (not pressed)
  normalizing to value between 0 and 100%'''
  return (1 - value) * 50


def start():
  urllib2.urlopen("http://localhost:50000/start","")
  send_data("ignition_status","off")
def stop():
  send_data("ignition_status","off")
  urllib2.urlopen("http://localhost:50000/stop","")


pygame.init()                        

try:
  res = urllib2.urlopen("http://localhost:50000/")
except urllib2.HTTPError, e:
    print e.code
except urllib2.URLError, e:
    print e.args

try: 

  wheel = None
  for j in range(0,pygame.joystick.get_count()):
    if pygame.joystick.Joystick(j).get_name() == WHEEL:
      wheel = pygame.joystick.Joystick(j)
      wheel.init()
      print "Found", wheel.get_name()

  if not wheel:
    print "No G27 steering wheel found"
    exit(-1)

  start()

  while True:
    for event in pygame.event.get(pygame.QUIT):
      exit(0)
    for event in pygame.event.get(pygame.JOYAXISMOTION):
      if DEBUG:
        print "Motion on axis: ", event.axis
      if event.axis == 0:
        send_data("angle", event.value * 600)
      elif event.axis == 1 and axis_mode ==1:
        if event.value < 0:
          send_data("accelerator", event.value * -100)
        else:
          send_data("brake", event.value * 100)
      elif event.axis == 1 and axis_mode == 2:
        send_data("accelerator", pedal_value(event.value))
      elif event.axis == 2 and axis_mode == 2:
        send_data("brake", pedal_value(event.value))
      elif event.axis == 3:
        send_data("clutch", pedal_value(event.value))
    for event in pygame.event.get(pygame.JOYBUTTONUP):
      if DEBUG:
        print "Released button is", event.button
      if (event.button >= 12 and event.button <= 17) or event.button == 22:
        gear = 0
        send_data("gear_lever_position", gear_lever_positions[gear])
    for event in pygame.event.get(pygame.JOYBUTTONDOWN):
      if DEBUG:
        print "Pressed button is", event.button
      if event.button == 0: 
        print "pressed button 0 - bye..."
        stop()
        exit(0)
      elif event.button == 11:
        send_data("ignition_status","start")
      elif event.button >= 12 and event.button <= 17:
        gear = event.button - 11
        send_data("gear_lever_position", gear_lever_positions[gear])
      elif event.button == 22:
        gear = -1
        send_data("gear_lever_position", gear_lever_positions[gear])
      elif event.button in status_buttons:
        vars()[status_buttons[event.button]] = not vars()[status_buttons[event.button]]
        send_data(status_buttons[event.button],str(vars()[status_buttons[event.button]]).lower())

except Exception as e:
  print e
