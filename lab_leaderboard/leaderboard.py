"""This is the script that will perform all the checks on day and time
and determine how much time is left in a class based on our schedule.

It will also change the background color based on whether students can
use a hall pass or not"""
# imports
from datetime import datetime
from datetime import timedelta

import requests as re
from icalendar import Calendar
from pytz import timezone

TZ = timezone("US/Pacific")
date = datetime.now() + timedelta(days=0)
datefor = "%s" % date.strftime("%Y-%m-%d")

# School Schedules
MONDAY = {
    "08:30-10:02": ("both", "class", "1st", "5th"),
    "10:08-11:40": ("both", "class", "2nd", "6th"),
    "11:40-12:14": ("north", "lunch"),
    "11:46-13:18": ("south", "class", "3rd", "7th"),
    "12:20-13:52": ("north", "class", "3rd", "7th"),
    "13:18-13:52": ("south", "lunch"),
    "13:52-15:30": ("both", "class", "4th", "8th"),
}
TUESDAY = {
    "08:30-9:54": ("both", "class", "1st", "5th"),
    "10:00-11:24": ("both", "class", "2nd", "6th"),
    "11:30-12:00": ("both", "advisory"),
    "12:00-12:30": ("north", "lunch"),
    "12:06-13:30": ("south", "class", "3rd", "7th"),
    "12:36-14:00": ("north", "class", "3rd", "7th"),
    "13:30-14:00": ("south", "lunch"),
    "14:06-15:30": ("both", "class", "4th", "8th"),
}
WEDNESDAY = {
    "9:00-10:26": ("both", "class", "1st", "5th"),
    "10:32-11:58": ("both", "class", "2nd", "6th"),
    "11:58-12:28": ("north", "lunch"),
    "12:04-13:29": ("south", "class", "3rd", "7th"),
    "12:34-13:59": ("north", "class", "3rd", "7th"),
    "13:29-13:59": ("south", "lunch"),
    "14:05-15:30": ("both", "class", "4th", "8th"),
}
THURSDAY = {
    "08:30-9:49": ("both", "class", "1st", "5th"),
    "9:55-11:14": ("both", "class", "2nd", "6th"),
    "11:20-12:05": ("both", "access/jagtime"),
    "12:05-12:40": ("north", "lunch"),
    "12:11-13:30": ("south", "class", "3rd", "7th"),
    "12:46-14:05": ("north", "class", "3rd", "7th"),
    "13:30-14:05": ("south", "lunch"),
    "14:11-15:30": ("both", "class", "4th", "8th"),
}
FRIDAY = THURSDAY


# define functions
def get_schedule():
    """
    returns which schedule should be displayed
    """
    today = date.today()
    weekday = today.weekday()
    if weekday == 0:
        schedule = MONDAY
    elif weekday == 1:
        schedule = TUESDAY
    elif weekday == 2:
        schedule = WEDNESDAY
    elif weekday == 3:
        schedule = THURSDAY
    elif weekday == 4:
        schedule = FRIDAY
    elif weekday == 5:
        schedule = "No school today!"
    else:
        schedule = "No school today!"
    return schedule


def get_time() -> tuple:
    """returns a tuple to indicate the day, A Day or B Day, hour and minute

    Returns:
        time: a dictionary with 'day' and 'AorB' keys as strings and 'hour'
            and 'min' as ints.
    """
    now = datetime.now()
    time = {
        "day": now.day,
        "AorB": results,
        "hour": now.hour,
        "min": now.minute,
    }
    return time


def get_a_or_b_day(events: list) -> str:
    """returns A, B, or No School based on school calendar

    NOTE: Century's website has a link to an iCal feed, and we need code
    [iCalFeed](https://www.hsd.k12.or.us/site/handlers/icalfeed.ashx?MIID=37)
    [howto](https://learnpython.com/blog/working-with-icalendar-with-python/)
    I will load the calendar, someone else can get it working.

    Args:
        events: a list of events from the calendar

    Returns:
        day: A if it's an 'A day', B if it's a 'B day', or 'No School' if
            neither.
    """
    day = "No School"
    for event in events:
        if "a day" in event.lower():
            day = "A Day"
        if "b day" in event.lower():
            day = "B Day"
    return day


def get_chs_events() -> list:
    """returns a list of today's events at CHS"""
    events = []
    path_to_ics_file = "https://www.hsd.k12.or.us"
    path_to_ics_file += "/site/handlers/icalfeed.ashx?MIID=37"

    # set start and stop time
    dtend = False
    dtstart = False

    # get calendar feed
    r = re.get(path_to_ics_file)
    gcal = Calendar.from_ical(r.text)
    for event in gcal.walk("VEVENT"):
        if "DTSART" in event:
            try:
                dtstart = event["DTSTART"].dt.astimezone(TZ)
            except Exception:
                dtstart = False
        if "DTEND" in event:
            try:
                dtend = event["DTEND"].dt.astimezone(TZ)
            except Exception:
                dtend = False
        if dtstart or dtend:
            if datefor in "%s" % dtstart or datefor in "%s" % dtend:
                # it's today, let's add the stuff
                summary = str(event["summary"])
                events.append(summary)
    return events


if __name__ == "__main__":
    print("Here's where we'll test our code.")
    # results = get_chs_events()
    # print(get_time())
    print(get_schedule())
