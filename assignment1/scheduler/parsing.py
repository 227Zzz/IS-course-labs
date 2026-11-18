"""Read the three timetable inputs for Task 1."""

import re
from pathlib import Path


def read_rows(path):
    """Yield the name and the comma-separated items inside the brackets."""
    with path.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            line = line.strip()
            if not line:
                continue
            match = re.fullmatch(r"([^\[\]]+?)\s*\[([^\[\]]*)\]", line)
            if match is None:
                raise ValueError(f"{path.name}, line {line_number}: expected Name [items]")
            name, contents = match.groups()
            items = [item.strip() for item in contents.split(",")] if contents.strip() else []
            yield name.strip(), items


def parse_inputs(folder):
    """Return lectures, classroom opening hours, and teacher qualifications."""
    folder = Path(folder)
    lectures = []
    for course, durations in read_rows(folder / "Classes.txt"):
        for duration in durations:
            lectures.append((course.lower(), int(duration)))

    classrooms = {}
    for room, hours in read_rows(folder / "Classrooms.txt"):
        opening, closing = map(int, hours)
        classrooms[room] = (opening, closing)

    teachers = {}
    for teacher, courses in read_rows(folder / "Teachers.txt"):
        teachers[teacher] = [course.lower() for course in courses]

    return {"lectures": lectures, "classrooms": classrooms, "teachers": teachers}


if __name__ == "__main__":
    sample_folder = Path(__file__).resolve().parents[1] / "sem1_files"
    print(parse_inputs(sample_folder))
