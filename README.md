# Aplikasi Kompresi Gambar dengan Principal Component Analysis (PCA)

## Deskripsi Proyek

Proyek ini adalah sebuah aplikasi web sederhana yang dibangun untuk mendemonstrasikan proses kompresi gambar menggunakan algoritma **Principal Component Analysis (PCA)**. Aplikasi ini dikembangkan sebagai bagian dari Ujian Akhir Semester (UAS) untuk mata kuliah Aljabar Linear Kelas A, Semester Genap 2024/2025 di Universitas Sebelas Maret.

[cite_start]PCA adalah teknik reduksi dimensi yang menyederhanakan data dengan mentransformasikannya menjadi sekumpulan komponen utama yang tidak berkorelasi.  Dalam konteks gambar, PCA digunakan untuk mengurangi jumlah komponen utama yang merepresentasikan data piksel, sehingga menghasilkan kompresi *lossy* (berbasis kualitas visual) dengan tetap mempertahankan warna asli gambar.

## Fitur Aplikasi

* **Unggah Gambar**: Pengguna dapat mengunggah gambar dengan format populer seperti PNG, JPG, JPEG, GIF, dan BMP. 
* **Kompresi Dinamis**: Tingkat kompresi dapat diatur secara interaktif melalui *slider* (0%-100%), yang menentukan persentase informasi yang akan dibuang. 
* **Perbandingan Visual**: Menampilkan gambar asli dan gambar hasil kompresi secara berdampingan untuk memudahkan perbandingan kualitas. 
* **Analisis Hasil**: Memberikan informasi mengenai waktu eksekusi algoritma kompresi dan persentase kompresi yang diterapkan. 
* **Unduh Hasil**: Pengguna dapat mengunduh gambar yang telah dikompresi. 
* **Reset**: Terdapat fungsionalitas untuk mereset aplikasi, membersihkan gambar yang diunggah dan hasil kompresi.

## Teknologi yang Digunakan

* **Backend**: Python 3
    * **Flask**: *Framework* web untuk menangani routing dan logika server.
* **Frontend**:
    * HTML5
    * CSS3
    * JavaScript
* **Library Utama**:
    * **scikit-learn**: Untuk implementasi algoritma PCA.
    * [cite_start]**Pillow (PIL)**: Untuk memanipulasi gambar seperti memuat dan menyimpan. 
    * **NumPy**: Untuk operasi numerik dan manipulasi array yang efisien.
    * **scikit-image**: Untuk metrik evaluasi kualitas gambar.

## Struktur Proyek

Proyek ini diorganisir dengan struktur direktori sebagai berikut, sesuai dengan pedoman tugas: 

```
.
├── src/                      # Folder berisi semua source code 
│   ├── app.py                # File utama Flask (routing & logika web)
│   ├── pca_image_compressor.py # Modul untuk logika kompresi PCA
│   └── templates/
│       └── index.html        # Template antarmuka pengguna
│   └── static/               # Folder untuk file statis (CSS, JS, gambar)
│       ├── uploads/          # Folder penyimpanan gambar asli (sementara)
│       └── compressed/       # Folder penyimpanan gambar hasil kompresi (sementara)
│
├── test/                     # Folder berisi data uji (contoh gambar) 
│   └── (contoh-gambar.jpg)
│
└── doc/                      # Folder berisi dokumentasi 
    └── README.md             # File ini
```

## Cara Menjalankan Aplikasi Secara Lokal

1.  **Clone Repositori (Jika ada)**
    ```bash
    git clone [https://url-repositori-anda.git](https://url-repositori-anda.git)
    cd nama-folder-proyek
    ```

2.  **Buat dan Aktifkan Lingkungan Virtual (Direkomendasikan)**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Instal Dependensi**
    Pastikan Anda memiliki semua library yang dibutuhkan. Anda dapat membuat file `requirements.txt` dengan isi sebagai berikut:
    ```
    Flask
    numpy
    scikit-learn
    scikit-image
    Pillow
    ```
    Lalu, instal dengan perintah:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi**
    Pindahkan terminal Anda ke dalam direktori `src/` dan jalankan file `app.py`.
    ```bash
    cd src
    python app.py
    ```

5.  **Akses Aplikasi**
    Buka browser web Anda dan kunjungi alamat berikut:
    ```
    [http://127.0.0.1:5000](http://127.0.0.1:5000)
    ```

## Tim Pengembang (Kelompok 14)

* Valentino Joan Cesar (NIM: L0124121)
* Aerio Ade Putra (NIM: L0124128)
* Nurman Aqil Wicaksono (NIM: L0124139)

--
**Fakultas Teknologi Informasi dan Sains Data** 
**Universitas Sebelas Maret** 
**Surakarta, 2025**
