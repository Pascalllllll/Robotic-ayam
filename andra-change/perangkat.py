# Blok setup robot. Dipakai bersama oleh main.py dan kalibrasi.py,
# jadi port dan ukuran roda cukup diubah di satu tempat ini.

from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.robotics import DriveBase

hub = InventorHub()
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A, Direction.CLOCKWISE)
line_sensor = ColorSensor(Port.C)
wall_sensor = ColorSensor(Port.E)
distance_sensor = UltrasonicSensor(Port.F)

# --- hasil pengukuran, ganti dengan hasil kalibrasi_warna.py ---

# RED = Color.RED
# GREEN = Color.GREEN
# YELLOW = Color.YELLOW

RED = Color(337)
GREEN = Color(135)
YELLOW = Color(10)

# Batasi warna yang dikenali supaya merah/hijau/kuning tidak tertukar dengan warna lain.
wall_sensor.detectable_colors([RED, GREEN, YELLOW, Color.NONE])

# Ganti dengan hasil kalibrasi robot kalian sendiri,
# lihat bagian 8 dasar-pybricks.md.
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=80)