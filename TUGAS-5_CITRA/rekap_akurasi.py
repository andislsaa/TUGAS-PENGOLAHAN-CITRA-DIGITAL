import os
import csv
import matplotlib.pyplot as plt

# ============================================================
# KONFIGURASI
# ============================================================

BASE_DIR = r"C:\Users\HP\TUGAS-5_CITRA"

FOLDER_OCR = os.path.join(
    BASE_DIR,
    "hasil_ocr"
)

FILE_HASIL = os.path.join(
    FOLDER_OCR,
    "hasil_ocr.txt"
)

FILE_CSV = os.path.join(
    FOLDER_OCR,
    "rekap_akurasi_lengkap.csv"
)


# ============================================================
# DAFTAR METODE
# ============================================================

METODE = [
    "Original",
    "Mean Filter",
    "Median Filter",
    "Gaussian Filter",
    "Sharpening"
]


# ============================================================
# BACA HASIL OCR
# ============================================================

data = []

nama_gambar = None

with open(
    FILE_HASIL,
    "r",
    encoding="utf-8"
) as file:

    for baris in file:

        baris = baris.strip()

        # -----------------------------------------------
        # Mendeteksi nama folder gambar
        # -----------------------------------------------

        if baris.startswith("0") and "_" in baris:

            nama_gambar = baris

        # -----------------------------------------------
        # Membaca hasil metode
        # -----------------------------------------------

        for metode in METODE:

            if baris.startswith(
                metode
            ):

                bagian = baris.split("|")

                hasil_ocr = (
                    bagian[0]
                    .split(":")[-1]
                    .strip()
                )

                akurasi_text = (
                    bagian[1]
                    .replace("%", "")
                    .strip()
                )

                akurasi = float(
                    akurasi_text
                )

                data.append({
                    "gambar": nama_gambar,
                    "metode": metode,
                    "ocr": hasil_ocr,
                    "akurasi": akurasi
                })


# ============================================================
# SIMPAN CSV
# ============================================================

with open(
    FILE_CSV,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Gambar",
        "Metode",
        "Hasil OCR",
        "Akurasi (%)"
    ])

    for item in data:

        writer.writerow([
            item["gambar"],
            item["metode"],
            item["ocr"],
            f"{item['akurasi']:.2f}"
        ])


# ============================================================
# BUAT TABEL 9 × 5
# ============================================================

gambar = []

for item in data:

    if item["gambar"] not in gambar:

        gambar.append(
            item["gambar"]
        )


print("\n")
print("=" * 100)
print("TABEL AKURASI OCR 9 GAMBAR × 5 METODE")
print("=" * 100)

header = (
    f"{'Gambar':<35}"
    f"{'Original':>12}"
    f"{'Mean':>12}"
    f"{'Median':>12}"
    f"{'Gaussian':>12}"
    f"{'Sharpening':>12}"
)

print(header)

print("-" * 100)


for nama in gambar:

    nilai = {}

    for item in data:

        if item["gambar"] == nama:

            nilai[item["metode"]] = (
                item["akurasi"]
            )

    print(
        f"{nama:<35}"
        f"{nilai.get('Original', 0):>11.2f}%"
        f"{nilai.get('Mean Filter', 0):>11.2f}%"
        f"{nilai.get('Median Filter', 0):>11.2f}%"
        f"{nilai.get('Gaussian Filter', 0):>11.2f}%"
        f"{nilai.get('Sharpening', 0):>11.2f}%"
    )


# ============================================================
# HITUNG RATA-RATA SETIAP METODE
# ============================================================

rata_rata = {}

for metode in METODE:

    nilai = [
        item["akurasi"]
        for item in data
        if item["metode"] == metode
    ]

    if nilai:

        rata_rata[metode] = (
            sum(nilai) / len(nilai)
        )


# ============================================================
# TAMPILKAN RATA-RATA
# ============================================================

print("\n")
print("=" * 60)
print("RATA-RATA AKURASI SETIAP METODE")
print("=" * 60)

for metode in METODE:

    print(
        f"{metode:<20} : "
        f"{rata_rata[metode]:.2f}%"
    )


# ============================================================
# GRAFIK 1
# AKURASI 9 GAMBAR UNTUK SETIAP METODE
# ============================================================

for metode in METODE:

    nilai = []

    label = []

    for nama in gambar:

        for item in data:

            if (
                item["gambar"] == nama
                and item["metode"] == metode
            ):

                nilai.append(
                    item["akurasi"]
                )

                label.append(
                    nama[:2]
                )

    plt.figure(
        figsize=(10, 5)
    )

    plt.bar(
        label,
        nilai
    )

    plt.ylim(
        0,
        105
    )

    plt.xlabel(
        "Nomor Gambar"
    )

    plt.ylabel(
        "Akurasi (%)"
    )

    plt.title(
        f"Akurasi OCR - {metode}"
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    plt.tight_layout()

    nama_file = (
        metode
        .replace(" ", "_")
        .lower()
    )

    plt.savefig(
        os.path.join(
            FOLDER_OCR,
            f"grafik_{nama_file}.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# GRAFIK 2
# RATA-RATA AKURASI SETIAP METODE
# ============================================================

plt.figure(
    figsize=(10, 6)
)

metode_nama = list(
    rata_rata.keys()
)

nilai_rata = list(
    rata_rata.values()
)

plt.bar(
    metode_nama,
    nilai_rata
)

plt.ylim(
    0,
    105
)

plt.xlabel(
    "Metode Filtering"
)

plt.ylabel(
    "Rata-rata Akurasi (%)"
)

plt.title(
    "Rata-rata Akurasi OCR Setiap Metode Filtering"
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        FOLDER_OCR,
        "grafik_rata_rata_akurasi.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# SELESAI
# ============================================================

print("\n")
print("=" * 60)
print("REKAP SELESAI")
print("=" * 60)

print(
    "\nFile CSV:"
)

print(
    FILE_CSV
)

print(
    "\nGrafik tersimpan di:"
)

print(
    FOLDER_OCR
)