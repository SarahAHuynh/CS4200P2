import contextlib
import random
import sys
import time
from pathlib import Path

from hill_climbing import (
    generate_board, count_conflicts, steepest_ascent,
    print_board, verify_local_minimum,
)
from min_conflicts import min_conflicts
from experiments import run_experiments


class TranscriptWriter:
    #show output in the terminal and keep a copy in a text file

    def __init__(self, terminal, output_file):
        self.terminal = terminal
        self.output_file = output_file

    def write(self, text):
        self.terminal.write(text)
        self.output_file.write(text)

    def flush(self):
        self.terminal.flush()
        self.output_file.flush()


def ask_user(question, output_file):
    # save typed answers too, since input() doesn't appear in the transcript
    answer = input(question).strip()
    output_file.write(question + answer + "\n")
    return answer


def ask_board_size(output_file):
    while True:
        answer = ask_user("Board size (8, 12, or 16): ", output_file)
        if answer in ("8", "12", "16"):
            return int(answer)
        print("Please enter 8, 12, or 16.")


def ask_algorithm(output_file):
    while True:
        print("\n[1] Steepest-Ascent Hill Climbing")
        print("[2] Min-Conflicts")
        answer = ask_user("Choose an algorithm: ", output_file)
        if answer in ("1", "2"):
            return answer
        print("Please enter 1 or 2.")


def enter_board(board_size, output_file):
    print(f"Enter {board_size} row numbers from 0 to {board_size - 1}, with a space in between each number.")
    print("Each number gives the row of the queen in that column.")

    while True:
        answer = ask_user("Board: ", output_file)
        try:
            board = [int(number) for number in answer.replace(",", " ").split()]
        except ValueError:
            print("Please enter numbers only.")
            continue
        if len(board) == board_size and all(0 <= row < board_size for row in board):
            return board
        print(f"Please enter exactly {board_size} numbers between 0 and {board_size - 1}.")


def show_search_result(initial_board, algorithm_choice):
    #run the selected search and display its final board and stats
    random_generator = random.Random()
    algorithm_name = (
        "Steepest-Ascent Hill Climbing" if algorithm_choice == "1" else "Min-Conflicts"
    )
    print("\n" + "=" * 55)
    print(f"{algorithm_name.upper()} | N = {len(initial_board)}")
    print("=" * 55)
    print("Initial Board:", initial_board)
    print("Initial Conflicts:", count_conflicts(initial_board))

    start_time = time.perf_counter()
    if algorithm_choice == "1":
        final_board, moves_made, solved = steepest_ascent(initial_board, random_generator)
    else:
        final_board, moves_made, solved = min_conflicts(initial_board, rng=random_generator)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    final_conflicts = count_conflicts(final_board)
    assert solved == (final_conflicts == 0)
    print("Final Board:", final_board)
    print("Final Conflicts:", final_conflicts)
    print("Steps Taken:", moves_made)
    print(f"Running Time: {elapsed_ms:.4f} ms")
    print("Solved:", solved)
    if algorithm_choice == "1":
        print("Valid Termination:", verify_local_minimum(final_board))
    print("Final Configuration:")
    print_board(final_board)
    print("Solution Verified:", final_conflicts == 0)
    print()


def next_output_filename():
    #avoid overwriting previous transcripts from earlier runs
    file_number = 1
    while Path(f"program_output({file_number}).txt").exists():
        file_number += 1
    return Path(f"program_output({file_number}).txt")


def main():
    transcript_path = next_output_filename()
    with transcript_path.open("w", encoding="utf-8") as output_file:
        with contextlib.redirect_stdout(TranscriptWriter(sys.stdout, output_file)):
            print("============================================")
            print("       CS4200 P2 - N-QUEENS SOLVER")
            print("============================================")

            while True:
                print("\n[1] Generate a Random N-Queens Board")
                print("[2] Enter a Board Manually")
                print("[3] Run 200-Case Analysis")
                print("[4] Exit")
                user_choice = ask_user("Enter your choice: ", output_file)

                if user_choice == "1":
                    board_size = ask_board_size(output_file)
                    board = generate_board(board_size)
                    show_search_result(board, ask_algorithm(output_file))
                elif user_choice == "2":
                    board_size = ask_board_size(output_file)
                    board = enter_board(board_size, output_file)
                    show_search_result(board, ask_algorithm(output_file))
                elif user_choice == "3":
                    run_experiments()
                elif user_choice == "4":
                    print("Exiting N-Queens solver. Goodbye!")
                    break
                else:
                    print("Invalid option. Please enter 1, 2, 3, or 4.")

    print("Transcript saved:", transcript_path)


if __name__ == "__main__":
    main()
