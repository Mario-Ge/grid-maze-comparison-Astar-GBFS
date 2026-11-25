
# Analisis Perbandingan Algoritma A* dan GBFS pada Grid Maze

## 1. Deskripsi Proyek

Proyek ini merupakan implementasi dan analisis perbandingan kinerja dua algoritma pencarian jalur, yaitu A* (A-Star) dan Greedy Best-First Search (GBFS), pada Grid Maze menggunakan Python.

Program berbasis Command Line Interface (CLI). Pengguna dapat memilih Grid dari enam preset yang tersedia atau membuat Grid kustom sendiri.

Setelah Grid dinyatakan valid, program secara otomatis menjalankan A* dan GBFS menggunakan Grid, Start, dan Goal yang sama.

Hasil pencarian dan pengukuran kinerja ditampilkan di terminal serta disimpan dalam format CSV dan TXT.

## 2. Tujuan Proyek

- Memahami cara kerja algoritma A* dan GBFS.
- Mengimplementasikan kedua algoritma menggunakan Python.
- Membandingkan hasil pencarian jalur pada Grid yang sama.
- Membandingkan panjang jalur dan jumlah simpul yang dihasilkan serta dieksplorasi.
- Mengukur waktu eksekusi dan penggunaan memori.
- Menyediakan data eksperimen dalam format CSV agar dapat dianalisis menggunakan Microsoft Excel atau aplikasi spreadsheet lainnya.

## 3. Teknologi yang Digunakan

- Python 3.12.3.
- Python Standard Library.
- Heapq untuk Priority Queue.
- Time untuk pengukuran waktu.
- Tracemalloc untuk pengukuran memori.
- Statistics untuk perhitungan rata-rata dan median.
- CSV untuk ekspor data.
- Unittest untuk pengujian otomatis.

Tidak menggunakan library pathfinding eksternal.

## 4. Algoritma

### A* (A-Star)

A* menggunakan kombinasi biaya aktual dan estimasi biaya menuju Goal.

Rumus prioritas:

    f(n) = g(n) + h(n)

Keterangan:

- g(n): biaya aktual dari Start menuju posisi saat ini.
- h(n): estimasi jarak menuju Goal.
- f(n): total biaya aktual dan estimasi.

A* menggunakan Manhattan Distance dan menjamin jalur terpendek pada aturan Grid proyek ini.

### Greedy Best-First Search (GBFS)

GBFS menggunakan heuristik saja untuk menentukan prioritas pencarian.

Rumus prioritas:

    f(n) = h(n)

GBFS tidak mempertimbangkan biaya aktual perjalanan dari Start menuju posisi sekarang sehingga tidak menjamin jalur terpendek.

### Manhattan Distance

Kedua algoritma menggunakan Manhattan Distance:

    h(n) = |r - r_goal| + |c - c_goal|

Aturan pergerakan:

- Atas.
- Kanan.
- Bawah.
- Kiri.

Gerakan diagonal tidak diperbolehkan dan biaya setiap perpindahan adalah 1.

## 5. Fitur Program

1. Enam Grid Preset:
   - Grid Terbuka.
   - Grid Satu Penghalang.
   - Grid Koridor Sempit.
   - Grid Banyak Penghalang.
   - Grid Tanpa Jalur.
   - Grid Persegi Panjang.

2. Pembuatan Grid Kustom dengan bentuk persegi maupun persegi panjang.

3. Validasi Grid, Start, dan Goal.

4. Eksekusi otomatis A* dan GBFS pada Grid yang sama.

5. Visualisasi jalur dan simpul yang dieksplorasi.

6. Pengukuran generated nodes dan expanded nodes.

7. Pengukuran waktu eksekusi.

8. Pengukuran penggunaan memori.

9. Ekspor hasil perbandingan ke CSV dan TXT.

10. Unit test menggunakan unittest.

## 6. Struktur Proyek

    grid-maze-comparison2/
    |
    |-- .venv/
    |
    |-- main.py
    |-- maze.py
    |-- astar.py
    |-- gbfs.py
    |-- metrics.py
    |-- report.py
    |
    |-- tests/
    |   |-- test_maze.py
    |   |-- test_algorithms.py
    |
    |-- outputs/
    |
    |-- project.md
    |-- skill.md
    |-- progress.md
    |-- README.md

### Tanggung Jawab File

| File | Fungsi |
|---|---|
| main.py | Menu utama dan alur program |
| maze.py | Grid, preset, validasi, dan heuristik |
| astar.py | Implementasi algoritma A* |
| gbfs.py | Implementasi algoritma GBFS |
| metrics.py | Pengukuran waktu dan memori |
| report.py | Visualisasi, perbandingan, dan ekspor laporan |
| tests/test_maze.py | Pengujian Grid dan validasi |
| tests/test_algorithms.py | Pengujian algoritma dan optimalitas A* |
| outputs/ | Penyimpanan hasil eksperimen |

## 7. Persiapan Lingkungan

### Persyaratan

- Python 3.12 atau versi Python 3 yang mendukung kode proyek.
- Terminal Linux atau lingkungan yang mendukung Python.

### Clone Repository

Jika proyek sudah diunggah ke GitHub:

    git clone <URL_REPOSITORY>

Masuk ke folder proyek:

    cd grid-maze-comparison2

### Membuat Virtual Environment

    python3 -m venv .venv

Aktifkan virtual environment:

    source .venv/bin/activate

Periksa versi Python:

    python --version

### Dependensi

Proyek menggunakan Python Standard Library sehingga tidak memerlukan instalasi library eksternal.

## 8. Menjalankan Program

Pastikan virtual environment aktif.

Jalankan:

    python main.py

Menu utama:

    ============================================
           PERBANDINGAN A* DAN GBFS
                     GRID MAZE
    ============================================
    1. Gunakan Grid Preset
    2. Buat Grid Kustom
    3. Keluar

    Pilih menu:

### Menggunakan Grid Preset

Pilih menu nomor 1, kemudian pilih salah satu dari enam Grid Preset.

### Membuat Grid Kustom

Pilih menu nomor 2.

Masukkan:

1. Jumlah baris.
2. Jumlah kolom.
3. Isi setiap baris menggunakan karakter 0 dan 1.
4. Koordinat Start.
5. Koordinat Goal.

Contoh Grid:

    00010
    01010
    00000

Start:

    0,0

Goal:

    2,4

## 9. Pengukuran Kinerja

### Pengukuran Waktu

Pengukuran waktu menggunakan:

    time.perf_counter_ns()

Ketentuan:

- Satu kali pemanasan.
- Sepuluh kali pengulangan.
- Hasil rata-rata dalam milidetik.
- Hasil median dalam milidetik.

### Pengukuran Memori

Pengukuran memori menggunakan:

    tracemalloc

Ketentuan:

- Sepuluh kali pengulangan.
- Pengukuran dilakukan terpisah dari pengukuran waktu.
- Hasil yang dilaporkan adalah median peak traced memory dalam KB.

Tracemalloc mengukur alokasi memori Python yang dilacak, bukan keseluruhan RAM proses.

Pengukuran hanya mencakup pemanggilan fungsi inti algoritma. Input, pembuatan Grid, validasi awal, visualisasi, dan ekspor laporan tidak ikut dihitung.

## 10. Pengujian Otomatis

Proyek menggunakan unittest.

Jalankan seluruh unit test:

    python -m unittest discover -s tests -v

Pengujian mencakup:

- Grid terbuka.
- Grid satu penghalang.
- Grid banyak penghalang.
- Grid tanpa jalur.
- Start sama dengan Goal.
- Grid persegi panjang.
- Larangan gerakan diagonal.
- Input Grid tidak valid.
- Validitas jalur hasil pencarian.
- Optimalitas A* menggunakan BFS sebagai oracle khusus unit test.

## 11. Hasil Eksperimen

Setiap kali program berhasil memproses satu Grid, dua file laporan akan dibuat di folder outputs/.

Format nama file:

    single_comparison_YYYYMMDD_HHMMSS.csv

    comparison_report_YYYYMMDD_HHMMSS.txt

### CSV

CSV memuat dua baris hasil utama:

- A*.
- GBFS.

Data meliputi informasi Grid, status pencarian, panjang jalur, generated nodes, expanded nodes, waktu, dan penggunaan memori.

File CSV dapat dibuka menggunakan Microsoft Excel atau aplikasi spreadsheet lainnya.

### TXT

Laporan TXT memuat informasi Grid, hasil kedua algoritma, metrik pengukuran, tabel perbandingan, dan kesimpulan berdasarkan hasil aktual.

## 12. Catatan Analisis

- A* menjamin jalur terpendek pada aturan Grid proyek ini.
- GBFS tidak menjamin jalur terpendek.
- GBFS tidak selalu lebih cepat atau lebih hemat memori daripada A*.
- Jumlah simpul yang dieksplorasi dipengaruhi pola Grid, Start, dan Goal.
- Waktu dan penggunaan memori dipengaruhi kondisi komputer dan proses lain yang sedang berjalan.
- Kesimpulan perbandingan harus berdasarkan hasil eksperimen aktual.

---

Proyek Analisis Perbandingan Algoritma A* dan GBFS pada Grid Maze Menggunakan Python.
