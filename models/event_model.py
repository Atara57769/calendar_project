from dataclasses import dataclass
from datetime import time

@dataclass
class Event:
    start_time:time
    end_time:time