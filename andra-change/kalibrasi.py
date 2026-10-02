from pybricks.tools import wait
from pybricks.parameters import Button, Color
from perangkat import hub, line_sensor

def ambil_sampel_stabil(jumlah=30):
    sampel = []
    for _ in range(jumlah):
        sampel.append(line_sensor.reflection())
        wait(15)
    sampel.sort()
    tengah = sampel[4:-4]
    return round(sum(tengah) / len(tengah))

print("\n" + "=" * 55)
print("     KALIBRASI SENSOR GARIS (PORT C)")
print("=" * 55)

print("\n[LANGKAH 1]: Letakkan sensor Port C tepat di atas GARIS HITAM.")
print("             Perhatikan angka Live, lalu tekan [TOMBOL KIRI <].")

hub.light.on(Color.BLUE)

while True:
    pressed = hub.buttons.pressed()
    if Button.LEFT in pressed:
        break
    live_val = line_sensor.reflection()
    bar = "#" * (live_val // 5)
    print(f"\r  >> Live Sensor: {live_val:3d}% [{bar:<20s}] (Arahkan ke HITAM)", end="")
    wait(80)

print(f"\n  [+] Sedang merekam data warna HITAM...")
try:
    hub.speaker.beep(frequency=500, duration=100)
except Exception:
    pass

black_val = ambil_sampel_stabil(30)
print(f"  [OK] Nilai BLACK tersimpan: {black_val}%\n")
wait(600)

print("[LANGKAH 2]: Pindahkan sensor Port C ke atas LANTAI PUTIH.")
print("             Perhatikan angka Live, lalu tekan [TOMBOL KANAN >].")

hub.light.on(Color.YELLOW)

while True:
    pressed = hub.buttons.pressed()
    if Button.RIGHT in pressed:
        break
    live_val = line_sensor.reflection()
    bar = "#" * (live_val // 5)
    print(f"\r  >> Live Sensor: {live_val:3d}% [{bar:<20s}] (Arahkan ke PUTIH)", end="")
    wait(80)

print(f"\n  [+] Sedang merekam data warna PUTIH...")
try:
    hub.speaker.beep(frequency=900, duration=100)
except Exception:
    pass

white_val = ambil_sampel_stabil(30)
print(f"  [OK] Nilai WHITE tersimpan: {white_val}%\n")
wait(400)

threshold = (black_val + white_val) / 2
kontras = white_val - black_val

hub.light.on(Color.GREEN)
try:
    hub.speaker.beep(frequency=880, duration=120)
    wait(80)
    hub.speaker.beep(frequency=1175, duration=180)
except Exception:
    pass

print("=" * 55)
print("              HASIL AKHIR KALIBRASI")
print("=" * 55)
print(f"BLACK     = {black_val}")
print(f"WHITE     = {white_val}")
print(f"THRESHOLD = {threshold:.1f}")
print(f"KONTRAS   = {kontras}%")
print("-" * 55)

if kontras >= 40:
    print("[STATUS]: Kontras SANGAT BAGUS (>= 40%).")
elif 25 <= kontras < 40:
    print("[STATUS]: Kontras CUKUP (25% - 39%).")
else:
    print("[PERINGATAN]: Kontras TERLALU RENDAH (< 25%). Dekatkan sensor ke lantai.")

print("\n" + "=" * 55)
print(">>> Salin dua baris ini ke baris 6-7 di main.py:")
print("=" * 55)
print(f"BLACK = {black_val}")
print(f"WHITE = {white_val}")
print("=" * 55 + "\n")