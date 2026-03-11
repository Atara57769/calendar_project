from typing import List
from datetime import time, timedelta, datetime
from service.data_service import get_busy_times


def find_available_slots(person_list: List[str], event_duration: timedelta) -> List[time]:

    events = get_busy_times(person_list)



    day_start = time(7, 0)
    day_end = time(19, 0)

    if not events:
        return [day_start]

    events.sort(key=lambda e: e.start_time)

    available = []

    # convert helper
    today = datetime.today()

    # קודם נבדוק זמן לפני האירוע הראשון
    if events:
        start_dt = datetime.combine(today, day_start)
        first_dt = datetime.combine(today, events[0].start_time)

        if first_dt - start_dt >= event_duration:
            available.append(day_start)

    # merge intervals
    merged = []

    for event in events:
        if not merged:
            merged.append(event)
            continue

        last = merged[-1]

        if event.start_time <= last.end_time:
            last.end_time = max(last.end_time, event.end_time)
        else:
            merged.append(event)

    # gaps בין אירועים
    for i in range(len(merged) - 1):

        end_current = merged[i].end_time
        start_next = merged[i + 1].start_time

        end_dt = datetime.combine(today, end_current)
        next_dt = datetime.combine(today, start_next)

        if next_dt - end_dt >= event_duration:
            available.append(end_current)

    # אחרי האירוע האחרון
    if merged:

        last_end = merged[-1].end_time

        last_dt = datetime.combine(today, last_end)
        day_end_dt = datetime.combine(today, day_end)

        if day_end_dt - last_dt >= event_duration:
            available.append(last_end)
            available.append(day_end)

    return available