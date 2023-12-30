# HuaweiCLI

Proyek ini adalah implementasi library api huawei untuk berkomunikasi dengan modem Huawei B818 menggunakan bahasa python. Proyek ini diadaptasi dari [huawei-lte](https://github.com/octave21/huawei-lte).

## Petunjuk Instalasi

1. Pastikan Python sudah terinstal di sistem Anda. Jika belum, instal Python dari [python.org](https://www.python.org/downloads/).

2. Unduh repositori ini:

    ```bash
    git clone https://github.com/NamaAnda/huawei-lte-api.git
    ```
3. Anda dapat membuka file `config.py`. Ganti nilai variabel `ip` dan `password` sesuai konfigurasi modem anda.

4. Masuk ke direktori proyek:

    ```bash
    cd huawei-lte-api
    ```

4. Instal dependensi:
    ```bash
    pip install -r requirements.txt
    ```
## Penggunaan

1. Pastikan modem Huawei anda terhubung dengan jaringan dan dapat diakses.

2. Jalankan skrip `huawei.py` untuk menjalankan API dan menu interaktif:

    ```bash
    python huawei.py
    ```

3. Pilih opsi untuk mengganti band sesuai kebutuhan Anda. Silahkan override code ini untuk menambah opsi pergantian band.



