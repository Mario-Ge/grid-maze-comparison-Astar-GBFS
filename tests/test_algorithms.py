
"""
test_algorithms.py

Unit test untuk algoritma:
- A*
- Greedy Best-First Search (GBFS)

Pengujian mencakup delapan skenario fungsional
dan pemeriksaan optimalitas A* menggunakan BFS.

BFS hanya digunakan sebagai oracle di dalam test.
"""

import unittest

from collections import deque

from maze import (
    get_preset,
    create_custom_grid,
    validate_grid,
    manhattan_distance,
)

from astar import astar_search
from gbfs import gbfs_search


# ============================================================
# 1. DAFTAR ALGORITMA YANG DIUJI
# ============================================================

ALGORITHMS = [
    astar_search,
    gbfs_search,
]


# ============================================================
# 2. BFS ORACLE
# ============================================================

def bfs_shortest_path_length(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> int | None:
    """
    Menghitung panjang jalur terpendek menggunakan BFS.

    Fungsi ini hanya digunakan sebagai oracle di unit test.

    Mengembalikan:
    - Integer panjang jalur jika Goal ditemukan.
    - None jika tidak ada jalur.
    """

    rows = len(grid)
    cols = len(grid[0])

    # Queue menyimpan posisi dan jarak dari Start.
    queue = deque([
        (start, 0)
    ])

    visited = {
        start
    }

    # Urutan gerakan:
    # Atas, kanan, bawah, kiri.
    directions = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]

    while queue:

        current, distance = queue.popleft()

        # Jika Goal ditemukan, kembalikan jaraknya.
        if current == goal:
            return distance

        row, col = current

        for row_offset, col_offset in directions:

            next_row = row + row_offset
            next_col = col + col_offset

            neighbor = (next_row, next_col)

            # Memastikan posisi berada dalam batas Grid.
            if not (
                0 <= next_row < rows
                and 0 <= next_col < cols
            ):
                continue

            # Tidak boleh melewati dinding.
            if grid[next_row][next_col] != 0:
                continue

            # Setiap posisi hanya dikunjungi sekali.
            if neighbor in visited:
                continue

            visited.add(neighbor)

            queue.append(
                (neighbor, distance + 1)
            )

    # Tidak ada jalur menuju Goal.
    return None


# ============================================================
# 3. TEST ALGORITMA
# ============================================================

class TestAlgorithms(unittest.TestCase):
    """Pengujian fungsional untuk A* dan GBFS."""

    # ========================================================
    # HELPER: MEMASTIKAN JALUR VALID
    # ========================================================

    def assert_valid_path(
        self,
        grid,
        start,
        goal,
        result,
    ):
        """
        Memastikan jalur yang ditemukan valid.

        Pemeriksaan:
        - Jalur dimulai dari Start.
        - Jalur berakhir di Goal.
        - Semua posisi berada dalam Grid.
        - Tidak melewati dinding.
        - Tidak bergerak diagonal.
        - Panjang jalur sesuai jumlah perpindahan.
        """

        self.assertTrue(result["found"])

        path = result["path"]

        self.assertIsInstance(path, list)

        self.assertGreaterEqual(len(path), 1)

        # Jalur harus dimulai dari Start.
        self.assertEqual(path[0], start)

        # Jalur harus berakhir di Goal.
        self.assertEqual(path[-1], goal)

        rows = len(grid)
        cols = len(grid[0])

        # Periksa setiap posisi.
        for row, col in path:

            # Posisi harus berada dalam batas Grid.
            self.assertTrue(
                0 <= row < rows
                and 0 <= col < cols
            )

            # Posisi tidak boleh berupa dinding.
            self.assertEqual(
                grid[row][col],
                0,
            )

        # Periksa setiap perpindahan.
        for index in range(len(path) - 1):

            current = path[index]
            next_position = path[index + 1]

            distance = manhattan_distance(
                current,
                next_position,
            )

            # Setiap perpindahan harus tepat satu sel.
            self.assertEqual(distance, 1)

        # Panjang jalur harus sesuai jumlah perpindahan.
        self.assertEqual(
            result["path_length"],
            len(path) - 1,
        )

    # ========================================================
    # HELPER: MEMASTIKAN HASIL KEDUA ALGORITMA
    # ========================================================

    def run_both_algorithms(
        self,
        grid,
        start,
        goal,
    ):
        """
        Menjalankan A* dan GBFS dengan input yang sama.
        """

        validate_grid(grid, start, goal)

        results = {}

        for search_function in ALGORITHMS:

            result = search_function(
                grid,
                start,
                goal,
            )

            results[result["algorithm"]] = result

        return results

    # ========================================================
    # FT-01: GRID TERBUKA
    # ========================================================

    def test_open_grid(self):
        """
        Memastikan A* dan GBFS menemukan jalur
        pada Grid terbuka.
        """

        grid, start, goal, _ = get_preset(1)

        results = self.run_both_algorithms(
            grid,
            start,
            goal,
        )

        for algorithm_name, result in results.items():

            with self.subTest(algorithm=algorithm_name):

                self.assert_valid_path(
                    grid,
                    start,
                    goal,
                    result,
                )

                # Jarak Manhattan minimum adalah 8.
                self.assertEqual(
                    result["path_length"],
                    8,
                )

    # ========================================================
    # FT-02: GRID SATU PENGHALANG
    # ========================================================

    def test_single_obstacle_grid(self):
        """
        Memastikan kedua algoritma menemukan jalur
        alternatif ketika terdapat satu penghalang.
        """

        grid, start, goal, _ = get_preset(2)

        results = self.run_both_algorithms(
            grid,
            start,
            goal,
        )

        for algorithm_name, result in results.items():

            with self.subTest(algorithm=algorithm_name):

                self.assert_valid_path(
                    grid,
                    start,
                    goal,
                    result,
                )

    # ========================================================
    # FT-03: GRID BANYAK PENGHALANG
    # ========================================================

    def test_multiple_obstacles_grid(self):
        """
        Memastikan kedua algoritma menemukan jalur
        pada Grid dengan banyak penghalang.
        """

        grid, start, goal, _ = get_preset(4)

        results = self.run_both_algorithms(
            grid,
            start,
            goal,
        )

        for algorithm_name, result in results.items():

            with self.subTest(algorithm=algorithm_name):

                self.assert_valid_path(
                    grid,
                    start,
                    goal,
                    result,
                )

    # ========================================================
    # FT-04: GRID TANPA JALUR
    # ========================================================

    def test_no_path_grid(self):
        """
        Memastikan kedua algoritma gagal menemukan jalur
        jika Start dan Goal tidak terhubung.
        """

        grid, start, goal, _ = get_preset(5)

        results = self.run_both_algorithms(
            grid,
            start,
            goal,
        )

        for algorithm_name, result in results.items():

            with self.subTest(algorithm=algorithm_name):

                self.assertFalse(
                    result["found"]
                )

                self.assertIsNone(
                    result["path"]
                )

                self.assertIsNone(
                    result["path_length"]
                )

                self.assertGreaterEqual(
                    result["generated_nodes"],
                    1,
                )

    # ========================================================
    # FT-05: START SAMA DENGAN GOAL
    # ========================================================

    def test_start_equals_goal(self):
        """
        Memastikan kedua algoritma dapat menangani
        Start yang sama dengan Goal.
        """

        grid = [
            [0, 0],
            [0, 0],
        ]

        start = (0, 0)
        goal = (0, 0)

        results = self.run_both_algorithms(
            grid,
            start,
            goal,
        )

        for algorithm_name, result in results.items():

            with self.subTest(algorithm=algorithm_name):

                self.assertTrue(result["found"])

                self.assertEqual(
                    result["path"],
                    [start],
                )

                self.assertEqual(
                    result["path_length"],
                    0,
                )

                self.assertEqual(
                    result["generated_nodes"],
                    1,
                )

                self.assertEqual(
                    result["expanded_nodes"],
                    1,
                )

                self.assertEqual(
                    result["explored"],
                    {start},
                )

    # ========================================================
    # FT-06: GRID PERSEGI PANJANG
    # ========================================================

    def test_rectangular_grid(self):
        """
        Memastikan kedua algoritma bekerja pada Grid
        dengan jumlah baris dan kolom berbeda.
        """

        grid, start, goal, _ = get_preset(6)

        # Pastikan Grid bukan berbentuk persegi.
        self.assertNotEqual(
            len(grid),
            len(grid[0]),
        )

        results = self.run_both_algorithms(
            grid,
            start,
            goal,
        )

        for algorithm_name, result in results.items():

            with self.subTest(algorithm=algorithm_name):

                self.assert_valid_path(
                    grid,
                    start,
                    goal,
                    result,
                )

    # ========================================================
    # FT-07: TIDAK BOLEH BERGERAK DIAGONAL
    # ========================================================

    def test_diagonal_only_path_is_not_allowed(self):
        """
        Memastikan algoritma tidak bergerak diagonal.

        Start dan Goal hanya bersinggungan secara diagonal.
        """

        grid = [
            [0, 1],
            [1, 0],
        ]

        start = (0, 0)
        goal = (1, 1)

        results = self.run_both_algorithms(
            grid,
            start,
            goal,
        )

        for algorithm_name, result in results.items():

            with self.subTest(algorithm=algorithm_name):

                self.assertFalse(
                    result["found"]
                )

                self.assertIsNone(
                    result["path"]
                )

                self.assertIsNone(
                    result["path_length"]
                )

    # ========================================================
    # FT-08: INPUT GRID TIDAK VALID
    # ========================================================

    def test_invalid_grid_input_is_rejected(self):
        """
        Memastikan Grid dengan input tidak valid
        ditolak sebelum pencarian.
        """

        # Karakter tidak valid.
        with self.assertRaises(ValueError):

            create_custom_grid(
                rows=2,
                cols=3,
                row_inputs=[
                    "000",
                    "01A",
                ],
            )

        # Koordinat Start berada di luar Grid.
        grid = [
            [0, 0],
            [0, 0],
        ]

        with self.assertRaises(ValueError):

            validate_grid(
                grid,
                (2, 0),
                (1, 1),
            )

    # ========================================================
    # 4. TEST OPTIMALITAS A*
    # ========================================================

    def test_astar_matches_bfs_optimal_path(self):
        """
        Memastikan panjang jalur A* sama dengan
        panjang jalur optimal yang dihitung BFS.

        BFS hanya digunakan sebagai oracle unit test.
        """

        # Uji seluruh enam preset.
        for preset_number, _ in [
            (number, name)
            for number, name in [
                (1, "Grid Terbuka"),
                (2, "Grid Satu Penghalang"),
                (3, "Grid Koridor Sempit"),
                (4, "Grid Banyak Penghalang"),
                (5, "Grid Tanpa Jalur"),
                (6, "Grid Persegi Panjang"),
            ]
        ]:

            with self.subTest(preset=preset_number):

                grid, start, goal, _ = get_preset(
                    preset_number
                )

                # Hitung jalur optimal menggunakan BFS.
                bfs_length = bfs_shortest_path_length(
                    grid,
                    start,
                    goal,
                )

                # Jalankan A*.
                astar_result = astar_search(
                    grid,
                    start,
                    goal,
                )

                if bfs_length is None:

                    # Jika BFS tidak menemukan jalur,
                    # A* juga tidak boleh menemukan jalur.
                    self.assertFalse(
                        astar_result["found"]
                    )

                    self.assertIsNone(
                        astar_result["path_length"]
                    )

                else:

                    # A* wajib menemukan jalur.
                    self.assertTrue(
                        astar_result["found"]
                    )

                    # Panjang jalur A* harus optimal.
                    self.assertEqual(
                        astar_result["path_length"],
                        bfs_length,
                    )

                    # Periksa validitas jalur A*.
                    self.assert_valid_path(
                        grid,
                        start,
                        goal,
                        astar_result,
                    )

    # ========================================================
    # 5. TEST FORMAT HASIL ALGORITMA
    # ========================================================

    def test_result_fields_are_consistent(self):
        """
        Memastikan kedua algoritma menghasilkan
        struktur dictionary dengan field yang sama.
        """

        grid, start, goal, _ = get_preset(1)

        expected_fields = {
            "algorithm",
            "found",
            "path",
            "path_length",
            "generated_nodes",
            "expanded_nodes",
            "explored",
        }

        for search_function in ALGORITHMS:

            with self.subTest(
                algorithm=search_function.__name__
            ):

                result = search_function(
                    grid,
                    start,
                    goal,
                )

                self.assertEqual(
                    set(result.keys()),
                    expected_fields,
                )

                self.assertGreaterEqual(
                    result["generated_nodes"],
                    1,
                )

                self.assertGreaterEqual(
                    result["expanded_nodes"],
                    1,
                )

                self.assertIsInstance(
                    result["explored"],
                    set,
                )


if __name__ == "__main__":
    unittest.main()
