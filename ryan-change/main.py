from pybricks.tools import wait, StopWatch

from perangkat import hub, robot, sensor, sensor_dinding, jarak, MERAH, HIJAU, KUNING

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

# --- setelan dinding ---
WALL_MM = 150        # jarak (mm) saat dinding dianggap di depan; sesuaikan agar sensor warna bisa membaca
MUNDUR_MM = 40      # mundur (mm) setelah warna terbaca, sebelum belok
MIN_MM = 30         # jarak terdekat (mm) ke dinding saat merayap membaca warna
CREEP_SPEED = 30    # kecepatan merayap mendekati dinding (mm/s)
READ_MS = 1500      # batas waktu merayap untuk membaca warna
COOLDOWN_MS = 1500  # setelah warna gagal dikenali, abaikan dinding selama ini
SEEK_SPEED = 60     # kecepatan maju pelan saat mencari garis setelah belok (mm/s)
SEEK_MS = 2000      # batas waktu mencari garis setelah belok

THRESHOLD = (BLACK + WHITE) / 2
SCALE = 200 / (WHITE - BLACK)

last_error = 0
lost_time = 0


def cari_garis():
    # Maju pelan sampai sensor garis menyentuh garis (gelap), atau waktu habis.
    timer = StopWatch()
    robot.drive(SEEK_SPEED, 0)
    while sensor.reflection() > THRESHOLD and timer.time() < SEEK_MS:
        wait(LOOP_MS)
    robot.stop()


def baca_warna():
    # Merayap pelan ke arah dinding sampai warna dikenali, jarak sudah
    # terlalu dekat (MIN_MM), atau waktu habis. Lalu berhenti.
    timer = StopWatch()
    robot.drive(CREEP_SPEED, 0)
    warna = sensor_dinding.color()
    while warna not in (MERAH, HIJAU, KUNING):
        if jarak.distance() <= MIN_MM or timer.time() > READ_MS:
            break
        wait(LOOP_MS)
        warna = sensor_dinding.color()
    robot.stop()
    return warna


def tangani_dinding():
    # Berhenti, baca warna dinding, belok, lalu kembali ke garis.
    # Mengembalikan True jika dinding dikenali dan robot sudah belok.
    robot.stop()
    wait(100)
    warna = baca_warna()
    print("Warna dinding:", warna, "HSV:", sensor_dinding.hsv())

    if warna == MERAH:
        hub.speaker.beep(400, 200)    # nada rendah = merah
        arah = -70        # negatif = kiri
    elif warna == HIJAU:
        hub.speaker.beep(800, 200)    # nada sedang = hijau
        arah = 70         # positif = kanan
    elif warna == KUNING:
        hub.speaker.beep(1200, 200)   # nada tinggi = kuning
        arah = -70
    else:
        # hub.speaker.beep(200, 400)    # nada sangat rendah = warna tidak dikenali
        # robot.straight(-MUNDUR_MM)
        return False

    robot.straight(-MUNDUR_MM)   # mundur sedikit agar ada ruang untuk belok
    robot.turn(arah)
    cari_garis()
    return True


cooldown = StopWatch()

while True:
    # Dinding di depan: baca warna, belok sesuai aturan, kembali ke garis.
    # Setelah gagal membaca warna, dinding diabaikan sebentar (COOLDOWN_MS)
    # supaya robot tidak berhenti-jalan terus di tempat yang sama.
    if jarak.distance() < WALL_MM and cooldown.time() > COOLDOWN_MS:
        if tangani_dinding():
            last_error = 0
            lost_time = 0
        else:
            cooldown.reset()
            last_error = 0
            lost_time = 0
        continue

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