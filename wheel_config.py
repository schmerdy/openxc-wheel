WHEEL_NAME = "G27 Racing Wheel"
STEERING_WHEEL = 0
ACCELERATOR = 1
BRAKE = 2
CLUTCH = 3

GEAR_1 = 12
GEAR_2 = 13
GEAR_3 = 14
GEAR_4 = 15
GEAR_5 = 16
GEAR_6 = 17
GEAR_REVERSE = 22

IGNITION = 11
PARKING_BRAKE = 10
HEADLAMP = 1
HIGH_BEAM = 3
WINDSHIELD_WIPER = 2

STEERING_WHEEL_TOLERANCE = 10
PEDAL_TOLERANCE = 5

class WheelConfig:

  WHEEL_NAME = "G27 Racing Wheel"

  STEERING_WHEEL_AXIS = 0
  ACCELERATOR_PEDAL_AXIS = 1 
  BRAKE_PEDAL_AXIS = 2
  CLUTCH_PEDAL_AXIS = 3

  GEAR_BUTTON_OFFSET = 11 # 1st gear: 12, 2nd gear: 13, ...
  NUMBER_OF_GEARS = 6
  GEAR_REVERSE_BUTTON = 22

  IGNITION_BUTTON = 11
  PARKING_BRAKE_BUTTON = 10
  HEADLAMP_BUTTON = 1
  HIGH_BEAM_BUTTON = 3
  WINDSHIELD_WIPER_BUTTON = 2

  def is_gear_lever(self,button):
    return (button - WheelConfig.GEAR_BUTTON_OFFSET in range(1, WheelConfig.NUMBER_OF_GEARS+1) or 
      button == WheelConfig.GEAR_REVERSE_BUTTON)

  def get_gear_from_button(self, button):
    # returns None when the button is not a gear shift button
    # -1 for reverse gear, gear otherwise
    if button == WheelConfig.GEAR_REVERSE_BUTTON:
      return -1
    if self.is_gear_lever(button):
      return button - WheelConfig.GEAR_BUTTON_OFFSET
    return None

  def get_steering_Wheel_angle(self, val):
    # pygame returns a value between -1 and 1 for every axis
    # openxc-vehicle-simulator expects a value between -600 and 600
    if val > 1:
      return 600
    if val < -1:
      return -600
    return val * 600

  def get_pedal_percentage(self, pedal, val):
    # pygame returns a value between -1 (fully pressed) and 1 (not pressed) for every axis
    # openxc-vehicle-simulator expects a percentage value between 0 and 100
    if pedal not in (WheelConfig.ACCELERATOR_PEDAL_AXIS, WheelConfig.BRAKE_PEDAL_AXIS, WheelConfig.CLUTCH_PEDAL_AXIS):
      return None
    if val > 1:
      return 0
    if val < -1:
      return 100
    return (1 - val) * 50


