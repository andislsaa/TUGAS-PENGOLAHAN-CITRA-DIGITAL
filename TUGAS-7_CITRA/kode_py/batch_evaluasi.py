import csv
import cv2
import numpy as np
import pytesseract
from pathlib import Path

# ============================================================
# 1. KONFIGURASI
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "gambar_asli"
OUTPUT_DIR = BASE_DIR / "HASIL" / "evaluasi_batch"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TEKS_ACUAN = "571012022000056"

METODE_OCR = [
    "Original",
    "Mean",
    "Median",
    "Gaussian",
    "Sharpening"
]

# Ambang dari eksperimen sebelumnya.
# Nilai ini perlu dievaluasi, bukan dianggap pasti optimal.
AMBANG_FOREGROUND = 8.25

# Semua gambar diketahui berisi tanda tangan.
LABEL_AKTUAL_TTD = "PRESENT"

# Ukuran maksimum jendela untuk memilih area crop.
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800

# Jika Tesseract tidak terdeteksi otomatis, hilangkan tanda #
# dan sesuaikan lokasi tesseract.exe di komputer kamu.
# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )


# ============================================================
# 2. FUNGSI MEMILIH AREA CROP
# ============================================================

def pilih_area(gambar, judul):
    tinggi, lebar = gambar.shape[:2]

    # Tampilkan gambar secara utuh dalam ukuran yang lebih kecil.
    # Rasio gambar tetap dipertahankan.
    skala = min(
        1000 / lebar,
        650 / tinggi,
        1.0
    )

    lebar_tampil = int(lebar * skala)
    tinggi_tampil = int(tinggi * skala)

    gambar_tampil = cv2.resize(
        gambar,
        (lebar_tampil, tinggi_tampil),
        interpolation=cv2.INTER_AREA
    )

    # Jendela dibuat dengan ukuran yang sesuai tampilan.
    cv2.namedWindow(
        judul,
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        judul,
        lebar_tampil,
        tinggi_tampil
    )

    print(f"\nPilih area: {judul}")
    print("Tarik kotak pada gambar yang tampil utuh.")
    print("Tekan ENTER atau SPACE untuk menyimpan crop.")
    print("Tekan ESC jika ingin membatalkan.")

    x, y, w, h = cv2.selectROI(
        judul,
        gambar_tampil,
        showCrosshair=True,
        fromCenter=False
    )

    cv2.destroyAllWindows()

    if w == 0 or h == 0:
        raise ValueError(
            f"Area {judul} belum dipilih dengan benar."
        )

    # Konversi koordinat tampilan ke gambar asli.
    x1 = round(x / skala)
    y1 = round(y / skala)
    x2 = round((x + w) / skala)
    y2 = round((y + h) / skala)

    return x1, y1, x2, y2

def crop_area(gambar, koordinat):
    x1, y1, x2, y2 = koordinat

    tinggi, lebar = gambar.shape[:2]

    # Pastikan koordinat tidak keluar dari batas gambar.
    x1 = max(0, min(x1, lebar))
    x2 = max(0, min(x2, lebar))
    y1 = max(0, min(y1, tinggi))
    y2 = max(0, min(y2, tinggi))

    if x2 <= x1 or y2 <= y1:
        return None

    return gambar[y1:y2, x1:x2]


# ============================================================
# 3. FUNGSI FILTER DAN OCR
# ============================================================

def terapkan_filter(gray, metode):
    if metode == "Original":
        hasil = gray.copy()

    elif metode == "Mean":
        hasil = cv2.blur(gray, (3, 3))

    elif metode == "Median":
        hasil = cv2.medianBlur(gray, 3)

    elif metode == "Gaussian":
        hasil = cv2.GaussianBlur(gray, (3, 3), 0)

    elif metode == "Sharpening":
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=np.float32)

        hasil = cv2.filter2D(gray, -1, kernel)

    else:
        raise ValueError(f"Metode tidak dikenal: {metode}")

    return hasil


def jalankan_ocr(area_nomor, metode):
    gray = cv2.cvtColor(
        area_nomor,
        cv2.COLOR_BGR2GRAY
    )

    hasil_filter = terapkan_filter(gray, metode)

    # Semua metode memakai tahap binerisasi yang sama.
    _, biner = cv2.threshold(
        hasil_filter,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    konfigurasi = (
        "--oem 3 --psm 7 "
        "-c tessedit_char_whitelist=0123456789"
    )

    teks = pytesseract.image_to_string(
        biner,
        config=konfigurasi
    )

    # Hanya simpan karakter angka.
    teks = "".join(
        karakter for karakter in teks
        if karakter.isdigit()
    )

    return teks, biner


# ============================================================
# 4. FUNGSI MENGHITUNG EDIT DISTANCE DAN CER
# ============================================================

def edit_distance(teks_acuan, teks_prediksi):
    # Menghitung jumlah operasi substitusi, penghapusan,
    # dan penyisipan untuk mengubah prediksi menjadi teks acuan.
    baris = list(range(len(teks_prediksi) + 1))

    for i, karakter_acuan in enumerate(teks_acuan, start=1):
        baris_baru = [i]

        for j, karakter_prediksi in enumerate(
            teks_prediksi, start=1
        ):
            biaya = (
                0 if karakter_acuan == karakter_prediksi
                else 1
            )

            baris_baru.append(min(
                baris_baru[-1] + 1,
                baris[j] + 1,
                baris[j - 1] + biaya
            ))

        baris = baris_baru

    return baris[-1]


def evaluasi_ocr(teks_acuan, teks_prediksi):
    jarak = edit_distance(teks_acuan, teks_prediksi)

    if len(teks_acuan) > 0:
        cer = jarak / len(teks_acuan) * 100
    else:
        cer = 0.0 if teks_prediksi == "" else 100.0

    cocok_persis = teks_prediksi == teks_acuan

    # Akurasi karakter di sini adalah 100% - CER,
    # dibatasi minimum 0% agar mudah dibaca.
    akurasi_karakter = max(0.0, 100.0 - cer)

    return {
        "edit_distance": jarak,
        "CER_persen": round(cer, 2),
        "akurasi_karakter_persen": round(
            akurasi_karakter, 2
        ),
        "OCR_cocok_persis": (
            "YA" if cocok_persis else "TIDAK"
        )
    }


# ============================================================
# 5. DETEKSI TANDA TANGAN BERDASARKAN FOREGROUND
# ============================================================

def deteksi_tanda_tangan(area_ttd):
    gray = cv2.cvtColor(
        area_ttd,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    _, biner = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = np.ones((2, 2), dtype=np.uint8)

    hasil_morfologi = cv2.morphologyEx(
        biner,
        cv2.MORPH_OPEN,
        kernel
    )

    jumlah_foreground = cv2.countNonZero(
        hasil_morfologi
    )

    jumlah_piksel = (
        hasil_morfologi.shape[0]
        * hasil_morfologi.shape[1]
    )

    persentase = (
        jumlah_foreground / jumlah_piksel * 100
        if jumlah_piksel > 0
        else 0.0
    )

    if persentase >= AMBANG_FOREGROUND:
        prediksi = "PRESENT"
    else:
        prediksi = "ABSENT"

    # Karena semua gambar diketahui berisi tanda tangan,
    # hasil yang diprediksi ABSENT dihitung sebagai miss.
    benar = prediksi == LABEL_AKTUAL_TTD

    return (
        round(persentase, 2),
        prediksi,
        "BENAR" if benar else "SALAH",
        hasil_morfologi
    )


# ============================================================
# 6. MEMUAT GAMBAR DAN MEMILIH AREA PADA GAMBAR PERTAMA
# ============================================================

if not INPUT_DIR.exists():
    raise FileNotFoundError(
        f"Folder gambar tidak ditemukan: {INPUT_DIR}"
    )

daftar_gambar = sorted([
    file for file in INPUT_DIR.iterdir()
    if file.suffix.lower() in [
        ".jpg", ".jpeg", ".png", ".bmp"
    ]
])

if not daftar_gambar:
    raise FileNotFoundError(
        "Tidak ada gambar yang ditemukan di gambar_asli."
    )

gambar_pertama = cv2.imread(str(daftar_gambar[0]))

if gambar_pertama is None:
    raise ValueError(
        f"Gambar gagal dibaca: {daftar_gambar[0].name}"
    )

print("=" * 65)
print("EVALUASI OCR DAN DETEKSI TANDA TANGAN")
print("=" * 65)
print("Jumlah gambar :", len(daftar_gambar))
print("Teks acuan    :", TEKS_ACUAN)
print("Metode OCR    :", ", ".join(METODE_OCR))

koordinat_nomor = pilih_area(
    gambar_pertama,
    "Pilih Nomor Ijazah"
)

koordinat_ttd = pilih_area(
    gambar_pertama,
    "Pilih Area Tanda Tangan"
)

print("\nKoordinat crop berhasil ditentukan.")
print("Nomor ijazah :", koordinat_nomor)
print("Tanda tangan :", koordinat_ttd)


# ============================================================
# 7. MEMPROSES SEMUA GAMBAR
# ============================================================

hasil_ocr_semua = []
hasil_ttd_semua = []

for indeks, file_gambar in enumerate(
    daftar_gambar, start=1
):
    print("\n" + "-" * 65)
    print(f"[{indeks}/{len(daftar_gambar)}] {file_gambar.name}")

    gambar = cv2.imread(str(file_gambar))

    if gambar is None:
        print("Gambar gagal dibaca, dilewati.")
        continue

    area_nomor = crop_area(
        gambar,
        koordinat_nomor
    )

    area_ttd = crop_area(
        gambar,
        koordinat_ttd
    )

    if area_nomor is None or area_ttd is None:
        print("Crop tidak valid, gambar dilewati.")
        continue

    nama = file_gambar.stem

    # Simpan crop untuk memeriksa apakah area yang dipilih tepat.
    cv2.imwrite(
        str(OUTPUT_DIR / f"{nama}_crop_nomor.jpg"),
        area_nomor
    )

    cv2.imwrite(
        str(OUTPUT_DIR / f"{nama}_crop_ttd.jpg"),
        area_ttd
    )

    # --------------------------------------------
    # OCR: evaluasi setiap metode secara independen
    # --------------------------------------------

    for metode in METODE_OCR:
        teks_prediksi, gambar_biner = jalankan_ocr(
            area_nomor,
            metode
        )

        metrik = evaluasi_ocr(
            TEKS_ACUAN,
            teks_prediksi
        )

        hasil_ocr_semua.append({
            "nama_gambar": file_gambar.name,
            "metode": metode,
            "teks_acuan": TEKS_ACUAN,
            "teks_prediksi": teks_prediksi,
            **metrik
        })

        cv2.imwrite(
            str(
                OUTPUT_DIR
                / f"{nama}_OCR_{metode}_threshold.jpg"
            ),
            gambar_biner
        )

        print(
            f"{metode:12} | "
            f"OCR={teks_prediksi or '(kosong)':18} | "
            f"CER={metrik['CER_persen']:6.2f}% | "
            f"Cocok={metrik['OCR_cocok_persis']}"
        )

    # --------------------------------------------
    # Deteksi tanda tangan
    # --------------------------------------------

    foreground, prediksi, evaluasi, biner_ttd = (
        deteksi_tanda_tangan(area_ttd)
    )

    hasil_ttd_semua.append({
        "nama_gambar": file_gambar.name,
        "label_aktual": LABEL_AKTUAL_TTD,
        "foreground_persen": foreground,
        "ambang_foreground_persen": AMBANG_FOREGROUND,
        "prediksi_tanda_tangan": prediksi,
        "evaluasi": evaluasi
    })

    cv2.imwrite(
        str(OUTPUT_DIR / f"{nama}_threshold_ttd.jpg"),
        biner_ttd
    )

    print(
        f"Deteksi tanda tangan | "
        f"Foreground={foreground:.2f}% | "
        f"Prediksi={prediksi} | "
        f"Evaluasi={evaluasi}"
    )


# ============================================================
# 8. SIMPAN CSV DETAIL OCR
# ============================================================

if hasil_ocr_semua:
    file_detail = OUTPUT_DIR / "hasil_ocr_detail.csv"

    with open(
        file_detail,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        kolom = list(hasil_ocr_semua[0].keys())

        writer = csv.DictWriter(
            file,
            fieldnames=kolom
        )

        writer.writeheader()
        writer.writerows(hasil_ocr_semua)

    # Ringkasan berdasarkan metode.
    ringkasan_ocr = []

    for metode in METODE_OCR:
        baris_metode = [
            baris for baris in hasil_ocr_semua
            if baris["metode"] == metode
        ]

        if not baris_metode:
            continue

        jumlah = len(baris_metode)

        jumlah_cocok = sum(
            baris["OCR_cocok_persis"] == "YA"
            for baris in baris_metode
        )

        akurasi_persis = jumlah_cocok / jumlah * 100

        rata_cer = sum(
            baris["CER_persen"]
            for baris in baris_metode
        ) / jumlah

        rata_akurasi_karakter = sum(
            baris["akurasi_karakter_persen"]
            for baris in baris_metode
        ) / jumlah

        ringkasan_ocr.append({
            "metode": metode,
            "jumlah_gambar": jumlah,
            "jumlah_ocr_cocok_persis": jumlah_cocok,
            "akurasi_pencocokan_persis_persen": round(
                akurasi_persis, 2
            ),
            "rata_rata_CER_persen": round(rata_cer, 2),
            "rata_rata_akurasi_karakter_persen": round(
                rata_akurasi_karakter, 2
            )
        })

    file_ringkasan = (
        OUTPUT_DIR / "ringkasan_ocr_per_metode.csv"
    )

    with open(
        file_ringkasan,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        kolom = list(ringkasan_ocr[0].keys())

        writer = csv.DictWriter(
            file,
            fieldnames=kolom
        )

        writer.writeheader()
        writer.writerows(ringkasan_ocr)

    print("\n" + "=" * 65)
    print("RINGKASAN OCR PER METODE")
    print("=" * 65)

    for baris in ringkasan_ocr:
        print(
            f"{baris['metode']:12} | "
            f"Akurasi cocok persis="
            f"{baris['akurasi_pencocokan_persis_persen']:6.2f}% | "
            f"Rata-rata CER="
            f"{baris['rata_rata_CER_persen']:6.2f}%"
        )


# ============================================================
# 9. SIMPAN CSV DETEKSI TANDA TANGAN
# ============================================================

if hasil_ttd_semua:
    file_ttd = (
        OUTPUT_DIR / "hasil_deteksi_tanda_tangan.csv"
    )

    with open(
        file_ttd,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        kolom = list(hasil_ttd_semua[0].keys())

        writer = csv.DictWriter(
            file,
            fieldnames=kolom
        )

        writer.writeheader()
        writer.writerows(hasil_ttd_semua)

    jumlah_ttd = len(hasil_ttd_semua)

    jumlah_terdeteksi = sum(
        baris["prediksi_tanda_tangan"] == "PRESENT"
        for baris in hasil_ttd_semua
    )

    jumlah_miss = sum(
        baris["prediksi_tanda_tangan"] == "ABSENT"
        for baris in hasil_ttd_semua
    )

    sensitivitas = (
        jumlah_terdeteksi / jumlah_ttd * 100
        if jumlah_ttd > 0 else 0
    )

    print("\n" + "=" * 65)
    print("RINGKASAN DETEKSI TANDA TANGAN")
    print("=" * 65)
    print("Jumlah gambar berlabel PRESENT :", jumlah_ttd)
    print("Diprediksi PRESENT             :", jumlah_terdeteksi)
    print("Terlewat (diprediksi ABSENT)    :", jumlah_miss)
    print(f"Sensitivitas / recall           : {sensitivitas:.2f}%")
    print(
        "Catatan: spesifisitas tidak dapat dihitung "
        "karena tidak ada gambar berlabel ABSENT."
    )


# ============================================================
# 10. SELESAI
# ============================================================

print("\n" + "=" * 65)
print("EVALUASI SELESAI")
print("=" * 65)
print("Folder hasil :", OUTPUT_DIR)
print("File OCR detail       : hasil_ocr_detail.csv")
print("Ringkasan OCR         : ringkasan_ocr_per_metode.csv")
print("Hasil deteksi tanda tangan: hasil_deteksi_tanda_tangan.csv")
print("=" * 65)