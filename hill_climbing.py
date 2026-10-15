
import random
import time


def generate_board(n, rng=None):
    # generate a random N-Queens board w each column having exactly one queen
    # value at each index represents the queen's row
    
    if n < 4:
        raise ValueError("N must be at least 4.")

    if rng is None:
        rng = random.Random()

    return [rng.randrange(n) for _ in range(n)]


def count_conflicts(board):
    # count number of pairs of queens attacking each other
    # queens conflict if they share the same row or diagonal
    # each pair is counted only once.
    
    conflicts = 0
    n = len(board)

    for i in range(n):
        for j in range(i + 1, n):
            same_row = board[i] == board[j]
            same_diagonal = abs(board[i] - board[j]) == j - i

            if same_row or same_diagonal:
                conflicts += 1

    return conflicts


def steepest_ascent(initial_board, rng=None):
    #  solve N-Queens using steepest-ascent hill climbing

    # every possible vertical queen move is considered
    # only moves that strictly reduce conflicts are accepted

    # returns final_board, steps, and if solution was found or not
    
    if rng is None:
        rng = random.Random()

    current_board = initial_board.copy()
    current_conflicts = count_conflicts(current_board)

    n = len(current_board)
    steps = 0

    while current_conflicts > 0:
        best_conflicts = current_conflicts
        best_moves = []

        # examine every queen in every column
        for col in range(n):
            original_row = current_board[col]

            # try placing this queen in every other row
            for row in range(n):
                if row == original_row:
                    continue

                current_board[col] = row

                neighbor_conflicts = count_conflicts(current_board)

                if neighbor_conflicts < best_conflicts:
                    best_conflicts = neighbor_conflicts
                    best_moves = [(col, row)]

                elif (
                    neighbor_conflicts == best_conflicts
                    and best_conflicts < current_conflicts
                ):
                    best_moves.append((col, row))

            # restore the queen before looking at next column
            current_board[col] = original_row

        # stop if no neighbor improves the heuristic (prevents sideways moves)
        if not best_moves:
            break

        # randomly choose equally good moves
        best_col, best_row = rng.choice(best_moves)

        current_board[best_col] = best_row
        current_conflicts = best_conflicts
        steps += 1

    solved = current_conflicts == 0

    return current_board, steps, solved


def print_board(board):
    # print board with Q for queens and . for empty spaces
    n = len(board)

    for row in range(n):
        line = []

        for col in range(n):
            if board[col] == row:
                line.append("Q")
            else:
                line.append(".")

        print(" ".join(line))


def run_hill_climbing(n, seed=None):
    # generate one random N-Queens problem and run hill climbing
    
    rng = random.Random(seed)

    initial_board = generate_board(n, rng)

    start_time = time.perf_counter()

    final_board, steps, solved = steepest_ascent(
        initial_board, rng
    )

    elapsed_time = (time.perf_counter() - start_time) * 1000

    print("=" * 50)
    print(f"STEEPEST-ASCENT HILL CLIMBING | N = {n}")
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

    print(f"Valid Termination: {verify_local_minimum(final_board)}")
    print()

    return final_board, steps, solved, elapsed_time

def test_conflicts():
    # test heuristic against boards with known conflict counts
    test_cases = [
        ([0, 0, 0, 0], 6),
        ([0, 1, 2, 3], 6),
        ([1, 3, 0, 2], 0),
        ([0, 2, 4, 1], 0),
        ([0, 4, 7, 5, 2, 6, 1, 3], 0),
    ]

    for board, expected in test_cases:
        actual = count_conflicts(board)

        assert actual == expected, (
            f"Board {board}: expected {expected}, got {actual}"
        )

    print("All heuristic tests passed.")


def verify_local_minimum(board):
    #check that no single queen move reduces conflicts
    n = len(board)
    current_conflicts = count_conflicts(board)

    for col in range(n):
        for row in range(n):
            if row == board[col]:
                continue

            neighbor = board.copy()
            neighbor[col] = row

            if count_conflicts(neighbor) < current_conflicts:
                return False

    return True

def main():
    test_conflicts()

    # 1 independent hill-climbing attempt for each board size
    for n in [8, 12, 16]:
        run_hill_climbing(n)


if __name__ == "__main__":
    main()