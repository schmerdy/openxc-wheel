import pygame
import math
import os

WHEEL_NAME = "G27 Racing Wheel"

    
def get_axis(num):
  clock = pygame.time.Clock()
  keep_going = True
  while keep_going:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        keep_going = False
      if event.type == pygame.JOYAXISMOTION:
        print event.axis, event.value
        if (num > 0 and event.value >= num) or (num < 0 and event.value <= num):
          return event.axis
    clock.tick(10)

def get_button():
  clock = pygame.time.Clock()
  keep_going = True
  button = None
  while keep_going:
    for event in pygame.event.get(pygame.JOYBUTTONDOWN):
      print event.button
      button = event.button
      break
    if button is not None:
      break
    clock.tick(10)
  print "release button", button
  while keep_going:
    for event in pygame.event.get(pygame.JOYBUTTONUP):
      if button == event.button:
        return button
    clock.tick(10)


# make sure pygame doesn't try to open an output window
os.environ["SDL_VIDEODRIVER"] = "dummy"
try:
  pygame.init() 
except Exception as ex:
  print ex
  exit(-1)

wheel = None
for j in range(0,pygame.joystick.get_count()):
  if pygame.joystick.Joystick(j).get_name() == WHEEL_NAME:
    wheel = pygame.joystick.Joystick(j)
    wheel.init()
    print "Found", wheel.get_name()

if not wheel:
  print "No " + WHEEL_NAME + " found"
  exit(0)
  #raise "No " + Wheel.config.WHEEL_NAME + " found"

print "steer all the way to the left"
print get_axis(-1)
print "steer all the way to the right"
print get_axis(1)

print "press gas pedal"
print get_axis(-1)
print "release gas pedal"
print get_axis(1)
print "press brake pedal"
print get_axis(-1)
print "release brake pedal"
print get_axis(1)
print "press clutch pedal"
print get_axis(-1)
print "release clutch pedal"
print get_axis(1)

print "shift to first gear"
print get_button()
print "shift to second gear"
print get_button()
print "shift to third gear"
print get_button()
print "shift to fourth gear"
print get_button()
print "shift to fifth gear"
print get_button()
print "shift to sixth gear"
print get_button()
print "shift to reverse gear"
print get_button()

print "press ignition button"
print get_button()
print "press handbrake button"
print get_button()
print "press headlamp button"
print get_button()
print "press high beam button"
print get_button()
print "press windshield wiper button"
print get_button()


