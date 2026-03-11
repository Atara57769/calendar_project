"""
This is the App entry point
"""
import sys
from datetime import timedelta

from service.calendar_service import find_available_slots
from service.data_service import get_data


def main():
    """Main entry point for the application"""
    print("\n\n")
    print("Your goal is to design and create a simple Calendar in Python. You can replace this main function with your own code.")
    print("Please see README.md")
    p=find_available_slots(
    ["Alice", "Jack"],
    timedelta(minutes=60)
)
    for person in p:
        print(person)
    sys.exit(1)


if __name__ == "__main__":
    main()
