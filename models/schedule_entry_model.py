from datetime import time
from dataclasses import dataclass

@dataclass
class ScheduleEntry:
    person: str
    title: str
    start_time: time
    end_time: time