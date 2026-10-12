
import csv
from pathlib import Path

import cv2
import numpy as np

# ============================================================
# KONFIGURASI
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

FOLDER_ASLI = BASE_DIR / "gambar_asli"
FOLDER_ABSENT = BASE_DIR / "HASIL" / "data_absent_simulasi"
FOLDER_OUTPUT = BASE_DIR / "HASIL" / "evaluasi_deteksi"

FOLDER_OUTPUT.mkdir(parents=True, exist_ok=True)

FILE_CSV = FOLDER_OUTPUT / "hasil_evaluasi_deteksi.csv"
FOLDER_MASK = FOLDER_OUTPUT / "hasil_threshold_roi"
FOLDER_MASK.mkdir(parents=True, exist_ok=True)

# Koordinat area tanda tangan pada gambar asli 3506 x 2481
X1, Y1, X2, Y2 = 2232, 1717, 3026, 2014

# Ambang awal untuk area tanda tangan saja.
# Nilai ini harus dievaluasi berdasarkan hasil pengujian.
THRESHOLD = 5.0

EKSTENSI = {".jpg", ".jpeg", ".png", ".bmp"}


# ============================================================
# DETEKSI PADA AREA TANDA TANGAN
# ============================================================

def deteksi_tanda_tangan(path_gambar):
    gambar = cv2.imread(str(path_gambar))

    if gambar is None:
        raise ValueError("Gambar tidak dapat dibaca.")

    tinggi, lebar = gambar.shape[:2]

    if X2 > lebar or Y2 > tinggi:
        raise ValueError(
            f"Dimensi gambar berbeda dari gambar referensi: "
            f"{lebar}x{tinggi}"
        )

    # Potong hanya area tanda tangan.
    roi = gambar[Y1:Y2, X1:X2]

    abu = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(abu, (5, 5), 0)

    _, biner = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = np.ones((2, 2), np.uint8)

    bersih = cv2.morphologyEx(
        biner,
        cv2.MORPH_OPEN,
        kernel
    )

    total_piksel = bersih.shape[0] * bersih.shape[1]
    jumlah_foreground = cv2.countNonZero(bersih)

    persentase = jumlah_foreground / total_piksel * 100

    prediksi = (
        "ADA TANDA TANGAN"
        if persentase >= THRESHOLD
        else "TIDAK ADA TANDA TANGAN"
    )

    return persentase, prediksi, bersih


# ============================================================
# PENGUJIAN
# ============================================================

def ambil_gambar(folder):
    if not folder.exists():
        print(f"[PERINGATAN] Folder tidak ditemukan: {folder}")
        return []

    return sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in EKSTENSI
    )


def main():
    hasil = []

    kelompok = [
        (FOLDER_ASLI, "ADA TANDA TANGAN"),
        (FOLDER_ABSENT, "TIDAK ADA TANDA TANGAN"),
    ]

    print("=" * 70)
    print("EVALUASI DETEKSI PADA AREA TANDA TANGAN")
    print(f"Ambang foreground: {THRESHOLD:.2f}%")
    print("=" * 70)

    for folder, label_asli in kelompok:
        gambar_list = ambil_gambar(folder)

        print(f"\nFolder: {folder}")
        print(f"Jumlah gambar: {len(gambar_list)}")

        for path in gambar_list:
            try:
                persen, prediksi, mask = deteksi_tanda_tangan(path)
                benar = prediksi == label_asli

                nama_mask = f"{path.stem}_ROI_threshold.png"
                cv2.imwrite(str(FOLDER_MASK / nama_mask), mask)

                hasil.append({
                    "nama_gambar": path.name,
                    "label_sebenarnya": label_asli,
                    "foreground_roi_persen": round(persen, 4),
                    "prediksi": prediksi,
                    "status": "BENAR" if benar else "SALAH",
                })

                print(
                    f"{path.name}: "
                    f"foreground ROI={persen:.2f}% | "
                    f"{prediksi} | "
                    f"{'BENAR' if benar else 'SALAH'}"
                )

            except Exception as error:
                print(f"[GAGAL] {path.name}: {error}")

    kolom = [
        "nama_gambar",
        "label_sebenarnya",
        "foreground_roi_persen",
        "prediksi",
        "status",
    ]

    with open(FILE_CSV, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=kolom)
        writer.writeheader()
        writer.writerows(hasil)

    # Label ADA TANDA TANGAN diperlakukan sebagai kelas positif.
    tp = sum(
        r["label_sebenarnya"] == "ADA TANDA TANGAN"
        and r["prediksi"] == "ADA TANDA TANGAN"
        for r in hasil
    )

    fn = sum(
        r["label_sebenarnya"] == "ADA TANDA TANGAN"
        and r["prediksi"] == "TIDAK ADA TANDA TANGAN"
        for r in hasil
    )

    tn = sum(
        r["label_sebenarnya"] == "TIDAK ADA TANDA TANGAN"
        and r["prediksi"] == "TIDAK ADA TANDA TANGAN"
        for r in hasil
    )

    fp = sum(
        r["label_sebenarnya"] == "TIDAK ADA TANDA TANGAN"
        and r["prediksi"] == "ADA TANDA TANGAN"
        for r in hasil
    )

    total = len(hasil)

    akurasi = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    print("\n" + "=" * 70)
    print("RINGKASAN EVALUASI")
    print("=" * 70)
    print(f"Total gambar        : {total}")
    print(f"True Positive (TP)  : {tp}")
    print(f"False Negative (FN) : {fn}")
    print(f"True Negative (TN)  : {tn}")
    print(f"False Positive (FP) : {fp}")
    print(f"Akurasi             : {akurasi * 100:.2f}%")
    print(f"Precision           : {precision * 100:.2f}%")
    print(f"Recall              : {recall * 100:.2f}%")
    print(f"F1-score            : {f1 * 100:.2f}%")
    print(f"\nCSV hasil: {FILE_CSV}")
    print(f"Gambar threshold: {FOLDER_MASK}")
    print("=" * 70)


if __name__ == "__main__":
    main()