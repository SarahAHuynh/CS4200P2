import random
import time

from hill_climbing import generate_board, count_conflicts, print_board


def min_conflicts(initial_board, max_steps=1000, max_restarts=10, rng=None):
    #move randomly chosen conflicted queens to their least conflicting rows
    random_generator = rng if rng is not None else random.Random()
    board_size = len(initial_board)
    if board_size < 4:
        raise ValueError("Board size must be at least 4.")

    total_moves = 0
    last_board = initial_board.copy()

    for attempt in range(max_restarts + 1):
        # the first attempt uses the supplied board; restarts get a fresh one
        board = initial_board.copy() if attempt == 0 else generate_board(board_size, random_generator)

        row_counts = [0] * board_size
        down_diagonal_counts = [0] * (2 * board_size - 1)
        up_diagonal_counts = [0] * (2 * board_size - 1)

        for column, row in enumerate(board):
            row_counts[row] += 1
            down_diagonal_counts[row - column + board_size - 1] += 1
            up_diagonal_counts[row + column] += 1

        for iteration in range(max_steps + 1):
            conflicted_columns = []
            for column, row in enumerate(board):
                # subtract one per line to exclude the queen itself
                queen_conflicts = (
                    row_counts[row] - 1
                    + down_diagonal_counts[row - column + board_size - 1] - 1
                    + up_diagonal_counts[row + column] - 1
                )
                if queen_conflicts > 0:
                    conflicted_columns.append(column)

            if not conflicted_columns:
                return board, total_moves, True
            if iteration == max_steps:
                break

            chosen_column = random_generator.choice(conflicted_columns)
            old_row = board[chosen_column]
            fewest_conflicts = float("inf")
            best_rows = []

            # we only need to compare possible rows for the selected queen
            for candidate_row in range(board_size):
                queen_conflicts = (
                    row_counts[candidate_row]
                    + down_diagonal_counts[candidate_row - chosen_column + board_size - 1]
                    + up_diagonal_counts[candidate_row + chosen_column]
                )
                if candidate_row == old_row:
                    queen_conflicts -= 3  # the queen appears in all three counts

                if queen_conflicts < fewest_conflicts:
                    fewest_conflicts = queen_conflicts
                    best_rows = [candidate_row]
                elif queen_conflicts == fewest_conflicts:
                    best_rows.append(candidate_row)

            new_row = random_generator.choice(best_rows)
            if new_row != old_row:
                # update the counters rather than recounting every pair
                row_counts[old_row] -= 1
                down_diagonal_counts[old_row - chosen_column + board_size - 1] -= 1
                up_diagonal_counts[old_row + chosen_column] -= 1

                board[chosen_column] = new_row
                row_counts[new_row] += 1
                down_diagonal_counts[new_row - chosen_column + board_size - 1] += 1
                up_diagonal_counts[new_row + chosen_column] += 1
                total_moves += 1

        last_board = board

    return last_board, total_moves, False


def run_min_conflicts(board_size, seed=None):
    # solve one generated board and show the result
    random_generator = random.Random(seed)
    initial_board = generate_board(board_size, random_generator)
    start_time = time.perf_counter()
    final_board, moves_made, solved = min_conflicts(initial_board, rng=random_generator)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print(f"\nMIN-CONFLICTS | N = {board_size}")
    print("Initial Board:", initial_board)
    print("Initial Conflicts:", count_conflicts(initial_board))
    print("Final Board:", final_board)
    print("Final Conflicts:", count_conflicts(final_board))
    print("Steps Taken:", moves_made)
    print(f"Running Time: {elapsed_ms:.4f} ms")
    print("Solved:", solved)
    print("Final Configuration:")
    print_board(final_board)
    print("Solution Verified:", count_conflicts(final_board) == 0)
    assert solved == (count_conflicts(final_board) == 0)
    return final_board, moves_made, solved, elapsed_ms


def test_min_conflicts():
    # A finished board should be recognized without making any moves
    known_solution = [0, 4, 7, 5, 2, 6, 1, 3]
    final_board, moves_made, solved = min_conflicts(known_solution, rng=random.Random(42))
    assert final_board == known_solution and moves_made == 0 and solved
    print("All Min-Conflicts basic tests passed.")


if __name__ == "__main__":
    test_min_conflicts()
    for size in (8, 12, 16):
        run_min_conflicts(size)
