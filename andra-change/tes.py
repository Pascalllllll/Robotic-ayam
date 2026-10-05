# Tes di skrip terpisah atau jalankan sementara
from perangkat import wall_sensor
from pybricks.tools import wait

while True:
    print("HSV:", wall_sensor.hsv())
    wait(300)