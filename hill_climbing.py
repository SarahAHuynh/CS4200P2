import random
import time


def generate_board(board_size, random_generator=None):
    # make a board with one randomly positioned queen in each column
    if board_size < 4:
        raise ValueError("Board size must be at least 4.")

    if random_generator is None:
        random_generator = random.Random()

    return [random_generator.randrange(board_size) for _ in range(board_size)]


def count_conflicts(board):
    # count pairs of queens that share a row or diagonal
    conflict_count = 0
    board_size = len(board)

    # compare each pair once so we don't double-count attacks
    for first_column in range(board_size):
        for second_column in range(first_column + 1, board_size):
            same_row = board[first_column] == board[second_column]
            same_diagonal = (
                abs(board[first_column] - board[second_column])
                == second_column - first_column
            )
            if same_row or same_diagonal:
                conflict_count += 1

    return conflict_count


def steepest_ascent(initial_board, random_generator=None):
    # keep making the best improving move until solved or stuck
    if random_generator is None:
        random_generator = random.Random()

    current_board = initial_board.copy()
    current_conflicts = count_conflicts(current_board)
    board_size = len(current_board)
    moves_made = 0

    while current_conflicts > 0:
        fewest_conflicts = current_conflicts
        best_moves = []

        # a neighbor is any board made by moving one queen in its column
        for column in range(board_size):
            original_row = current_board[column]
            for new_row in range(board_size):
                if new_row == original_row:
                    continue

                current_board[column] = new_row
                neighbor_conflicts = count_conflicts(current_board)

                if neighbor_conflicts < fewest_conflicts:
                    fewest_conflicts = neighbor_conflicts
                    best_moves = [(column, new_row)]
                elif neighbor_conflicts == fewest_conflicts and fewest_conflicts < current_conflicts:
                    best_moves.append((column, new_row))

            # put the queen back before checking another column
            current_board[column] = original_row

        # No sideways moves, so stop if none of the neighbors is better
        if not best_moves:
            break

        chosen_column, chosen_row = random_generator.choice(best_moves)
        current_board[chosen_column] = chosen_row
        current_conflicts = fewest_conflicts
        moves_made += 1

    return current_board, moves_made, current_conflicts == 0


def print_board(board):
    # show the final positions using Q for queens and dots for empty squares
    for row in range(len(board)):
        squares = ["Q" if board[column] == row else "." for column in range(len(board))]
        print(" ".join(squares))


def verify_local_minimum(board):
   #make sure there isn't a single-queen move that improves this board
    current_conflicts = count_conflicts(board)
    for column in range(len(board)):
        for new_row in range(len(board)):
            if new_row == board[column]:
                continue
            neighbor = board.copy()
            neighbor[column] = new_row
            if count_conflicts(neighbor) < current_conflicts:
                return False
    return True


def run_hill_climbing(board_size, seed=None):
    # run one hill climbing search and print the final config
    random_generator = random.Random(seed)
    initial_board = generate_board(board_size, random_generator)
    start_time = time.perf_counter()
    final_board, moves_made, solved = steepest_ascent(initial_board, random_generator)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print(f"\nSTEEPEST-ASCENT HILL CLIMBING | N = {board_size}")
    print("Initial Board:", initial_board)
    print("Initial Conflicts:", count_conflicts(initial_board))
    print("Final Board:", final_board)
    print("Final Conflicts:", count_conflicts(final_board))
    print("Steps Taken:", moves_made)
    print(f"Running Time: {elapsed_ms:.4f} ms")
    print("Solved:", solved)
    print("Valid Termination:", verify_local_minimum(final_board))
    print("Final Configuration:")
    print_board(final_board)
    return final_board, moves_made, solved, elapsed_ms


def test_conflicts():
    #quick checks for the conflict counting function
    known_boards = [
        ([0, 0, 0, 0], 6),
        ([0, 1, 2, 3], 6),
        ([1, 3, 0, 2], 0),
        ([0, 2, 4, 1], 0),
        ([0, 4, 7, 5, 2, 6, 1, 3], 0),
    ]
    for board, expected_conflicts in known_boards:
        assert count_conflicts(board) == expected_conflicts
    print("All heuristic tests passed.")


if __name__ == "__main__":
    test_conflicts()
    for size in (8, 12, 16):
        run_hill_climbing(size)
