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
        "neighbors",
        "state",
        "discovery_state",
    ]
    x: int
    y: int
    mine: bool
    neighbor_mine_count: int
    neighbors: List[Cell]
    state: CellState
    discovery_state: CellDiscoveryState

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.reset()

    def reset(self):
        self.mine = False
        self.neighbor_mine_count = 0
        self.state = CellState.Closed
        self.discovery_state = CellDiscoveryState.Undefined


class Board:
    grid: List[List[Cell]]
    width: int
    height: int
    state: BoardState

    # The board is intended to be reused, no constructor required
    def __init__(self):
        self.grid = None

        self.width = None
        self.height = None
        self.state = BoardState.Undefined

    def configure(self, width: int, height: int, settings: BoardGenerationSettings):
        """
            Configures the board with the given settings and generates mines.  
            Returns the starting position as a Tuple[int, int]
        """
        self.width = width
        self.height = height
        self.state = BoardState.Undefined

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
            for neighbor in self.grid[y][x].neighbors:
                neighbor.neighbor_mine_count += 1

        return start_position
