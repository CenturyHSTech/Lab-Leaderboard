import pytest

from lab_leaderboard import leaderboard


@pytest.fixture
def events():
    events = {
        "A Day": [
            "Family College Readiness Series at District Admin. Ctr.",
            "A DAY",
            "Native American/Alaska Native Parent Advisory Committee (PAC)",
        ],
        "B Day": ["Great Oregon ShakeOut", "B DAY", "Staff Flu Shot Clinic"],
        "No Day": [
            "Yakamah Harvest Festival Band",
            "Fall Bike Fest at Orenco Elementary",
        ],
    }
    return events


def test_get_a_or_b_day_for_A_Day(events):
    a_day = events.get("A Day")
    results = leaderboard.get_a_or_b_day(a_day)
    assert results == "A Day"


def test_get_a_or_b_day_for_B_Day(events):
    b_day = events.get("B Day")
    results = leaderboard.get_a_or_b_day(b_day)
    assert results == "B Day"


def test_get_a_or_b_day_for_No_School(events):
    no_day = events.get("No Day")
    results = leaderboard.get_a_or_b_day(no_day)
    assert results == "No School"
