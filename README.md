# minesweeper-solver-python

## Introduction

Python solver for Minesweeper. Uses naive (first-order) solving techniques and numerical methods for second-order solving of `Ax = b` linear system of equations. The solvers (should) output a probability of remaining cells being mines hence guessing is also informed and not purely a uniform random choice.

The code contains support for a few different solvers, most importantly:

| BoardSolver | Avg run time per board (Expert) | Avg win rate (Expert) |
|---|---|---|
| ScipyLinalgLstsq | 14.1ms | 31.4% |
| ScipyOptimizeLsqLinear | 200ms | 45.0% |

See [History](#history) for more about other languages, solvers, run times etc.


One way to improve the solving further is to consider expected value of each random guess. Some cells might, if non-mine, provide more valuable information than other cells that might have lower chance of being a mine. This could be potentiall solved by preprocessing a machine learning solver to identify these, or using some forms of Monte-Carlo estimation.

## Statistics

TODO

## Usage

Requirements:
* Python 3.x

Use a virtualenv or install dependencies using `pip`:
```
    pip install -r src/requirements.txt
```

Run the benchmark suite
```
    python src/benchmark.py
```

## History

This is the 4th iteration of a minesweeper solver I've developed.

| Year | Environment | Avg run time per board (Expert) | Avg win rate (Expert) | `Ax = b` solver |
|---|---|---|---|---|
| 2010 | C++ | 1500ms | ~10% | `matrix.h` by Rondall Jones |
| 2015 | Python | 40ms | 27% | `numpy.linalg.lstsq` |
| 2017 | C++ | - | - | Various (Eigen, Armadillo) |
| 2020 | Python | 14.1ms | 31.4% | Various (`scipy`) |

TODO

## License
See LICENSE