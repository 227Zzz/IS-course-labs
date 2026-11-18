"""Run the Task 1 baseline on the supplied lecture data."""

from pathlib import Path

from .chromosome import decode
from .display import show_schedule
from .ga_runner import run_ga
from .parsing import parse_inputs


def main():
    sample_folder = Path(__file__).resolve().parents[1] / "sem1_files"
    inputs = parse_inputs(sample_folder)
    ga = run_ga(inputs, random_seed=42, num_generations=6000, stop_criteria="reach_0")
    chromosome, fitness, _ = ga.best_solution(ga.last_generation_fitness)
    print(f"Final fitness: {fitness} (generation {ga.generations_completed})")
    show_schedule(inputs, decode(chromosome))


if __name__ == "__main__":
    main()
