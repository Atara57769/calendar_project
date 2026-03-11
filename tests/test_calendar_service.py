from datetime import time, timedelta

from models.schedule_entry_model import ScheduleEntry
from models.event_model import Event

from service.calendar_service import CalendarService


class FakeDataService:

    def __init__(self, entries):
        self.entries = entries

    def get_data(self):
        return self.entries


def test_get_busy_times_single_person():

    data = [
        ScheduleEntry("Alice", "Meeting", time(8, 0), time(9, 0)),
        ScheduleEntry("Bob", "Call", time(10, 0), time(11, 0)),
    ]

    service = CalendarService(FakeDataService(data))

    result = service.get_busy_times(["Alice"])

    assert len(result) == 1
    assert result[0].start_time == time(8, 0)


def test_get_busy_times_multiple_people():

    data = [
        ScheduleEntry("Alice", "Meeting", time(8, 0), time(9, 0)),
        ScheduleEntry("Bob", "Call", time(10, 0), time(11, 0)),
        ScheduleEntry("Charlie", "Review", time(12, 0), time(13, 0)),
    ]

    service = CalendarService(FakeDataService(data))

    result = service.get_busy_times(["Alice", "Bob"])

    assert len(result) == 2


def test_available_before_first_event():

    data = [
        ScheduleEntry("Alice", "Meeting", time(9, 0), time(10, 0)),
    ]

    service = CalendarService(FakeDataService(data))

    result = service.find_available_slots(["Alice"], timedelta(hours=1))

    assert time(7, 0) in result


def test_gap_between_events():

    data = [
        ScheduleEntry("Alice", "Meeting", time(8, 0), time(9, 0)),
        ScheduleEntry("Alice", "Review", time(11, 0), time(12, 0)),
    ]

    service = CalendarService(FakeDataService(data))

    result = service.find_available_slots(["Alice"], timedelta(hours=1))

    assert time(9, 0) in result


def test_after_last_event():

    data = [
        ScheduleEntry("Alice", "Meeting", time(8, 0), time(9, 0)),
        ScheduleEntry("Alice", "Review", time(10, 0), time(11, 0)),
    ]

    service = CalendarService(FakeDataService(data))

    result = service.find_available_slots(["Alice"], timedelta(hours=1))

    assert time(11, 0) in result


def test_merge_overlapping_events():

    data = [
        ScheduleEntry("Alice", "Meeting", time(8, 0), time(10, 0)),
        ScheduleEntry("Alice", "Call", time(9, 30), time(11, 0)),
        ScheduleEntry("Alice", "Lunch", time(12, 0), time(13, 0)),
    ]

    service = CalendarService(FakeDataService(data))

    result = service.find_available_slots(["Alice"], timedelta(hours=1))

    assert time(11, 0) in result


def test_no_events():

    service = CalendarService(FakeDataService([]))

    result = service.find_available_slots(["Alice"], timedelta(hours=1))

    assert result == [time(7, 0)]