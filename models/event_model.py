from dataclasses import dataclass
from datetime import time

@dataclass(frozen=True)
class Event:
    start_time:time
    end_time:time