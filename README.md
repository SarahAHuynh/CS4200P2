
# CS4200 P2 - N-Queens

This project compares two local search algorithms for N-Queens:

- Straightforward steepest-ascent hill climbing (no sideways moves or restarts within a trial)
- Min-Conflicts (up to 1,000 iterations per attempt, with up to 10 random restarts)

A board is represented by `board[column] = row`. The conflict heuristic counts unique pairs of queens that attack each other along a row or diagonal; zero conflicts means a valid solution.

## Files

- `program.py` - interactive entry point, like Project 1; saves numbered transcripts.
- `hill_climbing.py` - steepest-ascent hill-climbing solver and helper functions.
- `min_conflicts.py` - Min-Conflicts solver.
- `experiments.py` - 200-case analysis for each N and algorithm.
- `experiment_summary.csv` - six-case summary from the included experiment run.
- `experiment_details.csv` - all 1,200 individual trial records.
- `program_output(1).txt` - sample interactive program transcript.
- `sample_solutions.txt` - three solved configurations for N=8, 12, and 16.
- `CS4200P2 - Report.pdf` - two-page report describing the approach, results, and findings.

## Requirements

Python 3.9 or later. Uses only the standard library; no package installation is needed.

## How to run the program

From the folder containing the Python files:

```bash
python3 program.py
```

On Windows, you can also run `python program.py` or `py program.py`.

The main menu provides these choices:

1. Generate a random N-Queens board (N=8, 12, or 16)
2. Enter a board manually, with N space-separated row positions
3. Run the 200-case analysis for each of N=8, 12, and 16 using both algorithms
4. Exit

For options 1 and 2, choose `1` for hill climbing or `2` for Min-Conflicts. The program displays initial and final conflicts, steps, execution time, solution status, and the final board. A failed hill-climbing attempt is expected when it stops at a local minimum.

Example manual 8-Queens board: `5 2 6 3 0 7 1 4` (already solved).

## Run either solver directly

```bash
python3 hill_climbing.py
python3 min_conflicts.py
```

## Run the analysis directly

```bash
python3 experiments.py
```

For each N, the experiments use 200 random initial boards and reuse the same boards for both algorithms, for a total of 1,200 trials. The random seed is 42. Results are printed and saved to `experiment_summary.csv` and `experiment_details.csv` in the current working directory, overwriting existing CSV data.

`steps` means *actual queen moves*, not examined neighbors; unsuccessful trials are included in overall averages. Time is the measured search time per trial in milliseconds. Because timing depends on the computer and system load, your new measurements may not match the packaged CSV exactly. Min-Conflicts permits restarts, whereas the steepest-ascent implementation does not.

## Transcript output

Every interactive session automatically creates the next available `program_output(#).txt` file. It records menu options, typed inputs, final configurations, statistics, and the exit message. To show three verified solved configurations without relying on chance, see `sample_solutions.txt`.
