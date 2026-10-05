from pybricks.tools import wait
from pybricks.parameters import Icon

from perangkat import hub, robot, line_sensor, wall_sensor, distance_sensor

# --- hasil pengukuran, ukur ulang dengan kalibrasi.py setiap ganti lintasan atau ruangan ---
BLACK = 3
WHITE = 32

# Kecepatan
BASE_SPEED = 300
MIN_SPEED = 60
BACKUP_SPEED = -100

# PID
KP = 1.0 #1.6 
KD = 3.0

# Timing
BACKUP_MS = 100 #200
LOOP_MS = 10
LOST_MS = 200 #300

# Jarak Tembok
WALL_MM_DETECT_1 = 100
WALL_MM_DETECT_2 = 80

# Threshold Warna
MIN_YELLOW_HUE = 30
MAX_YELLOW_HUE = 50
MIN_GREEN_HUE = 140
MAX_GREEN_HUE = 160
MIN_RED_HUE = 340
MAX_RED_HUE = 360

# 1 kiri, 0 kanan
YELLOW_TURN_LEFT = 1

THRESHOLD = (BLACK + WHITE) / 2
SCALE = 200 / (WHITE - BLACK)

last_error = 0
lost_time = 0

hub.display.icon(Icon.HAPPY)

def detect_color():
    detected_color = None
    hsv = wall_sensor.hsv()
    h = hsv.h

    if MIN_YELLOW_HUE <= h <= MAX_YELLOW_HUE:
        detected_color = 'YELLOW'
    elif MIN_GREEN_HUE <= h <= MAX_GREEN_HUE:
        detected_color = 'GREEN'
    elif (MIN_RED_HUE < h <= MAX_RED_HUE):
        detected_color = 'RED'

    return detected_color

while True:

    # ===== wall detector ======

    if WALL_MM_DETECT_2 < distance_sensor.distance() < WALL_MM_DETECT_1:
        robot.stop()
        detected_color = detect_color()
        
        # jika deteksi pertama gagal, coba deteksi kedua yang lebih dekat
        if not detected_color:
            robot.drive(MIN_SPEED, 0)
            if distance_sensor.distance() < WALL_MM_DETECT_2:
                robot.stop()
                detected_color = detect_color()

        # jika deteksi kedua gagal, maka skip tembok
        if not detected_color:
            hub.speaker.beep(300, 200)
            hub.display.icon(Icon.FALSE)
            print('undefined')
            continue

        # negatif = kiri, positif = kanan
        if detected_color == 'YELLOW':
            hub.speaker.beep(1200, 200)
            if YELLOW_TURN_LEFT:
                hub.display.icon(Icon.ARROW_LEFT)
                direction = -90
                print('left yellow')
            else:
                hub.display.icon(Icon.ARROW_RIGHT)
                direction = 90
                print('right yellow')

        elif detected_color == 'GREEN':
            hub.speaker.beep(900, 200)
            hub.display.icon(Icon.ARROW_RIGHT)
            direction = 90
            print('green')

        elif detected_color == 'RED':
            hub.speaker.beep(600, 200)
            hub.display.icon(Icon.ARROW_LEFT)
            direction = -90
            print('red')
        
        robot.turn(direction)
        hub.display.icon(Icon.HAPPY)

        last_error = 0
        lost_time = 0

    # ==========================


    # ===== line follower ======

    if YELLOW_TURN_LEFT:
        error = (line_sensor.reflection() - THRESHOLD) * SCALE
    else:
        error = (THRESHOLD - line_sensor.reflection()) * SCALE

    if error > 80:
        lost_time = lost_time + LOOP_MS
    else:
        lost_time = 0

    if lost_time > (LOST_MS + BACKUP_MS):
        # Garis hilang: mundur ke arah garis terakhir terlihat.
        robot.drive(BACKUP_SPEED, 0)
    elif lost_time > LOST_MS:
        # Garis hilang: berputar ke arah garis terakhir terlihat.
        robot.drive(0, 90 if last_error > 0 else -90)
    else:
        derivative = error - last_error
        speed = BASE_SPEED - (BASE_SPEED - MIN_SPEED) * abs(error) / 100
        robot.drive(speed, KP * error + KD * derivative)
        last_error = error

    # ==========================

    wait(LOOP_MS)