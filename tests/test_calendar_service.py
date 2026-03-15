import pytest
from datetime import time, timedelta

from models.schedule_entry_model import ScheduleEntry
from service.calendar_service import CalendarService
from exceptions.calendar_exceptions import CalendarError


class FakeCalendarRepository:

    def __init__(self, entries):
        self.entries = entries

    def get_data(self):
        return self.entries


def test_available_slots_before_middle_after():

    data = [
        ScheduleEntry("Alice", "Meeting", time(8, 0), time(9, 0)),
        ScheduleEntry("Alice", "Review", time(11, 0), time(12, 0)),
    ]

    service = CalendarService(FakeCalendarRepository(data))

    result = service.find_available_slots(["Alice"], timedelta(hours=1))

    # before first event
    assert time(7, 0) in result

    # gap between events
    assert time(9, 0) in result

    # after last event
    assert time(12, 0) in result



def test_no_events():

    service = CalendarService(FakeCalendarRepository([]))

    result = service.find_available_slots(["Alice"], timedelta(hours=1))

    assert result == [time(7, 0)]


# -------- TESTS FOR EXCEPTIONS --------


def test_empty_person_list():

    service = CalendarService(FakeCalendarRepository([]))

    with pytest.raises(CalendarError):
        service.get_busy_times([])


def test_invalid_event_duration():

    service = CalendarService(FakeCalendarRepository([]))

    with pytest.raises(CalendarError):
        service.find_available_slots(["Alice"], timedelta(minutes=0))
    with pytest.raises(CalendarError):
        service.find_available_slots(["Alice"], timedelta(hours=20))


