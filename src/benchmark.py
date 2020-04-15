from board import Board, BoardGenerationSettings

import timeit


def main():
    # benchmark()

    board = Board()
    position = board.configure(
        30, 16, BoardGenerationSettings(99, 7206524071910848918, None, True)
    )

    print(board.width, board.height, board.generated_mines)

    board.solve(position)

    print(board.str_revealed())
    print()
    print(board.str_real())


def benchmark():
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
    board.configure(30, 16, BoardGenerationSettings(99))
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
