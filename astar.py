
"""
astar.py

Implementasi algoritma A* untuk pencarian jalur pada Grid Maze.

Prioritas pencarian:
    f(n) = g(n) + h(n)

Keterangan:
    g(n) = biaya aktual dari Start ke posisi sekarang.
    h(n) = estimasi jarak ke Goal menggunakan Manhattan Distance.
    f(n) = total biaya aktual dan estimasi.
"""

from heapq import heappop, heappush
from itertools import count
from math import inf

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
# 2. ALGORITMA A*
# ============================================================

def astar_search(
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
) -> dict:
    """
    Menjalankan algoritma A* pada Grid Maze.

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

    # Posisi awal memiliki biaya aktual sebesar 0.
    start_g = 0

    # Hitung heuristic posisi awal menuju Goal.
    start_h = manhattan_distance(start, goal)

    # Format heap:
    # (nilai_prioritas, urutan, posisi, biaya_aktual)
    #
    # A* menggunakan:
    # f(n) = g(n) + h(n)

    heappush(
        frontier,
        (
            start_g + start_h,
            next(counter),
            start,
            start_g,
        ),
    )

    # --------------------------------------------------------
    # B. Inisialisasi Struktur Data Pencarian
    # --------------------------------------------------------

    # Biaya terbaik dari Start menuju setiap posisi.
    g_score: dict[Coordinate, int] = {
        start: 0
    }

    # Menyimpan posisi sebelumnya.
    parent: dict[Coordinate, Coordinate] = {}

    # Posisi yang sudah diproses.
    closed_set: set[Coordinate] = set()

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

        # Ambil posisi dengan nilai prioritas terkecil.
        priority, _, current, entry_g = heappop(frontier)

        # ----------------------------------------------------
        # C1. Periksa entri heap yang sudah kedaluwarsa.
        # ----------------------------------------------------

        # Jika biaya pada heap berbeda dengan g_score terbaru,
        # berarti sudah ada jalur yang lebih baik.
        if entry_g != g_score.get(current, inf):
            continue

        # Lewati posisi yang sudah diproses.
        if current in closed_set:
            continue

        # Tandai posisi sebagai sudah diproses.
        closed_set.add(current)

        # Catat posisi yang dieksplorasi.
        explored.add(current)

        # Tambahkan jumlah posisi yang diproses.
        expanded_nodes += 1

        # ----------------------------------------------------
        # C2. Periksa apakah Goal sudah ditemukan.
        # ----------------------------------------------------

        # Goal dinyatakan ditemukan ketika dikeluarkan
        # dari heap melalui entri yang valid.
        if current == goal:

            path = _reconstruct_path(parent, current)

            return {
                "algorithm": "A*",
                "found": True,
                "path": path,
                "path_length": len(path) - 1,
                "generated_nodes": generated_nodes,
                "expanded_nodes": expanded_nodes,
                "explored": explored,
            }

        # ----------------------------------------------------
        # C3. Periksa seluruh tetangga.
        # ----------------------------------------------------

        neighbors = get_neighbors(grid, current)

        for neighbor in neighbors:

            # Tidak perlu memproses posisi yang sudah ditutup.
            if neighbor in closed_set:
                continue

            # Setiap perpindahan memiliki biaya 1.
            tentative_g = entry_g + 1

            # Ambil biaya terbaik yang sudah diketahui.
            previous_g = g_score.get(neighbor)

            # ------------------------------------------------
            # C4. Periksa apakah ditemukan jalur lebih baik.
            # ------------------------------------------------

            if (
                previous_g is None
                or tentative_g < previous_g
            ):

                # Jika posisi belum pernah ditemukan,
                # hitung sebagai generated node baru.
                if previous_g is None:
                    generated_nodes += 1

                # Perbarui biaya terbaik.
                g_score[neighbor] = tentative_g

                # Simpan asal posisi.
                parent[neighbor] = current

                # Hitung heuristic menuju Goal.
                h_score = manhattan_distance(
                    neighbor,
                    goal,
                )

                # Hitung prioritas A*.
                f_score = tentative_g + h_score

                # Masukkan posisi ke Priority Queue.
                heappush(
                    frontier,
                    (
                        f_score,
                        next(counter),
                        neighbor,
                        tentative_g,
                    ),
                )

    # --------------------------------------------------------
    # D. Goal Tidak Ditemukan
    # --------------------------------------------------------

    # Jika Priority Queue kosong, berarti tidak ada
    # jalur yang dapat mencapai Goal.

    return {
        "algorithm": "A*",
        "found": False,
        "path": None,
        "path_length": None,
        "generated_nodes": generated_nodes,
        "expanded_nodes": expanded_nodes,
        "explored": explored,
    }
