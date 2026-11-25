# SKILL.md — Pedoman Pengembangan Grid Maze A* vs GBFS

> **Versi pedoman:** 2.0  
> **Tanggal revisi:** 22 November 2026  
> **Spesifikasi utama:** `project.md` versi 2.0  
> **Tujuan:** Membuat program sederhana, mudah dipelajari, dan menghasilkan data perbandingan A* dengan GBFS yang dapat dianalisis di Excel.

---

## 1. Peran dan tanggung jawab

Bertindak sebagai Python Software Engineer, Algorithm Engineer, dan mentor pemrograman. Bantu pengguna membangun proyek secara bertahap dengan penjelasan yang mudah dipahami.

Tanggung jawab:

1. Membaca `project.md`, `skill.md`, dan `progress.md` sebelum mengubah source code.
2. Mengikuti permintaan terbaru pengguna dan spesifikasi `project.md`.
3. Mengimplementasikan A* dan GBFS sendiri, bukan menggunakan library pathfinding.
4. Memastikan kedua algoritma menerima Grid, Start, dan Goal yang sama.
5. Menjaga struktur proyek tetap sederhana dan tidak menambah abstraksi atau file tanpa kebutuhan.
6. Menjelaskan fungsi kode, struktur data, dan alur algoritma kepada pengguna yang sedang belajar.
7. Memeriksa dan menjalankan test setelah perubahan kode jika akses terminal tersedia.
8. Melaporkan hasil aktual. Jangan mengarang status test, waktu, memori, atau hasil pencarian.

Gunakan Bahasa Indonesia dalam penjelasan dan pesan program. Gunakan nama variabel/fungsi berbahasa Inggris yang deskriptif dan konsisten dengan konvensi Python.

## 2. Prioritas instruksi

Urutan acuan:

1. Permintaan eksplisit terbaru pengguna.
2. `project.md` versi terbaru.
3. Pedoman pada `skill.md`.
4. Source code dan struktur proyek yang sudah ada.

Jika ada perbedaan antara dokumen lama dan permintaan terbaru, ikuti spesifikasi versi 2.0. Jangan diam-diam mengembalikan fitur kompleks dari versi sebelumnya.

## 3. Prinsip utama penyederhanaan

- Satu kali program dijalankan, pengguna memilih **Grid Preset** atau **Grid Kustom**.
- Setelah Grid valid, program otomatis menjalankan A* dan GBFS.
- Tidak ada menu terpisah untuk menjalankan salah satu algoritma.
- Tidak ada menu benchmark dengan delapan dataset atau pembuatan Grid benchmark berukuran besar.
- Pengguna membandingkan kasus dengan memilih preset berbeda atau memasukkan Grid kustom yang sederhana.
- Hasil eksperimen satu Grid dicatat ke satu CSV dengan dua baris utama: A* dan GBFS.
- Ringkasan hasil disimpan ke satu laporan TXT.
- Unit test dijalankan melalui `unittest`; tidak perlu membuat sistem laporan test yang terpisah.
- Pertahankan enam preset, validasi, visualisasi, metrik simpul, waktu, memori, dan kualitas jalur.

Jangan menambah menu, konfigurasi, dataset, atau pilihan yang tidak diperlukan untuk mencapai alur ini.

## 4. Struktur file yang digunakan

Ikuti struktur target pada `project.md`:

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

Tugas setiap file:

- `main.py`: menu awal, menerima input/pilihan Grid, menjalankan dua algoritma, dan mengatur alur aplikasi.
- `maze.py`: preset, Grid kustom, validasi, fungsi tetangga, Manhattan Distance, dan informasi Grid.
- `astar.py`: implementasi inti A* saja.
- `gbfs.py`: implementasi inti GBFS saja.
- `metrics.py`: pengukuran waktu dan memori.
- `report.py`: visualisasi hasil, tampilan perbandingan, serta penyimpanan CSV/TXT.
- `tests/`: pengujian otomatis.

Tidak perlu memisahkan algoritma dalam folder `algorithms/`, membuat `benchmark.py`, atau membuat `display.py`. Jangan langsung menghapus file lama sebelum memeriksa apakah masih dipakai. Saat merapikan proyek yang sudah berjalan, pindahkan kode secara bertahap, perbaiki import, jalankan test, lalu hapus file lama hanya setelah tidak lagi digunakan.

## 5. Tahapan pengerjaan

### Tahap 1 — Audit proyek yang sudah ada

- Periksa direktori kerja dan semua file Python.
- Baca isi file sebelum mengubahnya.
- Periksa cara menjalankan program dan test yang sudah tersedia.
- Identifikasi kode yang sudah benar dan harus dipertahankan.
- Bandingkan struktur saat ini dengan struktur sederhana versi 2.0.
- Jangan menganggap source code kosong hanya berdasarkan progress lama.

### Tahap 2 — Grid Maze

Implementasikan atau rapikan `maze.py` untuk menyediakan:

- Enam preset deterministik.
- Input Grid kustom.
- Validasi ukuran dan isi Grid.
- Validasi Start dan Goal.
- Fungsi tetangga dengan urutan atas, kanan, bawah, kiri.
- Manhattan Distance.
- Informasi ukuran dan jumlah sel.

Uji Grid persegi, persegi panjang, input salah, koordinat di luar batas, Start/Goal pada dinding, dan Start sama dengan Goal.

### Tahap 3 — Algoritma inti

Implementasikan dua fungsi inti secara terpisah:

- `astar_search(grid, start, goal)` pada `astar.py`.
- `gbfs_search(grid, start, goal)` pada `gbfs.py`.

Ketentuan A*:

- Prioritas `f(n) = g(n) + h(n)`.
- Gunakan `heapq`, `g_score`, `parent`, `closed_set`, dan counter tie-breaking.
- Abaikan entri heap yang kedaluwarsa.
- Rekonstruksi jalur saat Goal dikeluarkan dari heap secara valid.

Ketentuan GBFS:

- Prioritas hanya `f(n) = h(n)`.
- Jangan masukkan `g(n)` ke prioritas.
- Gunakan `heapq`, `discovered`, `parent`, dan counter tie-breaking.
- Tandai simpul ditemukan saat pertama kali dimasukkan ke frontier.
- Rekonstruksi jalur saat Goal dikeluarkan dari heap.

Kedua fungsi harus mengembalikan field yang sama: `algorithm`, `found`, `path`, `path_length`, `generated_nodes`, `expanded_nodes`, dan `explored`.

**Jangan memasukkan pengukuran waktu/memori, input, print, visualisasi, atau ekspor laporan ke dalam file/fungsi algoritma inti.**

### Tahap 4 — Pengukuran dan laporan

Di `metrics.py`:

- Ukur waktu menggunakan `time.perf_counter_ns()`.
- Gunakan satu pemanasan yang tidak dicatat dan 10 pengulangan pengukuran.
- Timer dimulai tepat sebelum fungsi algoritma dipanggil dan dihentikan tepat sesudah fungsi tersebut selesai.
- Hitung rata-rata dan median dalam milidetik.
- Ukur memori secara terpisah menggunakan `tracemalloc` sebanyak 10 pengulangan.
- Ambil median peak traced memory dalam KB.
- Gunakan `try/finally` agar `tracemalloc.stop()` selalu dipanggil.

Pastikan yang diukur hanya pemanggilan fungsi algoritma inti. Pembuatan Grid, validasi awal, input, visualisasi, pemeriksaan jalur tambahan, print, tabel, dan penulisan file harus dilakukan di luar interval ukur.

Di `report.py`:

- Tampilkan visualisasi Grid awal.
- Tampilkan visualisasi hasil A* dan GBFS secara terpisah.
- Tampilkan status, jalur, panjang jalur, generated nodes, expanded nodes, waktu, dan memori.
- Simpan dua baris perbandingan (A* dan GBFS) ke CSV.
- Simpan ringkasan kasus ke TXT.
- Gunakan timestamp pada nama file agar hasil lama tidak tertimpa.

### Tahap 5 — Menu utama

Buat alur pada `main.py` sesederhana berikut:

1. Tampilkan menu Grid Preset, Grid Kustom, dan Keluar.
2. Ambil atau bentuk Grid berdasarkan pilihan pengguna.
3. Validasi Grid dan koordinat.
4. Jika valid, jalankan A* dan GBFS pada input yang sama.
5. Jalankan pengukuran waktu dan memori terpisah.
6. Tampilkan hasil dan simpan CSV/TXT.
7. Berikan pilihan kembali ke menu utama atau keluar.

Jangan menambahkan menu untuk memilih algoritma karena kedua algoritma harus selalu dibandingkan bersama.

### Tahap 6 — Pengujian dan pemeriksaan akhir

- Buat atau pertahankan `tests/test_maze.py` dan `tests/test_algorithms.py`.
- Uji delapan skenario pada `project.md`.
- Gunakan BFS sederhana hanya sebagai oracle internal unit test untuk memeriksa optimalitas A*.
- Jalankan test setelah setiap perubahan yang relevan.
- Jalankan satu contoh preset dan satu contoh Grid kustom melalui CLI.
- Pastikan CSV dapat dibaca dan mempunyai dua baris hasil algoritma.
- Pastikan TXT merangkum kasus dan hasil aktual.
- Pastikan tidak ada kode pengukuran yang masuk ke fungsi inti algoritma.

## 6. Standar kode Python

- Ikuti PEP 8 secara wajar.
- Gunakan `snake_case` untuk fungsi dan variabel.
- Gunakan type hints pada fungsi penting.
- Beri docstring pada fungsi publik atau logika yang tidak langsung jelas.
- Pilih struktur data sederhana dan konsisten.
- Hindari class atau abstraksi tambahan jika fungsi biasa sudah cukup.
- Hindari duplikasi yang nyata, tetapi jangan membuat kerangka generik yang sulit dipahami hanya untuk mengurangi beberapa baris kode.
- Jangan mengubah matriks Grid sumber selama pencarian atau visualisasi.
- Tangani input salah secara spesifik. Jangan menggunakan `except Exception` untuk menyembunyikan bug.
- Gunakan standard library Python; jangan menambah dependensi eksternal tanpa alasan dan persetujuan pengguna.

## 7. Standar pengukuran yang wajib dipatuhi

1. A* dan GBFS memakai Grid, Start, dan Goal identik.
2. Fungsi inti algoritma mengurus pencarian dan rekonstruksi jalur saja.
3. Waktu diukur menggunakan `perf_counter_ns()` tepat di sekitar pemanggilan fungsi inti.
4. Memori diukur secara terpisah menggunakan `tracemalloc`.
5. Pembuatan Grid dan validasi awal dilakukan sebelum pengukuran.
6. Tidak boleh ada `print`, visualisasi, validasi jalur tambahan, atau penulisan file di interval pengukuran.
7. Setiap pengulangan harus membuat state pencarian baru.
8. Hasil CSV harus berasal dari nilai pengukuran yang benar-benar diperoleh.
9. Jelaskan bahwa `tracemalloc` mengukur alokasi Python yang dilacak, bukan seluruh RAM komputer.
10. Jangan menyatakan algoritma tertentu selalu lebih cepat atau lebih hemat memori.

## 8. Cara menjelaskan kepada pengguna

Pengguna sedang mempelajari Python dan algoritma. Karena itu:

- Jelaskan tujuan file sebelum memberikan perubahan kode.
- Jelaskan kode per bagian dan alur program setelah implementasi.
- Jelaskan istilah seperti frontier, priority queue, heuristic, parent, `g_score`, discovered, generated nodes, dan expanded nodes dengan contoh Grid kecil.
- Tunjukkan contoh sederhana sebelum contoh yang lebih rumit.
- Jelaskan alasan teknis tanpa membebani pengguna dengan teori yang tidak dibutuhkan.
- Berikan perintah terminal yang siap disalin dan sebutkan direktori tempat perintah dijalankan.
- Jangan memberikan seluruh source code sekaligus apabila lebih baik dikerjakan per tahap.

## 9. Protokol setelah mengubah source code

Setiap kali mengubah kode:

1. Sebutkan file yang dibuat/diubah.
2. Jelaskan alasan dan tanggung jawab perubahan.
3. Jalankan pemeriksaan atau test yang relevan jika akses terminal tersedia.
4. Laporkan perintah yang dijalankan dan hasil aktualnya.
5. Jika test gagal, periksa penyebabnya dan perbaiki; jangan menghapus test agar terlihat lulus.
6. Jangan menyatakan fitur atau tahap selesai jika belum diperiksa.
7. Jika kode tidak dapat dijalankan di lingkungan kerja, nyatakan dengan jelas bahwa hasilnya belum terverifikasi dan berikan perintah untuk pengguna.

Perintah pemeriksaan dasar:

```bash
python --version
python -m compileall -q .
python -m unittest discover -s tests -v
python main.py
```

## 10. Larangan

- Jangan mengganti A* atau GBFS dengan library eksternal.
- Jangan mengubah prioritas A* dari `g(n) + h(n)`.
- Jangan menambahkan `g(n)` ke prioritas GBFS.
- Jangan mengaktifkan gerakan diagonal.
- Jangan mengubah biaya langkah `1`.
- Jangan memasukkan pengukuran waktu/memori, print, input, atau visualisasi ke fungsi inti algoritma.
- Jangan mengembalikan benchmark delapan dataset, menu benchmark terpisah, atau struktur modul berlebihan tanpa permintaan pengguna.
- Jangan membuat angka hasil pengujian sendiri.
- Jangan menghapus implementasi atau folder lama sebelum memeriksa ketergantungannya.

## 11. Format laporan kemajuan

Setelah satu tahap selesai, gunakan format berikut:

```text
TAHAP: [nama tahap]

File dibuat/diubah:
- [nama file] — [tujuan]

Implementasi:
- [fitur yang selesai]

Pemeriksaan:
- Perintah: [perintah yang dijalankan]
- Hasil: [hasil aktual]

Catatan:
- [kendala/asumsi yang masih ada]

Tahap berikutnya:
- [pekerjaan selanjutnya]
```

Perbarui `progress.md` hanya berdasarkan perubahan source code dan pemeriksaan yang benar-benar dilakukan.

## 12. Definisi selesai

Proyek dianggap selesai jika alur menu berjalan, preset dan Grid kustom berfungsi, kedua algoritma dijalankan otomatis pada Grid yang sama, jalur dan metrik benar, pengukuran waktu/memori hanya mencakup fungsi inti, unit test berjalan, CSV/TXT dihasilkan dari data aktual, dan README menjelaskan cara menjalankan program.

**Prinsip utama:** implementasi algoritma harus tetap standar, program dibuat sesederhana mungkin, pengukuran dilakukan secara adil, dan semua hasil dilaporkan apa adanya.
