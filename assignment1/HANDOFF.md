# HANDOFF: Task 1 baseline (for Tasks 3 & 4)

Use the Task 1 baseline for Tasks 3 and 4 through the functions described here.
Task 2 will add custom initial populations, crossover, and mutation through the arguments of `run_ga()`.

## 1. Quick start

Run everything from the assignment folder (`assignment1/`), in an environment with PyGAD installed
(`pip install pygad`). The sample was tested with PyGAD 3.9.2.

```python
from scheduler.parsing import parse_inputs
from scheduler.chromosome import decode
from scheduler.constraints import hard_penalty
from scheduler.display import show_schedule
from scheduler.ga_runner import run_ga

inputs = parse_inputs("sem1_files")      # read the input files
ga = run_ga(inputs)                      # baseline GA (fitness = -hard_penalty)

solution, fitness, _ = ga.best_solution()
schedule = decode(solution)
show_schedule(inputs, schedule)
```

Run `python -m scheduler.task1_demo` to reproduce the sample timetable. It uses seed 42,
runs for up to 6,000 generations, and stops when fitness reaches 0. The verified output is
`Final fitness: 0 (generation 5758)`, followed by all 10 lectures. A negative final fitness
equals the remaining hard penalty in magnitude. The quick-start call `run_ga(inputs)` uses
150 generations by default and may still have violations when it finishes.

Use module commands for the individual checks as well:

```bash
python -m scheduler.parsing
python -m scheduler.chromosome
python -m scheduler.constraints
python -m scheduler.ga_runner
```

All four commands and the demo were verified from `assignment1/` in the same environment.

## 2. Project structure

```
assignment1/
├── HANDOFF.md              <- this file
├── sem1_files/
│   ├── Classes.txt
│   ├── Classrooms.txt
│   ├── Teachers.txt
│   └── Preferences.txt     <- not used by Task 1; Task 3 reads it separately
├── scheduler/
│   ├── parsing.py          <- input files -> `inputs`
│   ├── chromosome.py       <- build_gene_space() + decode()
│   ├── constraints.py      <- hard_penalty()  (hard constraints only)
│   ├── display.py          <- show_schedule()
│   ├── ga_runner.py        <- run_ga()
│   └── task1_demo.py       <- end-to-end demo
```

## 3. Data model

`parse_inputs` returns an `inputs` dictionary with these keys:

| Key | Meaning |
|---|---|
| `lectures` | One `(course, duration_in_hours)` tuple per lecture, in input order. Repeated tuples are separate lectures. |
| `classrooms` | Room name -> opening and closing hours. |
| `teachers` | Teacher name -> courses they can teach. |

Course names are lowercase. Room and teacher IDs are integers starting at 0, in the order
they appear in their input files. `parse_inputs` reads only `Classes.txt`, `Classrooms.txt`,
and `Teachers.txt`. Task 3 must read `Preferences.txt` separately.

A chromosome has 3 genes per lecture, in lecture order: `[room_id, start_hour, teacher_id]`
(length = `3 * len(lectures)`). A full chromosome assigns every lecture exactly once.

- The gene space restricts teacher candidates to teachers qualified for the course.
  Custom populations and operators must keep their values within those gene spaces.
- Start-hour candidates include every hour at which the lecture fits in at least one room.
  Room and start are separate genes, so a lecture can still land in a room that is closed at that time.
  That is what the hard penalty checks.

`decode(chromosome)` returns a list of dictionaries, one per lecture, in the same order as
`inputs["lectures"]`. Each dictionary has the integer fields `room`, `start`, and `teacher`.

For example, this prints one decoded row:

```python
print(decode([0, 10, 1])[0])
```

Actual output:

```text
{'room': 0, 'start': 10, 'teacher': 1}
```

Use dictionary access such as `schedule[i]["teacher"]`. The course and duration come from
`inputs["lectures"][i]`; they are not included in the decoded row. Build teacher preferences
and workload balance on this decoded schedule.

## 4. Function reference

| Function | Purpose |
|---|---|
| `parse_inputs(folder)` | Reads `Classes.txt`, `Classrooms.txt`, and `Teachers.txt` and returns `inputs`. Does not read `Preferences.txt`. |
| `build_gene_space(inputs)` | Three candidate lists per lecture: room ID, start hour, teacher ID. |
| `decode(chromosome)` | Chromosome -> schedule (see above). |
| `hard_penalty(inputs, schedule)` | Hard-constraint violations; 0 = feasible. |
| `show_schedule(inputs, schedule)` | Prints one line per lecture: room, start-end, course, teacher. Sorted by room name, then start hour. |
| `run_ga(inputs, **kwargs)` | Runs the GA and returns the fitted PyGAD instance. |

### `hard_penalty` details

These checks assume a full chromosome whose values follow the gene spaces. Under that
contract, a penalty of 0 means the schedule is feasible.

- +1 for each lecture outside its room's opening hours.
- For each hour, a room (or teacher) booked by *n* lectures adds *n - 1* points for that resource
  (so three lectures at once = 2 points).
- Back-to-back lectures may share a room and a teacher.
- Sanity check: `python -m scheduler.constraints` prints `Hard penalty: 1` for the built-in example
  (one hour of room overlap).

### `run_ga` details

- Default fitness is `-hard_penalty(inputs, schedule)` (higher is better).
- Task 2 hooks: `initial_population`, `crossover_type`, `mutation_type`. Every supplied chromosome
  must follow the existing gene spaces.
- Any other PyGAD setting (e.g. `on_generation`, `num_generations`) can be passed by keyword.
- Results: `ga.best_solution()` (standard PyGAD), plus `ga.population` and
  `ga.last_generation_fitness` for the final population.

## 5. How to extend it (Task 3)

For a single fitness, `fitness_fn(inputs, schedule)` receives the decoded schedule and returns
the entire score. Include the hard penalty in that score. The example uses a weight of 1,000;
choose a weight larger than the possible range of total soft cost on your dataset so that
soft improvements cannot compensate for a hard violation.

`preference_cost` and `balance_cost` are placeholders, not functions provided by `scheduler`.
The Task 3 author must implement them before running these examples. Lower costs mean a better
schedule. For balance, sum lecture durations for every teacher, including teachers with zero hours.

```python
def my_score(inputs, schedule):
    return -1000 * hard_penalty(inputs, schedule) - preference_cost(inputs, schedule) - balance_cost(inputs, schedule)

ga = run_ga(inputs, fitness_fn=my_score)
```

For multiple objectives, return a list or vector and use NSGA-II parent selection:

```python
def my_scores(inputs, schedule):
    hard = 1000 * hard_penalty(inputs, schedule)
    return [-hard - preference_cost(inputs, schedule), -hard - balance_cost(inputs, schedule)]

ga = run_ga(inputs, fitness_fn=my_scores, parent_selection_type="nsga2")
```

For this version, the hard-penalty weight should exceed the cost range of each objective
so that every feasible schedule scores higher on both objectives than any infeasible schedule.
Recheck those bounds for larger inputs. `Preferences.txt` is not loaded by Task 1.

## 6. Status

- [x] Task 1 baseline works on the sample files (`python -m scheduler.task1_demo`): fitness 0 at generation 5758, with all 10 lectures displayed.
- [ ] Task 2: custom initial populations, crossover, and mutation are pending.
