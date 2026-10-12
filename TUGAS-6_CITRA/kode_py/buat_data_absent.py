import cv2
import os

# ==========================================
# KONFIGURASI
# ==========================================

INPUT_FOLDER = "hasil_crop"
OUTPUT_FOLDER = "data_absent_simulasi"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ekstensi = (".jpg", ".jpeg", ".png", ".bmp")

files = sorted([
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith(ekstensi)
])

if len(files) == 0:
    print("Tidak ada gambar di folder hasil_crop!")
    exit()

# ==========================================
# PILIH GAMBAR PERTAMA
# ==========================================

filename = files[0]

path = os.path.join(
    INPUT_FOLDER,
    filename
)

image = cv2.imread(path)

if image is None:
    print("Gagal membaca gambar.")
    exit()

print("=" * 70)
print("MEMBUAT DATA SIGNATURE ABSENT SIMULASI")
print("=" * 70)

print()
print("Gambar yang digunakan untuk menentukan area:")
print(filename)

print()
print("Ukuran gambar:")
print("Lebar  :", image.shape[1])
print("Tinggi :", image.shape[0])

# ==========================================
# TAMPILKAN GAMBAR
# ==========================================

display = image.copy()

# Ukuran jendela
scale = 1000 / image.shape[1]

if scale < 1:
    display = cv2.resize(
        image,
        None,
        fx=scale,
        fy=scale
    )

cv2.imshow(
    "Crop - Tekan tombol apa saja untuk lanjut",
    display
)

cv2.waitKey(0)
cv2.destroyAllWindows()

print()
print("Sekarang kita akan menggunakan koordinat area tanda tangan.")
print()
print("Koordinat dihitung dari gambar asli, bukan dari ukuran jendela.")
print()

# ==========================================
# MASUKKAN KOORDINAT
# ==========================================

print("Masukkan koordinat area tanda tangan.")
print()
print("x1 = batas kiri")
print("y1 = batas atas")
print("x2 = batas kanan")
print("y2 = batas bawah")
print()

x1 = int(input("x1 = "))
y1 = int(input("y1 = "))
x2 = int(input("x2 = "))
y2 = int(input("y2 = "))

# ==========================================
# VALIDASI
# ==========================================

height, width = image.shape[:2]

if not (
    0 <= x1 < x2 <= width
    and
    0 <= y1 < y2 <= height
):
    print()
    print("KOORDINAT TIDAK VALID!")
    print()
    print("Ukuran gambar:")
    print("Lebar :", width)
    print("Tinggi:", height)
    exit()

# ==========================================
# TAMPILKAN HASIL SIMULASI
# ==========================================

preview = image.copy()

cv2.rectangle(
    preview,
    (x1, y1),
    (x2, y2),
    (0, 0, 255),
    5
)

cv2.imshow(
    "AREA YANG AKAN DIHAPUS",
    preview
)

print()
print("Kotak merah menunjukkan area yang akan dihapus.")
print("Tekan Y jika sudah benar.")
print("Tekan N jika ingin mengulang.")

key = cv2.waitKey(0)
cv2.destroyAllWindows()

if key not in [ord("y"), ord("Y")]:
    print()
    print("Proses dibatalkan.")
    print("Jalankan kembali program untuk menentukan koordinat.")
    exit()

# ==========================================
# PROSES SEMUA 9 GAMBAR
# ==========================================

print()
print("=" * 70)
print("MEMBUAT DATA ABSENT")
print("=" * 70)

for nomor, filename in enumerate(files, start=1):

    input_path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    image = cv2.imread(input_path)

    if image is None:
        print("Gagal membaca:", filename)
        continue

    # Salin gambar
    absent = image.copy()

    # Hapus area tanda tangan
    absent[y1:y2, x1:x2] = 255

    # Nama output
    nama, ext = os.path.splitext(filename)

    output_name = f"{nama}_ABSENT.png"

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_name
    )

    cv2.imwrite(
        output_path,
        absent
    )

    print(
        f"[{nomor}/{len(files)}] {filename}"
        f" -> {output_name}"
    )

print()
print("=" * 70)
print("SELESAI")
print("=" * 70)

print()
print("Data absent tersimpan di:")
print(os.path.abspath(OUTPUT_FOLDER))