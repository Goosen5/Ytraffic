import re

from logic.per_stop.stops_line_a import LINE_A_STOPS
from logic.per_stop.stops_line_b import LINE_B_STOPS


STOPS = LINE_A_STOPS + LINE_B_STOPS


def normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def make_name_index():
    # map cleaned stop name to stop id for fuzzy event matches
    out = {}
    for stop in STOPS:
        out[normalise(stop["stop_name"])] = stop["stop_id"]
    return out


NAME_INDEX = make_name_index()
