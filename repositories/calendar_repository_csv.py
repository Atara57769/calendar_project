import csv
from datetime import datetime
from pathlib import Path
from exceptions.calendar_exceptions import RepositoryError, InvalidScheduleEntry
from models.schedule_entry_model import ScheduleEntry


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "resources" / "calendar.csv"


class CalendarRepositoryCsv:

    def get_data(self) -> list[ScheduleEntry]:
        entries = []

        try:
            with open(CSV_PATH, newline="") as file:
                reader = csv.reader(file)

                for row in reader:

                    if len(row) != 4:
                        raise InvalidScheduleEntry(f"Invalid CSV row: {row}")

                    person, title, start, end = row

                    try:
                        start_time = datetime.strptime(start, "%H:%M").time()
                        end_time = datetime.strptime(end, "%H:%M").time()
                    except ValueError as e:
                        raise InvalidScheduleEntry(
                            f"Invalid time format in row: {row}"
                        ) from e

                    entries.append(
                        ScheduleEntry(person, title, start_time, end_time)
                    )

        except FileNotFoundError as e:
            raise RepositoryError(f"Calendar file not found: {CSV_PATH}") from e

        except csv.Error as e:
            raise RepositoryError("CSV parsing error") from e

        return entries


