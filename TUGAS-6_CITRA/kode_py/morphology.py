import cv2
import os
import numpy as np

# ==========================================
# KONFIGURASI
# ==========================================

INPUT_FOLDER = "hasil_threshold/otsu"
OUTPUT_FOLDER = "hasil_morphology"

OPENING_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "opening"
)

CLOSING_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "closing"
)

FINAL_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "opening_closing"
)

# Buat folder
os.makedirs(OPENING_FOLDER, exist_ok=True)
os.makedirs(CLOSING_FOLDER, exist_ok=True)
os.makedirs(FINAL_FOLDER, exist_ok=True)


# ==========================================
# CARI SEMUA GAMBAR
# ==========================================

ekstensi = (".jpg", ".jpeg", ".png", ".bmp")

files = sorted([
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith(ekstensi)
])

if len(files) == 0:
    print("Tidak ada gambar di:")
    print(INPUT_FOLDER)
    exit()


print("=" * 70)
print("MORPHOLOGICAL OPERATION")
print("=" * 70)
print("Jumlah gambar :", len(files))
print()


# ==========================================
# KERNEL MORFOLOGI
# ==========================================

# Kernel kecil agar tanda tangan tidak rusak
kernel = cv2.getStructuringElement(
    cv2.MORPH_ELLIPSE,
    (3, 3)
)

print("Kernel : 3 x 3")
print()


# ==========================================
# PROSES SEMUA GAMBAR
# ==========================================

for nomor, filename in enumerate(files, start=1):

    input_path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    # Baca gambar binary
    image = cv2.imread(
        input_path,
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:
        print("Gagal membaca:", filename)
        continue


    # ======================================
    # OPENING
    # ======================================

    opening = cv2.morphologyEx(
        image,
        cv2.MORPH_OPEN,
        kernel
    )


    # ======================================
    # CLOSING
    # ======================================

    closing = cv2.morphologyEx(
        opening,
        cv2.MORPH_CLOSE,
        kernel
    )


    # ======================================
    # SIMPAN OPENING
    # ======================================

    nama, ext = os.path.splitext(filename)

    opening_path = os.path.join(
        OPENING_FOLDER,
        f"{nama}_opening.png"
    )

    cv2.imwrite(
        opening_path,
        opening
    )


    # ======================================
    # SIMPAN CLOSING
    # ======================================

    closing_path = os.path.join(
        CLOSING_FOLDER,
        f"{nama}_closing.png"
    )

    cv2.imwrite(
        closing_path,
        closing
    )


    # ======================================
    # SIMPAN HASIL AKHIR
    # ======================================

    final_path = os.path.join(
        FINAL_FOLDER,
        f"{nama}_opening_closing.png"
    )

    cv2.imwrite(
        final_path,
        closing
    )


    # ======================================
    # HITUNG FOREGROUND
    # ======================================

    # Karena background putih = 255
    # dan tinta/objek = 0,
    # foreground dihitung sebagai piksel hitam.

    foreground_before = np.sum(image == 0)

    foreground_after = np.sum(closing == 0)

    print(
        f"[{nomor}/{len(files)}] {filename}"
    )

    print(
        f"    Foreground sebelum : {foreground_before} piksel"
    )

    print(
        f"    Foreground sesudah : {foreground_after} piksel"
    )

    print()


# ==========================================
# SELESAI
# ==========================================

print("=" * 70)
print("MORPHOLOGY SELESAI")
print("=" * 70)

print()
print("Opening:")
print(os.path.abspath(OPENING_FOLDER))

print()
print("Closing:")
print(os.path.abspath(CLOSING_FOLDER))

print()
print("Hasil akhir:")
print(os.path.abspath(FINAL_FOLDER))