from typing import Protocol
from models.schedule_entry_model import ScheduleEntry


class CalendarRepository(Protocol):

    def get_data(self) -> list[ScheduleEntry]:
        ...