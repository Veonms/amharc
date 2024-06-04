from datetime import datetime, timedelta
from math import ceil

from glowmarkt.src.data_model import DateRange


def get_date_ranges(start_datetime: str, end_datetime: str):
    date_ranges = []

    date_diff = (
        datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")
        - datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")
    ).days

    temp_start_date = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")
    temp_end_date = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S") + timedelta(
        days=10
    )
    end_date_obj = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")

    for i in range(ceil(date_diff / 10)):
        if temp_end_date > end_date_obj:
            temp_end_date = end_date_obj
        date_ranges.append(
            DateRange(
                start_date=temp_start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                end_date=temp_end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            )
        )
        temp_start_date += timedelta(days=10)
        temp_end_date += timedelta(days=10)

    return date_ranges
