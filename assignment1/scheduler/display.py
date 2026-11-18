"""Print a decoded lecture schedule in room and start-time order."""

from operator import itemgetter


def show_schedule(inputs, schedule):
    """Print one line per lecture, using room and teacher names from the inputs."""
    lectures = inputs["lectures"]
    if len(schedule) != len(lectures):
        raise ValueError("Expected one assignment per lecture")

    rooms = list(inputs["classrooms"])
    teachers = list(inputs["teachers"])
    rows = []
    for (course, duration), assignment in zip(lectures, schedule):
        room = rooms[assignment["room"]]
        teacher = teachers[assignment["teacher"]]
        start = assignment["start"]
        rows.append((room, start, start + duration, course, teacher))

    print("Room | Time | Course | Teacher")
    for room, start, end, course, teacher in sorted(rows, key=itemgetter(0, 1)):
        print(f"{room} | {start:02d}:00–{end:02d}:00 | {course} | {teacher}")
