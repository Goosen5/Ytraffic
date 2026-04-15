from datetime import datetime

from logic.per_stop.rules import HOLIDAYS


def pick_band(value: float, bands) -> float:
    for low, high, mult in bands:
        if low <= value <= high:
            return mult
    return 1.0


def is_holiday(target_date) -> bool:
    # support ranges that can cross into next year
    year = target_date.year
    for start_mm_dd, end_mm_dd in HOLIDAYS:
        start = datetime.strptime(f"{year}-{start_mm_dd}", "%Y-%m-%d").date()
        end = datetime.strptime(f"{year}-{end_mm_dd}", "%Y-%m-%d").date()
        if start_mm_dd > end_mm_dd:
            end = datetime.strptime(f"{year + 1}-{end_mm_dd}", "%Y-%m-%d").date()
        if start <= target_date <= end:
            return True
    return False
