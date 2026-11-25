# PROGRESS.md — Perkembangan Proyek Grid Maze A* vs GBFS

> **Versi catatan:** 2.0  
> **Tanggal revisi dokumen:** 22 November 2026  
> **Spesifikasi aktif:** `project.md` versi 2.0  
> **Pedoman aktif:** `skill.md` versi 2.0  
> **Status dokumen:** Revisi tiga dokumen selesai; source code belum diaudit ulang terhadap spesifikasi sederhana versi 2.0.

---

## 1. Identitas proyek

**Judul:** Analisis Perbandingan Kinerja Algoritma A* dan Greedy Best-First Search (GBFS) pada Pencarian Jalur Grid Maze Menggunakan Python.

**Tujuan:** Membandingkan hasil pencarian jalur dan kinerja A* dengan GBFS pada Grid Maze yang sama, menggunakan kasus sederhana yang dapat diperiksa kembali melalui CSV dan Excel.

**Lingkungan pengembangan yang pernah dikonfirmasi:**

- Python `3.12.3`.
- Virtual environment berada di `/home/mg/Python/grid-maze-comparison/.venv`.
- Pip `24.0`.
- Ubuntu.
- Program menggunakan Python standard library.

Informasi lingkungan di atas berasal dari catatan pemeriksaan sebelumnya. Periksa kembali apabila direktori atau lingkungan pengembangan sudah berubah.

## 2. Keputusan spesifikasi versi 2.0

Permintaan terbaru pengguna adalah menyederhanakan struktur proyek dan alur program, tetapi tetap mempertahankan hasil utama perbandingan A* dan GBFS.

Keputusan yang berlaku:

1. Menu awal hanya berisi **Gunakan Grid Preset**, **Buat Grid Kustom**, dan **Keluar**.
2. Setelah Grid valid, program otomatis menjalankan A* dan GBFS pada Grid, Start, dan Goal yang sama.
3. Tidak ada lagi menu untuk memilih A*, GBFS, atau perbandingan secara terpisah.
4. Enam preset tetap dipertahankan.
5. Grid kustom tetap mendukung bentuk persegi dan persegi panjang.
6. Aturan algoritma tetap standar: A* menggunakan `g(n) + h(n)`, sedangkan GBFS menggunakan `h(n)` saja.
7. Heuristik tetap Manhattan Distance, biaya langkah `1`, dan pergerakan empat arah tanpa diagonal.
8. Hasil pencarian tetap memuat status, jalur, panjang jalur, generated nodes, expanded nodes, dan explored.
9. Visualisasi hasil A* dan GBFS tetap ditampilkan terpisah.
10. Pengukuran waktu dan memori hanya membungkus pemanggilan fungsi algoritma inti. Input, validasi awal, visualisasi, dan ekspor tidak ikut dihitung.
11. Pengukuran waktu menggunakan satu pemanasan dan 10 pengulangan; hasil meliputi rata-rata dan median.
12. Pengukuran memori dilakukan terpisah dengan 10 pengulangan; hasil yang dilaporkan adalah median peak traced memory.
13. Hasil eksperimen satu Grid disimpan ke satu CSV dengan dua baris hasil algoritma dan satu laporan TXT.
14. Pengujian fungsional tetap menggunakan `unittest` dan tidak membutuhkan sistem ekspor test tersendiri.
15. Benchmark delapan dataset, menu benchmark khusus, dan modul yang berlebihan dihapus dari ruang lingkup versi sederhana.

## 3. Struktur proyek target

Struktur sederhana yang ditetapkan pada `project.md` versi 2.0:

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

Tanggung jawab utama:

| File | Tanggung jawab |
|---|---|
| `main.py` | Menu dan alur program; otomatis menjalankan dua algoritma |
| `maze.py` | Preset, input kustom, validasi, tetangga, heuristik, dan informasi Grid |
| `astar.py` | Fungsi inti A* |
| `gbfs.py` | Fungsi inti GBFS |
| `metrics.py` | Pengukuran waktu dan memori fungsi inti |
| `report.py` | Visualisasi, ringkasan, ekspor CSV dan TXT |
| `tests/` | Pengujian fungsional |

Struktur lama yang memuat folder `algorithms/`, `benchmark.py`, atau `display.py` perlu diperiksa sebelum dirapikan. Jangan menghapus file lama sebelum isi dan import-nya diperiksa.

## 4. Status dokumen

| Dokumen | Status | Keterangan |
|---|---|---|
| `project.md` | Selesai direvisi | Spesifikasi versi 2.0, alur program dan struktur lebih sederhana |
| `skill.md` | Selesai direvisi | Pedoman implementasi sesuai spesifikasi versi 2.0 |
| `progress.md` | Selesai direvisi | Catatan keputusan dan status terbaru |

Ketiga dokumen versi 2.0 saling disesuaikan dan menggantikan isi perencanaan versi 1.0.

## 5. Status source code

Catatan progress versi 1.1 menyebut kerangka folder dan file placeholder. Namun, percakapan pengembangan yang lebih baru telah memuat proses implementasi/pengujian `maze.py` dan test Grid. Oleh karena itu, status lama yang menyatakan seluruh implementasi belum dimulai tidak boleh dipakai sebagai gambaran kondisi source code saat ini.

**Status yang aman untuk saat ini:** source code sudah mulai dikerjakan, tetapi belum dilakukan audit lengkap dalam revisi dokumen ini. Belum dapat dinyatakan bahwa seluruh source code sudah sesuai spesifikasi versi 2.0.

Sebelum melanjutkan implementasi:

1. Periksa struktur folder dan file lokal.
2. Periksa isi `maze.py`, file algoritma, `main.py`, file pengukuran, laporan, dan test.
3. Catat implementasi yang sudah benar agar tidak ditulis ulang.
4. Sesuaikan struktur lama ke struktur sederhana secara bertahap.
5. Pastikan fungsi inti A* dan GBFS tidak berisi pengukuran atau output.
6. Jalankan kembali seluruh test setelah penyesuaian.

## 6. Keluaran yang diharapkan

Setelah program versi 2.0 selesai, setiap satu kasus Grid menghasilkan:

- Tampilan Grid awal.
- Hasil A* dan visualisasi jalurnya.
- Hasil GBFS dan visualisasi jalurnya.
- Status pencarian, panjang jalur, generated nodes, dan expanded nodes.
- Rata-rata/median waktu eksekusi fungsi inti.
- Median peak traced memory fungsi inti.
- CSV perbandingan yang dapat dibuka di Excel.
- Laporan ringkas TXT.

Pola file keluaran:

```text
outputs/
├── single_comparison_YYYYMMDD_HHMMSS.csv
└── comparison_report_YYYYMMDD_HHMMSS.txt
```

CSV memuat dua baris utama, yaitu satu baris A* dan satu baris GBFS. Untuk membandingkan beberapa kasus di Excel, jalankan program pada beberapa preset atau Grid kustom, lalu gabungkan data CSV yang dihasilkan.

## 7. Pemeriksaan yang harus dilakukan

Perintah dasar dari direktori proyek:

```bash
python --version
find . -maxdepth 3 -not -path './.venv*' -print | sort
python -m compileall -q .
python -m unittest discover -s tests -v
python main.py
```

Pemeriksaan manual minimal:

- Pilih satu Grid preset terbuka.
- Pilih satu preset yang mempunyai penghalang.
- Pilih preset tanpa jalur.
- Buat satu Grid kustom sederhana.
- Pastikan setiap Grid valid menjalankan A* dan GBFS otomatis.
- Pastikan kedua algoritma menerima input yang sama.
- Pastikan waktu dan memori tidak mengukur proses input, validasi awal, visualisasi, atau ekspor.
- Buka CSV di Excel dan periksa dua baris algoritma beserta kolom metriknya.
- Buka laporan TXT dan cocokkan nilainya dengan hasil terminal/CSV.

Jangan mengubah status pemeriksaan menjadi lulus sebelum perintah atau pemeriksaan benar-benar dijalankan.

## 8. Langkah berikutnya

**Tahap berikutnya: audit source code yang sudah ada, lalu lakukan penyesuaian bertahap ke spesifikasi versi 2.0.**

Urutan kerja:

1. Periksa `pwd` dan `find . -maxdepth 3 -not -path './.venv*' -print | sort`.
2. Periksa isi file Python yang sudah ada.
3. Cocokkan struktur saat ini dengan struktur target di bagian 3.
4. Identifikasi apakah kode algoritma berada di `algorithms/astar.py` dan `algorithms/gbfs.py` atau sudah berada di lokasi lain.
5. Rapikan lokasi file tanpa mengubah rumus inti A* dan GBFS.
6. Sederhanakan menu `main.py` agar pemilihan Grid langsung menjalankan kedua algoritma.
7. Pastikan pengukuran di `metrics.py` hanya membungkus fungsi inti algoritma.
8. Sesuaikan `report.py` agar menghasilkan CSV dan TXT.
9. Jalankan compile check, unit test, dan uji CLI.
10. Perbarui progress ini berdasarkan hasil aktual.

---

**Prinsip pemeliharaan:** `project.md` adalah spesifikasi, `skill.md` adalah pedoman pengerjaan, dan `progress.md` adalah catatan kondisi aktual. Jika ada perubahan kebutuhan, revisi ketiganya secara konsisten. Jangan menghapus implementasi lama sebelum memastikan kode tersebut tidak lagi diperlukan.
