import os

WEEK_RANGE = (300, 500)
WEEKEND_RANGE = (200, 350)

# hourly multipliers for monday–sunday 0 midnight 23 11pm
WEEK_MULT_BY_HOUR = {
    0: 0.25,
    1: 0.20,
    2: 0.15,
    3: 0.10,
    4: 0.05,
    5: 0.2,
    6: 0.75,
    7: 1.0,
    8: 1.1,
    9: 1.2,
    10: 0.85,
    11: 0.9,
    12: 1.1,
    13: 0.95,
    14: 1.0,
    15: 1.05,
    16: 1.0,
    17: 1.2,
    18: 1.5,
    19: 1.2,
    20: 0.9,
    21: 0.6,
    22: 0.45,
    23: 0.30,
}

# multipliers are picked by checking whether the measured value falls within the band inclusive
RAIN_MULTIPLIER_BANDS = [
    (0.0, 0.0, 1.0),
    (0.1, 3.0, 1.05),
    (3.1, 6.0, 1.15),
    (6.1, 10.0, 1.30),
    (10.1, float("inf"), 1.35),
]

TEMP_MULTIPLIER_BANDS = [
    (-30.0, 9.99, 1.05),
    (10.0, 19.99, 1.00),
    (20.0, 50.0, 0.90),
    (50.01, float("inf"), 0.85),
]

EVENT_MULTIPLIER = 1.20

HOLLIDAY_MULTIPLIER = 0.80

HOLIDAYS = [
    ("01-01", "01-02"),
    ("04-25", "04-27"),
    ("05-01", "05-01"),
    ("05-08", "05-09"),
    ("05-29", "05-31"),
    ("06-09", "06-10"),
    ("07-14", "07-15"),
    ("08-15", "08-17"),
    ("11-01", "11-02"),
    ("11-11", "11-12"),
    ("12-15", "01-05"),
]

