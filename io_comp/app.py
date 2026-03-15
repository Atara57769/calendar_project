"""
This is the App entry point
"""
import logging
from datetime import timedelta

from repositories.calendar_repository_csv import CalendarRepositoryCsv
from service.calendar_service import CalendarService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the application"""
    logger.info("Starting calendar slot finder app")
    calendar_repo = CalendarRepositoryCsv()
    calendar_service = CalendarService(calendar_repo)

    try:
        slots = calendar_service.find_available_slots(
            ["Alice", "Jack"],
            timedelta(hours=1)
        )
        logger.info("Available slots: %s", slots)
        print(slots)
    except Exception as err:
        logger.error("Application error: %s", err)
        raise


if __name__ == "__main__":
    main()
