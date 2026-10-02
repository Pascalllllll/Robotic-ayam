from pybricks.tools import wait
from pybricks.parameters import Color
from perangkat import hub, robot, line_sensor, wall_sensor, eyes

BLACK = 10
WHITE = 96

THRESHOLD = (BLACK + WHITE) / 2
SCALE = 200 / max((WHITE - BLACK), 1)

SPEED = 65
KP = 0.75
KD = 1.0
MAX_TURN = 90
KEBALIKAN = True

WALL_DISTANCE_MM = 100
BACKUP_DISTANCE = -50

LOOP_MS = 10
last_error = 0

def cek_dinding():
    try:
        dist = eyes.distance()
        if dist is not None and 10 < dist <= WALL_DISTANCE_MM:
            return True
    except Exception:
        pass
    return False

def deteksi_warna_dinding():
    samples = []
    for _ in range(5):
        hsv = wall_sensor.hsv()
        samples.append(hsv.h)
        wait(15)
    samples.sort()
    h = samples[2]

    print(f"[PORT E] Hue Terbaca: {h}")

    if h >= 340 or h <= 25:
        return Color.RED
    elif 26 <= h <= 88:
        return Color.YELLOW
    elif 92 <= h <= 190:
        return Color.GREEN
    else:
        if h < 26 or h > 280:
            return Color.RED
        elif h < 90:
            return Color.YELLOW
        else:
            return Color.GREEN

def handle_dinding():
    robot.stop()
    wait(150)

    warna = deteksi_warna_dinding()
    print("-> Dinding Terdeteksi! Warna:", warna)

    if warna in (Color.RED, Color.GREEN, Color.YELLOW):
        hub.light.on(warna)

    try:
        if warna == Color.RED:
            hub.speaker.beep(frequency=440, duration=150)
        elif warna == Color.GREEN:
            hub.speaker.beep(frequency=880, duration=150)
        elif warna == Color.YELLOW:
            hub.speaker.beep(frequency=660, duration=150)
    except Exception:
        pass

    if warna == Color.GREEN:
        print("[AKSI] Hijau: Mundur sedikit -> Belok Kanan")
        robot.straight(BACKUP_DISTANCE)
        robot.turn(90)

    elif warna == Color.RED:
        print("[AKSI] Merah: Mundur sedikit -> Belok Kiri")
        robot.straight(BACKUP_DISTANCE)
        robot.turn(-90)

    elif warna == Color.YELLOW:
        print("[AKSI] Kuning: Mundur sedikit -> Belok Kanan")
        robot.straight(BACKUP_DISTANCE)
        robot.turn(90)

    else:
        robot.straight(BACKUP_DISTANCE)
        robot.turn(90)

    hub.light.on(Color.WHITE)
    robot.straight(40)

hub.light.on(Color.GREEN)
wait(1000)

while True:
    if cek_dinding():
        handle_dinding()
        last_error = 0
        continue

    val = line_sensor.reflection()
    error = (val - THRESHOLD) * SCALE

    if KEBALIKAN:
        error = -error

    derivative = error - last_error
    turn_rate = (KP * error) + (KD * derivative)

    if turn_rate > MAX_TURN:
        turn_rate = MAX_TURN
    elif turn_rate < -MAX_TURN:
        turn_rate = -MAX_TURN

    robot.drive(SPEED, turn_rate)

    last_error = error
    wait(LOOP_MS)