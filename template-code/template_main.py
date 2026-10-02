# Pengikut garis PD dengan kecepatan adaptif dan pencarian garis hilang.
# Penjelasan setiap bagian ada di pengikut-garis.md.

from pybricks.tools import wait

from template_perangkat import robot, sensor

# --- hasil pengukuran, ukur ulang dengan kalibrasi.py setiap ganti lintasan atau ruangan ---
BLACK = 9
WHITE = 85

# --- setelan, setel satu per satu ---
BASE_SPEED = 150
MIN_SPEED = 60
KP = 0.8
KD = 3.0
LOOP_MS = 10
LOST_MS = 300

THRESHOLD = (BLACK + WHITE) / 2
SCALE = 200 / (WHITE - BLACK)

last_error = 0
lost_time = 0

while True:
    # Tantangan dinding berwarna ditambahkan di sini:
    # cek dinding di depan, baca warnanya, lalu belok sesuai aturan,
    # dan kembali ke garis sebelum loop berlanjut.

    error = (sensor.reflection() - THRESHOLD) * SCALE

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

    wait(LOOP_MS)
