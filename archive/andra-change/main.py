from pybricks.tools import wait
from pybricks.parameters import Icon

from perangkat import hub, robot, line_sensor, wall_sensor, distance_sensor, RED, GREEN, YELLOW

# --- hasil pengukuran, ukur ulang dengan kalibrasi.py setiap ganti lintasan atau ruangan ---
BLACK = 3
WHITE = 32

# --- Speed ---
BASE_SPEED = 200
MIN_SPEED = 60
BACKUP_SPEED = -100

# --- PID ---
KP = 1.6
KD = 3.0

# --- Timing ---
BACKUP_MS = 200
LOOP_MS = 10
LOST_MS = 300

# --- Wall detection ---
WALL_MM_SLOW = 120
WALL_MM_DETECT = 80

# 1 kiri, 0 kanan
YELLOW_TURN_LEFT = 0

THRESHOLD = (BLACK + WHITE) / 2
SCALE = 200 / (WHITE - BLACK)

last_error = 0
lost_time = 0

hub.display.icon(Icon.HAPPY)

while True:

    # ===== wall detection ======

    if distance_sensor.distance() < WALL_MM_SLOW:
        while distance_sensor.distance() > WALL_MM_DETECT:
            robot.drive(MIN_SPEED, 0)
            wait(LOOP_MS)

        robot.stop()
        wait(500) 
        robot.drive(MIN_SPEED/2, 0)

        detected_color = None
        while True:
            hsv = wall_sensor.hsv()
            h = hsv.h

            if 30 <= h <= 50:
                detected_color = 'YELLOW'
                break
            elif 140 <= h <= 160:
                detected_color = 'GREEN'
                break
            elif (340 < h <= 360):
                detected_color = 'RED'
                break

            wait(LOOP_MS)
        
        robot.stop()

        # negatif = kiri, positif = kanan
        if detected_color == 'YELLOW':
            hub.speaker.beep(1200, 200)
            if YELLOW_TURN_LEFT:
                hub.display.icon(Icon.ARROW_LEFT)
                direction = -90
                print('kuning kiri')
            else:
                hub.display.icon(Icon.ARROW_RIGHT)
                direction = 90
                print('kuning kanan')

        elif detected_color == 'GREEN':
            hub.speaker.beep(800, 200)
            hub.display.icon(Icon.ARROW_RIGHT)
            direction = 90
            print('green')

        elif detected_color == 'RED':
            hub.speaker.beep(400, 200)
            hub.display.icon(Icon.ARROW_LEFT)
            direction = -90
            print('red')
        
        robot.turn(direction)
        hub.display.icon(Icon.HAPPY)

        last_error = 0
        lost_time = 0

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

    if lost_time > (LOST_MS + BACKUP_MS):
        # Garis hilang: berputar ke arah garis terakhir terlihat.
        robot.drive(0, 90 if last_error > 0 else -90)
    elif lost_time > LOST_MS:
        # Garis hilang: mundur dulu, baru berputar ke arah garis terakhir terlihat.
        robot.drive(BACKUP_SPEED, 0)
    else:
        derivative = error - last_error
        speed = BASE_SPEED - (BASE_SPEED - MIN_SPEED) * abs(error) / 100
        robot.drive(speed, KP * error + KD * derivative)
        last_error = error

    # ===========================

    wait(LOOP_MS)