# Blok setup robot. Dipakai bersama oleh main.py dan kalibrasi.py,
# jadi port dan ukuran roda cukup diubah di satu tempat ini.

from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

hub = InventorHub()
left = Motor(Port.E, Direction.COUNTERCLOCKWISE)
right = Motor(Port.F, Direction.CLOCKWISE)
sensor = ColorSensor(Port.D)

# Ganti dengan hasil kalibrasi robot kalian sendiri,
# lihat bagian 8 dasar-pybricks.md.
robot = DriveBase(left, right, wheel_diameter=56, axle_track=114)
