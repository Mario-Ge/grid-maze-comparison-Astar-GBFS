
"""
main.py

Program utama untuk perbandingan algoritma A* dan GBFS
pada pencarian jalur Grid Maze.

Menu utama:
1. Gunakan Grid Preset.
2. Buat Grid Kustom.
3. Keluar.

Setelah Grid valid:
- Jalankan A*.
- Jalankan GBFS.
- Ukur waktu dan memori.
- Tampilkan visualisasi.
- Tampilkan perbandingan.
- Simpan CSV dan TXT.
"""

from pathlib import Path

from maze import (
    list_presets,
    get_preset,
    create_custom_grid,
    validate_grid,
    Coordinate,
    Grid,
)

from astar import astar_search
from gbfs import gbfs_search

from metrics import measure_algorithm

from report import (
    display_grid_info,
    display_grid,
    display_algorithm_result,
    display_comparison_table,
    save_comparison_outputs,
)


# ============================================================
# 1. KONFIGURASI DIREKTORI OUTPUT
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = PROJECT_DIR / "outputs"


# ============================================================
# 2. MENU UTAMA
# ============================================================

def display_main_menu() -> None:
    """
    Menampilkan menu utama aplikasi.
    """

    print("\n")
    print("=" * 50)
    print("       PERBANDINGAN A* DAN GBFS")
    print("                GRID MAZE")
    print("=" * 50)

    print("1. Gunakan Grid Preset")
    print("2. Buat Grid Kustom")
    print("3. Keluar")

    print("=" * 50)


# ============================================================
# 3. INPUT BILANGAN BULAT POSITIF
# ============================================================

def read_positive_integer(prompt: str) -> int:
    """
    Meminta input bilangan bulat positif.

    Input yang salah akan diminta ulang.
    """

    while True:

        raw_value = input(prompt).strip()

        try:
            value = int(raw_value)

        except ValueError:
            print(
                "Input tidak valid. "
                "Masukkan bilangan bulat."
            )
            continue

        if value <= 0:
            print(
                "Nilai harus lebih besar dari nol."
            )
            continue

        return value


# ============================================================
# 4. MEMILIH GRID PRESET
# ============================================================

def select_preset():
    """
    Menampilkan enam preset dan meminta pengguna memilihnya.

    Mengembalikan:
    - grid
    - start
    - goal
    - nama preset
    """

    print("\n")
    print("=" * 50)
    print("DAFTAR GRID PRESET")
    print("=" * 50)

    for number, name in list_presets():
        print(f"{number}. {name}")

    print("0. Kembali ke Menu Utama")
    print("=" * 50)

    while True:

        raw_choice = input(
            "Pilih Grid Preset: "
        ).strip()

        try:
            choice = int(raw_choice)

        except ValueError:
            print(
                "Input tidak valid. "
                "Masukkan nomor preset."
            )
            continue

        if choice == 0:
            return None

        try:
            return get_preset(choice)

        except ValueError as error:
            print(f"Pilihan tidak valid: {error}")


# ============================================================
# 5. INPUT BARIS GRID KUSTOM
# ============================================================

def read_custom_rows(
    rows: int,
    cols: int,
) -> list[str]:
    """
    Meminta isi setiap baris Grid kustom.

    Format:
    - 0 = sel kosong.
    - 1 = dinding.

    Setiap baris harus memiliki jumlah karakter
    yang sama dengan jumlah kolom.
    """

    row_inputs = []

    print("\n")
    print("=" * 50)
    print("INPUT ISI GRID")
    print("=" * 50)

    print("Gunakan 0 untuk sel kosong.")
    print("Gunakan 1 untuk dinding.")
    print(f"Setiap baris harus memiliki {cols} karakter.")

    for index in range(rows):

        while True:

            raw_row = input(
                f"Baris {index + 1}: "
            ).strip()

            # Periksa jumlah karakter.
            if len(raw_row) != cols:

                print(
                    f"Baris harus memiliki tepat "
                    f"{cols} karakter."
                )

                continue

            # Periksa karakter yang digunakan.
            if any(
                character not in "01"
                for character in raw_row
            ):

                print(
                    "Baris hanya boleh menggunakan "
                    "karakter 0 dan 1."
                )

                continue

            row_inputs.append(raw_row)

            break

    return row_inputs


# ============================================================
# 6. INPUT KOORDINAT START DAN GOAL
# ============================================================

def read_coordinate(
    label: str,
    grid: Grid,
) -> Coordinate:
    """
    Meminta koordinat Start atau Goal.

    Format input:
    baris,kolom

    Contoh:
    0,0
    (0,0)

    Koordinat harus:
    - Berada di dalam batas Grid.
    - Tidak berada pada dinding.
    """

    rows = len(grid)
    cols = len(grid[0])

    while True:

        raw_coordinate = input(
            f"Masukkan koordinat {label} (baris,kolom): "
        ).strip()

        # Mendukung format (0,0) maupun 0,0.
        cleaned_coordinate = raw_coordinate.strip("()")

        parts = cleaned_coordinate.split(",")

        if len(parts) != 2:

            print(
                "Format koordinat salah. "
                "Contoh yang benar: 0,0"
            )

            continue

        try:

            row = int(parts[0].strip())
            col = int(parts[1].strip())

        except ValueError:

            print(
                "Koordinat harus berupa bilangan bulat."
            )

            continue

        # Periksa batas Grid.
        if not (
            0 <= row < rows
            and 0 <= col < cols
        ):

            print(
                f"Koordinat {label} berada di luar Grid."
            )

            continue

        # Periksa apakah posisi merupakan dinding.
        if grid[row][col] == 1:

            print(
                f"Koordinat {label} berada pada dinding. "
                "Pilih sel yang bernilai 0."
            )

            continue

        return (row, col)


# ============================================================
# 7. MEMBUAT GRID KUSTOM
# ============================================================

def create_custom_maze():
    """
    Meminta pengguna membuat Grid kustom.

    Tahapan:
    1. Memasukkan jumlah baris.
    2. Memasukkan jumlah kolom.
    3. Memasukkan isi setiap baris.
    4. Memasukkan koordinat Start.
    5. Memasukkan koordinat Goal.
    6. Memvalidasi Grid.

    Mengembalikan:
    grid, start, goal, nama Grid.
    """

    print("\n")
    print("=" * 50)
    print("MEMBUAT GRID KUSTOM")
    print("=" * 50)

    # --------------------------------------------------------
    # A. Input ukuran Grid
    # --------------------------------------------------------

    rows = read_positive_integer(
        "Masukkan jumlah baris: "
    )

    cols = read_positive_integer(
        "Masukkan jumlah kolom: "
    )

    # --------------------------------------------------------
    # B. Input isi Grid
    # --------------------------------------------------------

    row_inputs = read_custom_rows(
        rows,
        cols,
    )

    grid = create_custom_grid(
        rows,
        cols,
        row_inputs,
    )

    # --------------------------------------------------------
    # C. Input Start dan Goal
    # --------------------------------------------------------

    print("\n")
    print("INFORMASI KOORDINAT")
    print(f"Indeks baris : 0 sampai {rows - 1}")
    print(f"Indeks kolom : 0 sampai {cols - 1}")

    start = read_coordinate(
        "Start",
        grid,
    )

    goal = read_coordinate(
        "Goal",
        grid,
    )

    # --------------------------------------------------------
    # D. Validasi Grid
    # --------------------------------------------------------

    validate_grid(
        grid,
        start,
        goal,
    )

    return (
        grid,
        start,
        goal,
        "Grid Kustom",
    )


# ============================================================
# 8. MENJALANKAN PERBANDINGAN A* DAN GBFS
# ============================================================

def run_comparison(
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
    maze_type: str,
    maze_name: str,
) -> None:
    """
    Menjalankan seluruh proses perbandingan.

    Proses:
    1. Validasi Grid.
    2. Tampilkan Grid awal.
    3. Ukur A*.
    4. Ukur GBFS.
    5. Tampilkan hasil masing-masing.
    6. Tampilkan tabel perbandingan.
    7. Simpan CSV dan TXT.
    """

    # --------------------------------------------------------
    # A. Validasi awal
    # --------------------------------------------------------

    validate_grid(
        grid,
        start,
        goal,
    )

    # --------------------------------------------------------
    # B. Informasi Grid
    # --------------------------------------------------------

    print("\n")
    print("=" * 50)
    print("MEMULAI PERBANDINGAN")
    print("=" * 50)

    print(f"Nama Grid: {maze_name}")

    display_grid_info(
        grid,
        start,
        goal,
    )

    # --------------------------------------------------------
    # C. Tampilkan Grid awal
    # --------------------------------------------------------

    display_grid(
        grid,
        start,
        goal,
        title="GRID AWAL",
    )

    # --------------------------------------------------------
    # D. Pengukuran A*
    # --------------------------------------------------------

    print("\nMengukur kinerja A*...")

    astar_metrics = measure_algorithm(
        astar_search,
        grid,
        start,
        goal,
    )

    # --------------------------------------------------------
    # E. Pengukuran GBFS
    # --------------------------------------------------------

    print("Mengukur kinerja GBFS...")

    gbfs_metrics = measure_algorithm(
        gbfs_search,
        grid,
        start,
        goal,
    )

    # --------------------------------------------------------
    # F. Gabungkan hasil kedua algoritma
    # --------------------------------------------------------

    algorithm_metrics = [
        astar_metrics,
        gbfs_metrics,
    ]

    # --------------------------------------------------------
    # G. Tampilkan hasil A*
    # --------------------------------------------------------

    display_algorithm_result(
        astar_metrics,
        grid,
        start,
        goal,
    )

    # --------------------------------------------------------
    # H. Tampilkan hasil GBFS
    # --------------------------------------------------------

    display_algorithm_result(
        gbfs_metrics,
        grid,
        start,
        goal,
    )

    # --------------------------------------------------------
    # I. Tampilkan tabel perbandingan
    # --------------------------------------------------------

    display_comparison_table(
        algorithm_metrics,
    )

    # --------------------------------------------------------
    # J. Simpan hasil CSV dan TXT
    # --------------------------------------------------------

    try:

        csv_path, txt_path = save_comparison_outputs(
            grid=grid,
            start=start,
            goal=goal,
            maze_type=maze_type,
            maze_name=maze_name,
            algorithm_metrics=algorithm_metrics,
            output_dir=str(OUTPUT_DIR),
        )

        print("\n")
        print("=" * 50)
        print("HASIL BERHASIL DISIMPAN")
        print("=" * 50)

        print(f"CSV : {csv_path}")
        print(f"TXT : {txt_path}")

    except OSError as error:

        print("\nGagal menyimpan file laporan.")
        print(f"Detail: {error}")


# ============================================================
# 9. PILIHAN KEMBALI KE MENU ATAU KELUAR
# ============================================================

def ask_continue() -> bool:
    """
    Meminta pengguna kembali ke menu utama atau keluar.

    Mengembalikan:
    - True  = kembali ke menu utama.
    - False = keluar dari program.
    """

    print("\n")
    print("=" * 50)
    print("APA YANG INGIN KAMU LAKUKAN?")
    print("=" * 50)

    print("1. Kembali ke Menu Utama")
    print("2. Keluar")

    while True:

        choice = input(
            "Pilih menu: "
        ).strip()

        if choice == "1":
            return True

        if choice == "2":
            return False

        print(
            "Pilihan tidak valid. "
            "Masukkan 1 atau 2."
        )


# ============================================================
# 10. FUNGSI PROGRAM UTAMA
# ============================================================

def main() -> None:
    """
    Mengatur alur utama aplikasi Grid Maze.
    """

    while True:

        # ----------------------------------------------------
        # A. Tampilkan menu utama
        # ----------------------------------------------------

        display_main_menu()

        choice = input(
            "Pilih menu: "
        ).strip()

        # ----------------------------------------------------
        # B. Keluar dari aplikasi
        # ----------------------------------------------------

        if choice == "3":

            print("\nTerima kasih telah menggunakan program.")

            break

        # ----------------------------------------------------
        # C. Memilih Grid preset
        # ----------------------------------------------------

        elif choice == "1":

            selected_grid = select_preset()

            # Pengguna memilih kembali ke menu utama.
            if selected_grid is None:
                continue

            grid, start, goal, maze_name = selected_grid

            maze_type = "preset"

        # ----------------------------------------------------
        # D. Membuat Grid kustom
        # ----------------------------------------------------

        elif choice == "2":

            grid, start, goal, maze_name = create_custom_maze()

            maze_type = "custom"

        # ----------------------------------------------------
        # E. Pilihan menu tidak valid
        # ----------------------------------------------------

        else:

            print(
                "Pilihan tidak valid. "
                "Silakan pilih 1, 2, atau 3."
            )

            continue

        # ----------------------------------------------------
        # F. Jalankan perbandingan
        # ----------------------------------------------------

        run_comparison(
            grid,
            start,
            goal,
            maze_type,
            maze_name,
        )

        # ----------------------------------------------------
        # G. Kembali ke menu atau keluar
        # ----------------------------------------------------

        should_continue = ask_continue()

        if not should_continue:

            print("\nTerima kasih telah menggunakan program.")

            break


# ============================================================
# 11. ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna.")

    except EOFError:
        print("\n\nInput berakhir. Program dihentikan.")
