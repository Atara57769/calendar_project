from typing import List
from datetime import time, timedelta, datetime

from models.event_model import Event

DAY_START = time(7, 0)
DAY_END = time(19, 0)


class CalendarService:

    def __init__(self, data_service):
        self.data_service = data_service


    def get_busy_times(self, person_list: list[str]):

        entries = self.data_service.get_data()

        return [
            Event(e.start_time, e.end_time)
            for e in entries
            if e.person in person_list
        ]

    def find_available_slots(self, person_list: List[str], event_duration: timedelta) -> List[time]:

        events = self.get_busy_times(person_list)

        if not events:
            return [DAY_START]

        events.sort(key=lambda e: e.start_time)

        # merge overlapping events
        merged = []
        for event in events:
            if not merged or event.start_time > merged[-1].end_time:
                merged.append(event)
            else:
                merged[-1].end_time = max(merged[-1].end_time, event.end_time)

        today = datetime.today()

        available = []

        prev_end = DAY_START

        for event in merged:

            gap_start = datetime.combine(today, prev_end)
            gap_end = datetime.combine(today, event.start_time)

            if gap_end - gap_start >= event_duration:
                available.append(prev_end)

            prev_end = event.end_time

        # gap after last event
        last_gap_start = datetime.combine(today, prev_end)
        day_end_dt = datetime.combine(today, DAY_END)

        if day_end_dt - last_gap_start >= event_duration:
            available.append(prev_end)

        return available