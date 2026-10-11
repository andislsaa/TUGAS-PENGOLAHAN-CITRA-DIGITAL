import cv2
import pytesseract
import os
import re

# ============================================================
# KONFIGURASI
# ============================================================

NOMOR_BENAR = "571012022000056"

BASE_DIR = r"C:\Users\HP\TUGAS-5_CITRA"

FOLDER_INPUT = os.path.join(BASE_DIR, "hasil_filtering")
FOLDER_OUTPUT = os.path.join(BASE_DIR, "hasil_ocr")

# Lokasi Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ============================================================
# CEK TESSERACT
# ============================================================

print("=" * 70)
print("OCR NOMOR IJAZAH")
print("=" * 70)

try:
    versi = pytesseract.get_tesseract_version()
    print("Tesseract terdeteksi:", versi)
except Exception as e:
    print("Tesseract tidak ditemukan!")
    print(e)
    exit()


# ============================================================
# DAFTAR METODE
# ============================================================

METODE = {
    "Original": "01_original.png",
    "Mean Filter": "02_mean_filter.png",
    "Median Filter": "03_median_filter.png",
    "Gaussian Filter": "04_gaussian_filter.png",
    "Sharpening": "05_sharpening.png"
}


# ============================================================
# FUNGSI HITUNG AKURASI
# ============================================================

def hitung_akurasi(hasil_ocr, nomor_benar):

    jumlah_benar = 0

    for i in range(min(len(hasil_ocr), len(nomor_benar))):

        if hasil_ocr[i] == nomor_benar[i]:
            jumlah_benar += 1

    akurasi = (jumlah_benar / len(nomor_benar)) * 100

    return akurasi


# ============================================================
# FUNGSI OCR
# ============================================================

def lakukan_ocr(path_gambar):

    image = cv2.imread(path_gambar)

    if image is None:
        return ""

    # --------------------------------------------------------
    # 1. Grayscale
    # --------------------------------------------------------

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # --------------------------------------------------------
    # 2. Rotasi 90 derajat searah jarum jam
    # --------------------------------------------------------

    rotated = cv2.rotate(
        gray,
        cv2.ROTATE_90_CLOCKWISE
    )

    # --------------------------------------------------------
    # 3. Perbesar gambar
    # --------------------------------------------------------

    resized = cv2.resize(
        rotated,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC
    )

    # --------------------------------------------------------
    # 4. Threshold Otsu
    # --------------------------------------------------------

    _, threshold = cv2.threshold(
        resized,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # --------------------------------------------------------
    # 5. Konfigurasi Tesseract
    # --------------------------------------------------------

    config = (
        "--psm 7 "
        "-c tessedit_char_whitelist=0123456789"
    )

    # --------------------------------------------------------
    # 6. OCR
    # --------------------------------------------------------

    hasil = pytesseract.image_to_string(
        threshold,
        config=config
    )

    # --------------------------------------------------------
    # 7. Ambil hanya angka
    # --------------------------------------------------------

    hasil = re.sub(
        r"[^0-9]",
        "",
        hasil
    )

    return hasil, threshold


# ============================================================
# BUAT FOLDER OUTPUT
# ============================================================

os.makedirs(
    FOLDER_OUTPUT,
    exist_ok=True
)


# ============================================================
# FILE HASIL OCR
# ============================================================

file_hasil = os.path.join(
    FOLDER_OUTPUT,
    "hasil_ocr.txt"
)

file_ringkasan = os.path.join(
    FOLDER_OUTPUT,
    "ringkasan_akurasi.txt"
)


# ============================================================
# PROSES SEMUA GAMBAR
# ============================================================

semua_hasil = []

with open(
    file_hasil,
    "w",
    encoding="utf-8"
) as f:

    f.write("=" * 80 + "\n")
    f.write("HASIL OCR NOMOR IJAZAH\n")
    f.write("=" * 80 + "\n\n")

    f.write(
        f"Nomor benar : {NOMOR_BENAR}\n\n"
    )

    # Ambil semua folder gambar
    folder_gambar = sorted(
        [
            folder
            for folder in os.listdir(FOLDER_INPUT)
            if os.path.isdir(
                os.path.join(
                    FOLDER_INPUT,
                    folder
                )
            )
        ]
    )

    # --------------------------------------------------------
    # LOOP 9 GAMBAR
    # --------------------------------------------------------

    for nama_folder in folder_gambar:

        path_folder = os.path.join(
            FOLDER_INPUT,
            nama_folder
        )

        print("\n" + "=" * 70)
        print(nama_folder)
        print("=" * 70)

        f.write("\n")
        f.write("=" * 70 + "\n")
        f.write(nama_folder + "\n")
        f.write("=" * 70 + "\n")

        folder_ocr = os.path.join(
            FOLDER_OUTPUT,
            nama_folder
        )

        os.makedirs(
            folder_ocr,
            exist_ok=True
        )

        # ----------------------------------------------------
        # LOOP 5 METODE
        # ----------------------------------------------------

        for nama_metode, nama_file in METODE.items():

            path_gambar = os.path.join(
                path_folder,
                nama_file
            )

            if not os.path.exists(path_gambar):

                print(
                    nama_metode,
                    ": file tidak ditemukan"
                )

                continue

            # OCR
            hasil = lakukan_ocr(
                path_gambar
            )

            hasil_text = hasil[0]
            threshold = hasil[1]

            # Hitung akurasi
            akurasi = hitung_akurasi(
                hasil_text,
                NOMOR_BENAR
            )

            # Simpan gambar hasil threshold
            nama_output = (
                nama_metode
                .replace(" ", "_")
                .lower()
                + "_threshold.png"
            )

            path_threshold = os.path.join(
                folder_ocr,
                nama_output
            )

            cv2.imwrite(
                path_threshold,
                threshold
            )

            # Simpan hasil ke list
            semua_hasil.append({
                "gambar": nama_folder,
                "metode": nama_metode,
                "ocr": hasil_text,
                "akurasi": akurasi
            })

            # Tampilkan di terminal
            print(
                f"{nama_metode:<20} : "
                f"{hasil_text:<20} | "
                f"{akurasi:.2f}%"
            )

            # Simpan ke file
            f.write(
                f"{nama_metode:<20} : "
                f"{hasil_text:<20} | "
                f"{akurasi:.2f}%\n"
            )


# ============================================================
# HITUNG RATA-RATA PER METODE
# ============================================================

rata_rata = {}

for nama_metode in METODE.keys():

    data = [
        item["akurasi"]
        for item in semua_hasil
        if item["metode"] == nama_metode
    ]

    if len(data) > 0:

        rata_rata[nama_metode] = (
            sum(data) / len(data)
        )


# ============================================================
# SIMPAN RINGKASAN
# ============================================================

with open(
    file_ringkasan,
    "w",
    encoding="utf-8"
) as f:

    f.write("=" * 60 + "\n")
    f.write("RINGKASAN AKURASI OCR\n")
    f.write("=" * 60 + "\n\n")

    f.write(
        f"Nomor benar : {NOMOR_BENAR}\n\n"
    )

    for metode, nilai in rata_rata.items():

        f.write(
            f"{metode:<20} : "
            f"{nilai:.2f}%\n"
        )


# ============================================================
# TAMPILKAN RINGKASAN DI TERMINAL
# ============================================================

print("\n")
print("=" * 60)
print("RINGKASAN AKURASI OCR")
print("=" * 60)

print(
    f"Nomor benar : {NOMOR_BENAR}\n"
)

for metode, nilai in rata_rata.items():

    print(
        f"{metode:<20} : "
        f"{nilai:.2f}%"
    )

print("\nOCR SELESAI.")

print(
    "\nFile hasil:"
)

print(
    os.path.join(
        FOLDER_OUTPUT,
        "hasil_ocr.txt"
    )
)

print(
    os.path.join(
        FOLDER_OUTPUT,
        "ringkasan_akurasi.txt"
    )
)