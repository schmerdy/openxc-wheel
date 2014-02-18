import wheel_config
import pygame
import math
import os

class Wheel:
  """Talk to a Logitech G27 steering wheel via pygame

  On Linux and Mac OS-X, the G27 needs to be put in 'native' mode.
  Use LTWheelConf (http://steamcommunity.com/sharedfiles/filedetails/?id=142372419) for Linux,
  or FreeTheWheel (http://support.feralinteractive.com/en/faqs/free_the_wheel/) for Mac OS-X"""
  class Pedal(object):
    """represents a G27 pedal"""
    def __init__(self, on_change):
      self._state = None
      self.on_change = on_change

    @property
    def state(self):
      return self._state

    @state.setter
    def state(self, value):
      """convert the value coming from the G27 to the openxc format

      pygame returns a value between -1 (fully pressed) and 1 (not pressed) 
      for every axis
      openxc-vehicle-simulator expects a percentage value between 0 and 100
      """
      state = (1 - value) * 50
      if state > 100 - Wheel.config.PEDAL_TOLERANCE:
        state = 100
      if state < Wheel.config.PEDAL_TOLERANCE:
        state = 0
      if self._state is None or math.fabs(self._state - state) > Wheel.config.PEDAL_TOLERANCE:
        self._state = state
        self.on_change(self._state)

  class Button(object):
    """represents a G27 button"""
    def __init__(self, on_change):
      self._pressed = None
      self.value = False
      self.on_change = on_change

    @property
    def pressed(self):
      return _pressed

    @pressed.setter
    def pressed(self, value):
      if value != self._pressed:
        self._pressed = value
      if self._pressed:
        self.value = not self.value
      else:
        return
      self.on_change(self.value)
  

  class IgnitionButton(Button):
    """represents the G27 button used for ignition status"""

    ignition_status_values = {
      0: "off",
      1: "accessory",
      2: "start",
      3: "run"
    }

    def __init__(self, on_change):
      self._pressed = None
      self.value = 0
      self.on_change = on_change

    @property
    def pressed(self):
      return _pressed

    @pressed.setter
    def pressed(self, value):
      if value != self._pressed:
        self._pressed = value
      else:
        return
      if self.value == 3:
        self.value = 0
      elif (self.value < 2 and self._pressed) or (self.value == 2 and not self._pressed):
        self.value += 1
      else:
        return
      self.on_change(Wheel.IgnitionButton.ignition_status_values[self.value])

  class GearShift(object):
    """represents the G27 gear shift"""
    def __init__(self, on_change):
      self._gear = None
      self.on_change = on_change

    @property
    def gear(self):
      return _pressed

    @gear.setter
    def gear(self, value):
      if value != self._gear:
        self._gear = value
        self.on_change(self._gear)

  class SteeringWheel(object):
    """represents the G27 steering wheel"""
    def __init__(self, on_change):
      self._angle = None
      self.on_change = on_change

    @property
    def angle(self):
      return self._angle

    @angle.setter
    def angle(self, value):
      # pygame returns a value between -1 and 1 for every axis
      # openxc-vehicle-simulator expects a value between -600 and 600
      angle = value * 600
      if angle > 600 - Wheel.config.STEERING_WHEEL_TOLERANCE:
        angle = 600
      if angle < -600 + Wheel.config.STEERING_WHEEL_TOLERANCE:
        angle = -600
      if math.fabs(angle) < Wheel.config.STEERING_WHEEL_TOLERANCE:
        angle = 0
      if self._angle is None or math.fabs(self._angle - angle) > Wheel.config.STEERING_WHEEL_TOLERANCE:
        self._angle = angle
        self.on_change(self._angle)


  config = wheel_config
  gears = {
    0: "neutral",
    wheel_config.GEAR_1: "first",
    wheel_config.GEAR_2: "second",
    wheel_config.GEAR_3: "third",
    wheel_config.GEAR_4: "fourth",
    wheel_config.GEAR_5: "fifth",
    wheel_config.GEAR_6: "sixth",
    wheel_config.GEAR_REVERSE: "reverse"
  }

  def __init__(self):
    """create a new Wheel instance"""
    
    # make sure pygame doesn't try to open an output window
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    try:
      pygame.init() 
    except Exception as ex:
      return None

    self.wheel = None
    for j in range(0,pygame.joystick.get_count()):
      if pygame.joystick.Joystick(j).get_name() == Wheel.config.WHEEL_NAME:
        self.wheel = pygame.joystick.Joystick(j)
        self.wheel.init()
        print "Found", self.wheel.get_name()

    if not self.wheel:
      print "No", Wheel.config.WHEEL_NAME, "found"
      #raise "No " + Wheel.config.WHEEL_NAME + " found"

  def is_gear_button(self, button):
    """checks if a button event is actually the gear shift being moved"""
    return button in (
      Wheel.config.GEAR_1,
      Wheel.config.GEAR_2,
      Wheel.config.GEAR_3,
      Wheel.config.GEAR_4,
      Wheel.config.GEAR_5,
      Wheel.config.GEAR_6,
      Wheel.config.GEAR_REVERSE,
    )

  def register_pedal(self, axis, handler):
    """register event handler for a G27 pedal

    axis -- the number of the G27 axis (0-3)
    handler -- the event handler that is called when the axis is moved more than the tolerance
    """
    if axis == Wheel.config.ACCELERATOR:
      self.accelerator = Wheel.Pedal(handler)
    elif axis == Wheel.config.BRAKE:
      self.brake = Wheel.Pedal(handler)
    elif axis == Wheel.config.CLUTCH:
      self.clutch = Wheel.Pedal(handler)
    else:
      print "Pedal not configured", axis

  def register_steering_wheel(self, handler):
    """register event handler for the steering wheel

    handler -- the event handler that is called when the axis is moved more than the tolerance
    """
    self.steering_wheel = Wheel.SteeringWheel(handler)

  def register_gear_shift(self, handler):
    """register event handler for the gear shift

    handler -- the event handler that is called when the gear is switched
    """
    self.gear_shift = Wheel.GearShift(handler)

  def register_button(self, button, handler):
    """register event handler for a button

    handler -- the event handler that is called when the device mapped to the button is switched on or off
    All buttons function as toggle buttons (press to switch on, press again to switch off),
    with the exception of the ignition button: first press: accessory, second press: start, 
    release second press: run, third press: off. Repeat...
    """

    if button == Wheel.config.IGNITION:
      self.ignition = Wheel.IgnitionButton(handler)
    elif button == Wheel.config.PARKING_BRAKE:
      self.parking_brake = Wheel.Button(handler)
    elif button == Wheel.config.HEADLAMP:
      self.headlamp = Wheel.Button(handler)
    elif button == Wheel.config.HIGH_BEAM:
      self.high_beam = Wheel.Button(handler)
    elif button == Wheel.config.WINDSHIELD_WIPER:
      self.windshield_wiper = Wheel.Button(handler)
    else:
      raise "button not configured", button

  def handle_steering_wheel(self, value):
    self.steering_wheel.angle = value

  def handle_pedal(self ,pedal, value):
    if pedal == Wheel.config.ACCELERATOR:
      self.accelerator.state = value
    elif pedal == Wheel.config.BRAKE:
      self.brake.state = value
    elif pedal == Wheel.config.CLUTCH:
      self.clutch.state = value
    else:
      print "Pedal not configured", pedal

  def handle_gear_shift(self, value):
    self.gear_shift.gear = Wheel.gears.get(value)

  def handle_button(self, button, value):
    if button == Wheel.config.IGNITION:
      self.ignition.pressed = value
    elif button == Wheel.config.PARKING_BRAKE:
      self.parking_brake.pressed = value
    elif button == Wheel.config.HEADLAMP:
      self.headlamp.pressed = value
    elif button == Wheel.config.HIGH_BEAM:
      self.high_beam.pressed = value
    elif button == Wheel.config.WINDSHIELD_WIPER:
      self.windshield_wiper.pressed = value
    else:
      print "button not configured", button


  def loop(self):
    """process event coming from G27

    Exit the loop by hitting the Escape key
    """
    clock = pygame.time.Clock()
    keep_going = True
    while keep_going:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          keep_going = False
        if event.type == pygame.JOYAXISMOTION:
          if event.axis == Wheel.config.STEERING_WHEEL:
            self.handle_steering_wheel(event.value)
          else:
            self.handle_pedal(event.axis, event.value)
        elif event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
          if self.is_gear_button(event.button):
            self.handle_gear_shift(event.button if event.type == pygame.JOYBUTTONDOWN else 0)
          else:
            self.handle_button(event.button, (event.type == pygame.JOYBUTTONDOWN))
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            print "ESC pressed => quitting"
            pygame.event.post(pygame.event.Event(pygame.QUIT))
      clock.tick(100)

