from __future__ import annotations
from typing import List, Callable
from dataclasses import dataclass
from enum import Enum


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


@dataclass
class Cell:
    __slots__ = ["x", "y", "mine", "neighbors"]
    x: int
    y: int
    mine: bool
    neighbors: List[Cell]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mine = False
        self.neighbors = []

    def reset(self):
        self.mine = False


class Board:
    grid: List[List[Cell]]
    width: int
    height: int

    # The board is intended to be reused, no constructor required
    def __init__(self):
        self.grid = None
        self.width = None
        self.height = None

    def configure(self, width: int, height: int, mines: int):
        self.width = width
        self.height = height
        self.mines = mines

        # Reset the grid data if needed
        reconfigure = (
            self.grid is None or len(self.grid) != height or len(self.grid[0]) != width
        )

        if reconfigure:
            self.grid = [[Cell(i, j) for i in range(width)] for j in range(height)]

            # Link neighbouring cells
            self.link_neighbors()

        # Reset all cells
        self.reset_cells()

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
