import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# FOLDER INPUT DAN OUTPUT
# ============================================================

input_folder = "images"
output_folder = "hasil_ocr"

os.makedirs(output_folder, exist_ok=True)


# ============================================================
# MEMBACA SEMUA GAMBAR
# ============================================================

files = sorted([
    f for f in os.listdir(input_folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])


if len(files) == 0:
    print("Tidak ada gambar di folder images!")
    exit()


print("=" * 70)
print("ANALISIS ENHANCEMENT AREA NOMOR IJAZAH")
print("=" * 70)
print(f"Jumlah gambar : {len(files)}")
print()


# ============================================================
# PROSES SEMUA GAMBAR
# ============================================================

for nomor, file in enumerate(files, start=1):

    print("=" * 70)
    print(f"Memproses {nomor}/{len(files)} : {file}")
    print("=" * 70)


    # ========================================================
    # MEMBACA GAMBAR
    # ========================================================

    path = os.path.join(input_folder, file)

    img = cv2.imread(path)


    if img is None:
        print("Gagal membaca gambar!")
        continue


    # ========================================================
    # MENGECILKAN GAMBAR UNTUK PROSES PEMILIHAN AREA
    # ========================================================

    tinggi, lebar = img.shape[:2]

    max_width = 1200
    max_height = 700


    scale = min(
        max_width / lebar,
        max_height / tinggi,
        1.0
    )


    display_img = cv2.resize(
        img,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_AREA
    )


    # ========================================================
    # PILIH AREA NOMOR IJAZAH
    # ========================================================

    print()
    print("Pilih area NOMOR IJAZAH.")
    print("1. Klik dan tahan mouse")
    print("2. Drag pada bagian nomor ijazah")
    print("3. Lepaskan mouse")
    print("4. Tekan ENTER")
    print()


    roi = cv2.selectROI(
        f"Pilih Nomor Ijazah - {file}",
        display_img,
        showCrosshair=True,
        fromCenter=False
    )


    cv2.destroyAllWindows()


    x_display, y_display, w_display, h_display = roi


    # ========================================================
    # JIKA TIDAK MEMILIH AREA
    # ========================================================

    if w_display == 0 or h_display == 0:

        print("Area tidak dipilih.")
        print("Gambar dilewati.")
        continue


    # ========================================================
    # MENGEMBALIKAN KOORDINAT KE UKURAN GAMBAR ASLI
    # ========================================================

    x = int(x_display / scale)
    y = int(y_display / scale)

    w = int(w_display / scale)
    h = int(h_display / scale)


    # ========================================================
    # CROP AREA NOMOR IJAZAH
    # ========================================================

    crop = img[
        y:y + h,
        x:x + w
    ]


    if crop.size == 0:

        print("Crop kosong!")
        continue


    # ========================================================
    # KONVERSI INTERNAL KE GRAYSCALE
    #
    # Grayscale hanya digunakan untuk proses enhancement.
    # Tidak ditampilkan sebagai hasil terpisah.
    # ========================================================

    gray = cv2.cvtColor(
        crop,
        cv2.COLOR_BGR2GRAY
    )


    # ========================================================
    # METODE 1
    # BRIGHTNESS ADJUSTMENT
    # ========================================================

    brightness = cv2.convertScaleAbs(
        gray,
        alpha=1.0,
        beta=30
    )


    # ========================================================
    # METODE 2
    # CONTRAST STRETCHING
    # ========================================================

    minimum = np.min(gray)
    maximum = np.max(gray)


    if maximum > minimum:

        contrast_stretching = (
            (gray.astype(np.float32) - minimum)
            * 255
            / (maximum - minimum)
        ).astype(np.uint8)

    else:

        contrast_stretching = gray.copy()


    # ========================================================
    # METODE 3
    # HISTOGRAM EQUALIZATION
    # ========================================================

    histogram_equalization = cv2.equalizeHist(
        gray
    )


    # ========================================================
    # NAMA FOLDER HASIL
    # ========================================================

    nama_dasar = os.path.splitext(file)[0]


    folder_gambar = os.path.join(
        output_folder,
        nama_dasar
    )


    os.makedirs(
        folder_gambar,
        exist_ok=True
    )


    # ========================================================
    # SIMPAN CITRA SEBELUM ENHANCEMENT
    # ========================================================

    cv2.imwrite(
        os.path.join(
            folder_gambar,
            "sebelum_enhancement.png"
        ),
        crop
    )


    # ========================================================
    # SIMPAN HASIL BRIGHTNESS
    # ========================================================

    cv2.imwrite(
        os.path.join(
            folder_gambar,
            "brightness_adjustment.png"
        ),
        brightness
    )


    # ========================================================
    # SIMPAN HASIL CONTRAST STRETCHING
    # ========================================================

    cv2.imwrite(
        os.path.join(
            folder_gambar,
            "contrast_stretching.png"
        ),
        contrast_stretching
    )


    # ========================================================
    # SIMPAN HASIL HISTOGRAM EQUALIZATION
    # ========================================================

    cv2.imwrite(
        os.path.join(
            folder_gambar,
            "histogram_equalization.png"
        ),
        histogram_equalization
    )


    # ========================================================
    # ========================================================
    # PERBANDINGAN CITRA
    # SEBELUM + 3 METODE ENHANCEMENT
    # ========================================================
    # ========================================================

    plt.figure(figsize=(16, 10))


    # --------------------------------------------------------
    # 1. SEBELUM ENHANCEMENT
    # --------------------------------------------------------

    plt.subplot(2, 2, 1)

    plt.imshow(
        cv2.cvtColor(
            crop,
            cv2.COLOR_BGR2RGB
        )
    )

    plt.title(
        "Sebelum Enhancement",
        fontsize=14
    )

    plt.axis("off")


    # --------------------------------------------------------
    # 2. BRIGHTNESS ADJUSTMENT
    # --------------------------------------------------------

    plt.subplot(2, 2, 2)

    plt.imshow(
        brightness,
        cmap="gray"
    )

    plt.title(
        "Brightness Adjustment",
        fontsize=14
    )

    plt.axis("off")


    # --------------------------------------------------------
    # 3. CONTRAST STRETCHING
    # --------------------------------------------------------

    plt.subplot(2, 2, 3)

    plt.imshow(
        contrast_stretching,
        cmap="gray"
    )

    plt.title(
        "Contrast Stretching",
        fontsize=14
    )

    plt.axis("off")


    # --------------------------------------------------------
    # 4. HISTOGRAM EQUALIZATION
    # --------------------------------------------------------

    plt.subplot(2, 2, 4)

    plt.imshow(
        histogram_equalization,
        cmap="gray"
    )

    plt.title(
        "Histogram Equalization",
        fontsize=14
    )

    plt.axis("off")


    # --------------------------------------------------------
    # JUDUL UTAMA
    # --------------------------------------------------------

    plt.suptitle(
        "Perbandingan Sebelum dan Sesudah Enhancement\n"
        + nama_dasar,
        fontsize=17
    )


    plt.tight_layout()


    # ========================================================
    # SIMPAN GAMBAR PERBANDINGAN CITRA
    # ========================================================

    plt.savefig(
        os.path.join(
            folder_gambar,
            "01_perbandingan_citra.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )


    plt.close()


    # ========================================================
    # ========================================================
    # PERBANDINGAN HISTOGRAM
    # SEBELUM + 3 METODE ENHANCEMENT
    # ========================================================
    # ========================================================

    plt.figure(figsize=(16, 10))


    # --------------------------------------------------------
    # 1. HISTOGRAM SEBELUM ENHANCEMENT
    # --------------------------------------------------------

    plt.subplot(2, 2, 1)

    plt.hist(
        gray.ravel(),
        bins=256,
        range=(0, 256)
    )

    plt.title(
        "Histogram Sebelum Enhancement",
        fontsize=13
    )

    plt.xlabel("Intensitas Piksel")
    plt.ylabel("Jumlah Piksel")


    # --------------------------------------------------------
    # 2. HISTOGRAM BRIGHTNESS
    # --------------------------------------------------------

    plt.subplot(2, 2, 2)

    plt.hist(
        brightness.ravel(),
        bins=256,
        range=(0, 256)
    )

    plt.title(
        "Histogram Brightness Adjustment",
        fontsize=13
    )

    plt.xlabel("Intensitas Piksel")
    plt.ylabel("Jumlah Piksel")


    # --------------------------------------------------------
    # 3. HISTOGRAM CONTRAST STRETCHING
    # --------------------------------------------------------

    plt.subplot(2, 2, 3)

    plt.hist(
        contrast_stretching.ravel(),
        bins=256,
        range=(0, 256)
    )

    plt.title(
        "Histogram Contrast Stretching",
        fontsize=13
    )

    plt.xlabel("Intensitas Piksel")
    plt.ylabel("Jumlah Piksel")


    # --------------------------------------------------------
    # 4. HISTOGRAM EQUALIZATION
    # --------------------------------------------------------

    plt.subplot(2, 2, 4)

    plt.hist(
        histogram_equalization.ravel(),
        bins=256,
        range=(0, 256)
    )

    plt.title(
        "Histogram Histogram Equalization",
        fontsize=13
    )

    plt.xlabel("Intensitas Piksel")
    plt.ylabel("Jumlah Piksel")


    # --------------------------------------------------------
    # JUDUL UTAMA
    # --------------------------------------------------------

    plt.suptitle(
        "Perbandingan Histogram\n"
        + nama_dasar,
        fontsize=17
    )


    plt.tight_layout()


    # ========================================================
    # SIMPAN GAMBAR PERBANDINGAN HISTOGRAM
    # ========================================================

    plt.savefig(
        os.path.join(
            folder_gambar,
            "02_perbandingan_histogram.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )


    plt.close()


    # ========================================================
    # INFORMASI HASIL
    # ========================================================

    print()
    print("✓ Berhasil diproses")
    print()
    print("Hasil disimpan di:")
    print(os.path.abspath(folder_gambar))
    print()


# ============================================================
# SELESAI
# ============================================================

print("=" * 70)
print("SEMUA GAMBAR SELESAI DIPROSES")
print("=" * 70)

print()
print("Semua hasil tersimpan di:")
print(os.path.abspath(output_folder))
print()