from __future__ import annotations
from typing import List, Callable, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import random


class BoardState(Enum):
    Undefined = 0
    Won = 1
    Lost = 2


class CellState(Enum):
    Closed = 0
    Opened = 1
    Flagged = 2


class CellDiscoveryState(Enum):
    """
        Defines the discovery status of a cell.  
        Undefined: no additional information is known about the cell  
        Reached: opened neighboring cells offer information about the cell  
        Cleared: the state of the cell has been solved
    """

    Undefined = 0
    Reached = 1
    Cleared = 2


class BoardGenerationSettings:
    mines: int
    seed: Optional[int]
    start_position: Optional[Tuple[int, int]]
    force_start_area: Optional[bool]

    def __init__(self, mines, seed=None, start_position=None, force_start_area=None):
        self.mines = mines
        self.seed = seed
        self.start_position = start_position
        self.force_start_area = force_start_area


@dataclass
class Cell:
    __slots__ = [
        "x",
        "y",
        "mine",
        "neighbor_mine_count",
        "neighbor_flag_count",
        "neighbor_opened_count",
        "neighbor_count",
        "neighbors",
        "state",
        "discovery_state",
        "satisfied",
    ]
    x: int
    y: int
    mine: bool
    neighbor_mine_count: int
    neighbor_flag_count: int
    neighbor_opened_count: int
    neighbor_count: int
    neighbors: List[Cell]
    state: CellState
    discovery_state: CellDiscoveryState
    satisfied: bool

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.reset()

    def reset(self):
        self.mine = False
        self.neighbor_mine_count = 0
        self.neighbor_flag_count = 0
        self.neighbor_opened_count = 0
        self.neighbor_count = 0
        self.state = CellState.Closed
        self.discovery_state = CellDiscoveryState.Undefined
        self.satisfied = False

    def update_satisfied(self):
        """
            Updates the cell as satisfied if the conditions for it are met
        """
        if self.satisfied:
            return

        if (
            self.neighbor_mine_count == self.neighbor_flag_count
            or self.neighbor_mine_count
            == self.neighbor_count - self.neighbor_opened_count
        ):
            self.satisfied = True

    def str_real(self):
        return (
            "█"
            if self.mine
            else (
                " " if self.neighbor_mine_count == 0 else str(self.neighbor_mine_count)
            )
        )

    def str_revealed(self):
        if self.satisfied:
            return " "
        if self.state == CellState.Closed:
            return "█"
        elif self.state == CellState.Opened:
            return (
                " " if self.neighbor_mine_count == 0 else str(self.neighbor_mine_count)
            )
        elif self.state == CellState.Flagged:
            return "■"


class Board:
    grid: List[List[Cell]]
    width: int
    height: int
    state: BoardState
    opened_cells: int
    generated_mines: int

    # The board is intended to be reused, no constructor required
    def __init__(self):
        self.grid = None

        self.width = 0
        self.height = 0
        self.reset()

    def reset(self):
        self.state = BoardState.Undefined
        self.opened_cells = 0
        self.generated_mines = 0

    def configure_and_solve(
        self, width: int, height: int, settings: BoardGenerationSettings
    ):
        start_position = self.configure(width, height, settings)
        self.solve(start_position)

    def configure(self, width: int, height: int, settings: BoardGenerationSettings):
        """
            Configures the board with the given settings and generates mines.  
            Returns the starting position as a Tuple[int, int]
        """
        self.width = width
        self.height = height
        self.reset()

        reconfigure = (
            self.grid is None or len(self.grid) != height or len(self.grid[0]) != width
        )

        # Reset the grid data if needed
        if reconfigure:
            self.grid = [[Cell(i, j) for i in range(width)] for j in range(height)]
            self.link_neighbors()

        self.reset_cells()
        start_position = self.generate_mines(settings)
        return start_position

    def solve(self, start_position):
        """
            Solves the board from its current state using the given start position that will be opened.
        """
        print(self.width, self.height, self.generated_mines)
        non_mine_cell_count = self.width * self.height - self.generated_mines

        # Open the start position
        self.open_at(start_position[0], start_position[1])

        # Main loop
        # Keep track of active cells and perform first-order solving

        while self.state == BoardState.Undefined:
            if self.opened_cells == non_mine_cell_count:
                self.state = BoardState.Won
                break


    def flag_at(self, x, y):
        cell = self.grid[y][x]
        self.flag_cell(cell)

    def flag_cell(self, cell):
        if cell.state != CellState.Closed:
            return

        cell.state = CellState.Flagged
        for neighbor in cell.neighbors:
            neighbor.neighbor_flag_count += 1

    def open_at(self, x, y):
        cell = self.grid[y][x]
        self.open_cell(cell)

    def open_cell(self, cell):
        if cell.state != CellState.Closed:
            return

        cell.state = CellState.Opened
        self.opened_cells += 1

        cell_flag_satisfied = cell.neighbor_mine_count == cell.neighbor_flag_count
        cell_flag_remaining = (
            cell.neighbor_mine_count == cell.neighbor_count - cell.neighbor_opened_count
        )

        # Inform neighbors that the cell has been opened
        # Also perform quick-opens and flags for neighbors
        # since we are already looping through them here
        for neighbor in cell.neighbors:
            neighbor.neighbor_opened_count += 1

            # Opening a cell that is fully satisfied opens neighbors
            if cell_flag_satisfied and neighbor.state == CellState.Closed:
                self.open_cell(neighbor)

            # Opening a cell that only has N mines around it and only
            # N unopened cells remaining flags them all
            if cell_flag_remaining and neighbor.state == CellState.Closed:
                self.flag_cell(neighbor)

        cell.update_satisfied()

    def link_neighbors(self) -> None:
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if y > 0:
                    cell.neighbors.append(self.grid[y - 1][x])
                    if x > 0:
                        cell.neighbors.append(self.grid[y - 1][x - 1])
                    if x < self.width - 1:
                        cell.neighbors.append(self.grid[y - 1][x + 1])
                if x > 0:
                    cell.neighbors.append(self.grid[y][x - 1])
                if x < self.width - 1:
                    cell.neighbors.append(self.grid[y][x + 1])
                if y < self.height - 1:
                    cell.neighbors.append(self.grid[y + 1][x])
                    if x > 0:
                        cell.neighbors.append(self.grid[y + 1][x - 1])
                    if x < self.width - 1:
                        cell.neighbors.append(self.grid[y + 1][x + 1])

    def reset_cells(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.reset()

    def generate_mines(self, settings: BoardGenerationSettings) -> None:
        # Seeds the RNG. If None, uses current time
        random.seed(settings.seed)

        if settings.start_position is not None:
            start_position = settings.start_position
        else:
            start_position = (
                random.randrange(0, self.width),
                random.randrange(0, self.height),
            )

        # Generate a list of all random positions
        valid_positions: List[Tuple[int, int]] = []
        for j in range(self.height):
            for i in range(self.width):
                # Do not generate a mine on the start position
                if i == start_position[0] and j == start_position[1]:
                    continue

                # Do not generate mines neighboring the start position
                # if the force_start_area setting is enabled
                if settings.force_start_area:
                    if (
                        i >= start_position[0] - 1
                        and i <= start_position[0] + 1
                        and j >= start_position[1] - 1
                        and j <= start_position[1] + 1
                    ):
                        continue

                valid_positions.append((i, j))

        mine_count = min(settings.mines, len(valid_positions))

        mine_positions = random.sample(valid_positions, mine_count)

        for position in mine_positions:
            x, y = position
            self.grid[y][x].mine = True
            self.generated_mines += 1
            for neighbor in self.grid[y][x].neighbors:
                neighbor.neighbor_mine_count += 1

        return start_position

    def str_real(self):
        return "\n".join(
            ["".join([cell.str_real() for cell in row]) for row in self.grid]
        )

    def str_revealed(self):
        return "\n".join(
            ["".join([cell.str_revealed() for cell in row]) for row in self.grid]
        )
