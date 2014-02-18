### test class to define wheel API
import wheel

def handle_accelerator(val):
  print "Accelerator", val
def handle_brake(val):
  print "Brake", val
def handle_clutch(val):
  print "Clutch", val

def on_angle(val):
  print "Steering Wheel Angle:", val

def on_ignition(pressed):
  print("ignition on" if pressed else "ignition off")
def on_parking_brake(pressed):
  print("handbrake on" if pressed else "handbrake off")
def on_headlamp(pressed):
  print("lights on" if pressed else "lights off")
def on_high_beam(pressed):
  print("highbeam on" if pressed else "highbeam off")
def on_windshied_wiper(pressed):
  print("wipers on" if pressed else "wipers off")

def on_gear_shift(gear):
  print gear, "gear"

g27 = wheel.Wheel()

g27.register_steering_wheel(on_angle)
g27.register_pedal(g27.config.ACCELERATOR, handle_accelerator)
g27.register_pedal(g27.config.BRAKE, handle_brake)
g27.register_pedal(g27.config.CLUTCH, handle_clutch)
g27.register_button(g27.config.IGNITION, on_ignition)
g27.register_button(g27.config.PARKING_BRAKE, on_parking_brake)
g27.register_button(g27.config.HEADLAMP, on_headlamp)
g27.register_button(g27.config.HIGH_BEAM, on_high_beam)
g27.register_button(g27.config.WINDSHIELD_WIPER, on_windshied_wiper)
g27.register_gear_shift(on_gear_shift)

print(g27.steering_wheel.angle)
g27.steering_wheel.angle = 0
print(g27.steering_wheel.angle)
g27.steering_wheel.angle = 0.001
print(g27.steering_wheel.angle)
g27.steering_wheel.angle = 0.05
print(g27.steering_wheel.angle)
g27.accelerator.state = -0.2
print(g27.accelerator.state)
g27.gear_shift.gear = 1
g27.parking_brake.pressed = False
g27.gear_shift.gear = 0
g27.gear_shift.gear = 2
g27.gear_shift.gear = 0
g27.parking_brake.pressed = True

g27.loop()



