# openxc-wheel

Use to control the OpenXC vehicle simulator (http://openxcplatform.com/projects/simulator.html) from a Logitech G27 steering wheel.

## Requirements

Written on Python 2.7.2, uses the pygame library to connect to the steering wheel. If you use the pip package manager, simply run 

*pip install -r pip-requirements.txt*

from the project directory. Otherwise install the latest pygame version (written on 1.9.2pre) before using the script
The Logitech wheel only shows 2 axis (steering wheel and accelerator/brake combined) in Linux by default and it also
does not show the gear shift. To get it fully functional, the wheel needs to be put in "native" mode.
For Linux, you can use LTWheelConf from the pip_requirements file. Follow the instructions in 
http://euro-truck-simulator-2.wikia.com/wiki/How_to_get_Logitech_steering_wheels_working_properly_on_Ubuntu_(G25/G27/DF/DFP/DFGT/MF/MR).


You also need the OpenXC vehicle simulator, get it from https://github.com/openxc/openxc-vehicle-simulator


## Usage

- Start the vehicle simulator by running python emulate.py from the openxc-vehicle-simulator directory
- Connect the G27 to via USB
- Run python control.py
- Press the left-most red button on the gearshift to start the engine
- Use gas and break pedal and the steering wheel to send events to the emulator

