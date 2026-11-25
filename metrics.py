
"""
metrics.py

Modul untuk mengukur kinerja algoritma A* dan GBFS.

Pengukuran waktu:
- 1 kali pemanasan.
- 10 kali pengulangan.
- Menggunakan time.perf_counter_ns().
- Menghitung rata-rata dan median.

Pengukuran memori:
- Dilakukan secara terpisah dari waktu.
- 10 kali pengulangan.
- Menggunakan tracemalloc.
- Menghitung median peak traced memory.
"""

import statistics
import time
import tracemalloc

from collections.abc import Callable

from maze import Coordinate, Grid


# ============================================================
# 1. KONSTANTA PENGUKURAN
# ============================================================

TIME_RUNS = 10
MEMORY_RUNS = 10

WARMUP_RUNS = 1

BYTES_TO_KB = 1024


# ============================================================
# 2. PENGUKURAN WAKTU
# ============================================================

def measure_execution_time(
    search_function: Callable,
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
) -> dict:
    """
    Mengukur waktu eksekusi fungsi algoritma.

    Proses:
    1. Satu kali pemanasan.
    2. Sepuluh kali pengukuran.
    3. Menghitung rata-rata dan median.

    Timer hanya membungkus pemanggilan fungsi algoritma inti.

    Mengembalikan:
    - result
    - time_runs
    - time_mean_ms
    - time_median_ms
    """

    # --------------------------------------------------------
    # A. Pemanasan
    # --------------------------------------------------------

    for _ in range(WARMUP_RUNS):
        search_function(grid, start, goal)

    # --------------------------------------------------------
    # B. Pengukuran waktu
    # --------------------------------------------------------

    execution_times = []

    last_result = None

    for _ in range(TIME_RUNS):

        # Mulai pengukuran tepat sebelum fungsi algoritma.
        start_time = time.perf_counter_ns()

        result = search_function(
            grid,
            start,
            goal,
        )

        # Hentikan pengukuran tepat setelah fungsi selesai.
        end_time = time.perf_counter_ns()

        elapsed_time = end_time - start_time

        execution_times.append(elapsed_time)

        last_result = result

    # --------------------------------------------------------
    # C. Perhitungan statistik waktu
    # --------------------------------------------------------

    mean_time_ns = statistics.mean(execution_times)

    median_time_ns = statistics.median(execution_times)

    # Konversi nanodetik menjadi milidetik.
    mean_time_ms = mean_time_ns / 1_000_000

    median_time_ms = median_time_ns / 1_000_000

    return {
        "result": last_result,
        "time_runs": TIME_RUNS,
        "time_mean_ms": mean_time_ms,
        "time_median_ms": median_time_ms,
    }


# ============================================================
# 3. PENGUKURAN MEMORI
# ============================================================

def measure_peak_memory(
    search_function: Callable,
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
) -> dict:
    """
    Mengukur peak traced memory fungsi algoritma.

    Proses:
    1. Sepuluh kali pengukuran memori.
    2. Memulai tracemalloc sebelum fungsi algoritma.
    3. Mengambil peak memory setelah fungsi selesai.
    4. Menghentikan tracemalloc menggunakan finally.
    5. Menghitung median peak memory dalam KB.

    Pengukuran ini tidak mengukur seluruh RAM proses,
    melainkan alokasi memori Python yang dilacak.
    """

    # Hindari menghentikan tracing milik pemanggil.
    if tracemalloc.is_tracing():
        raise RuntimeError(
            "tracemalloc sedang aktif. "
            "Hentikan tracing sebelumnya sebelum "
            "menjalankan pengukuran memori."
        )

    # Menyimpan peak memory setiap pengulangan.
    peak_memory_values = []

    for _ in range(MEMORY_RUNS):

        # Mulai pelacakan memori.
        tracemalloc.start()

        try:

            # Panggil hanya fungsi inti algoritma.
            search_function(
                grid,
                start,
                goal,
            )

            # Ambil peak memory setelah fungsi selesai.
            _, peak_memory = tracemalloc.get_traced_memory()

            peak_memory_values.append(peak_memory)

        finally:

            # Pastikan tracing selalu dihentikan.
            tracemalloc.stop()

    # --------------------------------------------------------
    # Perhitungan median peak memory
    # --------------------------------------------------------

    median_peak_bytes = statistics.median(
        peak_memory_values
    )

    median_peak_kb = median_peak_bytes / BYTES_TO_KB

    return {
        "memory_runs": MEMORY_RUNS,
        "memory_median_kb": median_peak_kb,
    }


# ============================================================
# 4. PENGUKURAN LENGKAP SATU ALGORITMA
# ============================================================

def measure_algorithm(
    search_function: Callable,
    grid: Grid,
    start: Coordinate,
    goal: Coordinate,
) -> dict:
    """
    Mengukur waktu dan memori satu algoritma.

    Pengukuran waktu dan memori dilakukan terpisah.

    Mengembalikan:
    - result
    - time_runs
    - time_mean_ms
    - time_median_ms
    - memory_runs
    - memory_median_kb
    """

    # --------------------------------------------------------
    # A. Ukur waktu
    # --------------------------------------------------------

    time_results = measure_execution_time(
        search_function,
        grid,
        start,
        goal,
    )

    # --------------------------------------------------------
    # B. Ukur memori secara terpisah
    # --------------------------------------------------------

    memory_results = measure_peak_memory(
        search_function,
        grid,
        start,
        goal,
    )

    # --------------------------------------------------------
    # C. Gabungkan hasil pengukuran
    # --------------------------------------------------------

    return {
        "result": time_results["result"],
        "time_runs": time_results["time_runs"],
        "time_mean_ms": time_results["time_mean_ms"],
        "time_median_ms": time_results["time_median_ms"],
        "memory_runs": memory_results["memory_runs"],
        "memory_median_kb": memory_results["memory_median_kb"],
    }
