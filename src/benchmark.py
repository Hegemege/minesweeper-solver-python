from board import Board, BoardState, BoardResult, BoardSolver, BoardGenerationSettings
from typing import List

import timeit
import functools
import sys
import os


def main():
    # benchmark_methods()

    # debug(BoardSolver.ScipySparseLinalgLsqr)
    # exit()

    benchmark_board(benchmark_easy, 1000, BoardSolver.ScipyLinalgLstsq)
    # benchmark_board(benchmark_easy, 1000, BoardSolver.ScipyOptimizeLsqLinear)
    # benchmark_board(benchmark_easy, 1000, BoardSolver.ScipySparseLinalgLsqr)
    benchmark_board(benchmark_easy, 1000, BoardSolver.ScipySparseLinalgLsmr)

    benchmark_board(benchmark_medium, 1000, BoardSolver.ScipyLinalgLstsq)
    # benchmark_board(benchmark_medium, 1000, BoardSolver.ScipyOptimizeLsqLinear)
    # benchmark_board(benchmark_medium, 1000, BoardSolver.ScipySparseLinalgLsqr)
    benchmark_board(benchmark_medium, 1000, BoardSolver.ScipySparseLinalgLsmr)

    benchmark_board(benchmark_expert, 1000, BoardSolver.ScipyLinalgLstsq)
    # benchmark_board(benchmark_expert, 1000, BoardSolver.ScipyOptimizeLsqLinear)
    # benchmark_board(benchmark_expert, 1000, BoardSolver.ScipySparseLinalgLsqr)
    benchmark_board(benchmark_expert, 1000, BoardSolver.ScipySparseLinalgLsmr)


def benchmark_board(board_benchmark, repeats, solver=BoardSolver.ScipyLinalgLstsq):
    print("Running", board_benchmark.__name__)
    print("Repeats", repeats)
    print("Solver", solver)
    print("-" * 25)

    board_results = []

    # TODO: functools causes some delays

    # Disable stdout prints (scipy)
    sys.stdout = open(os.devnull, "w")

    t = timeit.Timer(functools.partial(board_benchmark, board_results, True, solver))
    timeit_result = t.timeit(number=repeats)

    # Enable stdout prints again
    sys.stdout = sys.__stdout__

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


def benchmark_easy(
    board_results, force_start_area=True, solver=BoardSolver.ScipyLinalgLstsq
):
    board = Board()
    board.configure_and_solve(
        9, 9, BoardGenerationSettings(10, None, None, force_start_area), solver
    )
    board_results.append(board.get_result())


def benchmark_medium(
    board_results, force_start_area=True, solver=BoardSolver.ScipyLinalgLstsq
):
    board = Board()
    board.configure_and_solve(
        16, 16, BoardGenerationSettings(40, None, None, force_start_area), solver
    )
    board_results.append(board.get_result())


def benchmark_expert(
    board_results, force_start_area=True, solver=BoardSolver.ScipyLinalgLstsq
):
    board = Board()
    board.configure_and_solve(
        30, 16, BoardGenerationSettings(99, None, None, force_start_area), solver
    )
    board_results.append(board.get_result())


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
            setup="from __main__ import setup_expert_board,benchmark_board_link_neighbors; board = setup_expert_board()",
            number=1000,
        ),
    )

    print(
        "benchmark_board_reset_cells",
        timeit.timeit(
            stmt="benchmark_board_reset_cells(board)",
            setup="from __main__ import setup_expert_board,benchmark_board_reset_cells; board = setup_expert_board()",
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
