# Tes di skrip terpisah atau jalankan sementara
from perangkat import wall_sensor, distance_sensor
from pybricks.tools import wait

lost_time = 0
while True:
    print("HSV:", wall_sensor.hsv())
    print(f"tembok: {distance_sensor.distance()}")
    lost_time += 10
    print(lost_time)
    wait(300)