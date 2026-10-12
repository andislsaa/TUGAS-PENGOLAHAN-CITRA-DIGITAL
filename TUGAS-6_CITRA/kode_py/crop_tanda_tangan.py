import cv2
import os

# ==========================================
# FOLDER
# ==========================================

INPUT_FOLDER = "gambar_asli"
OUTPUT_FOLDER = "hasil_crop"

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
    print("Tidak ada gambar di folder gambar_asli!")
    exit()

print("Jumlah gambar:", len(files))

# ==========================================
# BUKA GAMBAR PERTAMA
# ==========================================

first_file = files[0]
first_path = os.path.join(INPUT_FOLDER, first_file)

image = cv2.imread(first_path)

if image is None:
    print("Gambar gagal dibaca!")
    exit()

height, width = image.shape[:2]

print("Ukuran gambar:")
print("Lebar  :", width)
print("Tinggi :", height)

# ==========================================
# PERKECIL HANYA UNTUK TAMPILAN
# TANPA MENGUBAH RASIO
# ==========================================

MAX_WIDTH = 1000
MAX_HEIGHT = 750

scale = min(
    MAX_WIDTH / width,
    MAX_HEIGHT / height,
    1
)

display_width = int(width * scale)
display_height = int(height * scale)

display_image = cv2.resize(
    image,
    (display_width, display_height),
    interpolation=cv2.INTER_AREA
)

# ==========================================
# PILIH AREA TANDA TANGAN
# ==========================================

window_name = "Pilih Tanda Tangan Dekan"

print("\n==========================================")
print("PILIH AREA TANDA TANGAN")
print("==========================================")
print("Drag kotak pada tanda tangan Dekan.")
print("Kemudian tekan ENTER.")
print("==========================================")

cv2.namedWindow(
    window_name,
    cv2.WINDOW_AUTOSIZE
)

x_display, y_display, w_display, h_display = cv2.selectROI(
    window_name,
    display_image,
    showCrosshair=True,
    fromCenter=False
)

cv2.destroyAllWindows()

# ==========================================
# CEK
# ==========================================

if w_display == 0 or h_display == 0:
    print("Area tidak dipilih.")
    exit()

# ==========================================
# KEMBALIKAN KOORDINAT KE GAMBAR ASLI
# ==========================================

x = int(x_display / scale)
y = int(y_display / scale)
w = int(w_display / scale)
h = int(h_display / scale)

print("\nKoordinat crop:")
print("X      :", x)
print("Y      :", y)
print("Width  :", w)
print("Height :", h)

# ==========================================
# CROP SEMUA 9 GAMBAR
# ==========================================

print("\n==========================================")
print("MEMPROSES GAMBAR")
print("==========================================")

for nomor, filename in enumerate(files, start=1):

    input_path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    img = cv2.imread(input_path)

    if img is None:
        print("Gagal membaca:", filename)
        continue

    img_height, img_width = img.shape[:2]

    x1 = max(0, x)
    y1 = max(0, y)

    x2 = min(img_width, x + w)
    y2 = min(img_height, y + h)

    crop = img[y1:y2, x1:x2]

    output_name = f"{nomor:02d}_crop_{filename}"

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_name
    )

    cv2.imwrite(output_path, crop)

    print(
        f"[{nomor}/{len(files)}] {filename}"
        f" -> {output_name}"
    )

print("\n==========================================")
print("CROP SELESAI")
print("==========================================")
print("Hasil ada di folder:", OUTPUT_FOLDER)