from board import Board, BoardState, BoardResult, BoardSolver, BoardGenerationSettings
from typing import List

import timeit
import functools
import sys
import os
import random


def main():
    global devnull
    devnull = open(os.devnull, "w")

    # For benchmarking and timing specific methods of the solving procedure
    # benchmark_methods()

    # For debugging a specific solver with fixed seed
    # debug(BoardSolver.ScipySparseLinalgLsqr)
    # exit()

    # For benchmarking specific board setups
    # run_benchmark(
    #    benchmark_custom(26, 13, 84),
    #    1000,
    #    solver=BoardSolver.ScipyLinalgLstsq,
    #    seeds=None,
    # )

    # Note: 10k expert boards reserves roughly 1GB of memory
    # if garbage collect is not enabled
    run_benchmark(benchmark_expert, 1000, enable_gc=True)
    print()
    print()
    benchmark_all_solvers(repeats=100, shared_seeds=True, random_seed=123)


def benchmark_all_solvers(repeats=1000, shared_seeds=False, random_seed=None):
    """
        Runs basic benchmark on all basic board setups and solvers
    """
    random.seed(random_seed)
    seeds = None
    if shared_seeds:
        seeds = [random.randrange(sys.maxsize) for i in range(repeats)]

    board_setups = [benchmark_easy, benchmark_medium, benchmark_expert]
    board_solvers = [enum for enum in BoardSolver]

    for setup in board_setups:
        for solver in board_solvers:
            run_benchmark(setup, repeats, solver, seeds)


def run_benchmark(
    board_setup,
    repeats,
    solver=BoardSolver.ScipyLinalgLstsq,
    seeds=None,
    enable_gc=False,
):
    """
        Main benchmark for a board setup with configurable repeats, solver and seeds
    """

    print("Running", board_setup.__name__)
    print("Repeats", repeats)
    print("Solver", solver)
    print("-" * 25)

    board_results = []

    # TODO: functools causes some delays

    # Disable stdout prints (scipy)
    toggle_output(False)

    copy_seeds = seeds[:] if seeds is not None else None

    t = timeit.Timer(
        functools.partial(board_setup, board_results, True, solver, copy_seeds),
        "gc.enable()" if enable_gc else "",
    )
    timeit_result = t.timeit(number=repeats)

    # Enable stdout prints again
    toggle_output(True)

    display_results(repeats, board_results, timeit_result)

    print("-" * 50)


def display_results(repeats, board_results: List[BoardResult], timeit_result):
    win_rate = sum(
        map(lambda board: board.state == BoardState.Won, board_results)
    ) / float(len(board_results))

    ex_board = board_results[0]
    print("Board", ex_board.width, ex_board.height, ex_board.mines)
    print("Repeats", repeats)
    print("Total runtime", timeit_result, "seconds")
    print("Average per board", 1000 * timeit_result / len(board_results), "ms")
    print("Win rate", win_rate)


def benchmark_custom(width, height, mines):
    def benchmark_board(
        board_results,
        force_start_area=True,
        solver=BoardSolver.ScipyLinalgLstsq,
        seeds=None,
    ):
        current_seed = get_next_seed(seeds)

        board = Board()
        board.configure_and_solve(
            width,
            height,
            BoardGenerationSettings(mines, current_seed, None, force_start_area),
            solver,
        )
        board_results.append(board.get_result())

    return benchmark_board


def benchmark_easy(
    board_results,
    force_start_area=True,
    solver=BoardSolver.ScipyLinalgLstsq,
    seeds=None,
):
    benchmark_custom(9, 9, 10)(board_results, force_start_area, solver, seeds)


def benchmark_medium(
    board_results,
    force_start_area=True,
    solver=BoardSolver.ScipyLinalgLstsq,
    seeds=None,
):
    benchmark_custom(16, 16, 40)(board_results, force_start_area, solver, seeds)


def benchmark_expert(
    board_results,
    force_start_area=True,
    solver=BoardSolver.ScipyLinalgLstsq,
    seeds=None,
):
    benchmark_custom(30, 16, 99)(board_results, force_start_area, solver, seeds)


def get_next_seed(seeds):
    if seeds is not None and len(seeds) > 0:
        return seeds.pop(0)
    return None


def toggle_output(on):
    global devnull
    sys.stdout = sys.__stdout__ if on else devnull


def debug(solver=BoardSolver.ScipyLinalgLstsq):
    board = Board()
    seed = 3283476030983952662
    position = board.configure(
        30, 16, BoardGenerationSettings(99, seed, None, True), solver, True
    )

    print(board.width, board.height, board.generated_mines)

    board.solve(position)

    print(board.str_revealed(True))
    print()
    print(board.str_real())


def benchmark_methods():
    print(
        "benchmark_board_link_neighbors",
        timeit.timeit(
            stmt="benchmark_board_link_neighbors(board)",
            setup="""\
from __main__ import setup_expert_board, benchmark_board_link_neighbors
board = setup_expert_board()
                """,
            number=1000,
        ),
    )

    print(
        "benchmark_board_reset_cells",
        timeit.timeit(
            stmt="benchmark_board_reset_cells(board)",
            setup="""\
from __main__ import setup_expert_board, benchmark_board_reset_cells
board = setup_expert_board()
                """,
            number=1000,
        ),
    )


def setup_expert_board():
    board = Board()
    board.configure(30, 16, BoardGenerationSettings(99, None, None, True))
    return board


def benchmark_board_link_neighbors(board: Board):
    # Manually unlink neighbors
    for row in board.grid:
        for cell in row:
            cell.neighbors.clear()

    board.link_neighbors()


def benchmark_board_reset_cells(board: Board):
    board.reset_cells()


if __name__ == "__main__":
    main()
