import os
import re

# ============================================================
# PENGATURAN
# ============================================================

FILE_HASIL = os.path.join(
    "hasil_ocr",
    "hasil_ocr.txt"
)

FILE_OUTPUT = os.path.join(
    "hasil_ocr",
    "tabel_ocr.txt"
)

NOMOR_BENAR = "571012022000056"

METODE = [
    "Original",
    "Mean Filter",
    "Median Filter",
    "Gaussian Filter",
    "Sharpening"
]

# ============================================================
# CEK FILE
# ============================================================

if not os.path.exists(FILE_HASIL):
    print("File hasil OCR tidak ditemukan!")
    print("Pastikan ocr.py sudah dijalankan terlebih dahulu.")
    exit()

# ============================================================
# BACA HASIL OCR
# ============================================================

with open(FILE_HASIL, "r", encoding="utf-8") as file:
    isi = file.read()

# ============================================================
# MENYIMPAN DATA
# ============================================================

data = {
    "Original": [],
    "Mean Filter": [],
    "Median Filter": [],
    "Gaussian Filter": [],
    "Sharpening": []
}

# ============================================================
# PARSING DATA HASIL OCR
# ============================================================
#
# Format hasil_ocr.txt:
#
# Original            : 571012022000056 | 100.00%
# Mean Filter         : 571012022000056 | 100.00%
#
# ============================================================

gambar_sekarang = None

for baris in isi.splitlines():

    baris = baris.strip()

    # --------------------------------------------------------
    # Deteksi nama gambar
    # --------------------------------------------------------

    if re.match(r"^\d{2}_", baris):
        gambar_sekarang = baris
        continue

    # --------------------------------------------------------
    # Deteksi metode dan hasil OCR
    # --------------------------------------------------------

    for metode in METODE:

        pola = rf"^{re.escape(metode)}\s*:\s*(.*?)\s*\|\s*([\d.]+)%$"

        cocok = re.search(pola, baris)

        if cocok:

            hasil_ocr = cocok.group(1).strip()
            akurasi = float(cocok.group(2))

            # ------------------------------------------------
            # Hitung jumlah karakter benar
            # ------------------------------------------------

            karakter_benar = 0

            for i in range(
                min(len(hasil_ocr), len(NOMOR_BENAR))
            ):
                if hasil_ocr[i] == NOMOR_BENAR[i]:
                    karakter_benar += 1

            # ------------------------------------------------
            # Simpan data
            # ------------------------------------------------

            data[metode].append({
                "gambar": gambar_sekarang,
                "ocr": hasil_ocr,
                "karakter_benar": karakter_benar,
                "akurasi": akurasi
            })

# ============================================================
# CETAK HASIL RATA-RATA
# ============================================================

print()
print("=" * 100)
print("RINGKASAN HASIL OCR")
print("=" * 100)
print()

header = (
    f"{'Metode':<20}"
    f"{'Hasil OCR':<25}"
    f"{'Karakter Benar':<18}"
    f"{'Akurasi':<12}"
)

print(header)
print("-" * 100)

hasil_tabel = []

for metode in METODE:

    daftar = data[metode]

    if len(daftar) == 0:
        print(
            f"{metode:<20}"
            f"{'-':<25}"
            f"{0:<18.2f}"
            f"{0:<12.2f} %"
        )
        continue

    # --------------------------------------------------------
    # Rata-rata karakter benar
    # --------------------------------------------------------

    rata_karakter = sum(
        item["karakter_benar"]
        for item in daftar
    ) / len(daftar)

    # --------------------------------------------------------
    # Rata-rata akurasi
    # --------------------------------------------------------

    rata_akurasi = sum(
        item["akurasi"]
        for item in daftar
    ) / len(daftar)

    # --------------------------------------------------------
    # Hasil OCR
    #
    # Karena ini rekap 9 gambar, ditampilkan sebagai
    # nomor ground truth yang digunakan.
    # --------------------------------------------------------

    hasil_ocr = NOMOR_BENAR

    # --------------------------------------------------------
    # Cetak
    # --------------------------------------------------------

    print(
        f"{metode:<20}"
        f"{hasil_ocr:<25}"
        f"{rata_karakter:<18.2f}"
        f"{rata_akurasi:<12.2f} %"
    )

    hasil_tabel.append({
        "metode": metode,
        "ocr": hasil_ocr,
        "karakter": rata_karakter,
        "akurasi": rata_akurasi
    })

# ============================================================
# SIMPAN KE FILE TXT
# ============================================================

with open(FILE_OUTPUT, "w", encoding="utf-8") as file:

    file.write("=" * 100 + "\n")
    file.write("RINGKASAN HASIL OCR\n")
    file.write("=" * 100 + "\n\n")

    file.write(header + "\n")
    file.write("-" * 100 + "\n")

    for item in hasil_tabel:

        file.write(
            f"{item['metode']:<20}"
            f"{item['ocr']:<25}"
            f"{item['karakter']:<18.2f}"
            f"{item['akurasi']:<12.2f} %\n"
        )

    file.write("\n")
    file.write("=" * 100 + "\n")

print()
print("=" * 100)
print("Tabel berhasil dibuat!")
print(f"Disimpan di : {FILE_OUTPUT}")
print("=" * 100)