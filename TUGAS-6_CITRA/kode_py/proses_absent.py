import cv2
import os
import numpy as np

# ==========================================
# KONFIGURASI FOLDER
# ==========================================

INPUT_FOLDER = "data_absent_simulasi"

GRAY_FOLDER = "absent_grayscale"
THRESHOLD_FOLDER = "absent_threshold"
MORPHOLOGY_FOLDER = "absent_morphology"

os.makedirs(GRAY_FOLDER, exist_ok=True)
os.makedirs(THRESHOLD_FOLDER, exist_ok=True)
os.makedirs(MORPHOLOGY_FOLDER, exist_ok=True)

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

print("=" * 80)
print("MEMPROSES DATA SIGNATURE ABSENT")
print("=" * 80)
print("Jumlah gambar :", len(files))
print()

# ==========================================
# KERNEL MORFOLOGI
# ==========================================

kernel = cv2.getStructuringElement(
    cv2.MORPH_ELLIPSE,
    (3, 3)
)

hasil = []

# ==========================================
# PROSES SEMUA GAMBAR
# ==========================================

for nomor, filename in enumerate(files, start=1):

    input_path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    # --------------------------------------
    # BACA GAMBAR
    # --------------------------------------

    image = cv2.imread(input_path)

    if image is None:
        print("Gagal membaca:", filename)
        continue

    # --------------------------------------
    # 1. GRAYSCALE
    # --------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    nama, ext = os.path.splitext(filename)

    gray_path = os.path.join(
        GRAY_FOLDER,
        f"{nama}_gray.png"
    )

    cv2.imwrite(
        gray_path,
        gray
    )

    # --------------------------------------
    # 2. OTSU THRESHOLD
    # --------------------------------------

    otsu_value, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    threshold_path = os.path.join(
        THRESHOLD_FOLDER,
        f"{nama}_otsu.png"
    )

    cv2.imwrite(
        threshold_path,
        binary
    )

    # --------------------------------------
    # 3. OPENING
    # --------------------------------------

    opening = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        kernel
    )

    # --------------------------------------
    # 4. CLOSING
    # --------------------------------------

    closing = cv2.morphologyEx(
        opening,
        cv2.MORPH_CLOSE,
        kernel
    )

    morphology_path = os.path.join(
        MORPHOLOGY_FOLDER,
        f"{nama}_opening_closing.png"
    )

    cv2.imwrite(
        morphology_path,
        closing
    )

    # --------------------------------------
    # 5. HITUNG FOREGROUND
    # --------------------------------------

    total_pixels = closing.size

    # Hitam dianggap foreground
    foreground_pixels = int(
        np.sum(closing == 0)
    )

    foreground_percentage = (
        foreground_pixels /
        total_pixels
    ) * 100

    # --------------------------------------
    # SIMPAN DATA
    # --------------------------------------

    hasil.append([
        nomor,
        filename,
        total_pixels,
        foreground_pixels,
        foreground_percentage
    ])

    print(
        f"[{nomor}/{len(files)}] {filename}"
    )

    print(
        f"    Otsu threshold : {otsu_value:.2f}"
    )

    print(
        f"    Total piksel   : {total_pixels}"
    )

    print(
        f"    Foreground     : {foreground_pixels}"
    )

    print(
        f"    Persentase     : "
        f"{foreground_percentage:.2f}%"
    )

    print()

# ==========================================
# SIMPAN CSV
# ==========================================

csv_path = "hasil_foreground_absent.csv"

with open(
    csv_path,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    import csv

    writer = csv.writer(file)

    writer.writerow([
        "No",
        "Gambar",
        "Total Piksel",
        "Foreground",
        "Persentase Foreground"
    ])

    for row in hasil:
        writer.writerow([
            row[0],
            row[1],
            row[2],
            row[3],
            round(row[4], 2)
        ])

# ==========================================
# SELESAI
# ==========================================

print("=" * 80)
print("PEMROSESAN ABSENT SELESAI")
print("=" * 80)

print()
print("Grayscale:")
print(os.path.abspath(GRAY_FOLDER))

print()
print("Threshold:")
print(os.path.abspath(THRESHOLD_FOLDER))

print()
print("Morphology:")
print(os.path.abspath(MORPHOLOGY_FOLDER))

print()
print("CSV:")
print(os.path.abspath(csv_path))