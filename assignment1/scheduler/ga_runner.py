"""Run the baseline GA and plug in alternative fitness functions or operators."""

import pygad

from .chromosome import build_gene_space, decode
from .constraints import hard_penalty


def baseline_fitness(inputs, schedule):
    return -hard_penalty(inputs, schedule)


def run_ga(
    inputs,
    fitness_fn=baseline_fitness,
    *,
    initial_population=None,
    crossover_type="single_point",
    mutation_type="random",
    random_seed=42,
    **ga_settings,
):
    """Run the following six steps and return the fitted PyGAD instance.

    1. Build the allowed values for each gene.
    2. Decode each chromosome when PyGAD asks for its fitness.
    3. Score the schedule with fitness_fn(inputs, schedule).
    4. Configure the population, crossover, mutation and run settings.
    5. Run the GA.
    6. Return the GA so the caller can inspect solutions and fitness history.
    """
    spaces = build_gene_space(inputs)

    def evaluate(ga_instance, chromosome, solution_index):
        return fitness_fn(inputs, decode(chromosome))

    population_size = ga_settings.pop("sol_per_pop", 60)
    if initial_population is not None:
        population_size = len(initial_population)
        if any(len(row) != len(spaces) for row in initial_population):
            raise ValueError(f"Each initial chromosome must have {len(spaces)} genes")

    settings = {
        "num_generations": 150,
        "num_parents_mating": min(12, population_size),
        "parent_selection_type": "tournament",
    }
    settings.update(ga_settings)
    ga = pygad.GA(
        fitness_func=evaluate,
        gene_space=spaces,
        gene_type=int,
        num_genes=len(spaces),
        sol_per_pop=population_size,
        initial_population=initial_population,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        random_seed=random_seed,
        **settings,
    )
    ga.run()
    return ga


if __name__ == "__main__":
    from pathlib import Path

    from .display import show_schedule
    from .parsing import parse_inputs

    inputs = parse_inputs(Path(__file__).resolve().parents[1] / "sem1_files")
    ga = run_ga(inputs)
    chromosome, fitness, _ = ga.best_solution(ga.last_generation_fitness)
    show_schedule(inputs, decode(chromosome))
    print(f"Baseline fitness: {fitness} (0 means feasible)")
