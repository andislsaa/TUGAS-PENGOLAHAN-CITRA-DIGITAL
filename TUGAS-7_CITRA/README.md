# Prototype Verifikasi Ijazah Menggunakan Pengolahan Citra dan OCR

## 1. Deskripsi Proyek

Proyek ini merupakan prototype verifikasi ijazah yang menggabungkan teknik pengolahan citra digital, Optical Character Recognition (OCR), dan deteksi tanda tangan.

Sistem digunakan untuk membaca nomor ijazah dari gambar serta mendeteksi keberadaan tanda tangan pada area yang dipilih pengguna.

## 2. Tujuan

* Menerapkan pengolahan citra digital pada gambar ijazah.
* Membandingkan hasil pembacaan nomor ijazah menggunakan beberapa metode enhancement.
* Mendeteksi keberadaan tanda tangan berdasarkan persentase piksel foreground.
* Mengevaluasi hasil OCR dan deteksi tanda tangan.

## 3. Teknologi yang Digunakan

* Python
* OpenCV
* NumPy
* Pytesseract
* Tesseract OCR
* CSV untuk menyimpan hasil pengujian

## 4. Metode yang Digunakan

### A. OCR dan Enhancement

Sistem membandingkan lima metode:

1. Original
2. Mean Filter
3. Median Filter
4. Gaussian Filter
5. Sharpening

Hasil pembacaan nomor ijazah dari setiap metode dibandingkan untuk menentukan metode yang memberikan hasil sesuai dengan nomor acuan.

### B. Deteksi Tanda Tangan

Tahapan deteksi tanda tangan:

1. Memilih area tanda tangan atau Region of Interest (ROI).
2. Mengubah area ROI menjadi grayscale.
3. Mengurangi gangguan menggunakan Gaussian Blur.
4. Melakukan thresholding dengan metode Otsu.
5. Membersihkan piksel menggunakan operasi morfologi.
6. Menghitung persentase foreground.
7. Mengklasifikasikan hasil sebagai PRESENT atau ABSENT menggunakan ambang 5%.

## 5. Hasil Pengujian Prototype

Pengujian pada gambar `01_HighQuality_Enhanced.jpg` menghasilkan:

| Komponen                        | Hasil           |
| ------------------------------- | --------------- |
| Nomor ijazah                    | 571012022000056 |
| Metode enhancement yang dipilih | Original        |
| Persentase foreground           | 10,38%          |
| Deteksi tanda tangan            | PRESENT         |

Kelima metode OCR pada gambar tersebut menghasilkan nomor yang sama, yaitu `571012022000056`.

### Evaluasi Deteksi Tanda Tangan

Pengujian batch menggunakan sembilan gambar asli dan sembilan gambar simulasi tanpa tanda tangan menghasilkan:

| Metrik         | Hasil |
| -------------- | ----: |
| True Positive  |     9 |
| False Negative |     0 |
| True Negative  |     9 |
| False Positive |     0 |
| Akurasi        |  100% |
| Precision      |  100% |
| Recall         |  100% |
| F1-score       |  100% |

**Catatan:** gambar tanpa tanda tangan merupakan data simulasi yang dibuat dengan menutupi area tanda tangan pada gambar asli. Oleh karena itu, hasil evaluasi ini merupakan pengujian awal dalam kondisi terkontrol, bukan bukti akurasi pada seluruh jenis ijazah nyata.

## 6. Struktur Folder

* `gambar_asli/` — gambar ijazah untuk pengujian.
* `kode_py/` — skrip pendukung pengolahan citra.
* `HASIL/evaluasi_batch/` — hasil evaluasi OCR dan deteksi pada gambar asli.
* `HASIL/data_absent_simulasi/` — gambar simulasi tanpa tanda tangan.
* `HASIL/evaluasi_deteksi/` — hasil evaluasi deteksi tanda tangan dan gambar threshold.
* `HASIL/prototype/` — hasil prototype dan CSV.
* `main.py` — program utama prototype.
* `batch_evaluasi.py` — program evaluasi OCR batch.
* `evaluasi_deteksi.py` — program evaluasi deteksi tanda tangan.
* `requirements.txt` — daftar dependensi Python.

## 7. Instalasi dan Cara Menjalankan

Pastikan Python dan Tesseract OCR sudah terpasang.

Buka terminal di folder proyek, lalu jalankan:

```bash
pip install -r requirements.txt
```

Jalankan prototype:

```bash
py main.py
```

Jalankan evaluasi OCR batch:

```bash
py batch_evaluasi.py
```

Jalankan evaluasi deteksi tanda tangan:

```bash
py evaluasi_deteksi.py
```

Pada prototype, pilih gambar ijazah, tandai area nomor ijazah, kemudian tandai area tanda tangan. Sistem akan menampilkan hasil OCR dan deteksi tanda tangan serta menyimpan hasil prototype dalam format CSV.

## 8. Keterbatasan

* Pengguna harus memilih area nomor ijazah dan tanda tangan secara manual.
* Hasil OCR dipengaruhi kualitas dan keterbacaan gambar.
* Deteksi tanda tangan berbasis foreground dapat salah mengklasifikasikan coretan atau teks lain di area yang dipilih.
* Data simulasi tanpa tanda tangan belum mewakili seluruh variasi ijazah nyata.
* Sistem ini merupakan prototype pemeriksaan citra, bukan alat autentikasi resmi untuk memastikan keaslian ijazah atau tanda tangan.

## 9. Kesimpulan

Prototype berhasil membaca nomor ijazah pada gambar uji dan mendeteksi keberadaan tanda tangan berdasarkan area yang dipilih. Pengujian awal menunjukkan hasil yang baik pada dataset yang digunakan, tetapi masih diperlukan pengujian menggunakan lebih banyak gambar nyata dengan variasi kualitas dan kondisi tanda tangan.
