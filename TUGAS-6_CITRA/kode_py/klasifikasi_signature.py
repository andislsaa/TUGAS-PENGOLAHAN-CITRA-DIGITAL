import csv

# ==========================================================
# DATA PRESENT
# ==========================================================

data_present = [
    ("01_HighQuality_Enhanced", 8.53),
    ("02_LowContrast", 8.55),
    ("03_Blurred", 11.71),
    ("04_HighNoise", 8.41),
    ("05_LowResolution_Upsampled", 9.24),
    ("06_Faded_Underexposed", 8.60),
    ("07_ColorShift_WarmTint", 8.55),
    ("08_JPEGCompression_Artifacts", 8.52),
    ("09_CombinedDegradation", 9.00),
]

# ==========================================================
# DATA ABSENT
# ==========================================================

data_absent = [
    ("01_HighQuality_Enhanced", 0.05),
    ("02_LowContrast", 8.10),
    ("03_Blurred", 0.09),
    ("04_HighNoise", 6.36),
    ("05_LowResolution_Upsampled", 0.06),
    ("06_Faded_Underexposed", 8.10),
    ("07_ColorShift_WarmTint", 8.10),
    ("08_JPEGCompression_Artifacts", 0.05),
    ("09_CombinedDegradation", 8.10),
]

# ==========================================================
# THRESHOLD KLASIFIKASI
# ==========================================================

THRESHOLD = 8.25

# ==========================================================
# HASIL
# ==========================================================

hasil = []

print("=" * 100)
print("KLASIFIKASI KEBERADAAN TANDA TANGAN")
print("=" * 100)

print()
print(f"Threshold klasifikasi : {THRESHOLD:.2f}%")
print()

print("-" * 100)
print(
    f"{'No':<4}"
    f"{'Kondisi':<35}"
    f"{'Aktual':<15}"
    f"{'Foreground %':<18}"
    f"{'Prediksi':<20}"
    f"{'Status'}"
)
print("-" * 100)

nomor = 1

# ==========================================================
# PROSES PRESENT
# ==========================================================

for nama, persentase in data_present:

    if persentase >= THRESHOLD:
        prediksi = "SIGNATURE PRESENT"
    else:
        prediksi = "SIGNATURE ABSENT"

    aktual = "SIGNATURE PRESENT"

    benar = prediksi == aktual

    if benar:
        status = "BENAR"
    else:
        status = "SALAH"

    hasil.append([
        nomor,
        nama,
        aktual,
        persentase,
        prediksi,
        status
    ])

    print(
        f"{nomor:<4}"
        f"{nama:<35}"
        f"{aktual:<15}"
        f"{persentase:<18.2f}"
        f"{prediksi:<20}"
        f"{status}"
    )

    nomor += 1

# ==========================================================
# PROSES ABSENT
# ==========================================================

for nama, persentase in data_absent:

    if persentase >= THRESHOLD:
        prediksi = "SIGNATURE PRESENT"
    else:
        prediksi = "SIGNATURE ABSENT"

    aktual = "SIGNATURE ABSENT"

    benar = prediksi == aktual

    if benar:
        status = "BENAR"
    else:
        status = "SALAH"

    hasil.append([
        nomor,
        nama,
        aktual,
        persentase,
        prediksi,
        status
    ])

    print(
        f"{nomor:<4}"
        f"{nama:<35}"
        f"{aktual:<15}"
        f"{persentase:<18.2f}"
        f"{prediksi:<20}"
        f"{status}"
    )

    nomor += 1

# ==========================================================
# HITUNG AKURASI
# ==========================================================

jumlah_data = len(hasil)

jumlah_benar = sum(
    1 for row in hasil
    if row[5] == "BENAR"
)

jumlah_salah = jumlah_data - jumlah_benar

akurasi = (
    jumlah_benar / jumlah_data
) * 100

# ==========================================================
# CONFUSION MATRIX
# ==========================================================

TP = 0
TN = 0
FP = 0
FN = 0

for row in hasil:

    aktual = row[2]
    prediksi = row[4]

    if aktual == "SIGNATURE PRESENT" and prediksi == "SIGNATURE PRESENT":
        TP += 1

    elif aktual == "SIGNATURE ABSENT" and prediksi == "SIGNATURE ABSENT":
        TN += 1

    elif aktual == "SIGNATURE ABSENT" and prediksi == "SIGNATURE PRESENT":
        FP += 1

    elif aktual == "SIGNATURE PRESENT" and prediksi == "SIGNATURE ABSENT":
        FN += 1

# ==========================================================
# TAMPILKAN HASIL AKHIR
# ==========================================================

print()
print("=" * 100)
print("HASIL EVALUASI")
print("=" * 100)

print()
print("Jumlah data       :", jumlah_data)
print("Prediksi benar    :", jumlah_benar)
print("Prediksi salah    :", jumlah_salah)

print()
print(f"Akurasi            : {akurasi:.2f}%")

print()
print("Confusion Matrix:")
print()
print("True Positive (TP) :", TP)
print("True Negative (TN) :", TN)
print("False Positive (FP):", FP)
print("False Negative (FN):", FN)

# ==========================================================
# SIMPAN CSV
# ==========================================================

csv_file = "hasil_klasifikasi_signature.csv"

with open(
    csv_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "No",
        "Kondisi",
        "Aktual",
        "Persentase Foreground",
        "Prediksi",
        "Status"
    ])

    for row in hasil:
        writer.writerow(row)

print()
print("=" * 100)
print("SELESAI")
print("=" * 100)

print()
print("Hasil disimpan:")
print(csv_file)