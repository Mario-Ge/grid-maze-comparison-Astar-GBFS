
"""
maze.py

Modul untuk mengelola Grid Maze:
- Enam Grid preset.
- Pembuatan Grid kustom.
- Validasi Grid, Start, dan Goal.
- Pencarian tetangga.
- Manhattan Distance.
- Informasi dasar Grid.
"""

from typing import TypeAlias


# ============================================================
# 1. TYPE ALIAS
# ============================================================

Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = list[list[int]]


# ============================================================
# 2. GRID PRESET
# ============================================================

# Format setiap preset:
# (nama, matriks_grid, koordinat_start, koordinat_goal)

PRESETS: dict[
    int,
    tuple[str, Grid, Coordinate, Coordinate]
] = {

    # Preset 1: Grid terbuka tanpa dinding.
    1: (
        "Grid Terbuka",
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        (0, 0),
        (4, 4),
    ),

    # Preset 2: Satu penghalang dengan jalur alternatif.
    2: (
        "Grid Satu Penghalang",
        [
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        (0, 0),
        (0, 4),
    ),

    # Preset 3: Koridor sempit dengan beberapa belokan.
    3: (
        "Grid Koridor Sempit",
        [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ],
        (1, 1),
        (5, 5),
    ),

    # Preset 4: Banyak penghalang, tetapi tersedia jalur.
    4: (
        "Grid Banyak Penghalang",
        [
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 1],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0],
        ],
        (0, 0),
        (6, 6),
    ),

    # Preset 5: Tidak ada jalur karena kolom tengah
    # sepenuhnya tertutup dinding.
    5: (
        "Grid Tanpa Jalur",
        [
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ],
        (2, 0),
        (2, 4),
    ),

    # Preset 6: Grid persegi panjang 4 baris x 7 kolom.
    6: (
        "Grid Persegi Panjang",
        [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0],
        ],
        (0, 0),
        (3, 6),
    ),
}


# ============================================================
# 3. MENDAPATKAN DAFTAR PRESET
# ============================================================

def list_presets() -> list[tuple[int, str]]:
    """
    Mengembalikan nomor dan nama seluruh Grid preset.
    """

    return [
        (number, preset[0])
        for number, preset in PRESETS.items()
    ]


# ============================================================
# 4. MENDAPATKAN GRID PRESET
# ============================================================

def get_preset(
    preset_number: int,
) -> tuple[Grid, Coordinate, Coordinate, str]:
    """
    Mengambil Grid berdasarkan nomor preset.

    Mengembalikan:
    - grid
    - start
    - goal
    - nama preset
    """

    if preset_number not in PRESETS:
        raise ValueError(
            f"Nomor preset {preset_number} tidak tersedia."
        )

    name, original_grid, start, goal = PRESETS[preset_number]

    # Salin Grid agar perubahan tidak memengaruhi preset asli.
    grid = [row.copy() for row in original_grid]

    validate_grid(grid, start, goal)

    return grid, start, goal, name


# ============================================================
# 5. MEMBUAT GRID KUSTOM
# ============================================================

def create_custom_grid(
    rows: int,
    cols: int,
    row_inputs: list[str],
) -> Grid:
    """
    Membuat Grid kustom dari input setiap baris.

    Format input:
    - 0 = sel kosong.
    - 1 = dinding.

    Contoh:
    ["000100", "010000", "000000"]
    """

    if type(rows) is not int or rows <= 0:
        raise ValueError(
            "Jumlah baris harus berupa bilangan bulat positif."
        )

    if type(cols) is not int or cols <= 0:
        raise ValueError(
            "Jumlah kolom harus berupa bilangan bulat positif."
        )

    if len(row_inputs) != rows:
        raise ValueError(
            f"Grid harus memiliki tepat {rows} baris."
        )

    grid: Grid = []

    for index, raw_row in enumerate(row_inputs):

        if not isinstance(raw_row, str):
            raise ValueError(
                f"Input baris ke-{index + 1} harus berupa teks."
            )

        row = raw_row.strip()

        if len(row) != cols:
            raise ValueError(
                f"Baris ke-{index + 1} harus memiliki "
                f"tepat {cols} karakter."
            )

        if any(character not in "01" for character in row):
            raise ValueError(
                f"Baris ke-{index + 1} hanya boleh "
                "mengandung karakter 0 dan 1."
            )

        grid.append([
            int(character)
            for character in row
        ])

    return grid


# ============================================================
# 6. VALIDASI GRID, START, DAN GOAL
# ============================================================

def validate_grid(
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
) -> None:
    """
    Memvalidasi struktur Grid, Start, dan Goal.

    Memunculkan ValueError jika ditemukan input tidak valid.
    """

    if not isinstance(grid, list) or not grid:
        raise ValueError("Grid tidak boleh kosong.")

    if any(not isinstance(row, list) or not row for row in grid):
        raise ValueError(
            "Setiap baris Grid harus berupa list yang tidak kosong."
        )

    rows = len(grid)
    cols = len(grid[0])

    # Memastikan semua baris mempunyai jumlah kolom sama.
    for index, row in enumerate(grid):

        if len(row) != cols:
            raise ValueError(
                f"Jumlah kolom pada baris ke-{index + 1} "
                "tidak konsisten."
            )

    # Memastikan seluruh sel hanya berisi 0 atau 1.
    for row in grid:

        for cell in row:

            if type(cell) is not int or cell not in (0, 1):
                raise ValueError(
                    "Setiap sel Grid hanya boleh bernilai 0 atau 1."
                )

    # Validasi koordinat Start dan Goal.
    for label, coordinate in (
        ("Start", start),
        ("Goal", goal),
    ):

        if not isinstance(coordinate, (tuple, list)):
            raise ValueError(
                f"Koordinat {label} harus berupa pasangan koordinat."
            )

        if len(coordinate) != 2:
            raise ValueError(
                f"Koordinat {label} harus memiliki dua nilai."
            )

        row, col = coordinate

        if (
            type(row) is not int
            or type(col) is not int
        ):
            raise ValueError(
                f"Koordinat {label} harus berupa bilangan bulat."
            )

        if not (0 <= row < rows and 0 <= col < cols):
            raise ValueError(
                f"Koordinat {label} berada di luar batas Grid."
            )

        if grid[row][col] == 1:
            raise ValueError(
                f"Koordinat {label} tidak boleh berada pada dinding."
            )


# ============================================================
# 7. MENDAPATKAN TETANGGA
# ============================================================

def get_neighbors(
    grid: Grid,
    position: Coordinate,
) -> list[Coordinate]:
    """
    Mendapatkan tetangga yang dapat dilalui.

    Urutan pemeriksaan:
    1. Atas
    2. Kanan
    3. Bawah
    4. Kiri

    Pergerakan diagonal tidak diperbolehkan.
    """

    row, col = position

    rows = len(grid)
    cols = len(grid[0])

    # Urutan arah harus konsisten agar hasil deterministik.
    directions = [
        (-1, 0),  # Atas
        (0, 1),   # Kanan
        (1, 0),   # Bawah
        (0, -1),  # Kiri
    ]

    neighbors: list[Coordinate] = []

    for row_offset, col_offset in directions:

        next_row = row + row_offset
        next_col = col + col_offset

        # Memastikan posisi berada dalam batas Grid.
        if (
            0 <= next_row < rows
            and 0 <= next_col < cols
        ):

            # Hanya sel kosong yang dapat dilalui.
            if grid[next_row][next_col] == 0:

                neighbors.append(
                    (next_row, next_col)
                )

    return neighbors


# ============================================================
# 8. MANHATTAN DISTANCE
# ============================================================

def manhattan_distance(
    position: Coordinate,
    goal: Coordinate,
) -> int:
    """
    Menghitung Manhattan Distance antara dua koordinat.

    Rumus:
    h(n) = |r - r_goal| + |c - c_goal|
    """

    row_distance = abs(position[0] - goal[0])
    col_distance = abs(position[1] - goal[1])

    return row_distance + col_distance


# ============================================================
# 9. INFORMASI GRID
# ============================================================

def get_grid_info(
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
) -> dict[str, int]:
    """
    Menghasilkan informasi dasar Grid.

    Informasi:
    - Jumlah baris.
    - Jumlah kolom.
    - Jumlah seluruh sel.
    - Jumlah sel yang dapat dilalui.
    - Jumlah dinding.
    - Koordinat Start.
    - Koordinat Goal.
    """

    validate_grid(grid, start, goal)

    rows = len(grid)
    cols = len(grid[0])

    passable_cells = sum(
        cell == 0
        for row in grid
        for cell in row
    )

    wall_cells = sum(
        cell == 1
        for row in grid
        for cell in row
    )

    return {
        "rows": rows,
        "cols": cols,
        "n": rows * cols,
        "passable_cells": passable_cells,
        "wall_cells": wall_cells,
        "start_row": start[0],
        "start_col": start[1],
        "goal_row": goal[0],
        "goal_col": goal[1],
    }