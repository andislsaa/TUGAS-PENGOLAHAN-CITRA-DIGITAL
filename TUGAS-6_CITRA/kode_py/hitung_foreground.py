import cv2
import os
import csv

# ==========================================
# KONFIGURASI
# ==========================================

INPUT_FOLDER = "hasil_morphology/opening_closing"
OUTPUT_FILE = "hasil_foreground.csv"

# ==========================================
# CARI SEMUA GAMBAR
# ==========================================

ekstensi = (".jpg", ".jpeg", ".png", ".bmp")

files = sorted([
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith(ekstensi)
])

if len(files) == 0:
    print("Tidak ada gambar di folder:")
    print(INPUT_FOLDER)
    exit()

# ==========================================
# HEADER
# ==========================================

print("=" * 90)
print("ANALISIS FOREGROUND")
print("=" * 90)

print(
    f"{'No':<4}"
    f"{'Gambar':<45}"
    f"{'Total':>12}"
    f"{'Foreground':>15}"
    f"{'Persentase':>15}"
)

print("-" * 90)

hasil = []

# ==========================================
# PROSES
# ==========================================

for nomor, filename in enumerate(files, start=1):

    path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    image = cv2.imread(
        path,
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:
        print("Gagal membaca:", filename)
        continue

    # Total seluruh piksel
    total_pixels = image.size

    # Foreground = piksel hitam
    foreground_pixels = int((image == 0).sum())

    # Persentase foreground
    foreground_percentage = (
        foreground_pixels / total_pixels
    ) * 100

    print(
        f"{nomor:<4}"
        f"{filename:<45}"
        f"{total_pixels:>12}"
        f"{foreground_pixels:>15}"
        f"{foreground_percentage:>14.2f}%"
    )

    hasil.append([
        nomor,
        filename,
        total_pixels,
        foreground_pixels,
        round(foreground_percentage, 2)
    ])

# ==========================================
# SIMPAN CSV
# ==========================================

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "No",
        "Gambar",
        "Total Piksel",
        "Foreground",
        "Persentase Foreground"
    ])

    writer.writerows(hasil)

# ==========================================
# SELESAI
# ==========================================

print()
print("=" * 90)
print("SELESAI")
print("=" * 90)

print("Hasil disimpan sebagai:")
print(os.path.abspath(OUTPUT_FILE))