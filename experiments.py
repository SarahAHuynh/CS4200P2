
import csv
import random
import time
from statistics import mean

from hill_climbing import generate_board, count_conflicts, steepest_ascent
from min_conflicts import min_conflicts


# Experiment settings
BOARD_SIZES = [8, 12, 16]
NUM_TRIALS = 200
RANDOM_SEED = 42

MAX_STEPS = 1000
MAX_RESTARTS = 10

DETAILS_FILE = "experiment_details.csv"
SUMMARY_FILE = "experiment_summary.csv"


def run_single_trial(algorithm, initial_board, rng):
    # run one search attempt and measure its execution time
    # returns the final board, step count, success status, and running time in ms
   
    start_time = time.perf_counter()

    if algorithm == "Hill Climbing":
        final_board, steps, solved = steepest_ascent(
            initial_board, rng
        )

    elif algorithm == "Min-Conflicts":
        final_board, steps, solved = min_conflicts(
            initial_board,
            max_steps=MAX_STEPS,
            max_restarts=MAX_RESTARTS,
            rng=rng
        )

    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    # independently verify the returned configuration
    final_conflicts = count_conflicts(final_board)
    valid_solution = final_conflicts == 0

    if solved != valid_solution:
        raise AssertionError(
            f"{algorithm} returned an incorrect solution status."
        )

    if len(final_board) != len(initial_board):
        raise AssertionError("Invalid board size returned.")

    if any(row < 0 or row >= len(final_board)
           for row in final_board):
        raise AssertionError("Invalid queen position returned.")

    return {
        "final_board": final_board,
        "steps": steps,
        "solved": solved,
        "final_conflicts": final_conflicts,
        "time_ms": elapsed_ms
    }


def calculate_statistics(algorithm, n, results):
    # calculate performance statistics for one algorithm
    and one board size.
    
    total_trials = len(results)

    successful = [r for r in results if r["solved"]]
    failed = [r for r in results if not r["solved"]]

    success_count = len(successful)
    failure_count = len(failed)

    success_rate = (success_count / total_trials) * 100

    avg_steps = mean(r["steps"] for r in results)
    avg_time = mean(r["time_ms"] for r in results)

    # only calculate successful run averages when solutions exist
    avg_success_steps = (
        mean(r["steps"] for r in successful)
        if successful else 0
    )

    avg_failure_steps = (
        mean(r["steps"] for r in failed)
        if failed else 0
    )

    avg_success_time = (
        mean(r["time_ms"] for r in successful)
        if successful else 0
    )

    return {
        "algorithm": algorithm,
        "n": n,
        "trials": total_trials,
        "solved": success_count,
        "failed": failure_count,
        "success_rate": success_rate,
        "avg_steps": avg_steps,
        "avg_success_steps": avg_success_steps,
        "avg_failure_steps": avg_failure_steps,
        "avg_time_ms": avg_time,
        "avg_success_time_ms": avg_success_time
    }


def run_experiments():
    # run both algorithms on the same starting boards

    # each N uses 200 randomly generated instances
    # results are collected for later comparison
    
    all_details = []
    all_summaries = []

    algorithms = ["Hill Climbing", "Min-Conflicts"]

    print("=" * 78)
    print("CS4200 PROJECT 2 - N-QUEENS EXPERIMENTS")
    print("=" * 78)

    print(f"Trials per algorithm and board size: {NUM_TRIALS}")
    print(f"Random Seed: {RANDOM_SEED}")
    print(f"Board Sizes: {BOARD_SIZES}")
    print()

    for n in BOARD_SIZES:
        print(f"Running experiments for N = {n}...")

        # generate the boards once, then reuse them for both algorithms
        board_rng = random.Random(RANDOM_SEED + n)

        initial_boards = [
            generate_board(n, board_rng)
            for _ in range(NUM_TRIALS)
        ]

        for algorithm_index, algorithm in enumerate(algorithms):
            results = []

            for trial_index, initial_board in enumerate(initial_boards):
                # use an independent, reproducible RNG for each run
                trial_seed = (
                    RANDOM_SEED * 1000000
                    + n * 10000
                    + algorithm_index * 1000
                    + trial_index
                )

                trial_rng = random.Random(trial_seed)

                result = run_single_trial(
                    algorithm,
                    initial_board.copy(),
                    trial_rng
                )

                results.append(result)

                # Save the data for each individual attempt
                all_details.append({
                    "algorithm": algorithm,
                    "n": n,
                    "trial": trial_index + 1,
                    "initial_board": str(initial_board),
                    "initial_conflicts": count_conflicts(initial_board),
                    "final_board": str(result["final_board"]),
                    "final_conflicts": result["final_conflicts"],
                    "solved": result["solved"],
                    "steps": result["steps"],
                    "time_ms": round(result["time_ms"], 6)
                })

            summary = calculate_statistics(
                algorithm, n, results
            )

            all_summaries.append(summary)

            print(
                f"  {algorithm}: "
                f"{summary['solved']}/{NUM_TRIALS} solved "
                f"({summary['success_rate']:.1f}%)"
            )

        print()

    return all_details, all_summaries


def save_csv(filename, rows):
    # save a list of dictionaries to a CSV file
    
    if not rows:
        return

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys())
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {filename}")


def print_summary(summaries):
    # display a table with the results from every experiment
    print()
    print("=" * 105)
    print("FINAL EXPERIMENT RESULTS")
    print("=" * 105)

    header = (
        f"{'Algorithm':<18}"
        f"{'N':>5}"
        f"{'Solved':>10}"
        f"{'Success %':>12}"
        f"{'Avg Steps':>12}"
        f"{'Solved Steps':>15}"
        f"{'Avg Time (ms)':>18}"
    )

    print(header)
    print("-" * 105)

    for row in summaries:
        print(
            f"{row['algorithm']:<18}"
            f"{row['n']:>5}"
            f"{row['solved']:>10}"
            f"{row['success_rate']:>11.1f}%"
            f"{row['avg_steps']:>12.2f}"
            f"{row['avg_success_steps']:>15.2f}"
            f"{row['avg_time_ms']:>18.4f}"
        )

    print("=" * 105)

    print("\nDefinitions:")
    print("Avg Steps    = Average queen moves across all trials.")
    print("Solved Steps = Average queen moves for successful trials.")
    print("Avg Time     = Average search execution time per trial.")
    print("Unsuccessful trials are included in overall averages.")
    print("A zero Solved Steps value may mean no successful trials.")


def main():
    details, summaries = run_experiments()

    print_summary(summaries)

    save_csv(DETAILS_FILE, details)
    save_csv(SUMMARY_FILE, summaries)

    print("\nExperiment completed successfully.")
    print(f"Total searches performed: {len(details)}")


if __name__ == "__main__":
    main()
