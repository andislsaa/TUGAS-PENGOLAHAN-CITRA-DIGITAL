import os
import cv2
import matplotlib.pyplot as plt

# ==========================================
# Folder input dan output
# ==========================================
input_folder = "images"
output_folder = "hasil"

os.makedirs(output_folder, exist_ok=True)

# Membaca semua gambar
files = sorted([
    f for f in os.listdir(input_folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

print("="*40)
print("Jumlah gambar :", len(files))
print("="*40)

for file in files:

    path = os.path.join(input_folder, file)

    # Membaca gambar
    img = cv2.imread(path)

    if img is None:
        print(f"Gagal membaca {file}")
        continue

    # BGR -> RGB
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # RGB -> Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # -----------------------------
    # Simpan grayscale
    # -----------------------------
    gray_name = os.path.join(output_folder, "gray_" + file)
    cv2.imwrite(gray_name, gray)

    # -----------------------------
    # Membuat Figure
    # -----------------------------
    plt.figure(figsize=(12,8))

    # Citra Asli
    plt.subplot(2,2,1)
    plt.imshow(rgb)
    plt.title("Citra Asli")
    plt.axis("off")

    # Grayscale
    plt.subplot(2,2,2)
    plt.imshow(gray, cmap='gray')
    plt.title("Grayscale")
    plt.axis("off")

    # Histogram RGB
    plt.subplot(2,2,3)

    colors = ('r','g','b')

    for i, c in enumerate(colors):
        hist = cv2.calcHist([rgb],[i],None,[256],[0,256])
        plt.plot(hist,color=c)

    plt.title("Histogram RGB")
    plt.xlabel("Intensitas")
    plt.ylabel("Jumlah Piksel")
    plt.xlim([0,256])

    # Histogram Grayscale
    plt.subplot(2,2,4)

    plt.hist(gray.ravel(),
             bins=256,
             range=(0,256),
             color='black')

    plt.title("Histogram Grayscale")
    plt.xlabel("Intensitas")
    plt.ylabel("Jumlah Piksel")

    plt.tight_layout()

    # Simpan hasil
    save_name = os.path.join(
        output_folder,
        file.replace(".jpg","_hasil.png")
    )

    plt.savefig(save_name, dpi=300)
    plt.close()

    print(f"✓ {file} selesai diproses")

print("="*40)
print("SEMUA GAMBAR BERHASIL DIPROSES")
print("Hasil tersimpan pada folder 'hasil'")
print("="*40)