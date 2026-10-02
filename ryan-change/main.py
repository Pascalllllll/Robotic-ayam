from pybricks.tools import wait
from pybricks.parameters import Icon

from perangkat import hub, robot, line_sensor, wall_sensor, distance_sensor, RED, GREEN, YELLOW

# --- hasil pengukuran, ukur ulang dengan kalibrasi.py setiap ganti lintasan atau ruangan ---
BLACK = 5
WHITE = 40

# --- setelan, setel satu per satu ---
BASE_SPEED = 150
MIN_SPEED = 60
KP = 0.8
KD = 3.0
LOOP_MS = 10
LOST_MS = 300
WALL_MM = 80

# 1 kiri, 0 kanan
YELLOW_TURN_LEFT = 1

THRESHOLD = (BLACK + WHITE) / 2
SCALE = 200 / (WHITE - BLACK)

last_error = 0
lost_time = 0

hub.display.icon(Icon.HAPPY)

while True:

    # ===== wall detection ======

    if distance_sensor.distance() < WALL_MM:
        robot.drive(MIN_SPEED / 2, 0)
        
        color = wall_sensor.color()
        while color not in (RED, GREEN, YELLOW):
            wait(LOOP_MS)
            color = wall_sensor.color()
        robot.stop()

        # negatif = kiri, positif = kanan
        if color == RED:
            hub.display.icon(Icon.ARROW_LEFT)
            hub.speaker.beep(400, 200)
            direction = -90
        elif color == GREEN:
            hub.display.icon(Icon.ARROW_RIGHT)
            hub.speaker.beep(800, 200)
            direction = 90
        elif color == YELLOW:
            hub.speaker.beep(1200, 200)
            if YELLOW_TURN_LEFT:
                hub.display.icon(Icon.ARROW_LEFT)
                direction = -90
            else:
                hub.display.icon(Icon.ARROW_RIGHT)
                direction = 90

        robot.turn(direction)
        hub.display.icon(Icon.HAPPY)

    # ===========================


    # ===== line following ======

    if YELLOW_TURN_LEFT:
        error = (line_sensor.reflection() - THRESHOLD) * SCALE
    else:
        error = (THRESHOLD - line_sensor.reflection()) * SCALE

    if error > 80:
        lost_time = lost_time + LOOP_MS
    else:
        lost_time = 0

    if lost_time > LOST_MS:
        # Garis hilang: berputar ke arah garis terakhir terlihat.
        robot.drive(0, 90 if last_error > 0 else -90)
    else:
        derivative = error - last_error
        speed = BASE_SPEED - (BASE_SPEED - MIN_SPEED) * abs(error) / 100
        robot.drive(speed, KP * error + KD * derivative)
        last_error = error

    # ===========================

    wait(LOOP_MS)