import cv2
import os

# ==========================================
# KONFIGURASI
# ==========================================

INPUT_FOLDER = "hasil_grayscale"
OUTPUT_FOLDER = "hasil_threshold"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================================
# CARI SEMUA GAMBAR GRAYSCALE
# ==========================================

ekstensi = (".jpg", ".jpeg", ".png", ".bmp")

files = sorted([
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith(ekstensi)
])

if len(files) == 0:
    print("Tidak ada gambar di folder hasil_grayscale!")
    exit()

print("=" * 70)
print("THRESHOLDING 3 METODE")
print("=" * 70)
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

    gray = cv2.imread(
        input_path,
        cv2.IMREAD_GRAYSCALE
    )

    if gray is None:
        print("Gagal membaca:", filename)
        continue

    nama, ext = os.path.splitext(filename)

    # ======================================
    # 1. GLOBAL THRESHOLD
    # ======================================

    _, global_threshold = cv2.threshold(
        gray,
        127,
        255,
        cv2.THRESH_BINARY
    )

    # ======================================
    # 2. OTSU THRESHOLD
    # ======================================

    otsu_value, otsu_threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # ======================================
    # 3. ADAPTIVE THRESHOLD
    # ======================================

    adaptive_threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        21,
        5
    )

    # ======================================
    # BUAT FOLDER MASING-MASING
    # ======================================

    folder_global = os.path.join(
        OUTPUT_FOLDER,
        "global"
    )

    folder_otsu = os.path.join(
        OUTPUT_FOLDER,
        "otsu"
    )

    folder_adaptive = os.path.join(
        OUTPUT_FOLDER,
        "adaptive"
    )

    os.makedirs(folder_global, exist_ok=True)
    os.makedirs(folder_otsu, exist_ok=True)
    os.makedirs(folder_adaptive, exist_ok=True)

    # ======================================
    # SIMPAN GLOBAL
    # ======================================

    global_path = os.path.join(
        folder_global,
        f"{nama}_global.png"
    )

    cv2.imwrite(
        global_path,
        global_threshold
    )

    # ======================================
    # SIMPAN OTSU
    # ======================================

    otsu_path = os.path.join(
        folder_otsu,
        f"{nama}_otsu.png"
    )

    cv2.imwrite(
        otsu_path,
        otsu_threshold
    )

    # ======================================
    # SIMPAN ADAPTIVE
    # ======================================

    adaptive_path = os.path.join(
        folder_adaptive,
        f"{nama}_adaptive.png"
    )

    cv2.imwrite(
        adaptive_path,
        adaptive_threshold
    )

    # ======================================
    # INFORMASI
    # ======================================

    print(
        f"[{nomor}/{len(files)}] {filename}"
    )

    print(
        f"    Global   : threshold = 127"
    )

    print(
        f"    Otsu     : threshold = {otsu_value:.2f}"
    )

    print(
        f"    Adaptive : Gaussian"
    )

# ==========================================
# SELESAI
# ==========================================

print()
print("=" * 70)
print("THRESHOLDING SELESAI")
print("=" * 70)

print("Hasil tersimpan di:")
print(os.path.abspath(OUTPUT_FOLDER))