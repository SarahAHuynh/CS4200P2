import csv
import random
import time
from statistics import mean

from hill_climbing import generate_board, count_conflicts, steepest_ascent
from min_conflicts import min_conflicts

BOARD_SIZES = (8, 12, 16)
TRIALS_PER_SIZE = 200
RANDOM_SEED = 42
MAX_STEPS = 1000
MAX_RESTARTS = 10


def save_results(filename, records):
    # write a list of trial or summary records to a CSV file
    with open(filename, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print("Saved:", filename)


def summarize_results(algorithm_name, board_size, trial_results):
    # calculate success rates and average costs for one group of trials
    successful_runs = [run for run in trial_results if run["solved"]]
    failed_runs = [run for run in trial_results if not run["solved"]]

    return {
        "algorithm": algorithm_name,
        "n": board_size,
        "trials": len(trial_results),
        "solved": len(successful_runs),
        "failed": len(failed_runs),
        "success_rate": len(successful_runs) / len(trial_results) * 100,
        "avg_steps": mean(run["steps"] for run in trial_results),
        "avg_success_steps": mean(run["steps"] for run in successful_runs) if successful_runs else 0,
        "avg_failure_steps": mean(run["steps"] for run in failed_runs) if failed_runs else 0,
        "avg_time_ms": mean(run["time_ms"] for run in trial_results),
        "avg_success_time_ms": mean(run["time_ms"] for run in successful_runs) if successful_runs else 0,
    }


def run_experiments():
    # run 200 paired tests per board size and save the measurements
    all_trials = []
    all_summaries = []
    algorithms = ("Hill Climbing", "Min-Conflicts")

    print("N-QUEENS EXPERIMENTS")
    print("Trials per algorithm and board size:", TRIALS_PER_SIZE)
    print("Random seed:", RANDOM_SEED)

    for board_size in BOARD_SIZES:
        board_random = random.Random(RANDOM_SEED + board_size)
        starting_boards = [
            generate_board(board_size, board_random)
            for _ in range(TRIALS_PER_SIZE)
        ]

        # both methods use these exact same starting boards
        for algorithm_number, algorithm_name in enumerate(algorithms):
            trial_results = []

            for trial_number, starting_board in enumerate(starting_boards, start=1):
                trial_seed = (
                    RANDOM_SEED * 1000000 + board_size * 10000
                    + algorithm_number * 1000 + trial_number - 1
                )
                random_generator = random.Random(trial_seed)

                start_time = time.perf_counter()
                if algorithm_name == "Hill Climbing":
                    final_board, moves_made, solved = steepest_ascent(
                        starting_board, random_generator
                    )
                else:
                    final_board, moves_made, solved = min_conflicts(
                        starting_board,
                        max_steps=MAX_STEPS,
                        max_restarts=MAX_RESTARTS,
                        rng=random_generator,
                    )
                elapsed_ms = (time.perf_counter() - start_time) * 1000

                remaining_conflicts = count_conflicts(final_board)
                assert len(final_board) == board_size
                assert all(0 <= row < board_size for row in final_board)
                assert solved == (remaining_conflicts == 0)

                result = {
                    "algorithm": algorithm_name,
                    "n": board_size,
                    "trial": trial_number,
                    "initial_board": str(starting_board),
                    "initial_conflicts": count_conflicts(starting_board),
                    "final_board": str(final_board),
                    "final_conflicts": remaining_conflicts,
                    "solved": solved,
                    "steps": moves_made,
                    "time_ms": round(elapsed_ms, 6),
                }
                trial_results.append(result)
                all_trials.append(result)

            summary = summarize_results(algorithm_name, board_size, trial_results)
            all_summaries.append(summary)
            print(
                f"N={board_size:>2}  {algorithm_name:<14}  "
                f"solved {summary['solved']}/{TRIALS_PER_SIZE} "
                f"({summary['success_rate']:.1f}%)"
            )

    save_results("experiment_details.csv", all_trials)
    save_results("experiment_summary.csv", all_summaries)

    print("\nAlgorithm          N  Solved   Success    Avg Steps    Avg Time (ms)")
    for summary in all_summaries:
        print(
            f"{summary['algorithm']:<17}{summary['n']:>2}  "
            f"{summary['solved']:>3}/200  {summary['success_rate']:>6.1f}%  "
            f"{summary['avg_steps']:>11.2f}  {summary['avg_time_ms']:>14.4f}"
        )
    print("Total searches performed:", len(all_trials))
    return all_trials, all_summaries


if __name__ == "__main__":
    run_experiments()
