"""Score the hard constraints for a schedule decoded from the gene space."""

from collections import Counter


def hard_penalty(inputs, schedule):
    """Count room-hours violations and excess concurrent room or teacher bookings."""
    lectures = inputs["lectures"]
    if len(schedule) != len(lectures):
        raise ValueError("Expected one assignment per lecture")

    room_hours = list(inputs["classrooms"].values())
    room_usage = Counter()
    teacher_usage = Counter()
    penalty = 0

    for (_, duration), assignment in zip(lectures, schedule):
        room = assignment["room"]
        teacher = assignment["teacher"]
        start = assignment["start"]
        end = start + duration
        opening, closing = room_hours[room]
        if start < opening or end > closing:
            penalty += 1

        for hour in range(start, end):
            room_usage[room, hour] += 1
            teacher_usage[teacher, hour] += 1

    penalty += sum(count - 1 for count in room_usage.values())
    penalty += sum(count - 1 for count in teacher_usage.values())
    return penalty


if __name__ == "__main__":
    from .chromosome import decode

    example = {
        "lectures": [("math", 2), ("math", 2)],
        "classrooms": {"P1": (10, 16)},
        "teachers": {"Anna": ["math"], "Charles": ["math"]},
    }
    # Room P1 is shared from 11 to 12. The teachers are different.
    schedule = decode([0, 10, 0, 0, 11, 1])
    print("Hard penalty:", hard_penalty(example, schedule))
