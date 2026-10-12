# Deteksi Keberadaan Tanda Tangan pada Ijazah

## 📌 Deskripsi

Mini project ini merupakan implementasi pengolahan citra digital untuk mendeteksi keberadaan tanda tangan kepala sekolah/dekan pada area tanda tangan ijazah.

Proses dilakukan dengan memanfaatkan beberapa teknik pengolahan citra, yaitu:

1. Crop area tanda tangan
2. Konversi citra menjadi grayscale
3. Thresholding menggunakan metode Otsu
4. Operasi morfologi opening
5. Operasi morfologi closing
6. Perhitungan jumlah piksel foreground
7. Penentuan aturan klasifikasi `SIGNATURE PRESENT` atau `SIGNATURE ABSENT`
8. Pengujian menggunakan citra dengan tanda tangan dan citra simulasi tanpa tanda tangan

Project dibuat menggunakan bahasa pemrograman **Python** dan library **OpenCV**.

---

# 🎯 Tujuan

Tujuan dari mini project ini adalah:

* Memahami proses segmentasi citra menggunakan thresholding.
* Membandingkan hasil segmentasi pada beberapa kondisi citra.
* Menggunakan operasi morfologi untuk memperbaiki hasil segmentasi.
* Menghitung karakteristik area hasil segmentasi berupa jumlah piksel foreground.
* Membuat aturan sederhana untuk menentukan keberadaan tanda tangan.
* Menguji sistem pada citra yang memiliki tanda tangan dan citra yang tidak memiliki tanda tangan.
* Menghitung akurasi sistem berdasarkan hasil klasifikasi.

---

# 🛠️ Teknologi yang Digunakan

Project ini menggunakan:

* **Python 3.13**
* **OpenCV**
* **NumPy**
* **CSV**
* **Visual Studio Code**
* **Git dan GitHub**

---

# 📁 Struktur Folder

Struktur folder utama project:

```text
TUGAS-6-CITRA/
│
├── hasil_crop/
│
├── hasil_threshold/
│   ├── global/
│   ├── otsu/
│   └── adaptive/
│
├── hasil_morphology/
│   ├── opening/
│   ├── closing/
│   └── opening_closing/
│
├── data_absent_simulasi/
│
├── absent_grayscale/
├── absent_threshold/
├── absent_morphology/
│
├── crop_tanda_tangan.py
├── grayscale.py
├── threshold.py
├── morphology.py
├── hitung_foreground.py
├── buat_data_absent.py
├── proses_absent.py
├── klasifikasi_signature.py
│
├── hasil_foreground.csv
├── hasil_foreground_absent.csv
├── hasil_klasifikasi_signature.csv
│
└── README.md
```

---

# 📷 Dataset

Dataset terdiri dari **9 citra ijazah** yang memiliki karakteristik berbeda.

Perbedaan citra terdiri dari:

1. `01_HighQuality_Enhanced`
2. `02_LowContrast`
3. `03_Blurred`
4. `04_HighNoise`
5. `05_LowResolution_Upsampled`
6. `06_Faded_Underexposed`
7. `07_ColorShift_WarmTint`
8. `08_JPEGCompression_Artifacts`
9. `09_CombinedDegradation`

Kesembilan citra tersebut memiliki area tanda tangan yang sama, tetapi kondisi kualitas dan warna citranya berbeda.

---

# 🔄 Alur Pemrosesan

Alur utama sistem:

```text
Citra Ijazah
     │
     ▼
Crop Area Tanda Tangan
     │
     ▼
Grayscale
     │
     ▼
Thresholding
(Otsu)
     │
     ▼
Morphological Operation
     │
     ├── Opening
     │
     └── Closing
     │
     ▼
Hitung Foreground
     │
     ▼
Persentase Foreground
     │
     ▼
Klasifikasi
     │
     ├── SIGNATURE PRESENT
     │
     └── SIGNATURE ABSENT
```

---

# 1. Crop Area Tanda Tangan

Tahap pertama adalah mengambil area tanda tangan dari citra ijazah.

Program:

```text
crop_tanda_tangan.py
```

Hasil crop disimpan pada:

```text
hasil_crop/
```

Setiap citra menghasilkan satu area crop tanda tangan.

Contoh:

```text
01_crop_01_HighQuality_Enhanced.jpg
02_crop_02_LowContrast.jpg
03_crop_03_Blurred.jpg
...
09_crop_09_CombinedDegradation.jpg
```

Crop dilakukan agar proses selanjutnya hanya berfokus pada area tanda tangan.

---

# 2. Konversi Grayscale

Setelah proses crop, citra dikonversi dari citra berwarna menjadi grayscale.

Grayscale digunakan karena thresholding tidak membutuhkan informasi warna RGB secara langsung.

Secara umum, grayscale memiliki rentang intensitas:

```text
0   = hitam
255 = putih
```

Hasil grayscale digunakan sebagai input untuk proses thresholding.

---

# 3. Thresholding

Thresholding digunakan untuk memisahkan foreground dan background.

Pada project ini digunakan beberapa metode thresholding:

* Global Threshold
* Otsu Threshold
* Adaptive Threshold

Namun, untuk proses klasifikasi utama digunakan hasil:

```text
Otsu Threshold
```

Otsu menentukan nilai threshold secara otomatis berdasarkan distribusi intensitas citra.

Hasil thresholding berupa citra biner:

```text
Hitam = foreground
Putih = background
```

Program:

```text
threshold.py
```

Hasil disimpan pada:

```text
hasil_threshold/
```

---

# 4. Morphological Operation

Setelah thresholding, dilakukan operasi morfologi untuk memperbaiki hasil segmentasi.

Operasi yang digunakan:

## Opening

Opening dilakukan dengan urutan:

```text
Erosion → Dilation
```

Opening digunakan untuk mengurangi noise kecil dan objek kecil yang tidak diperlukan.

## Closing

Closing dilakukan dengan urutan:

```text
Dilation → Erosion
```

Closing digunakan untuk mengisi celah kecil dan menghubungkan bagian foreground yang terputus.

Program:

```text
morphology.py
```

Hasil disimpan pada:

```text
hasil_morphology/
```

Strukturnya:

```text
hasil_morphology/
├── opening/
├── closing/
└── opening_closing/
```

Pada eksperimen digunakan kernel:

```text
3 × 3
```

---

# 5. Perhitungan Foreground

Setelah operasi morfologi, jumlah piksel foreground dihitung.

Foreground didefinisikan sebagai piksel berwarna hitam pada citra hasil segmentasi.

Program:

```text
hitung_foreground.py
```

Total piksel setiap citra:

```text
281052 piksel
```

Persentase foreground dihitung menggunakan rumus:

```text
Persentase Foreground =
(Jumlah Foreground / Total Piksel) × 100%
```

---

# 6. Hasil Foreground Citra PRESENT

Hasil pengolahan 9 citra yang memiliki tanda tangan:

| No | Kondisi                    | Foreground | Persentase |
| -: | -------------------------- | ---------: | ---------: |
|  1 | HighQuality Enhanced       |     23.986 |      8,53% |
|  2 | LowContrast                |     24.032 |      8,55% |
|  3 | Blurred                    |     32.923 |     11,71% |
|  4 | HighNoise                  |     23.648 |      8,41% |
|  5 | LowResolution Upsampled    |     25.966 |      9,24% |
|  6 | Faded Underexposed         |     24.169 |      8,60% |
|  7 | ColorShift WarmTint        |     24.038 |      8,55% |
|  8 | JPEG Compression Artifacts |     23.956 |      8,52% |
|  9 | Combined Degradation       |     25.306 |      9,00% |

Nilai foreground terendah pada kelompok `PRESENT` adalah:

```text
8,41%
```

Nilai tertinggi adalah:

```text
11,71%
```

---

# 7. Pembuatan Data SIGNATURE ABSENT

Dataset awal hanya memiliki citra yang mempunyai tanda tangan.

Untuk melakukan pengujian klasifikasi `SIGNATURE PRESENT` dan `SIGNATURE ABSENT`, dibuat 9 citra `ABSENT` simulasi.

Program:

```text
buat_data_absent.py
```

Area tanda tangan pada crop dihapus dengan menggantinya menjadi warna putih.

Hasil disimpan pada:

```text
data_absent_simulasi/
```

Data tersebut merupakan **data simulasi**, bukan foto ijazah asli yang sejak awal tidak memiliki tanda tangan.

Hal ini penting karena hasil akurasi harus dipahami sesuai dengan jenis dataset yang digunakan.

---

# 8. Pemrosesan Data ABSENT

Data ABSENT kemudian diproses menggunakan metode yang sama dengan data PRESENT.

Alurnya:

```text
ABSENT
  ↓
Grayscale
  ↓
Otsu Threshold
  ↓
Opening
  ↓
Closing
  ↓
Foreground
```

Program:

```text
proses_absent.py
```

Hasil disimpan pada:

```text
absent_grayscale/
absent_threshold/
absent_morphology/
```

---

# 9. Hasil Foreground Citra ABSENT

Hasil pengolahan data simulasi tanpa tanda tangan:

| No | Kondisi                    | Foreground | Persentase |
| -: | -------------------------- | ---------: | ---------: |
|  1 | HighQuality Enhanced       |        127 |      0,05% |
|  2 | LowContrast                |     22.752 |      8,10% |
|  3 | Blurred                    |        250 |      0,09% |
|  4 | HighNoise                  |     17.888 |      6,36% |
|  5 | LowResolution Upsampled    |        157 |      0,06% |
|  6 | Faded Underexposed         |     22.753 |      8,10% |
|  7 | ColorShift WarmTint        |     22.753 |      8,10% |
|  8 | JPEG Compression Artifacts |        134 |      0,05% |
|  9 | Combined Degradation       |     22.753 |      8,10% |

Nilai foreground tertinggi pada kelompok `ABSENT` adalah:

```text
8,10%
```

---

# 10. Aturan Klasifikasi

Berdasarkan hasil eksperimen, nilai foreground tertinggi pada data ABSENT adalah:

```text
8,10%
```

Sedangkan nilai foreground terendah pada data PRESENT adalah:

```text
8,41%
```

Nilai batas klasifikasi ditentukan dari titik tengah kedua nilai tersebut:

```text
(8,10 + 8,41) / 2
= 8,255%
```

Kemudian digunakan threshold klasifikasi:

```text
8,25%
```

Aturan klasifikasi:

```text
Jika persentase foreground >= 8,25%
    → SIGNATURE PRESENT

Jika persentase foreground < 8,25%
    → SIGNATURE ABSENT
```

Aturan tersebut digunakan dalam program:

```text
klasifikasi_signature.py
```

---

# 11. Hasil Klasifikasi

Pengujian dilakukan terhadap:

```text
9 citra PRESENT
+
9 citra ABSENT simulasi
=
18 citra
```

Hasil klasifikasi:

```text
Jumlah data       : 18
Prediksi benar    : 18
Prediksi salah    : 0
```

Dengan demikian:

```text
Akurasi = 18 / 18 × 100%
        = 100%
```

---

# 12. Confusion Matrix

Hasil confusion matrix:

|                | Predicted PRESENT | Predicted ABSENT |
| -------------- | ----------------: | ---------------: |
| Actual PRESENT |                 9 |                0 |
| Actual ABSENT  |                 0 |                9 |

Keterangan:

```text
True Positive  (TP) = 9
True Negative  (TN) = 9
False Positive (FP) = 0
False Negative (FN) = 0
```

Akurasi:

```text
100,00%
```

Artinya seluruh 18 citra pada dataset pengujian berhasil diklasifikasikan sesuai label yang digunakan.

---

# 13. Instalasi

## Persyaratan

Pastikan Python sudah terinstall.

Cek versi Python:

```powershell
python --version
```

atau:

```powershell
py --version
```

Project ini dikembangkan menggunakan Python 3.13.

---

## Install Library

Buka PowerShell pada folder project:

```powershell
cd C:\Users\HP\TUGAS-6-CITRA
```

Kemudian install OpenCV dan NumPy:

```powershell
pip install opencv-python numpy
```

Jika menggunakan Python tertentu:

```powershell
python -m pip install opencv-python numpy
```

---

# 14. Cara Menjalankan Program

## Langkah 1 — Crop

Jalankan:

```powershell
python crop_tanda_tangan.py
```

Tujuan:

```text
Mengambil area tanda tangan dari citra ijazah.
```

Output:

```text
hasil_crop/
```

---

## Langkah 2 — Grayscale

Jalankan:

```powershell
python grayscale.py
```

Tujuan:

```text
Mengubah citra crop menjadi grayscale.
```

---

## Langkah 3 — Thresholding

Jalankan:

```powershell
python threshold.py
```

Program menghasilkan beberapa metode thresholding:

```text
Global Threshold
Otsu Threshold
Adaptive Threshold
```

Hasil disimpan pada:

```text
hasil_threshold/
```

Untuk proses klasifikasi selanjutnya digunakan:

```text
Otsu Threshold
```

---

## Langkah 4 — Morphology

Jalankan:

```powershell
python morphology.py
```

Operasi yang dilakukan:

```text
Opening
Closing
```

dan kombinasi:

```text
Opening → Closing
```

Hasil:

```text
hasil_morphology/
```

---

## Langkah 5 — Hitung Foreground

Jalankan:

```powershell
python hitung_foreground.py
```

Program menghitung:

* total piksel
* jumlah foreground
* persentase foreground

Output:

```text
hasil_foreground.csv
```

---

# 15. Membuat Data ABSENT

Karena dataset awal hanya memiliki citra dengan tanda tangan, dibuat data ABSENT simulasi.

Jalankan:

```powershell
python buat_data_absent.py
```

Program akan meminta koordinat area tanda tangan.

Pada eksperimen ini digunakan:

```text
x1 = 0
y1 = 0
x2 = 820
y2 = 315
```

Hasil:

```text
data_absent_simulasi/
```

---

# 16. Memproses Data ABSENT

Jalankan:

```powershell
python proses_absent.py
```

Program melakukan:

```text
Grayscale
Otsu Threshold
Opening
Closing
Foreground
```

Hasil:

```text
absent_grayscale/
absent_threshold/
absent_morphology/
hasil_foreground_absent.csv
```

---

# 17. Menjalankan Klasifikasi

Setelah data PRESENT dan ABSENT tersedia, jalankan:

```powershell
python klasifikasi_signature.py
```

Program akan:

1. Membaca persentase foreground.
2. Menggunakan threshold klasifikasi 8,25%.
3. Menentukan `SIGNATURE PRESENT` atau `SIGNATURE ABSENT`.
4. Membandingkan hasil dengan label aktual.
5. Menghitung jumlah prediksi benar dan salah.
6. Menghitung akurasi.
7. Menghitung confusion matrix.

Output:

```text
hasil_klasifikasi_signature.csv
```

---

# 18. Analisis

## 18.1 Mengapa thresholding diperlukan sebelum melakukan analisis keberadaan tanda tangan?

Thresholding diperlukan untuk memisahkan foreground dan background pada citra.

Citra grayscale masih memiliki berbagai nilai intensitas sehingga bagian tanda tangan dan background belum terpisah secara jelas.

Dengan thresholding, citra grayscale diubah menjadi citra biner. Pada project ini, piksel gelap dianggap sebagai foreground dan piksel terang sebagai background.

Hasil segmentasi tersebut memungkinkan jumlah piksel foreground dihitung. Jumlah dan persentase foreground kemudian digunakan sebagai karakteristik untuk menentukan apakah area tanda tangan terdeteksi atau tidak.

Metode Otsu digunakan karena dapat menentukan nilai threshold secara otomatis berdasarkan distribusi intensitas citra.

---

## 18.2 Apa masalah yang terjadi jika threshold terlalu tinggi atau terlalu rendah?

Jika threshold terlalu tinggi, terlalu banyak piksel dapat dianggap sebagai foreground. Akibatnya, noise atau bagian background yang bukan tanda tangan dapat ikut terdeteksi.

Sebaliknya, jika threshold terlalu rendah, sebagian piksel tanda tangan dapat dianggap sebagai background. Akibatnya, bentuk tanda tangan dapat menjadi terputus atau bahkan sebagian besar hilang.

Dengan demikian, nilai threshold memengaruhi kualitas segmentasi dan jumlah foreground yang dihasilkan.

Pada project ini, thresholding Otsu digunakan pada tahap segmentasi, sedangkan nilai **8,25%** digunakan sebagai batas klasifikasi berdasarkan persentase foreground hasil eksperimen.

---

# 19. Kesimpulan

Berdasarkan eksperimen yang dilakukan, proses pengolahan citra dapat digunakan untuk membuat klasifikasi sederhana terhadap keberadaan tanda tangan berdasarkan persentase foreground.

Tahapan yang digunakan meliputi:

```text
Crop
↓
Grayscale
↓
Otsu Threshold
↓
Opening
↓
Closing
↓
Foreground Analysis
↓
Classification
```

Dari 18 citra pengujian yang terdiri dari 9 citra PRESENT dan 9 citra ABSENT simulasi, diperoleh:

```text
Jumlah data   : 18
Benar         : 18
Salah         : 0
Akurasi       : 100%
```

Threshold klasifikasi yang digunakan adalah:

```text
8,25% foreground
```

Dengan aturan:

```text
Foreground >= 8,25%
→ SIGNATURE PRESENT

Foreground < 8,25%
→ SIGNATURE ABSENT
```

Namun, hasil akurasi 100% harus dipahami berdasarkan dataset pengujian yang digunakan. Data `SIGNATURE ABSENT` pada eksperimen ini merupakan **data simulasi yang dibuat dengan menghapus area tanda tangan dari citra yang memiliki tanda tangan**. Oleh karena itu, pengujian dengan citra ijazah asli yang memang tidak memiliki tanda tangan masih diperlukan untuk menguji kemampuan sistem pada kondisi nyata.

---

# 👨‍💻 Author

Mini Project Pengolahan Citra Digital

Project:

**Deteksi Keberadaan Tanda Tangan pada Ijazah**

Bahasa:

**Python**

Library:

**OpenCV dan NumPy**
