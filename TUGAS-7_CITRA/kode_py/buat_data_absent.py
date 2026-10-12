
import cv2
from pathlib import Path

# ============================================================
# KONFIGURASI FOLDER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "gambar_asli"
OUTPUT_DIR = BASE_DIR / "HASIL" / "data_absent_simulasi"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# PILIH GAMBAR UNTUK MENENTUKAN AREA TANDA TANGAN
# ============================================================

gambar_pertama = INPUT_DIR / "01_HighQuality_Enhanced.jpg"

image = cv2.imread(str(gambar_pertama))

if image is None:
    raise FileNotFoundError(
        f"Gambar tidak ditemukan: {gambar_pertama}"
    )

print("=" * 60)
print("PEMBUATAN DATA SIMULASI TANPA TANDA TANGAN")
print("=" * 60)
print("Pilih area tanda tangan pada gambar.")
print("Tarik kotak mengelilingi tanda tangan, lalu tekan ENTER.")
print("Tekan ESC jika ingin membatalkan.")

# Perkecil tampilan jika gambar terlalu besar,

# Perkecil gambar agar seluruh ijazah terlihat di layar.
tinggi_asli, lebar_asli = image.shape[:2]

# Lebar tampilan maksimal 900 piksel dan tinggi 650 piksel.
skala = min(900 / lebar_asli, 650 / tinggi_asli, 1.0)

preview = cv2.resize(
    image,
    (int(lebar_asli * skala), int(tinggi_asli * skala)),
    interpolation=cv2.INTER_AREA
)

cv2.namedWindow("Pilih Area Tanda Tangan", cv2.WINDOW_AUTOSIZE)

print("1. Tarik kotak pada area tanda tangan.")
print("2. Tekan ENTER atau SPACE untuk menyimpan pilihan.")
print("3. Tekan ESC untuk membatalkan.")

x, y, w, h = cv2.selectROI(
    "Pilih Area Tanda Tangan",
    preview,
    showCrosshair=True,
    fromCenter=False
)

cv2.destroyAllWindows()

if w == 0 or h == 0:
    raise SystemExit("Pemilihan area dibatalkan.")

# Kembalikan koordinat ke ukuran gambar asli.
x1 = round(x / skala)
y1 = round(y / skala)
x2 = round((x + w) / skala)
y2 = round((y + h) / skala)

if w == 0 or h == 0:
    raise SystemExit("Pemilihan area dibatalkan.")

# Konversi koordinat tampilan ke koordinat gambar asli.
x1 = int(x / skala)
y1 = int(y / skala)
x2 = int((x + w) / skala)
y2 = int((y + h) / skala)

print(f"Area terpilih: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

# ============================================================
# KONFIRMASI AREA
# ============================================================

konfirmasi = image.copy()

cv2.rectangle(
    konfirmasi,
    (x1, y1),
    (x2, y2),
    (0, 0, 255),
    5
)

preview_konfirmasi = cv2.resize(
    konfirmasi,
    (int(lebar_asli * skala), int(tinggi_asli * skala))
)

cv2.imshow("Periksa Area Merah - Tekan Y untuk lanjut", preview_konfirmasi)
print("Periksa kotak merah.")
print("Tekan Y untuk melanjutkan atau tombol lain untuk membatalkan.")

key = cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()

if key not in (ord("y"), ord("Y")):
    raise SystemExit("Dibatalkan. Jalankan ulang untuk memilih area.")

# ============================================================
# BUAT SALINAN SIMULASI TANPA TANDA TANGAN
# ============================================================

ekstensi_gambar = {".jpg", ".jpeg", ".png", ".bmp"}
jumlah_berhasil = 0

for file_gambar in sorted(INPUT_DIR.iterdir()):
    if file_gambar.suffix.lower() not in ekstensi_gambar:
        continue

    gambar = cv2.imread(str(file_gambar))

    if gambar is None:
        print(f"[GAGAL] Tidak dapat membaca: {file_gambar.name}")
        continue

    tinggi, lebar = gambar.shape[:2]

    # Koordinat area dipakai kembali untuk gambar
    # dengan dimensi yang sama seperti gambar referensi.
    if lebar != lebar_asli or tinggi != tinggi_asli:
        print(
            f"[LEWATI] Dimensi berbeda: {file_gambar.name} "
            f"({lebar}x{tinggi})"
        )
        continue

    gambar_simulasi = gambar.copy()

    # Mengisi area tanda tangan dengan warna putih.
    gambar_simulasi[y1:y2, x1:x2] = 255

    nama_output = OUTPUT_DIR / (
        file_gambar.stem + "_ABSENT_SIMULASI.png"
    )

    if cv2.imwrite(str(nama_output), gambar_simulasi):
        jumlah_berhasil += 1
        print(f"[OK] {nama_output.name}")
    else:
        print(f"[GAGAL] Menyimpan {nama_output.name}")

print("=" * 60)
print(f"Selesai. Berhasil membuat {jumlah_berhasil} gambar simulasi.")
print(f"Folder hasil: {OUTPUT_DIR}")
print("CATATAN: Data ini adalah simulasi untuk pengujian awal.")
print("=" * 60)