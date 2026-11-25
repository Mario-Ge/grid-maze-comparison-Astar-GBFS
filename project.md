# PROJECT.md — Perbandingan Algoritma A* dan GBFS pada Grid Maze

> **Versi spesifikasi:** 2.0  
> **Tanggal revisi:** 22 November 2026  
> **Bahasa pemrograman:** Python 3  
> **Antarmuka:** Command Line Interface (CLI)  
> **Dokumen pedoman:** `skill.md`  
> **Catatan:** Dokumen ini menggantikan spesifikasi versi 1.0. Fokus revisi adalah menyederhanakan struktur dan alur program tanpa mengubah inti algoritma maupun informasi hasil pencarian.

---

## 1. Identitas dan tujuan proyek

**Judul:** Analisis Perbandingan Kinerja Algoritma A* dan Greedy Best-First Search (GBFS) pada Pencarian Jalur Grid Maze Menggunakan Python.

Program digunakan untuk membandingkan dua algoritma pencarian jalur:

1. **A*** sebagai algoritma pencarian berbasis biaya aktual dan heuristik.
2. **Greedy Best-First Search (GBFS)** sebagai algoritma pencarian berbasis heuristik.

Pengguna memilih satu Grid Maze, baik dari preset yang tersedia maupun dengan membuat Grid sendiri. Setelah Grid dinyatakan valid, program langsung menjalankan A* dan GBFS pada Grid, Start, dan Goal yang sama.

Hasil yang ditampilkan meliputi status pencarian, jalur, panjang jalur, jumlah simpul dibangkitkan, jumlah simpul dieksplorasi, visualisasi, waktu eksekusi, dan penggunaan memori. Hasil perbandingan satu Grid disimpan dalam CSV agar mudah dibuka dan dianalisis menggunakan Microsoft Excel atau aplikasi spreadsheet lain. Ringkasan hasil juga disimpan dalam TXT.

Tujuan proyek:

- Memahami cara kerja dan perbedaan A* dengan GBFS.
- Mengimplementasikan kedua algoritma secara langsung menggunakan Python.
- Membuktikan perbedaan hasil pencarian pada beberapa Grid sederhana.
- Membandingkan jumlah simpul, panjang jalur, waktu eksekusi, dan penggunaan memori.
- Menyediakan data CSV aktual untuk dianalisis atau dihitung ulang di Excel.

## 2. Alur program yang disederhanakan

Saat program dijalankan, tampilkan menu utama berikut:

```text
============================================
       PERBANDINGAN A* DAN GBFS
                 GRID MAZE
============================================
1. Gunakan Grid Preset
2. Buat Grid Kustom
3. Keluar

Pilih menu:
```

Alur setelah pilihan dibuat:

1. Jika pengguna memilih **Grid Preset**, tampilkan daftar preset dan minta pengguna memilih salah satunya.
2. Jika pengguna memilih **Grid Kustom**, minta ukuran Grid, isi setiap baris, koordinat Start, dan koordinat Goal.
3. Validasi Grid serta koordinatnya.
4. Jika input valid, tampilkan Grid awal dan informasi dasar Grid.
5. Jalankan A* dan GBFS secara otomatis pada input yang sama.
6. Tampilkan hasil dan visualisasi A* serta GBFS secara terpisah.
7. Tampilkan ringkasan perbandingan kedua algoritma.
8. Simpan hasil ke CSV dan TXT.
9. Berikan pilihan untuk kembali ke menu utama atau keluar.

**Tidak ada menu untuk memilih A*, GBFS, atau mode perbandingan.** Kedua algoritma selalu dijalankan setelah satu Grid berhasil dipilih atau dibuat. Dengan demikian, pengguna tidak perlu menjalankan algoritma satu per satu dan kedua hasil selalu menggunakan kasus yang sama.

Kesalahan input yang dapat diperkirakan harus ditangani dengan pesan yang mudah dipahami. Program memberi kesempatan untuk memasukkan ulang data atau kembali ke menu, bukan berhenti dengan traceback.

## 3. Struktur dan aturan Grid Maze

### 3.1 Representasi Grid

Grid direpresentasikan sebagai matriks dua dimensi:

| Nilai | Arti | Dapat dilalui? |
|---|---|---|
| `0` | Sel kosong | Ya |
| `1` | Dinding/penghalang | Tidak |

Start dan Goal disimpan sebagai koordinat `(baris, kolom)` dengan indeks dimulai dari `0`. Keduanya tidak disimpan sebagai angka khusus di dalam matriks.

Contoh:

```python
grid = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0],
]

start = (0, 0)
goal = (3, 4)
```

Grid dapat berbentuk persegi maupun persegi panjang. Jumlah sel keseluruhan adalah:

\[
n = jumlah\ baris \times jumlah\ kolom
\]

Informasi Grid yang ditampilkan:

- Jumlah baris dan kolom.
- Jumlah seluruh sel (`n`).
- Jumlah sel yang dapat dilalui (`0`).
- Jumlah dinding (`1`).
- Koordinat Start dan Goal.

### 3.2 Aturan pergerakan

- Gerakan hanya empat arah: atas, kanan, bawah, dan kiri.
- Gerakan diagonal tidak diperbolehkan.
- Biaya setiap perpindahan adalah `1`.
- Urutan pemeriksaan tetangga harus konsisten: atas, kanan, bawah, kiri.
- Perpindahan hanya sah jika sel tujuan berada di dalam batas Grid dan bernilai `0`.

### 3.3 Heuristik Manhattan Distance

Kedua algoritma menggunakan Manhattan Distance:

\[
h(n) = |r-r_g| + |c-c_g|
\]

`r` dan `c` adalah baris dan kolom posisi saat ini, sedangkan `r_g` dan `c_g` adalah baris dan kolom Goal. Heuristik ini sesuai dengan aturan gerak empat arah dan biaya langkah `1`.

## 4. Pilihan Grid

### 4.1 Grid preset

Program menyediakan enam preset deterministik yang ditulis langsung dalam kode:

1. **Grid Terbuka** — tanpa dinding atau hanya sedikit dinding; tersedia jalur.
2. **Grid Satu Penghalang** — satu penghalang menghalangi sebagian jalur langsung, tetapi tersedia jalur alternatif.
3. **Grid Koridor Sempit** — jalur yang tersedia terbatas dan memiliki belokan.
4. **Grid Banyak Penghalang** — beberapa penghalang dengan jalur penyelesaian yang tetap tersedia.
5. **Grid Tanpa Jalur** — Start dan Goal sama-sama valid, tetapi tidak saling terhubung.
6. **Grid Persegi Panjang** — jumlah baris dan kolom berbeda serta mempunyai jalur penyelesaian.

Setiap preset mempunyai matriks, Start, dan Goal yang tetap. Hasilnya harus konsisten setiap kali preset yang sama dipilih.

### 4.2 Grid kustom

Pengguna memasukkan:

1. Jumlah baris.
2. Jumlah kolom.
3. Isi setiap baris menggunakan karakter `0` dan `1` tanpa pemisah.
4. Koordinat Start.
5. Koordinat Goal.

Contoh untuk Grid dengan enam kolom: `000100`.

### 4.3 Validasi input

Program harus menolak input apabila:

- Jumlah baris atau kolom bukan bilangan bulat positif.
- Grid kosong atau jumlah kolom antarbaris tidak sama.
- Isi baris memiliki karakter selain `0` dan `1`.
- Koordinat bukan dua bilangan bulat.
- Start atau Goal berada di luar batas Grid.
- Start atau Goal berada pada dinding.

Start boleh sama dengan Goal. Pada kasus tersebut, kedua algoritma harus menghasilkan jalur yang terdiri dari satu koordinat dengan panjang `0`.

## 5. Ketentuan implementasi algoritma

Kedua algoritma harus diimplementasikan sendiri menggunakan Python standard library. Library pathfinding eksternal tidak diperbolehkan.

### 5.1 A*

A* menggunakan fungsi prioritas:

\[
f(n) = g(n) + h(n)
\]

- `g(n)` adalah biaya aktual dari Start sampai simpul saat ini.
- `h(n)` adalah estimasi biaya dari simpul saat ini menuju Goal.
- `f(n)` adalah jumlah biaya aktual dan estimasi biaya.

Ketentuan implementasi:

- Gunakan `heapq` sebagai priority queue.
- Simpan biaya terbaik setiap koordinat pada `g_score`.
- Gunakan `parent` untuk merekonstruksi jalur.
- Gunakan `closed_set` untuk mencatat simpul yang sudah diproses.
- Jika ditemukan biaya lebih kecil untuk simpul yang belum diproses, perbarui `g_score` dan `parent`, kemudian masukkan entri prioritas baru.
- Lewati entri heap yang sudah kedaluwarsa.
- Goal dinyatakan ditemukan ketika entri valid untuk Goal dikeluarkan dari heap.
- Gunakan counter untuk tie-breaking agar urutan proses deterministik.

Dengan aturan gerak dan heuristik proyek ini, A* harus menemukan jalur terpendek apabila jalur tersedia.

### 5.2 Greedy Best-First Search (GBFS)

GBFS menggunakan fungsi prioritas:

\[
f(n) = h(n)
\]

Prioritas GBFS hanya menggunakan Manhattan Distance. **Jangan memasukkan `g(n)` ke dalam prioritas GBFS.**

Ketentuan implementasi:

- Gunakan `heapq` sebagai priority queue.
- Gunakan `discovered` agar setiap koordinat dimasukkan ke frontier satu kali.
- Gunakan `parent` untuk merekonstruksi jalur.
- Gunakan counter untuk tie-breaking deterministik.
- Goal dinyatakan ditemukan ketika dikeluarkan dari heap.
- Jika frontier kosong, nyatakan bahwa jalur tidak ditemukan.

GBFS wajib menghasilkan jalur yang valid jika berhasil, tetapi tidak wajib menghasilkan jalur terpendek.

### 5.3 Data hasil algoritma

Kedua fungsi algoritma mengembalikan informasi dengan nama field yang sama:

| Field | Keterangan |
|---|---|
| `algorithm` | Nama algoritma: `A*` atau `GBFS` |
| `found` | Status apakah Goal ditemukan |
| `path` | Daftar koordinat jalur; `None` jika tidak ditemukan |
| `path_length` | Jumlah perpindahan; `None` jika tidak ditemukan |
| `generated_nodes` | Jumlah koordinat unik yang dibangkitkan, termasuk Start |
| `expanded_nodes` | Jumlah simpul valid yang dikeluarkan dari heap untuk diproses, termasuk Goal jika ditemukan |
| `explored` | Kumpulan koordinat yang sudah dieksplorasi |

Ketentuan penghitungan:

- Start dihitung sebagai satu simpul dibangkitkan.
- Koordinat yang ditemukan kembali tidak menambah `generated_nodes`.
- Pada A*, entri heap kedaluwarsa tidak menambah `expanded_nodes`.
- Goal ikut dihitung sebagai simpul dieksplorasi ketika dikeluarkan dari heap dan dikenali sebagai tujuan.
- Jika Start sama dengan Goal: `generated_nodes = 1`, `expanded_nodes = 1`, `path = [Start]`, dan `path_length = 0`.
- Jika Goal tidak ditemukan: `found = False`, `path = None`, dan `path_length = None`.

Fungsi inti A* dan GBFS **tidak boleh** mengukur waktu, mengukur memori, mencetak hasil, meminta input, melakukan visualisasi, atau menyimpan file.

## 6. Pengukuran waktu dan memori

### 6.1 Prinsip pengukuran

Pengukuran dilakukan pada **pemanggilan fungsi algoritma inti saja**, yaitu fungsi A* atau fungsi GBFS yang menerima Grid, Start, dan Goal lalu menjalankan pencarian sampai rekonstruksi jalur selesai.

Bagian berikut tidak boleh masuk ke interval pengukuran:

- Input dari pengguna.
- Pembuatan atau pemilihan Grid.
- Validasi awal Grid dan koordinat.
- Visualisasi atau pencetakan terminal.
- Pemeriksaan jalur setelah fungsi algoritma selesai.
- Pembuatan tabel perbandingan.
- Penyimpanan CSV dan TXT.

Pengukuran waktu dan memori dilakukan secara terpisah agar pelacakan memori tidak memengaruhi pengukuran waktu.

### 6.2 Pengukuran waktu

- Gunakan `time.perf_counter_ns()`.
- Lakukan 1 pemanggilan awal sebagai pemanasan; hasilnya tidak dicatat.
- Lakukan 10 pengulangan pengukuran untuk setiap algoritma.
- Catat waktu tepat sebelum dan sesudah pemanggilan fungsi inti.
- Hitung dan laporkan rata-rata serta median waktu dalam milidetik.
- Buat state pencarian baru pada setiap pemanggilan. Fungsi algoritma harus menginisialisasi ulang frontier, parent, skor, dan himpunan pencarian di dalam fungsinya.

Rumus rata-rata:

\[
T_{rata-rata} = \frac{T_1 + T_2 + \cdots + T_{10}}{10}
\]

### 6.3 Pengukuran memori

- Gunakan `tracemalloc` dari standard library.
- Ukur secara terpisah dari waktu.
- Lakukan 10 pengulangan untuk setiap algoritma.
- Mulai pelacakan tepat sebelum pemanggilan fungsi inti dan ambil peak setelah fungsi selesai.
- Gunakan `try/finally` agar `tracemalloc.stop()` selalu dijalankan.
- Laporkan median peak traced memory dalam KB.

`tracemalloc` mengukur alokasi memori Python yang dilacak, bukan keseluruhan RAM proses atau memori native sistem operasi.

### 6.4 Batas interpretasi

Waktu eksekusi pada Grid yang sangat kecil dapat berubah karena kondisi komputer dan proses lain yang berjalan. Karena itu, angka waktu dan memori harus diperlakukan sebagai hasil pengukuran pada lingkungan pengujian tersebut, bukan sebagai angka mutlak yang berlaku untuk semua komputer.

Untuk eksperimen Excel, pengguna dapat menjalankan program berulang kali dengan beberapa kasus sederhana. Setiap hasil CSV menjadi satu data kasus yang dapat digabungkan di Excel. A* dan GBFS harus selalu dibandingkan pada Grid, Start, dan Goal yang sama.

## 7. Pemeriksaan validitas jalur

Jika algoritma menemukan Goal, jalur harus memenuhi semua ketentuan berikut:

1. Koordinat pertama sama dengan Start.
2. Koordinat terakhir sama dengan Goal.
3. Semua koordinat berada dalam batas Grid.
4. Semua koordinat jalur berada pada sel bernilai `0`.
5. Manhattan Distance antara dua koordinat berurutan tepat `1`.
6. `path_length == len(path) - 1`.

Jalur A* dan GBFS ditampilkan secara terpisah. Visualisasi tidak boleh mengubah matriks Grid sumber.

## 8. Visualisasi terminal

Gunakan simbol berikut:

| Simbol | Arti |
|---|---|
| `S` | Start |
| `G` | Goal |
| `#` | Dinding |
| `.` | Sel kosong yang belum dieksplorasi |
| `e` | Sel yang dieksplorasi dan bukan bagian jalur |
| `*` | Jalur akhir |

Urutan prioritas tampilan: Start dan Goal, dinding, jalur akhir, sel eksplorasi, lalu sel kosong. Tampilkan Grid awal, kemudian hasil visualisasi A* dan GBFS secara terpisah.

## 9. Pengujian fungsional

Unit test menggunakan `unittest` dan sekurang-kurangnya mencakup delapan skenario:

| ID | Skenario | Hasil yang diharapkan |
|---|---|---|
| FT-01 | Grid terbuka | A* dan GBFS menemukan jalur valid |
| FT-02 | Satu penghalang | Kedua algoritma menemukan jalur valid jika tersedia |
| FT-03 | Banyak penghalang | Kedua algoritma menemukan jalur valid jika tersedia |
| FT-04 | Tidak ada jalur | Kedua algoritma menyatakan Goal tidak dapat dicapai |
| FT-05 | Start sama dengan Goal | Kedua algoritma menghasilkan panjang jalur 0 |
| FT-06 | Grid persegi panjang | Kedua algoritma dapat bekerja pada Grid nonpersegi |
| FT-07 | Hanya bersinggungan diagonal | Algoritma tidak boleh bergerak diagonal |
| FT-08 | Input tidak valid | Validator menolak input dengan benar |

Optimalitas A* diperiksa menggunakan BFS sederhana sebagai oracle **di dalam unit test saja**. BFS tidak ditampilkan di menu, tidak dijalankan pada penggunaan normal program, dan bukan algoritma pembanding.

Jalankan unit test dengan:

```bash
python -m unittest discover -s tests -v
```

Hasil `PASS` atau `FAIL` harus berasal dari eksekusi test yang sebenarnya.

## 10. Hasil program dan file keluaran

Program harus menampilkan hasil berikut di terminal untuk kedua algoritma:

- Status ditemukan/tidak ditemukan.
- Jalur yang diperoleh.
- Panjang jalur.
- Jumlah simpul dibangkitkan.
- Jumlah simpul dieksplorasi.
- Rata-rata dan median waktu eksekusi.
- Median peak penggunaan memori.
- Visualisasi hasil pencarian.

Hasil satu Grid disimpan dalam dua file dengan timestamp agar hasil sebelumnya tidak tertimpa:

```text
outputs/
├── single_comparison_YYYYMMDD_HHMMSS.csv
└── comparison_report_YYYYMMDD_HHMMSS.txt
```

### 10.1 CSV perbandingan

File CSV berisi dua baris utama: satu untuk A* dan satu untuk GBFS. Kolom minimal:

- `timestamp`, `maze_type`, `maze_name`
- `rows`, `cols`, `n`, `passable_cells`, `wall_cells`
- `start_row`, `start_col`, `goal_row`, `goal_col`
- `algorithm`, `found`, `path_length`
- `generated_nodes`, `expanded_nodes`
- `time_runs`, `time_mean_ms`, `time_median_ms`
- `memory_runs`, `memory_median_kb`

Gunakan encoding UTF-8. Kolom harus mempunyai header dan dapat dibuka di Excel. Angka yang ditulis harus berasal dari pengukuran aktual.

### 10.2 Laporan TXT

Laporan TXT minimal berisi:

1. Tanggal dan waktu pengujian.
2. Nama/jenis Grid, ukuran, Start, dan Goal.
3. Ringkasan hasil A*.
4. Ringkasan hasil GBFS.
5. Tabel perbandingan metrik.
6. Catatan bahwa pengukuran waktu dan memori hanya mencakup pemanggilan fungsi inti.
7. Kesimpulan singkat berdasarkan hasil aktual.

### 10.3 Penyederhanaan keluaran dari versi sebelumnya

CSV `single_comparison` menjadi satu-satunya CSV eksperimen kinerja karena satu kali penggunaan program hanya membandingkan satu Grid. Data waktu dan memori berada langsung di CSV tersebut. CSV `performance_benchmark` terpisah tidak diperlukan karena akan menduplikasi data yang sama.

Pengujian fungsional tetap tersedia melalui `unittest` dan hasil PASS/FAIL ditampilkan di terminal. Ekspor CSV khusus hasil unit test tidak diwajibkan pada versi sederhana ini.

## 11. Struktur folder proyek

Gunakan struktur berikut agar mudah dipahami dan tidak terlalu banyak modul:

```text
grid-maze-comparison/
├── main.py
├── maze.py
├── astar.py
├── gbfs.py
├── metrics.py
├── report.py
├── tests/
│   ├── test_maze.py
│   └── test_algorithms.py
├── outputs/
├── project.md
├── skill.md
├── progress.md
└── README.md
```

Tanggung jawab setiap file:

| File | Tanggung jawab |
|---|---|
| `main.py` | Menu awal, menerima pilihan, menjalankan alur program dan kedua algoritma |
| `maze.py` | Enam preset, input custom, validasi, tetangga, Manhattan Distance, dan informasi Grid |
| `astar.py` | Fungsi inti A* dan rekonstruksi jalur |
| `gbfs.py` | Fungsi inti GBFS dan rekonstruksi jalur |
| `metrics.py` | Pengukuran waktu dan memori dari pemanggilan fungsi algoritma inti |
| `report.py` | Visualisasi hasil, tabel perbandingan, ekspor CSV dan TXT |
| `tests/test_maze.py` | Test preset, input, validasi, tetangga, dan heuristik |
| `tests/test_algorithms.py` | Test A*, GBFS, validitas jalur, dan optimalitas A* |
| `outputs/` | Lokasi file hasil program |

Tidak perlu membuat folder `algorithms/`, `benchmark.py`, atau `display.py` pada struktur sederhana ini. Jangan menambah modul baru kecuali ada kebutuhan nyata yang dapat dijelaskan.

## 12. Teknologi dan batasan

- Python 3.
- Utamakan standard library: `heapq`, `time`, `tracemalloc`, `statistics`, `csv`, `pathlib`, `datetime`, `unittest`, dan modul standar lain yang diperlukan.
- Tidak menggunakan library pathfinding eksternal.
- Tidak membutuhkan NumPy, Pandas, Matplotlib, database, GUI, atau koneksi internet.
- Program utama dijalankan dengan `python main.py`.
- Unit test dijalankan dengan `python -m unittest discover -s tests -v`.

## 13. Kriteria penerimaan

- [ ] Menu awal menyediakan pilihan Grid Preset, Grid Kustom, dan Keluar.
- [ ] Enam preset dapat dipilih dan menghasilkan Grid deterministik.
- [ ] Grid kustom dapat menerima Grid persegi dan persegi panjang.
- [ ] Input Grid, Start, dan Goal divalidasi.
- [ ] Setelah Grid valid, program langsung menjalankan A* dan GBFS.
- [ ] Kedua algoritma menggunakan Grid, Start, dan Goal yang sama.
- [ ] A* menggunakan prioritas `g(n) + h(n)`.
- [ ] GBFS menggunakan prioritas `h(n)` saja.
- [ ] Keduanya menggunakan Manhattan Distance, biaya langkah 1, dan gerakan empat arah.
- [ ] Hasil pencarian memuat status, jalur, panjang jalur, generated nodes, expanded nodes, dan explored.
- [ ] Jalur yang ditemukan lolos pemeriksaan validitas.
- [ ] A* menghasilkan jalur optimal pada kasus yang diperiksa dengan BFS oracle di unit test.
- [ ] Visualisasi A* dan GBFS ditampilkan secara terpisah.
- [ ] Pengukuran waktu hanya membungkus pemanggilan fungsi algoritma inti.
- [ ] Pengukuran memori dilakukan terpisah dan hanya melacak pemanggilan fungsi algoritma inti.
- [ ] Hasil waktu, memori, dan metrik pencarian ditampilkan di terminal.
- [ ] CSV satu Grid dan laporan TXT dibuat dari hasil aktual.
- [ ] CSV dapat dibuka di Excel.
- [ ] Unit test mencakup delapan skenario fungsional.
- [ ] Tidak ada hasil pengujian yang dibuat-buat.

## 14. Prinsip analisis

- A* menjamin jalur terpendek dalam ketentuan proyek ini.
- GBFS tidak menjamin jalur terpendek.
- GBFS tidak selalu lebih cepat atau lebih hemat memori daripada A*.
- Jumlah simpul yang dieksplorasi tidak selalu sama dengan jumlah sel pada Grid.
- Hasil waktu dan memori dipengaruhi ukuran/pola Grid, Start, Goal, komputer, dan kondisi proses lain.
- Kesimpulan harus berdasarkan CSV aktual dari kasus yang diuji, bukan asumsi bahwa satu algoritma selalu unggul.
- Untuk perbandingan yang adil, A* dan GBFS wajib diuji pada input yang identik.

---

**Acuan utama:** `project.md` versi 2.0. Pedoman pengerjaan terdapat di `skill.md`, sedangkan status pelaksanaan dicatat di `progress.md`.
