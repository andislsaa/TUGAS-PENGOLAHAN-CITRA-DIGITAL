
import csv
import re
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

import cv2
import numpy as np
import pytesseract


# =========================================================
# KONFIGURASI
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "HASIL" / "prototype"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Berdasarkan eksperimen klasifikasi sebelumnya.
# Nilai ini perlu divalidasi pada area tanda tangan prototype.
SIGNATURE_THRESHOLD = 5.0

# Ubah menjadi True jika Tesseract tidak ditemukan otomatis.
# Contoh:
# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )


# =========================================================
# PILIH GAMBAR
# =========================================================

def pilih_gambar():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    path = filedialog.askopenfilename(
        title="Pilih gambar ijazah",
        initialdir=str(BASE_DIR / "gambar_asli"),
        filetypes=[
            ("Gambar", "*.jpg *.jpeg *.png *.bmp"),
            ("Semua file", "*.*"),
        ],
    )

    root.destroy()

    if not path:
        return None

    return Path(path)


# =========================================================
# PILIH AREA PADA GAMBAR
# =========================================================

def pilih_area(gambar, judul):
    tinggi, lebar = gambar.shape[:2]

    # Perkecil hanya untuk tampilan agar muat di layar.
    skala = min(1000 / lebar, 750 / tinggi, 1.0)

    tampilan = cv2.resize(
        gambar,
        (int(lebar * skala), int(tinggi * skala)),
        interpolation=cv2.INTER_AREA,
    )

    print(f"\nPilih {judul}.")
    print("Tarik kotak dengan mouse, lalu tekan ENTER.")
    print("Tekan ESC untuk membatalkan.")

    cv2.namedWindow(judul, cv2.WINDOW_NORMAL)

    x, y, w, h = cv2.selectROI(
        judul,
        tampilan,
        showCrosshair=True,
        fromCenter=False,
    )

    cv2.destroyWindow(judul)

    if w == 0 or h == 0:
        return None

    # Kembalikan koordinat ke ukuran gambar asli.
    x1 = int(x / skala)
    y1 = int(y / skala)
    x2 = int((x + w) / skala)
    y2 = int((y + h) / skala)

    x1 = max(0, min(x1, lebar - 1))
    y1 = max(0, min(y1, tinggi - 1))
    x2 = max(x1 + 1, min(x2, lebar))
    y2 = max(y1 + 1, min(y2, tinggi))

    return gambar[y1:y2, x1:x2].copy()


# =========================================================
# GRAYSCALE DAN IMAGE ENHANCEMENT
# =========================================================

def buat_metode_enhancement(citra):
    if len(citra.shape) == 3:
        gray = cv2.cvtColor(citra, cv2.COLOR_BGR2GRAY)
    else:
        gray = citra.copy()

    # Mean filter
    mean = cv2.blur(gray, (3, 3))

    # Median filter
    median = cv2.medianBlur(gray, 3)

    # Gaussian filter
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0)

    # Sharpening
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0],
    ], dtype=np.float32)

    sharpening = cv2.filter2D(
        gray,
        -1,
        kernel,
    )

    return {
        "Original": gray,
        "Mean": mean,
        "Median": median,
        "Gaussian": gaussian,
        "Sharpening": sharpening,
    }


# =========================================================
# OCR NOMOR IJAZAH
# =========================================================

def jalankan_ocr(gambar_gray):
    # Perbesar citra agar karakter kecil lebih mudah dibaca.
    tinggi, lebar = gambar_gray.shape[:2]

    faktor = max(1, min(4, 1000 // max(lebar, 1)))

    gambar_besar = cv2.resize(
        gambar_gray,
        (lebar * faktor, tinggi * faktor),
        interpolation=cv2.INTER_CUBIC,
    )

    # Threshold Otsu
    _, biner = cv2.threshold(
        gambar_besar,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    teks = pytesseract.image_to_string(
        biner,
        config="--psm 6",
    )

    # Hilangkan spasi dan simbol yang bukan bagian nomor.
    nomor = re.sub(r"[^A-Za-z0-9/-]", "", teks)

    return nomor, biner


# =========================================================
# DETEKSI TANDA TANGAN
# =========================================================


def deteksi_tanda_tangan(citra_gray):
    """
    Mendeteksi tanda tangan dari area ROI yang sudah dipilih.
    Input harus berupa citra grayscale.
    """

    if citra_gray is None or citra_gray.size == 0:
        return 0.0, "ABSENT", np.zeros((1, 1), dtype=np.uint8)

    # Mengurangi noise sebelum thresholding.
    blur = cv2.GaussianBlur(
        citra_gray,
        (5, 5),
        0,
    )

    # Memisahkan tinta yang lebih gelap dari latar belakang.
    _, biner = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    # Membersihkan noise kecil.
    kernel = np.ones((2, 2), dtype=np.uint8)

    bersih = cv2.morphologyEx(
        biner,
        cv2.MORPH_OPEN,
        kernel,
    )

    jumlah_piksel = bersih.size

    if jumlah_piksel == 0:
        return 0.0, "ABSENT", bersih

    piksel_tinta = cv2.countNonZero(bersih)
    persentase = piksel_tinta / jumlah_piksel * 100

    prediksi = (
        "PRESENT"
        if persentase >= SIGNATURE_THRESHOLD
        else "ABSENT"
    )

    return round(persentase, 2), prediksi, bersih


# =========================================================
# SIMPAN HASIL
# =========================================================

def simpan_csv(data):
    file_csv = OUTPUT_DIR / "hasil_prototype.csv"

    with open(
        file_csv,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "Nama File",
            "Nomor Ijazah",
            "Metode Enhancement",
            "Persentase Foreground",
            "Deteksi Tanda Tangan",
        ])

        writer.writerow(data)

    return file_csv


# =========================================================
# PROGRAM UTAMA
# =========================================================

def main():
    print("=" * 60)
    print("PROTOTYPE VERIFIKASI IJAZAH")
    print("=" * 60)

    path = pilih_gambar()

    if path is None:
        print("Pemilihan gambar dibatalkan.")
        return

    gambar = cv2.imread(str(path))

    if gambar is None:
        print("Gambar tidak dapat dibaca.")
        return

    print("\nFile:", path.name)
    print("Ukuran gambar:", gambar.shape[1], "x", gambar.shape[0])

    # Pilih kedua area pada gambar yang sama.
    area_nomor = pilih_area(
        gambar,
        "Pilih Area Nomor Ijazah",
    )

    if area_nomor is None:
        print("Area nomor tidak dipilih.")
        return

    area_ttd = pilih_area(
        gambar,
        "Pilih Area Tanda Tangan",
    )

    if area_ttd is None:
        print("Area tanda tangan tidak dipilih.")
        return

    # Jalankan OCR pada setiap metode enhancement.
    metode = buat_metode_enhancement(area_nomor)

    hasil_ocr = {}

    print("\n" + "=" * 60)
    print("PERBANDINGAN OCR")
    print("=" * 60)

    for nama, citra in metode.items():
        nomor, biner = jalankan_ocr(citra)
        hasil_ocr[nama] = nomor

        print(f"{nama:<12}: {nomor or '(tidak terbaca)'}")

        cv2.imwrite(
            str(OUTPUT_DIR / f"ocr_{nama.lower()}.png"),
            biner,
        )

    # Default memakai Median.
    # Pilihan metode dapat diganti setelah evaluasi CER.
    metode_terpilih = "Original"
    nomor_ijazah = hasil_ocr[metode_terpilih]

    # Proses deteksi tanda tangan.
    if len(area_ttd.shape) == 3:
        gray_ttd = cv2.cvtColor(
            area_ttd,
            cv2.COLOR_BGR2GRAY,
        )
    else:
        gray_ttd = area_ttd.copy()

    foreground, tanda_tangan, biner_ttd = (
        deteksi_tanda_tangan(gray_ttd)
    )

    cv2.imwrite(
        str(OUTPUT_DIR / "area_nomor.png"),
        area_nomor,
    )

    cv2.imwrite(
        str(OUTPUT_DIR / "area_tanda_tangan.png"),
        area_ttd,
    )

    cv2.imwrite(
        str(OUTPUT_DIR / "tanda_tangan_threshold.png"),
        biner_ttd,
    )

    hasil_csv = simpan_csv([
        path.name,
        nomor_ijazah,
        metode_terpilih,
        round(foreground, 4),
        tanda_tangan,
    ])

    print("\n" + "=" * 60)
    print("HASIL VERIFIKASI IJAZAH")
    print("=" * 60)
    print("Nama file             :", path.name)
    print("Nomor ijazah          :", nomor_ijazah or "TIDAK TERBACA")
    print("Metode OCR            :", metode_terpilih)
    print(f"Persentase foreground : {foreground:.2f}%")
    print("Tanda tangan          :", tanda_tangan)
    print("Hasil CSV             :", hasil_csv)
    print("Folder hasil          :", OUTPUT_DIR)
    print("=" * 60)

    # Tampilkan hasil visual.
    cv2.imshow("Area Nomor Ijazah", area_nomor)
    cv2.imshow("Area Tanda Tangan", area_ttd)
    cv2.imshow("Hasil Threshold Tanda Tangan", biner_ttd)

    print("\nTekan sembarang tombol pada jendela gambar untuk keluar.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()