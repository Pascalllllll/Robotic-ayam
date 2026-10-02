# Blok setup robot. Dipakai bersama oleh main.py dan kalibrasi.py,
# jadi port dan ukuran roda cukup diubah di satu tempat ini.

from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.robotics import DriveBase

hub = InventorHub()
left = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right = Motor(Port.A, Direction.CLOCKWISE)
sensor = ColorSensor(Port.C)
sensor_dinding = ColorSensor(Port.E)
jarak = UltrasonicSensor(Port.F)

# --- hasil pengukuran, ganti dengan hasil kalibrasi_warna.py ---
# Nilai awal di bawah masih warna bawaan Pybricks.
MERAH = Color(352, 88, 29)
HIJAU = Color(133, 53, 11)
KUNING = Color(29, 67, 32)

# Batasi warna yang dikenali supaya merah/hijau/kuning tidak tertukar
# dengan warna lain.
sensor_dinding.detectable_colors([MERAH, HIJAU, KUNING, Color.NONE])

# Ganti dengan hasil kalibrasi robot kalian sendiri,
# lihat bagian 8 dasar-pybricks.md.
robot = DriveBase(left, right, wheel_diameter=56, axle_track=114)