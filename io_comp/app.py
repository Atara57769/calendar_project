"""
This is the App entry point
"""
from datetime import timedelta

from service.calendar_service import  CalendarService
from service.data_service import DataService


def main():
    """Main entry point for the application"""
    data_service = DataService()
    calendar_service = CalendarService(data_service)

    slots = calendar_service.find_available_slots(
        ["Alice", "Jack"],
        timedelta(hours=1)
    )

    print(slots)


if __name__ == "__main__":
    main()
