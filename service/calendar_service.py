import logging
from typing import List
from datetime import time, timedelta, datetime

from exceptions.calendar_exceptions import CalendarError
from repositories.calendar_repository_protocol import CalendarRepository
from models.event_model import Event
from config.calendar_config import DAY_START, DAY_END

logger = logging.getLogger(__name__)


class CalendarService:

    def __init__(self, calendar_repository: CalendarRepository):
        self.calendar_repository = calendar_repository
        logger.debug("Initialized CalendarService with repository %s", type(calendar_repository).__name__)

    def get_busy_times(self, person_list: List[str]) -> List[Event]:
        """Return busy events for the given people."""
        logger.debug("get_busy_times called with persons=%s", person_list)

        if not person_list:
            logger.error("Person list is empty")
            raise CalendarError("Person list cannot be empty")

        entries = self.calendar_repository.get_data()
        busy_events = [
            Event(e.start_time, e.end_time)
            for e in entries
            if e.person in person_list
        ]
        logger.info("Found %d busy events for %s", len(busy_events), person_list)
        return busy_events

    @staticmethod
    def validate_event_duration(event_duration: timedelta) -> None:
        """Validate meeting duration against workday constraints."""
        logger.debug("Validating event duration %s", event_duration)

        if event_duration <= timedelta(0):
            logger.error("Event duration is not positive: %s", event_duration)
            raise CalendarError("Event duration must be positive")

        workday_duration = (
            datetime.combine(datetime.today(), DAY_END)
            - datetime.combine(datetime.today(), DAY_START)
        )

        if event_duration > workday_duration:
            logger.error("Event duration too long: %s > %s", event_duration, workday_duration)
            raise CalendarError("Event duration longer than workday")

    @staticmethod
    def merge_and_find_gaps(events: List[Event], event_duration: timedelta) -> List[time]:
        """Merge overlapping events and return available gaps."""
        logger.debug("merge_and_find_gaps called with %d events and duration %s", len(events), event_duration)

        if not events:
            logger.info("No busy events. Entire workday available starting at %s", DAY_START)
            return [DAY_START]

        events = sorted(events, key=lambda e: e.start_time)

        today: datetime = datetime.today()
        available_slots: List[time] = []
        prev_end: time = DAY_START

        for event in events:
            if event.end_time <= DAY_START:
                logger.debug("Skipping event before workday: %s-%s", event.start_time, event.end_time)
                continue

            if event.start_time >= DAY_END:
                logger.debug("Event starts after workday: %s", event.start_time)
                break

            gap_start: datetime = datetime.combine(today, prev_end)
            gap_end: datetime = datetime.combine(today, event.start_time)

            if gap_end - gap_start >= event_duration:
                available_slots.append(prev_end)

            prev_end = max(prev_end, event.end_time)

        last_gap_start: datetime = datetime.combine(today, prev_end)
        day_end_dt: datetime = datetime.combine(today, DAY_END)
        if day_end_dt - last_gap_start >= event_duration:
            available_slots.append(prev_end)

        logger.info("Computed available slots: %s", available_slots)
        return available_slots

    def find_available_slots(self, person_list: List[str], event_duration: timedelta) -> List[time]:
        logger.info("Finding available slots for persons=%s with duration=%s", person_list, event_duration)
        self.validate_event_duration(event_duration)
        events: List[Event] = self.get_busy_times(person_list)
        available_slots = self.merge_and_find_gaps(events, event_duration)
        logger.info("Found %d available slots", len(available_slots))
        return available_slots