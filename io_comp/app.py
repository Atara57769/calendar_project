import logging
import argparse
import sys
from datetime import timedelta

from repositories.calendar_repository_csv import CalendarRepositoryCsv
from service.calendar_service import CalendarService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Calendar slot finder")

    parser.add_argument(
        "--people",
        nargs="+",
        default=[],
        help="People to check availability for"
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help="Meeting duration in minutes"
    )

    args = parser.parse_args()

    if not args.people or args.duration is None:
        logger.error("No parameters provided.\n")
        parser.print_help()
        sys.exit(1)

    return args


def main() -> None:
    """Main entry point for the application."""

    args = parse_args()

    logging.getLogger().setLevel(args.log_level)

    logger.info("Starting calendar slot finder app")
    logger.debug("CLI arguments: %s", args)

    calendar_repo = CalendarRepositoryCsv()
    calendar_service = CalendarService(calendar_repo)

    try:
        slots = calendar_service.find_available_slots(
            args.people,
            timedelta(minutes=args.duration),
        )

        logger.info("Available slots found: %s", slots)

        print("\nAvailable meeting slots:")
        for slot in slots:
            print(slot)

    except Exception as err:
        logger.exception("Application error occurred")
        raise


if __name__ == "__main__":
    main()