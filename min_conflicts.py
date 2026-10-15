
import random
import time

from hill_climbing import generate_board, count_conflicts, print_board


def min_conflicts(initial_board, max_steps=1000, max_restarts=10, rng=None):
    # solve N-Queens using the Min-Conflicts algorithm
    # randomly select a queen thats in a conflict and move it to row that minimizes its conflicts

    # if the step limit is reached, generate new random board and try again

    # returns: final_board, steps, solved

    if rng is None:
        rng = random.Random()

    n = len(initial_board)

    if n < 4:
        raise ValueError("N must be at least 4.")

    steps = 0
    final_board = initial_board.copy()

    # first attempt uses the given board
    # later attempts generate new random boards
    for attempt in range(max_restarts + 1):

        if attempt == 0:
            board = initial_board.copy()
        else:
            board = generate_board(n, rng)

        # track number of queens in each row and diagonal
        row_counts = [0] * n
        descending = [0] * (2 * n - 1)
        ascending = [0] * (2 * n - 1)

        for col, row in enumerate(board):
            row_counts[row] += 1
            descending[row - col + n - 1] += 1
            ascending[row + col] += 1

        #attempt to solve the current board
        for iteration in range(max_steps + 1):

            conflicted_queens = []

            # find all queens that are attacking another queen
            for col, row in enumerate(board):
                conflicts = (
                    row_counts[row] - 1
                    + descending[row - col + n - 1] - 1
                    + ascending[row + col] - 1
                )

                if conflicts > 0:
                    conflicted_queens.append(col)

            # no conflicted queens means the puzzle is solved
            if not conflicted_queens:
                return board, steps, True

            # stop this attempt once the step limit is reached
            if iteration == max_steps:
                break

            # randomly choose one queen involved in a conflict
            col = rng.choice(conflicted_queens)
            old_row = board[col]

            best_conflicts = float("inf")
            best_rows = []

            # evaluate every possible row for the chosen queen
            for row in range(n):

                conflicts = (
                    row_counts[row]
                    + descending[row - col + n - 1]
                    + ascending[row + col]
                )

                # do not count the queen attacking itself
                if row == old_row:
                    conflicts -= 3

                if conflicts < best_conflicts:
                    best_conflicts = conflicts
                    best_rows = [row]

                elif conflicts == best_conflicts:
                    best_rows.append(row)

            # randomly break ties between equally good rows
            new_row = rng.choice(best_rows)

            # only update the board if the queen actually moves
            if new_row != old_row:

                # remove the queen from old position
                row_counts[old_row] -= 1
                descending[old_row - col + n - 1] -= 1
                ascending[old_row + col] -= 1

                # move the queen.
                board[col] = new_row

                # udpate counts for its new position
                row_counts[new_row] += 1
                descending[new_row - col + n - 1] += 1
                ascending[new_row + col] += 1

                steps += 1

        # save the last configuration if this attempt fails
        final_board = board

    return final_board, steps, False


def run_min_conflicts(n, seed=None):
    # generate one random N-Queens board and solve it using Min-Conflicts
    
    rng = random.Random(seed)

    initial_board = generate_board(n, rng)

    start_time = time.perf_counter()

    final_board, steps, solved = min_conflicts(
        initial_board,
        max_steps=1000,
        max_restarts=10,
        rng=rng
    )

    elapsed_time = (time.perf_counter() - start_time) * 1000

    print("=" * 50)
    print(f"MIN-CONFLICTS | N = {n}")
    print("=" * 50)

    print(f"Initial Board: {initial_board}")
    print(f"Initial Conflicts: {count_conflicts(initial_board)}")

    print(f"\nFinal Board: {final_board}")
    print(f"Final Conflicts: {count_conflicts(final_board)}")
    print(f"Steps Taken: {steps}")
    print(f"Running Time: {elapsed_time:.4f} ms")
    print(f"Solved: {solved}")

    print("\nFinal Configuration:")
    print_board(final_board)

    # confirm the success result matches actual board
    valid_solution = count_conflicts(final_board) == 0
    print(f"\nSolution Verified: {valid_solution}")

    assert solved == valid_solution, (
        "The reported solution status does not match the board."
    )

    print()

    return final_board, steps, solved, elapsed_time


def test_min_conflicts():
    # test that the algorithm recognizes a solved board and produces correct/good solutions
    

    # a known valid 8-Queens solution
    solved_board = [0, 4, 7, 5, 2, 6, 1, 3]

    result, steps, solved = min_conflicts(
        solved_board,
        rng=random.Random(42)
    )

    assert solved is True
    assert count_conflicts(result) == 0
    assert steps == 0
    assert result == solved_board

    print("All Min-Conflicts basic tests passed.")


def main():
    test_min_conflicts()

    # solve one random instance for each required board size
    for n in [8, 12, 16]:
        run_min_conflicts(n)


if __name__ == "__main__":
    main()
