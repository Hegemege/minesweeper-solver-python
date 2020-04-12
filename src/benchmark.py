from board import Board

import timeit


def main():
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
    board.configure(16, 30, 99)
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
