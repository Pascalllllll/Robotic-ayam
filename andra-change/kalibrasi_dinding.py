# ========================================================
# SCRIPT INTERAKTIF KALIBRASI WARNA DINDING (PORT D)
# ========================================================
# Cara Pakai:
# 1. Dekatkan sensor Port D ke kertas dinding (jarak 2-3 cm).
# 2. Tekan Tombol KANAN di Hub untuk merekam warna:
#    - Rekam 1: Kertas MERAH
#    - Rekam 2: Kertas KUNING
#    - Rekam 3: Kertas HIJAU
# 3. Hasil rentang Hue akan otomatis dicetak untuk main.py.
# ========================================================

from pybricks.tools import wait
from pybricks.parameters import Color, Button
from perangkat import hub, wall_sensor

if wall_sensor is None:
    print("[ERROR] Sensor warna di Port D tidak ditemukan! Cek kabel.")
    while True:
        wait(1000)

TARGET_WARNA = ["MERAH", "KUNING", "HIJAU"]
hasil_kalibrasi = {}

def ambil_sampel_hsv(jumlah=20):
    """Mengambil beberapa sampel untuk mencari min, max, dan rata-rata."""
    h_list = []
    s_list = []
    v_list = []
    
    for _ in range(jumlah):
        hsv = wall_sensor.hsv()
        h_list.append(hsv.h)
        s_list.append(hsv.s)
        v_list.append(hsv.v)
        wait(25)
    
    h_list.sort()
    # Mengambil nilai tengah/median dan rentang
    h_min = min(h_list)
    h_max = max(h_list)
    h_med = h_list[len(h_list) // 2]
    s_med = sum(s_list) // len(s_list)
    v_med = sum(v_list) // len(v_list)
    
    return h_min, h_max, h_med, s_med, v_med

print("\n" + "=" * 45)
print("     KALIBRASI WARNA DINDING (PORT D)")
print("=" * 45)

for warna in TARGET_WARNA:
    if warna == "MERAH":
        hub.light.on(Color.RED)
    elif warna == "KUNING":
        hub.light.on(Color.YELLOW)
    elif warna == "HIJAU":
        hub.light.on(Color.GREEN)
        
    print(f"\n>>> Arahkan sensor ke kertas [{warna}] (jarak 2-3 cm).")
    print("    Tekan [TOMBOL KANAN] di Hub jika sudah siap...")
    
    # Tunggu tombol kanan ditekan
    while True:
        pressed = hub.buttons.pressed()
        if Button.RIGHT in pressed:
            break
        # Tampilkan live preview nilai Hue saat ini
        live_hsv = wall_sensor.hsv()
        print(f"\rLive -> H: {live_hsv.h:3d} | S: {live_hsv.s:3d}% | V: {live_hsv.v:3d}%", end="")
        wait(150)
    
    # Bunyi beep tanda merekam
    try:
        hub.speaker.beep(frequency=700, duration=80)
    except Exception:
        pass
    
    print(f"\n[+] Sedang merekam data warna {warna}...")
    h_min, h_max, h_med, s_med, v_med = ambil_sampel_hsv(25)
    
    hasil_kalibrasi[warna] = {
        "min": h_min,
        "max": h_max,
        "med": h_med,
        "s": s_med,
        "v": v_med
    }
    
    print(f"    Selesai! Rentang Hue {warna}: {h_min} s/d {h_max} (Median: {h_med})")
    wait(600)  # Debounce tombol

# Tanda selesai semua warna
hub.light.on(Color.WHITE)
try:
    hub.speaker.beep(frequency=1000, duration=150)
    wait(100)
    hub.speaker.beep(frequency=1200, duration=200)
except Exception:
    pass

# ========================================================
# REKOMENDASI KODE UNTUK main.py
# ========================================================
print("\n" + "=" * 50)
print("             HASIL KALIBRASI WARNA")
print("=" * 50)
for w, d in hasil_kalibrasi.items():
    print(f"{w:7s} -> H-Min: {d['min']:3d} | H-Max: {d['max']:3d} | Median: {d['med']:3d} (Sat: {d['s']}%, Val: {d['v']}%)")

print("\n" + "-" * 50)
print("Salin fungsi ini ke dalam main.py kamu:")
print("-" * 50)

h_merah = hasil_kalibrasi["MERAH"]["med"]
h_kuning = hasil_kalibrasi["KUNING"]["med"]
h_hijau = hasil_kalibrasi["HIJAU"]["med"]

# Tentukan batas ambang (threshold) tengah antar warna
ambang_mk = (h_merah + h_kuning) // 2 if h_merah < h_kuning else 25
ambang_kh = (h_kuning + h_hijau) // 2

kode_rekomendasi = f"""def deteksi_warna_dinding():
    \"\"\"Membaca warna dinding hasil kalibrasi Port D.\"\"\"
    if wall_sensor is None:
        return Color.YELLOW

    samples = []
    for _ in range(5):
        samples.append(wall_sensor.hsv().h)
        wait(15)
    samples.sort()
    h = samples[2]  # Median

    print(f"[PORT D] Hue Terbaca: {{h}}")

    # Nilai batas berdasarkan kalibrasi:
    if h >= 340 or h <= {ambang_mk}:
        return Color.RED
    elif {ambang_mk + 1} <= h <= {ambang_kh}:
        return Color.YELLOW
    elif {ambang_kh + 1} <= h <= 200:
        return Color.GREEN
    else:
        return Color.YELLOW"""

print(kode_rekomendasi)
print("=" * 50 + "\n")