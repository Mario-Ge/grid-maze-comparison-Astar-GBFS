
"""
test_maze.py

Unit test untuk modul maze.py.

Pengujian meliputi:
- Daftar enam preset.
- Pengambilan Grid preset.
- Pembuatan Grid kustom.
- Validasi Grid.
- Validasi Start dan Goal.
- Pencarian tetangga.
- Manhattan Distance.
- Informasi dasar Grid.
"""

import unittest

from maze import (
    list_presets,
    get_preset,
    create_custom_grid,
    validate_grid,
    get_neighbors,
    manhattan_distance,
    get_grid_info,
)


class TestMaze(unittest.TestCase):
    """Pengujian fungsional untuk modul maze.py."""

    # ========================================================
    # 1. PENGUJIAN GRID PRESET
    # ========================================================

    def test_list_presets_returns_six_presets(self):
        """Memastikan terdapat enam Grid preset."""

        presets = list_presets()

        self.assertEqual(len(presets), 6)

        expected_names = [
            "Grid Terbuka",
            "Grid Satu Penghalang",
            "Grid Koridor Sempit",
            "Grid Banyak Penghalang",
            "Grid Tanpa Jalur",
            "Grid Persegi Panjang",
        ]

        actual_names = [
            name for _, name in presets
        ]

        self.assertEqual(actual_names, expected_names)

    def test_all_presets_are_valid_and_deterministic(self):
        """Memastikan semua preset valid dan konsisten."""

        for preset_number, _ in list_presets():

            with self.subTest(preset=preset_number):

                first = get_preset(preset_number)
                second = get_preset(preset_number)

                # Hasil preset harus konsisten.
                self.assertEqual(first, second)

                grid, start, goal, _ = first

                # Memastikan Grid, Start, dan Goal valid.
                validate_grid(grid, start, goal)

                # Start dan Goal harus dapat dilalui.
                self.assertEqual(grid[start[0]][start[1]], 0)
                self.assertEqual(grid[goal[0]][goal[1]], 0)

    def test_get_preset_invalid_number(self):
        """Memastikan nomor preset yang tidak tersedia ditolak."""

        for preset_number in (0, 7, -1):

            with self.subTest(preset=preset_number):

                with self.assertRaises(ValueError):
                    get_preset(preset_number)

    # ========================================================
    # 2. PENGUJIAN GRID KUSTOM
    # ========================================================

    def test_create_custom_grid_success(self):
        """Memastikan Grid kustom dapat dibuat."""

        grid = create_custom_grid(
            rows=2,
            cols=3,
            row_inputs=[
                "001",
                "010",
            ],
        )

        expected_grid = [
            [0, 0, 1],
            [0, 1, 0],
        ]

        self.assertEqual(grid, expected_grid)

    def test_custom_grid_invalid_row_count(self):
        """Memastikan jumlah baris harus sesuai."""

        with self.assertRaises(ValueError):
            create_custom_grid(
                rows=3,
                cols=3,
                row_inputs=[
                    "000",
                    "000",
                ],
            )

    def test_custom_grid_invalid_dimensions(self):
        """Memastikan ukuran Grid harus positif."""

        with self.assertRaises(ValueError):
            create_custom_grid(
                rows=0,
                cols=3,
                row_inputs=[],
            )

        with self.assertRaises(ValueError):
            create_custom_grid(
                rows=2,
                cols=0,
                row_inputs=["", ""],
            )

    def test_custom_grid_invalid_row_length(self):
        """Memastikan jumlah karakter setiap baris sesuai."""

        with self.assertRaises(ValueError):
            create_custom_grid(
                rows=2,
                cols=3,
                row_inputs=[
                    "00",
                    "000",
                ],
            )

    def test_custom_grid_invalid_characters(self):
        """Memastikan hanya karakter 0 dan 1 yang diterima."""

        with self.assertRaises(ValueError):
            create_custom_grid(
                rows=2,
                cols=3,
                row_inputs=[
                    "0A0",
                    "000",
                ],
            )

    # ========================================================
    # 3. PENGUJIAN VALIDASI GRID
    # ========================================================

    def test_validate_empty_grid(self):
        """Memastikan Grid kosong ditolak."""

        with self.assertRaises(ValueError):
            validate_grid(
                [],
                (0, 0),
                (0, 0),
            )

    def test_validate_inconsistent_rows(self):
        """Memastikan jumlah kolom setiap baris harus sama."""

        grid = [
            [0, 0],
            [0],
        ]

        with self.assertRaises(ValueError):
            validate_grid(
                grid,
                (0, 0),
                (1, 0),
            )

    def test_validate_invalid_cell_value(self):
        """Memastikan nilai sel hanya boleh 0 atau 1."""

        grid = [
            [0, 2],
            [0, 0],
        ]

        with self.assertRaises(ValueError):
            validate_grid(
                grid,
                (0, 0),
                (1, 1),
            )

    def test_validate_start_out_of_bounds(self):
        """Memastikan Start tidak boleh di luar Grid."""

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

    def test_validate_goal_out_of_bounds(self):
        """Memastikan Goal tidak boleh di luar Grid."""

        grid = [
            [0, 0],
            [0, 0],
        ]

        with self.assertRaises(ValueError):
            validate_grid(
                grid,
                (0, 0),
                (0, 2),
            )

    def test_validate_start_on_wall(self):
        """Memastikan Start tidak boleh berada di dinding."""

        grid = [
            [1, 0],
            [0, 0],
        ]

        with self.assertRaises(ValueError):
            validate_grid(
                grid,
                (0, 0),
                (1, 1),
            )

    def test_validate_invalid_coordinate_format(self):
        """Memastikan koordinat harus berupa dua bilangan bulat."""

        grid = [
            [0, 0],
            [0, 0],
        ]

        with self.assertRaises(ValueError):
            validate_grid(
                grid,
                (0,),
                (1, 1),
            )

        with self.assertRaises(ValueError):
            validate_grid(
                grid,
                (0, 1.5),
                (1, 1),
            )

    def test_start_can_equal_goal(self):
        """Memastikan Start boleh sama dengan Goal."""

        grid = [
            [0, 0],
            [0, 0],
        ]

        # Tidak boleh menghasilkan ValueError.
        validate_grid(
            grid,
            (0, 0),
            (0, 0),
        )

    # ========================================================
    # 4. PENGUJIAN TETANGGA
    # ========================================================

    def test_get_neighbors_direction_order(self):
        """Memastikan urutan tetangga atas, kanan, bawah, kiri."""

        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        neighbors = get_neighbors(
            grid,
            (1, 1),
        )

        expected_neighbors = [
            (0, 1),  # Atas
            (1, 2),  # Kanan
            (2, 1),  # Bawah
            (1, 0),  # Kiri
        ]

        self.assertEqual(
            neighbors,
            expected_neighbors,
        )

    def test_get_neighbors_respects_walls_and_bounds(self):
        """Memastikan tetangga dinding dan luar Grid tidak dipilih."""

        grid = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0],
        ]

        neighbors = get_neighbors(
            grid,
            (1, 1),
        )

        self.assertEqual(
            neighbors,
            [
                (1, 2),
                (2, 1),
            ],
        )

    def test_get_neighbors_does_not_move_diagonally(self):
        """Memastikan gerakan diagonal tidak diperbolehkan."""

        grid = [
            [0, 1],
            [1, 0],
        ]

        neighbors = get_neighbors(
            grid,
            (0, 0),
        )

        self.assertEqual(neighbors, [])

    # ========================================================
    # 5. PENGUJIAN MANHATTAN DISTANCE
    # ========================================================

    def test_manhattan_distance(self):
        """Memastikan perhitungan Manhattan Distance benar."""

        distance = manhattan_distance(
            (1, 2),
            (4, 5),
        )

        self.assertEqual(distance, 6)

    def test_manhattan_distance_same_position(self):
        """Jarak posisi terhadap dirinya sendiri harus nol."""

        distance = manhattan_distance(
            (2, 2),
            (2, 2),
        )

        self.assertEqual(distance, 0)

    # ========================================================
    # 6. PENGUJIAN INFORMASI GRID
    # ========================================================

    def test_get_grid_info(self):
        """Memastikan informasi Grid dihitung dengan benar."""

        grid = [
            [0, 0, 1],
            [0, 1, 0],
        ]

        info = get_grid_info(
            grid,
            (0, 0),
            (1, 2),
        )

        expected_info = {
            "rows": 2,
            "cols": 3,
            "n": 6,
            "passable_cells": 4,
            "wall_cells": 2,
            "start_row": 0,
            "start_col": 0,
            "goal_row": 1,
            "goal_col": 2,
        }

        self.assertEqual(info, expected_info)


if __name__ == "__main__":
    unittest.main()
