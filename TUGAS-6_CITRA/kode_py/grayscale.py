import cv2
import os

# ==========================================
# KONFIGURASI FOLDER
# ==========================================

INPUT_FOLDER = "hasil_crop"
OUTPUT_FOLDER = "hasil_grayscale"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================================
# CARI SEMUA GAMBAR
# ==========================================

ekstensi = (".jpg", ".jpeg", ".png", ".bmp")

files = sorted([
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith(ekstensi)
])

if len(files) == 0:
    print("Tidak ada gambar di folder hasil_crop!")
    exit()

print("=" * 60)
print("KONVERSI GRAYSCALE")
print("=" * 60)
print("Jumlah gambar :", len(files))
print()

# ==========================================
# PROSES SEMUA GAMBAR
# ==========================================

for nomor, filename in enumerate(files, start=1):

    input_path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    # Baca gambar
    image = cv2.imread(input_path)

    if image is None:
        print("Gagal membaca:", filename)
        continue

    # ======================================
    # KONVERSI RGB/BGR → GRAYSCALE
    # ======================================

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # ======================================
    # SIMPAN HASIL
    # ======================================

    nama, ext = os.path.splitext(filename)

    output_name = f"{nama}_gray.png"

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_name
    )

    cv2.imwrite(
        output_path,
        gray
    )

    print(
        f"[{nomor}/{len(files)}] "
        f"{filename} -> {output_name}"
    )

# ==========================================
# SELESAI
# ==========================================

print()
print("=" * 60)
print("GRAYSCALE SELESAI")
print("=" * 60)
print("Hasil tersimpan di:")
print(os.path.abspath(OUTPUT_FOLDER))