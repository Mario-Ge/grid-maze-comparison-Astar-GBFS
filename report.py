
"""
report.py

Modul untuk:
- Visualisasi Grid Maze.
- Menampilkan informasi Grid.
- Menampilkan hasil algoritma.
- Menampilkan tabel perbandingan.
- Menyimpan hasil eksperimen ke CSV.
- Menyimpan laporan hasil ke TXT.
"""

import csv

from datetime import datetime
from pathlib import Path
from typing import Any

from maze import Coordinate, Grid, get_grid_info


# ============================================================
# 1. VISUALISASI GRID
# ============================================================

def render_grid(
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
    path: list[Coordinate] | None = None,
    explored: set[Coordinate] | None = None,
) -> list[list[str]]:
    """
    Membuat representasi visual Grid Maze.

    Prioritas simbol:
    1. Start dan Goal.
    2. Dinding.
    3. Jalur akhir.
    4. Sel yang dieksplorasi.
    5. Sel kosong.
    
    Grid asli tidak diubah.
    """

    path_cells = set(path or [])
    explored_cells = set(explored or [])

    visual_grid = []

    for row_index, row in enumerate(grid):

        visual_row = []

        for col_index, cell in enumerate(row):

            position = (row_index, col_index)

            # Start dan Goal memiliki prioritas tertinggi.
            if position == start:
                symbol = "S"

            elif position == goal:
                symbol = "G"

            # Dinding.
            elif cell == 1:
                symbol = "#"

            # Jalur akhir.
            elif position in path_cells:
                symbol = "*"

            # Sel yang sudah dieksplorasi.
            elif position in explored_cells:
                symbol = "e"

            # Sel kosong.
            else:
                symbol = "."

            visual_row.append(symbol)

        visual_grid.append(visual_row)

    return visual_grid


def display_grid(
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
    path: list[Coordinate] | None = None,
    explored: set[Coordinate] | None = None,
    title: str = "Visualisasi Grid",
) -> None:
    """
    Menampilkan Grid Maze di terminal.
    """

    visual_grid = render_grid(
        grid,
        start,
        goal,
        path,
        explored,
    )

    print()
    print("=" * 50)
    print(title)
    print("=" * 50)

    for row in visual_grid:
        print(" ".join(row))


# ============================================================
# 2. INFORMASI GRID
# ============================================================

def display_grid_info(
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
) -> None:
    """
    Menampilkan informasi dasar Grid Maze.
    """

    info = get_grid_info(grid, start, goal)

    print()
    print("=" * 50)
    print("INFORMASI GRID")
    print("=" * 50)

    print(f"Jumlah baris       : {info['rows']}")
    print(f"Jumlah kolom       : {info['cols']}")
    print(f"Jumlah seluruh sel : {info['n']}")
    print(f"Sel yang dapat dilalui: {info['passable_cells']}")
    print(f"Jumlah dinding     : {info['wall_cells']}")

    print(
        f"Start              : "
        f"({info['start_row']}, {info['start_col']})"
    )

    print(
        f"Goal               : "
        f"({info['goal_row']}, {info['goal_col']})"
    )


# ============================================================
# 3. MENAMPILKAN HASIL ALGORITMA
# ============================================================

def display_algorithm_result(
    algorithm_metrics: dict[str, Any],
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
) -> None:
    """
    Menampilkan hasil pencarian dan pengukuran
    satu algoritma.
    """

    result = algorithm_metrics["result"]

    algorithm_name = result["algorithm"]

    print()
    print("=" * 50)
    print(f"HASIL ALGORITMA {algorithm_name}")
    print("=" * 50)

    # Status pencarian.
    status = (
        "Ditemukan"
        if result["found"]
        else "Tidak ditemukan"
    )

    print(f"Status           : {status}")

    # Jalur.
    if result["found"]:
        print(f"Path             : {result['path']}")
        print(f"Path Length      : {result['path_length']}")
    else:
        print("Path             : Tidak ditemukan")
        print("Path Length      : Tidak ditemukan")

    # Metrik simpul.
    print(
        f"Generated Nodes  : "
        f"{result['generated_nodes']}"
    )

    print(
        f"Expanded Nodes   : "
        f"{result['expanded_nodes']}"
    )

    # Pengukuran waktu.
    print()
    print("PENGUKURAN WAKTU")

    print(f"Pengulangan      : {algorithm_metrics['time_runs']}")

    print(
        f"Rata-rata        : "
        f"{algorithm_metrics['time_mean_ms']:.6f} ms"
    )

    print(
        f"Median           : "
        f"{algorithm_metrics['time_median_ms']:.6f} ms"
    )

    # Pengukuran memori.
    print()
    print("PENGUKURAN MEMORI")

    print(f"Pengulangan      : {algorithm_metrics['memory_runs']}")

    print(
        f"Median Peak      : "
        f"{algorithm_metrics['memory_median_kb']:.6f} KB"
    )

    # Visualisasi hasil pencarian.
    display_grid(
        grid,
        start,
        goal,
        result["path"],
        result["explored"],
        title=f"VISUALISASI {algorithm_name}",
    )


# ============================================================
# 4. TABEL PERBANDINGAN ALGORITMA
# ============================================================

def display_comparison_table(
    algorithm_metrics: list[dict[str, Any]],
) -> None:
    """
    Menampilkan tabel perbandingan A* dan GBFS.
    """

    print()
    print("=" * 100)
    print("TABEL PERBANDINGAN A* DAN GBFS")
    print("=" * 100)

    header = (
        f"{'Algoritma':<12}"
        f"{'Status':<14}"
        f"{'Path':>8}"
        f"{'Generated':>12}"
        f"{'Expanded':>12}"
        f"{'Median (ms)':>16}"
        f"{'Memory (KB)':>16}"
    )

    print(header)
    print("-" * 100)

    for metrics in algorithm_metrics:

        result = metrics["result"]

        algorithm = result["algorithm"]

        status = (
            "Ditemukan"
            if result["found"]
            else "Gagal"
        )

        path_length = (
            str(result["path_length"])
            if result["path_length"] is not None
            else "-"
        )

        print(
            f"{algorithm:<12}"
            f"{status:<14}"
            f"{path_length:>8}"
            f"{result['generated_nodes']:>12}"
            f"{result['expanded_nodes']:>12}"
            f"{metrics['time_median_ms']:>16.6f}"
            f"{metrics['memory_median_kb']:>16.6f}"
        )

    print("=" * 100)


# ============================================================
# 5. MEMBUAT KESIMPULAN BERDASARKAN HASIL AKTUAL
# ============================================================

def _build_conclusion(
    algorithm_metrics: list[dict[str, Any]],
) -> list[str]:
    """
    Membuat kesimpulan berdasarkan hasil pengukuran aktual.

    Kesimpulan hanya berlaku untuk kasus Grid yang diuji.
    """

    results = {
        item["result"]["algorithm"]: item
        for item in algorithm_metrics
    }

    lines = []

    astar = results.get("A*")
    gbfs = results.get("GBFS")

    if astar is None or gbfs is None:
        return [
            "Perbandingan belum lengkap karena kedua hasil "
            "algoritma belum tersedia."
        ]

    astar_result = astar["result"]
    gbfs_result = gbfs["result"]

    # Perbandingan keberhasilan pencarian.
    if astar_result["found"] and gbfs_result["found"]:

        if astar_result["path_length"] == gbfs_result["path_length"]:
            lines.append(
                "A* dan GBFS menemukan jalur dengan panjang "
                "yang sama pada kasus ini."
            )

        else:
            lines.append(
                f"A* menghasilkan jalur sepanjang "
                f"{astar_result['path_length']} langkah, "
                f"sedangkan GBFS menghasilkan jalur sepanjang "
                f"{gbfs_result['path_length']} langkah."
            )

    elif astar_result["found"]:
        lines.append(
            "A* menemukan jalur, sedangkan GBFS tidak menemukan jalur."
        )

    elif gbfs_result["found"]:
        lines.append(
            "GBFS menemukan jalur, sedangkan A* tidak menemukan jalur."
        )

    else:
        lines.append(
            "Kedua algoritma tidak menemukan jalur pada kasus ini."
        )

    # Perbandingan jumlah expanded nodes.
    astar_expanded = astar_result["expanded_nodes"]
    gbfs_expanded = gbfs_result["expanded_nodes"]

    if astar_expanded < gbfs_expanded:
        lines.append(
            "A* mengeksplorasi lebih sedikit simpul pada kasus ini."
        )

    elif gbfs_expanded < astar_expanded:
        lines.append(
            "GBFS mengeksplorasi lebih sedikit simpul pada kasus ini."
        )

    else:
        lines.append(
            "Jumlah expanded nodes kedua algoritma sama."
        )

    # Perbandingan median waktu.
    astar_time = astar["time_median_ms"]
    gbfs_time = gbfs["time_median_ms"]

    if astar_time < gbfs_time:
        lines.append(
            "Median waktu A* lebih rendah pada pengukuran ini."
        )

    elif gbfs_time < astar_time:
        lines.append(
            "Median waktu GBFS lebih rendah pada pengukuran ini."
        )

    else:
        lines.append(
            "Median waktu kedua algoritma sama."
        )

    # Perbandingan median memori.
    astar_memory = astar["memory_median_kb"]
    gbfs_memory = gbfs["memory_median_kb"]

    if astar_memory < gbfs_memory:
        lines.append(
            "Median peak traced memory A* lebih rendah pada kasus ini."
        )

    elif gbfs_memory < astar_memory:
        lines.append(
            "Median peak traced memory GBFS lebih rendah pada kasus ini."
        )

    else:
        lines.append(
            "Median peak traced memory kedua algoritma sama."
        )

    return lines


# ============================================================
# 6. MENYIMPAN HASIL PERBANDINGAN KE CSV DAN TXT
# ============================================================

def save_comparison_outputs(
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
    maze_type: str,
    maze_name: str,
    algorithm_metrics: list[dict[str, Any]],
    output_dir: str = "outputs",
) -> tuple[Path, Path]:
    """
    Menyimpan hasil satu Grid ke dua file:

    1. CSV: dua baris hasil algoritma.
    2. TXT: laporan ringkasan perbandingan.

    Kedua file menggunakan timestamp yang sama.
    """

    # --------------------------------------------------------
    # A. Persiapan informasi
    # --------------------------------------------------------

    now = datetime.now()

    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    filename_timestamp = now.strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    info = get_grid_info(grid, start, goal)

    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_path = output_path / (
        f"single_comparison_{filename_timestamp}.csv"
    )

    txt_path = output_path / (
        f"comparison_report_{filename_timestamp}.txt"
    )

    # --------------------------------------------------------
    # B. Menyimpan CSV
    # --------------------------------------------------------

    fieldnames = [
        "timestamp",
        "maze_type",
        "maze_name",
        "rows",
        "cols",
        "n",
        "passable_cells",
        "wall_cells",
        "start_row",
        "start_col",
        "goal_row",
        "goal_col",
        "algorithm",
        "found",
        "path_length",
        "generated_nodes",
        "expanded_nodes",
        "time_runs",
        "time_mean_ms",
        "time_median_ms",
        "memory_runs",
        "memory_median_kb",
    ]

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for metrics in algorithm_metrics:

            result = metrics["result"]

            row = {
                "timestamp": timestamp,
                "maze_type": maze_type,
                "maze_name": maze_name,
                "rows": info["rows"],
                "cols": info["cols"],
                "n": info["n"],
                "passable_cells": info["passable_cells"],
                "wall_cells": info["wall_cells"],
                "start_row": info["start_row"],
                "start_col": info["start_col"],
                "goal_row": info["goal_row"],
                "goal_col": info["goal_col"],
                "algorithm": result["algorithm"],
                "found": result["found"],
                "path_length": result["path_length"],
                "generated_nodes": result["generated_nodes"],
                "expanded_nodes": result["expanded_nodes"],
                "time_runs": metrics["time_runs"],
                "time_mean_ms": metrics["time_mean_ms"],
                "time_median_ms": metrics["time_median_ms"],
                "memory_runs": metrics["memory_runs"],
                "memory_median_kb": metrics["memory_median_kb"],
            }

            writer.writerow(row)

    # --------------------------------------------------------
    # C. Menyusun laporan TXT
    # --------------------------------------------------------

    lines = [
        "=" * 65,
        "LAPORAN PERBANDINGAN ALGORITMA A* DAN GBFS",
        "GRID MAZE",
        "=" * 65,
        "",
        f"Tanggal pengujian : {timestamp}",
        f"Jenis Grid        : {maze_type}",
        f"Nama Grid         : {maze_name}",
        "",
        "INFORMASI GRID",
        "-" * 65,
        f"Jumlah baris       : {info['rows']}",
        f"Jumlah kolom       : {info['cols']}",
        f"Jumlah seluruh sel : {info['n']}",
        f"Sel dapat dilalui  : {info['passable_cells']}",
        f"Jumlah dinding     : {info['wall_cells']}",
        f"Start              : {start}",
        f"Goal               : {goal}",
        "",
    ]

    # Hasil setiap algoritma.
    for metrics in algorithm_metrics:

        result = metrics["result"]

        lines.extend([
            "=" * 65,
            f"HASIL {result['algorithm']}",
            "=" * 65,
            f"Status          : {'Ditemukan' if result['found'] else 'Tidak ditemukan'}",
            f"Path            : {result['path']}",
            f"Path Length     : {result['path_length']}",
            f"Generated Nodes : {result['generated_nodes']}",
            f"Expanded Nodes  : {result['expanded_nodes']}",
            f"Time Runs       : {metrics['time_runs']}",
            f"Time Mean       : {metrics['time_mean_ms']:.6f} ms",
            f"Time Median     : {metrics['time_median_ms']:.6f} ms",
            f"Memory Runs     : {metrics['memory_runs']}",
            f"Memory Median   : {metrics['memory_median_kb']:.6f} KB",
            "",
        ])

    # Tabel perbandingan.
    lines.extend([
        "=" * 65,
        "RINGKASAN PERBANDINGAN",
        "=" * 65,
        "",
        f"{'Algoritma':<12}"
        f"{'Path':>8}"
        f"{'Generated':>12}"
        f"{'Expanded':>12}",
        "-" * 44,
    ])

    for metrics in algorithm_metrics:

        result = metrics["result"]

        lines.append(
            f"{result['algorithm']:<12}"
            f"{str(result['path_length']):>8}"
            f"{result['generated_nodes']:>12}"
            f"{result['expanded_nodes']:>12}"
        )

    # Kesimpulan berdasarkan data aktual.
    lines.extend([
        "",
        "=" * 65,
        "KESIMPULAN",
        "=" * 65,
    ])

    lines.extend(_build_conclusion(algorithm_metrics))

    # Catatan metodologi pengukuran.
    lines.extend([
        "",
        "=" * 65,
        "CATATAN PENGUKURAN",
        "=" * 65,
        (
            "Pengukuran waktu hanya mencakup pemanggilan "
            "fungsi inti algoritma."
        ),
        (
            "Pengukuran memori dilakukan secara terpisah "
            "menggunakan tracemalloc."
        ),
        (
            "tracemalloc mengukur alokasi memori Python yang "
            "dilacak, bukan keseluruhan RAM proses."
        ),
        (
            "Hasil pengukuran berlaku untuk kasus Grid dan "
            "lingkungan pengujian ini."
        ),
        "",
    ])

    txt_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return csv_path, txt_path