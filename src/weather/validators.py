import re
from weather.exceptions import ValidError


def is_valid_city(city) -> bool:
    if not re.fullmatch(r"^[A-Za-zА-Яа-я\s-]+$", city):
        raise ValidError("City name is invalid")
    return True
