
"""
gbfs.py

Implementasi Greedy Best-First Search (GBFS)
untuk pencarian jalur pada Grid Maze.

Prioritas pencarian:
    f(n) = h(n)

GBFS hanya menggunakan Manhattan Distance
dan tidak mempertimbangkan biaya aktual perjalanan.
"""

from heapq import heappop, heappush
from itertools import count

from maze import (
    Coordinate,
    Grid,
    get_neighbors,
    manhattan_distance,
)


# ============================================================
# 1. REKONSTRUKSI JALUR
# ============================================================

def _reconstruct_path(
    parent: dict[Coordinate, Coordinate],
    current: Coordinate,
) -> list[Coordinate]:
    """
    Membangun kembali jalur dari Goal menuju Start.

    Parent menyimpan posisi sebelumnya dari setiap koordinat.
    Hasil akhir dibalik agar urutannya Start menuju Goal.
    """

    path = [current]

    while current in parent:
        current = parent[current]
        path.append(current)

    path.reverse()

    return path


# ============================================================
# 2. ALGORITMA GREEDY BEST-FIRST SEARCH
# ============================================================

def gbfs_search(
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
) -> dict:
    """
    Menjalankan algoritma Greedy Best-First Search.

    Parameter:
        grid  : Matriks Grid Maze.
        start : Koordinat awal.
        goal  : Koordinat tujuan.

    Mengembalikan:
        dictionary berisi:
        - algorithm
        - found
        - path
        - path_length
        - generated_nodes
        - expanded_nodes
        - explored
    """

    # --------------------------------------------------------
    # A. Inisialisasi Priority Queue
    # --------------------------------------------------------

    frontier = []

    # Counter digunakan untuk tie-breaking deterministik.
    counter = count()

    # Hitung Manhattan Distance dari Start ke Goal.
    start_h = manhattan_distance(start, goal)

    # Format heap:
    # (nilai_heuristik, urutan, posisi)
    #
    # GBFS menggunakan:
    # f(n) = h(n)

    heappush(
        frontier,
        (
            start_h,
            next(counter),
            start,
        ),
    )

    # --------------------------------------------------------
    # B. Inisialisasi Struktur Data Pencarian
    # --------------------------------------------------------

    # Mencatat semua posisi yang sudah ditemukan.
    # Start dihitung sebagai posisi yang sudah ditemukan.
    discovered: set[Coordinate] = {
        start
    }

    # Menyimpan posisi sebelumnya.
    parent: dict[Coordinate, Coordinate] = {}

    # Posisi yang sudah dieksplorasi.
    explored: set[Coordinate] = set()

    # Start dihitung sebagai satu generated node.
    generated_nodes = 1

    # Belum ada posisi yang diproses.
    expanded_nodes = 0

    # --------------------------------------------------------
    # C. Proses Pencarian
    # --------------------------------------------------------

    while frontier:

        # Ambil posisi dengan Manhattan Distance terkecil.
        heuristic, _, current = heappop(frontier)

        # Tandai posisi sebagai sudah dieksplorasi.
        explored.add(current)

        # Tambahkan jumlah posisi yang diproses.
        expanded_nodes += 1

        # ----------------------------------------------------
        # C1. Periksa apakah Goal sudah ditemukan.
        # ----------------------------------------------------

        # Goal dinyatakan ditemukan ketika dikeluarkan
        # dari Priority Queue.
        if current == goal:

            path = _reconstruct_path(parent, current)

            return {
                "algorithm": "GBFS",
                "found": True,
                "path": path,
                "path_length": len(path) - 1,
                "generated_nodes": generated_nodes,
                "expanded_nodes": expanded_nodes,
                "explored": explored,
            }

        # ----------------------------------------------------
        # C2. Periksa seluruh tetangga.
        # ----------------------------------------------------

        neighbors = get_neighbors(grid, current)

        for neighbor in neighbors:

            # Setiap koordinat hanya boleh dimasukkan
            # ke dalam frontier satu kali.
            if neighbor in discovered:
                continue

            # Tandai sebagai sudah ditemukan.
            discovered.add(neighbor)

            # Simpan asal posisi.
            parent[neighbor] = current

            # Setiap posisi baru dihitung sebagai
            # satu generated node.
            generated_nodes += 1

            # Hitung Manhattan Distance menuju Goal.
            h_score = manhattan_distance(
                neighbor,
                goal,
            )

            # Masukkan ke Priority Queue.
            #
            # Perhatikan:
            # Tidak ada g(n) di dalam prioritas GBFS.

            heappush(
                frontier,
                (
                    h_score,
                    next(counter),
                    neighbor,
                ),
            )

    # --------------------------------------------------------
    # D. Goal Tidak Ditemukan
    # --------------------------------------------------------

    # Jika Priority Queue kosong, berarti tidak ada
    # jalur yang dapat mencapai Goal.

    return {
        "algorithm": "GBFS",
        "found": False,
        "path": None,
        "path_length": None,
        "generated_nodes": generated_nodes,
        "expanded_nodes": expanded_nodes,
        "explored": explored,
    }
