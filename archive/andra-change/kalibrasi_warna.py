# Mengukur warna dinding (merah, hijau, kuning) untuk sensor warna dinding (port C).
#
# Cara pakai:
# 1. Jalankan program ini. Robot tidak bergerak.
# 2. Saat diminta, arahkan sensor ke dinding warna yang disebut, pada jarak
#    yang sama dengan jarak robot berhenti di lintasan (sekitar WALL_MM di main.py),
#    dengan cahaya ruangan yang sama dengan saat lomba.
# 3. Tekan tombol tengah hub. Tunggu bunyi bip, lalu pindah ke warna berikutnya.
# 4. Salin tiga baris MERAH, HIJAU, KUNING yang tercetak ke perangkat.py,
#    menggantikan tiga baris dengan nama yang sama.

from math import sin, cos, atan2, radians, degrees

from pybricks.parameters import Button
from pybricks.tools import wait

from perangkat import hub, wall_sensor

SAMPLES = 50   # jumlah pembacaan per warna
GAP = 20       # jeda antar pembacaan (ms)


def tunggu_tombol():
    while Button.LEFT not in hub.buttons.pressed():
        wait(10)
    while Button.LEFT in hub.buttons.pressed():
        wait(10)
    wait(300)


def ukur():
    # Rata-rata hue memakai rata-rata lingkaran, karena merah berada di
    # sekitar 0 / 360 derajat dan rata-rata biasa akan salah.
    sx = 0
    sy = 0
    total_s = 0
    total_v = 0
    for i in range(SAMPLES):
        c = wall_sensor.hsv()
        sx += cos(radians(c.h))
        sy += sin(radians(c.h))
        total_s += c.s
        total_v += c.v
        wait(GAP)
    h = int(degrees(atan2(sy, sx))) % 360
    s = int(total_s / SAMPLES)
    v = int(total_v / SAMPLES)
    return h, s, v


def selisih_hue(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


hasil = {}

for nama in ("MERAH", "HIJAU", "KUNING"):
    print("Arahkan sensor ke dinding", nama, "lalu tekan tombol kiri.")
    tunggu_tombol()
    h, s, v = ukur()
    hasil[nama] = (h, s, v)
    hub.speaker.beep(800, 200)
    print(nama, "terukur: H =", h, "S =", s, "V =", v)

print("")
print("Salin ke perangkat.py:")
for nama in ("RED", "GREEN", "YELLOW"):
    h, s, v = hasil[nama]
    print(nama, "= Color(" + str(h) + ",", str(s) + ",", str(v) + ")")

# Peringatan jika dua warna terlalu mirip.
pasangan = (("MERAH", "KUNING"), ("KUNING", "HIJAU"), ("MERAH", "HIJAU"))
for a, b in pasangan:
    d = selisih_hue(hasil[a][0], hasil[b][0])
    if d < 25:
        print("Peringatan:", a, "dan", b, "hanya beda hue", d, "derajat.")
        print("Dekatkan sensor ke dinding atau atur ulang pencahayaan, lalu ulangi.")