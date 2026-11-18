"""Encode each lecture as three integer genes: room ID, start hour, teacher ID."""


def build_gene_space(inputs):
    """Return one list of allowed values per gene, in lecture order."""
    gene_space = []
    for course, duration in inputs["lectures"]:
        room_ids = []
        start_hours = set()
        for room_id, (opening, closing) in enumerate(inputs["classrooms"].values()):
            if opening + duration <= closing:
                room_ids.append(room_id)
                start_hours.update(range(opening, closing - duration + 1))

        teacher_ids = [
            teacher_id
            for teacher_id, courses in enumerate(inputs["teachers"].values())
            if course in courses
        ]
        if not room_ids or not teacher_ids:
            raise ValueError(f"No suitable room or qualified teacher for {course} ({duration}h)")

        gene_space.extend([room_ids, sorted(start_hours), teacher_ids])
    return gene_space


def decode(chromosome):
    """Return one assignment per lecture, in the same order as inputs['lectures']."""
    if len(chromosome) % 3:
        raise ValueError("Expected three genes per lecture: room ID, start hour, teacher ID")

    schedule = []
    for i in range(0, len(chromosome), 3):
        room, start, teacher = chromosome[i:i + 3]
        schedule.append({"room": int(room), "start": int(start), "teacher": int(teacher)})
    return schedule


if __name__ == "__main__":
    from pathlib import Path
    from random import Random

    from .parsing import parse_inputs

    inputs = parse_inputs(Path(__file__).resolve().parents[1] / "sem1_files")
    gene_space = build_gene_space(inputs)
    rng = Random(42)
    chromosome = [rng.choice(candidates) for candidates in gene_space]
    schedule = decode(chromosome)
    print(f"{len(chromosome)} genes -> {len(schedule)} lectures")
    for lecture, assignment in zip(inputs["lectures"], schedule):
        print(lecture, assignment)
