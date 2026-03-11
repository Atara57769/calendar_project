from datetime import time, timedelta
from unittest.mock import patch

from service.calendar_service import find_available_slots
from models.event_model import Event


@patch("service.calendar_service.get_busy_times")
def test_available_before_first_event(mock_get_busy):

    mock_get_busy.return_value = [
        Event(time(9, 0), time(10, 0))
    ]

    result = find_available_slots(["Alice"], timedelta(hours=1))

    assert time(7, 0) in result


@patch("service.calendar_service.get_busy_times")
def test_gap_between_events(mock_get_busy):

    mock_get_busy.return_value = [
        Event(time(8, 0), time(9, 0)),
        Event(time(11, 0), time(12, 0)),
    ]

    result = find_available_slots(["Alice"], timedelta(hours=1))

    assert time(9, 0) in result


@patch("service.calendar_service.get_busy_times")
def test_after_last_event(mock_get_busy):

    mock_get_busy.return_value = [
        Event(time(8, 0), time(9, 0)),
        Event(time(10, 0), time(11, 0)),
    ]

    result = find_available_slots(["Alice"], timedelta(hours=1))

    assert time(11, 0) in result


@patch("service.calendar_service.get_busy_times")
def test_merge_overlapping_events(mock_get_busy):

    mock_get_busy.return_value = [
        Event(time(8, 0), time(10, 0)),
        Event(time(9, 30), time(11, 0)),
        Event(time(12, 0), time(13, 0)),
    ]

    result = find_available_slots(["Alice"], timedelta(hours=1))

    # אחרי merge צריך להיות gap ב־11:00
    assert time(11, 0) in result


@patch("service.calendar_service.get_busy_times")
def test_no_events(mock_get_busy):

    mock_get_busy.return_value = []

    result = find_available_slots(["Alice"], timedelta(hours=1))

    assert time(7, 0) in result