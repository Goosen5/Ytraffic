from datetime import datetime

from logic.traffic_update.rules import HOLIDAYS


def pick_band(value: float, bands) -> float:
    for low, high, mult in bands:
        if low <= value <= high:
            return mult
    return 1.0


def is_holiday(target_date) -> bool:
    # support holiday ranges that can span to next year
    year = target_date.year
    for start_mm_dd, end_mm_dd in HOLIDAYS:
        start = datetime.strptime(f"{year}-{start_mm_dd}", "%Y-%m-%d").date()
        end = datetime.strptime(f"{year}-{end_mm_dd}", "%Y-%m-%d").date()
        if start_mm_dd > end_mm_dd:
            end = datetime.strptime(f"{year + 1}-{end_mm_dd}", "%Y-%m-%d").date()
        if start <= target_date <= end:
            return True
    return False


def recover_base_seed(traffic: int, hour_mult: float, rain_mult: float, temp_mult: float, event_mult: float, holiday_mult: float):
    total_mult = hour_mult * rain_mult * temp_mult * event_mult * holiday_mult
    if total_mult == 0:
        return 0.0
    return traffic / total_mult
