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


# define functions
def get_time() -> tuple:
    """returns a tuple to indicate the day, A Day or B Day, hour and minute

    Returns:
        time: a dictionary with 'day' and 'AorB' keys as strings and 'hour'
            and 'min' as ints.
    """
    time = {
        "day": "",
        "AorB": "",
        "hour": 0,
        "min": 0,
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
    results = get_chs_events()
    print(results)
