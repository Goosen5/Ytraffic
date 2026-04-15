from logic.globales import (
    EVENT_MULTIPLIER,
    HOLLIDAY_MULTIPLIER,
    HOLIDAYS,
    RAIN_MULTIPLIER_BANDS,
    TEMP_MULTIPLIER_BANDS,
    WEEK_MULT_BY_HOUR,
)


WEEKEND_MULT_BY_HOUR = {
    0: 0.20, 1: 0.15, 2: 0.10, 3: 0.08, 4: 0.05,
    5: 0.20, 6: 0.75, 7: 1.00, 8: 1.10, 9: 1.20,
    10: 0.85, 11: 0.90, 12: 1.10, 13: 0.95, 14: 1.00,
    15: 1.05, 16: 1.00, 17: 1.20, 18: 1.50, 19: 1.20,
    20: 0.90, 21: 0.60, 22: 0.45, 23: 0.30,
}
