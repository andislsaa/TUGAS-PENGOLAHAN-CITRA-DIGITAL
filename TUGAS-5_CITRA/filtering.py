import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# FOLDER
# ============================================================

input_folder = "images"
output_folder = "hasil_filtering"

os.makedirs(output_folder, exist_ok=True)


# ============================================================
# MEMBACA GAMBAR
# ============================================================

files = sorted([
    f for f in os.listdir(input_folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

if len(files) == 0:
    print("Tidak ada gambar di folder images!")
    exit()


print("=" * 60)
print("FILTERING, NOISE REDUCTION, DAN SHARPENING")
print("=" * 60)
print(f"Jumlah gambar : {len(files)}")
print()


# ============================================================
# PROSES SETIAP GAMBAR
# ============================================================

for nomor, file in enumerate(files, start=1):

    print("=" * 60)
    print(f"Gambar {nomor}/{len(files)} : {file}")
    print("=" * 60)

    path = os.path.join(input_folder, file)

    img = cv2.imread(path)

    if img is None:
        print("Gagal membaca gambar!")
        continue


    # ========================================================
    # PERKECIL GAMBAR UNTUK MEMUDAHKAN PEMILIHAN CROP
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
    print("Pilih bagian NOMOR IJAZAH.")
    print("1. Klik dan tahan mouse")
    print("2. Drag sampai seluruh nomor terpilih")
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
    # CEK APAKAH CROP DIPILIH
    # ========================================================

    if w_display == 0 or h_display == 0:
        print("Area tidak dipilih.")
        print("Gambar dilewati.")
        continue


    # ========================================================
    # KEMBALIKAN KOORDINAT KE UKURAN GAMBAR ASLI
    # ========================================================

    x = int(x_display / scale)
    y = int(y_display / scale)
    w = int(w_display / scale)
    h = int(h_display / scale)

    crop = img[y:y+h, x:x+w]


    if crop.size == 0:
        print("Crop kosong!")
        continue


    # ========================================================
    # KONVERSI KE GRAYSCALE UNTUK PROSES FILTER
    # ========================================================

    gray = cv2.cvtColor(
        crop,
        cv2.COLOR_BGR2GRAY
    )


    # ========================================================
    # 1. MEAN FILTER
    # ========================================================

    mean_filter = cv2.blur(
        gray,
        (5, 5)
    )


    # ========================================================
    # 2. MEDIAN FILTER
    # ========================================================

    median_filter = cv2.medianBlur(
        gray,
        5
    )


    # ========================================================
    # 3. GAUSSIAN FILTER
    # ========================================================

    gaussian_filter = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )


    # ========================================================
    # 4. SHARPENING
    # ========================================================

    kernel_sharpening = np.array([
        [0, -1,  0],
        [-1, 5, -1],
        [0, -1,  0]
    ])

    sharpening = cv2.filter2D(
        gray,
        -1,
        kernel_sharpening
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
    # SIMPAN HASIL INDIVIDUAL
    # ========================================================

    cv2.imwrite(
        os.path.join(
            folder_gambar,
            "01_original.png"
        ),
        crop
    )

    cv2.imwrite(
        os.path.join(
            folder_gambar,
            "02_mean_filter.png"
        ),
        mean_filter
    )

    cv2.imwrite(
        os.path.join(
            folder_gambar,
            "03_median_filter.png"
        ),
        median_filter
    )

    cv2.imwrite(
        os.path.join(
            folder_gambar,
            "04_gaussian_filter.png"
        ),
        gaussian_filter
    )

    cv2.imwrite(
        os.path.join(
            folder_gambar,
            "05_sharpening.png"
        ),
        sharpening
    )


    # ========================================================
    # PERBANDINGAN SEMUA HASIL
    # ========================================================

    plt.figure(figsize=(14, 10))


    # --------------------------------------------------------
    # ORIGINAL
    # --------------------------------------------------------

    plt.subplot(2, 3, 1)

    plt.imshow(
        cv2.cvtColor(
            crop,
            cv2.COLOR_BGR2RGB
        )
    )

    plt.title(
        "Original",
        fontsize=14
    )

    plt.axis("off")


    # --------------------------------------------------------
    # MEAN FILTER
    # --------------------------------------------------------

    plt.subplot(2, 3, 2)

    plt.imshow(
        mean_filter,
        cmap="gray"
    )

    plt.title(
        "Mean Filter",
        fontsize=14
    )

    plt.axis("off")


    # --------------------------------------------------------
    # MEDIAN FILTER
    # --------------------------------------------------------

    plt.subplot(2, 3, 3)

    plt.imshow(
        median_filter,
        cmap="gray"
    )

    plt.title(
        "Median Filter",
        fontsize=14
    )

    plt.axis("off")


    # --------------------------------------------------------
    # GAUSSIAN FILTER
    # --------------------------------------------------------

    plt.subplot(2, 3, 4)

    plt.imshow(
        gaussian_filter,
        cmap="gray"
    )

    plt.title(
        "Gaussian Filter",
        fontsize=14
    )

    plt.axis("off")


    # --------------------------------------------------------
    # SHARPENING
    # --------------------------------------------------------

    plt.subplot(2, 3, 5)

    plt.imshow(
        sharpening,
        cmap="gray"
    )

    plt.title(
        "Sharpening",
        fontsize=14
    )

    plt.axis("off")


    # --------------------------------------------------------
    # JUDUL
    # --------------------------------------------------------

    plt.suptitle(
        f"Perbandingan Filtering dan Sharpening\n{nama_dasar}",
        fontsize=18
    )

    plt.tight_layout()


    # ========================================================
    # SIMPAN GAMBAR PERBANDINGAN
    # ========================================================

    plt.savefig(
        os.path.join(
            folder_gambar,
            "00_perbandingan_semua_metode.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )


    # ========================================================
    # TAMPILKAN HASIL
    # ========================================================

    plt.show()

    plt.close()


    # ========================================================
    # SELESAI SATU GAMBAR
    # ========================================================

    print()
    print("✓ Berhasil diproses")
    print(f"✓ Hasil disimpan di:")
    print(f"  {folder_gambar}")
    print()


# ============================================================
# SELESAI
# ============================================================

print("=" * 60)
print("SEMUA GAMBAR SELESAI DIPROSES")
print("=" * 60)

print()
print("Folder hasil:")
print(os.path.abspath(output_folder))