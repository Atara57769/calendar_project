import pytest
from datetime import time
from unittest.mock import patch

from service.data_service import get_person_events, get_busy_times
from models.schedule_entry_model import ScheduleEntry
from models.event_model import Event


def test_get_person_events():

    entries = [
        ScheduleEntry("Alice", "Meeting", time(8, 0), time(9, 0)),
        ScheduleEntry("Bob", "Call", time(10, 0), time(11, 0)),
        ScheduleEntry("Alice", "Lunch", time(13, 0), time(14, 0)),
    ]

    result = get_person_events("Alice", entries)

    assert len(result) == 2
    assert result[0].start_time == time(8, 0)
    assert result[1].start_time == time(13, 0)


@patch("service.data_service.get_data")
def test_get_busy_times_single_person(mock_get_data):

    mock_get_data.return_value = [
        ScheduleEntry("Alice", "Meeting", time(8, 0), time(9, 0)),
        ScheduleEntry("Bob", "Call", time(10, 0), time(11, 0)),
    ]

    result = get_busy_times(["Alice"])

    assert len(result) == 1
    assert result[0].start_time == time(8, 0)


@patch("service.data_service.get_data")
def test_get_busy_times_multiple_people(mock_get_data):

    mock_get_data.return_value = [
        ScheduleEntry("Alice", "Meeting", time(8, 0), time(9, 0)),
        ScheduleEntry("Bob", "Call", time(10, 0), time(11, 0)),
        ScheduleEntry("Charlie", "Review", time(12, 0), time(13, 0)),
    ]

    result = get_busy_times(["Alice", "Bob"])

    assert len(result) == 2