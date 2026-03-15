class CalendarError(Exception):
    """Base exception for calendar domain"""


class InvalidScheduleEntry(CalendarError):
    """Raised when schedule entry data is invalid"""


class RepositoryError(CalendarError):
    """Raised when repository cannot load data"""