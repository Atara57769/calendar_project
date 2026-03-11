import csv
from datetime import datetime
from pathlib import Path

from models.event_model import Event
from models.schedule_entry_model import ScheduleEntry


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "resources" / "calendar.csv"


def get_data():
    entries = []

    with open(CSV_PATH, newline="") as f:
        reader = csv.reader(f)

        for row in reader:
            person, title, start, end = row

            start_time = datetime.strptime(start, "%H:%M").time()
            end_time = datetime.strptime(end, "%H:%M").time()

            entry = ScheduleEntry(person, title, start_time, end_time)

            entries.append(entry)

    return entries

def get_person_events(name: str, entries: list[ScheduleEntry]):
    return [
        Event(e.start_time, e.end_time)
        for e in entries
        if e.person == name
    ]

def get_busy_times(person_list: list[str]):

    entries = get_data()
    return [
        Event(e.start_time, e.end_time)
        for e in entries
        if e.person in person_list
    ]