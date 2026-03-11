import csv
from datetime import datetime
from pathlib import Path

from models.schedule_entry_model import ScheduleEntry


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "resources" / "calendar.csv"


class DataService:


    def get_data(self):
        entries = []

        with open(CSV_PATH, newline="") as file:
            reader = csv.reader(file)

            for row in reader:
                person, title, start, end = row

                start_time = datetime.strptime(start, "%H:%M").time()
                end_time = datetime.strptime(end, "%H:%M").time()

                entries.append(
                    ScheduleEntry(person, title, start_time, end_time)
                )

        return entries


